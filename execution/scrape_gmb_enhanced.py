#!/usr/bin/env python3
"""
Enhanced Google My Business Lead Scraper with Email & Social Media Extraction

Extracts business listing details from Google My Business profiles,
scrapes individual websites for email addresses and social media links,
and scores leads based on contact availability.

Usage:
    python scrape_gmb_enhanced.py --query "restaurants in NYC" --max-results 20
"""

import argparse
import json
import csv
import sys
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import quote_plus, urljoin, urlparse

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install selenium webdriver-manager requests beautifulsoup4")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()


class EmailSocialExtractor:
    """Extract emails and social media links from websites"""
    
    # Email regex pattern
    EMAIL_PATTERN = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    
    # Social media patterns
    SOCIAL_PATTERNS = {
        'facebook': re.compile(r'(?:https?://)?(?:www\.)?facebook\.com/[\w\-\.]+', re.I),
        'instagram': re.compile(r'(?:https?://)?(?:www\.)?instagram\.com/[\w\-\.]+', re.I),
        'tiktok': re.compile(r'(?:https?://)?(?:www\.)?tiktok\.com/@?[\w\-\.]+', re.I),
        'linkedin': re.compile(r'(?:https?://)?(?:www\.)?linkedin\.com/(?:company|in)/[\w\-\.]+', re.I),
        'twitter': re.compile(r'(?:https?://)?(?:www\.)?(?:twitter|x)\.com/[\w\-\.]+', re.I),
    }
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def extract_from_website(self, url: str) -> Dict[str, any]:
        """
        Extract email and social media links from a website.
        
        Args:
            url: Website URL to scrape
            
        Returns:
            Dictionary with email and social media links
        """
        result = {
            'email': None,
            'facebook': None,
            'instagram': None,
            'tiktok': None,
            'linkedin': None,
            'twitter': None,
        }
        
        if not url or url == 'N/A':
            return result
        
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Fetch the webpage
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get all text and links
            page_text = soup.get_text()
            page_html = str(soup)
            
            # Extract email
            emails = self.EMAIL_PATTERN.findall(page_text)
            if emails:
                # Filter out common false positives
                valid_emails = [
                    e for e in emails 
                    if not any(x in e.lower() for x in ['example.com', 'test.com', 'domain.com', 'wix.com', 'sentry.io'])
                ]
                if valid_emails:
                    result['email'] = valid_emails[0]  # Take first valid email
            
            # Extract social media links
            for platform, pattern in self.SOCIAL_PATTERNS.items():
                matches = pattern.findall(page_html)
                if matches:
                    # Clean up the URL
                    social_url = matches[0]
                    if not social_url.startswith('http'):
                        social_url = 'https://' + social_url
                    
                    # Store based on platform (twitter/x both go to twitter key)
                    if platform == 'twitter' or 'x.com' in social_url:
                        result['twitter'] = social_url
                    else:
                        result[platform] = social_url
            
            return result
            
        except requests.Timeout:
            print(f"      ⚠️  Timeout accessing {url}")
            return result
        except requests.RequestException as e:
            print(f"      ⚠️  Error accessing {url}: {str(e)[:30]}")
            return result
        except Exception as e:
            print(f"      ⚠️  Unexpected error: {str(e)[:30]}")
            return result


class LeadScorer:
    """Calculate lead scores based on contact availability"""
    
    @staticmethod
    def calculate_score(lead_data: Dict) -> int:
        """
        Calculate lead score on 1-5 scale.
        
        Scoring:
        - Base: 1 point
        - +3 points if has email
        - +1 point if has social media
        
        Args:
            lead_data: Dictionary with lead information
            
        Returns:
            Score from 1-5
        """
        score = 1  # Base score
        
        # +3 points for email
        if lead_data.get('email') and lead_data['email'] != 'N/A':
            score += 3
        
        # +1 point for social media
        social_platforms = ['facebook', 'instagram', 'tiktok', 'linkedin', 'twitter']
        has_social = any(
            lead_data.get(platform) and lead_data[platform] != 'N/A' 
            for platform in social_platforms
        )
        if has_social:
            score += 1
        
        return min(score, 5)  # Cap at 5
    
    @staticmethod
    def get_score_label(score: int) -> str:
        """Get descriptive label for score"""
        labels = {
            5: "⭐⭐⭐⭐⭐ Excellent",
            4: "⭐⭐⭐⭐ Good",
            3: "⭐⭐⭐ Moderate",
            2: "⭐⭐ Fair",
            1: "⭐ Low"
        }
        return labels.get(score, "Unknown")


class GMBScraperEnhanced:
    """Enhanced Google My Business profile scraper with email and social media extraction"""
    
    def __init__(self, headless: bool = True, scrape_websites: bool = True):
        """
        Initialize the enhanced scraper.
        
        Args:
            headless: Run browser in headless mode
            scrape_websites: Whether to scrape individual websites for emails/social
        """
        self.driver = None
        self.headless = headless
        self.scrape_websites = scrape_websites
        self.results = []
        self.email_extractor = EmailSocialExtractor() if scrape_websites else None
        self.scorer = LeadScorer()
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Anti-detection measures
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": self.driver.execute_script("return navigator.userAgent").replace('Headless', '')
            })
            
            print("✓ Browser initialized successfully")
            
        except Exception as e:
            print(f"✗ Error initializing browser: {e}")
            raise
    
    def search_google_maps(self, query: str, max_results: int = 20) -> List[Dict]:
        """Search Google Maps and extract business data with enhanced fields"""
        if not self.driver:
            self.setup_driver()
        
        encoded_query = quote_plus(query)
        url = f"https://www.google.com/maps/search/{encoded_query}"
        
        print(f"\n🔍 Searching for: {query}")
        print(f"📍 URL: {url}\n")
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
                )
            except TimeoutException:
                print("⚠️  Timeout waiting for results.")
                return []
            
            results_panel = self.driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
            self._scroll_results(results_panel, max_results)
            
            listings = self.driver.find_elements(By.CSS_SELECTOR, "div[role='feed'] > div > div > a")
            
            print(f"📊 Found {len(listings)} listings, processing up to {max_results}...")
            
            for idx, listing in enumerate(listings[:max_results], 1):
                try:
                    print(f"  [{idx}/{min(len(listings), max_results)}] Extracting GMB data...", end=" ")
                    
                    self.driver.execute_script("arguments[0].click();", listing)
                    time.sleep(2)
                    
                    business_data = self._extract_business_data()
                    
                    if business_data:
                        business_data['lead_number'] = idx
                        
                        # Extract email and social media if enabled
                        if self.scrape_websites and business_data.get('website') != 'N/A':
                            print("✓")
                            print(f"      🌐 Scraping website for email/social...", end=" ")
                            enhanced_data = self.email_extractor.extract_from_website(
                                business_data['website']
                            )
                            business_data.update(enhanced_data)
                            print("✓")
                        else:
                            print("✓")
                            # Set default values if not scraping websites
                            business_data.update({
                                'email': 'N/A',
                                'facebook': 'N/A',
                                'instagram': 'N/A',
                                'tiktok': 'N/A',
                                'linkedin': 'N/A',
                                'twitter': 'N/A',
                            })
                        
                        # Calculate lead score
                        business_data['lead_score'] = self.scorer.calculate_score(business_data)
                        business_data['score_label'] = self.scorer.get_score_label(
                            business_data['lead_score']
                        )
                        
                        self.results.append(business_data)
                    else:
                        print("✗ (no data)")
                    
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"✗ Error: {str(e)[:50]}")
                    continue
            
            print(f"\n✓ Successfully extracted {len(self.results)} business profiles")
            
            # Sort by lead score (highest first)
            self.results.sort(key=lambda x: x.get('lead_score', 0), reverse=True)
            
            return self.results
            
        except Exception as e:
            print(f"✗ Error during search: {e}")
            return []
    
    def _scroll_results(self, element, target_count: int):
        """Scroll the results panel to load more listings"""
        last_height = 0
        scroll_attempts = 0
        max_scrolls = min(target_count // 5, 10)
        
        while scroll_attempts < max_scrolls:
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", 
                element
            )
            time.sleep(1.5)
            
            new_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", 
                element
            )
            
            if new_height == last_height:
                break
                
            last_height = new_height
            scroll_attempts += 1
    
    def _extract_business_data(self) -> Optional[Dict]:
        """Extract business data from the currently displayed profile"""
        try:
            data = {
                'name': 'N/A',
                'address': 'N/A',
                'phone': 'N/A',
                'website': 'N/A',
                'rating': 'N/A',
                'reviews': 'N/A',
                'category': 'N/A',
                'hours': 'N/A',
                'price_level': 'N/A',
                'description': 'N/A',
                'google_maps_url': 'N/A'
            }
            
            # Business Name
            try:
                name_elem = self.driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf")
                data['name'] = name_elem.text.strip()
            except NoSuchElementException:
                pass
            
            # Rating and Reviews
            try:
                rating_elem = self.driver.find_element(By.CSS_SELECTOR, "div.F7nice span[aria-label*='stars']")
                rating_text = rating_elem.get_attribute('aria-label')
                rating_match = re.search(r'([\d.]+)\s*stars?', rating_text)
                if rating_match:
                    data['rating'] = rating_match.group(1)
                
                reviews_elem = self.driver.find_element(By.CSS_SELECTOR, "div.F7nice span[aria-label*='reviews']")
                reviews_text = reviews_elem.get_attribute('aria-label')
                reviews_match = re.search(r'([\d,]+)\s*reviews?', reviews_text)
                if reviews_match:
                    data['reviews'] = reviews_match.group(1)
            except NoSuchElementException:
                pass
            
            # Category
            try:
                category_elem = self.driver.find_element(By.CSS_SELECTOR, "button.DkEaL")
                data['category'] = category_elem.text.strip()
            except NoSuchElementException:
                pass
            
            # Address
            try:
                address_elem = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id='address']")
                data['address'] = address_elem.get_attribute('aria-label').replace('Address: ', '')
            except NoSuchElementException:
                pass
            
            # Phone
            try:
                phone_elem = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id*='phone']")
                phone_text = phone_elem.get_attribute('aria-label')
                data['phone'] = phone_text.replace('Phone: ', '').replace('Copy phone number', '').strip()
            except NoSuchElementException:
                pass
            
            # Website
            try:
                website_elem = self.driver.find_element(By.CSS_SELECTOR, "a[data-item-id='authority']")
                data['website'] = website_elem.get_attribute('href')
            except NoSuchElementException:
                pass
            
            # Hours
            try:
                hours_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id*='hours']")
                data['hours'] = hours_button.get_attribute('aria-label').replace('Hours: ', '')
            except NoSuchElementException:
                pass
            
            # Price Level
            try:
                price_elem = self.driver.find_element(By.CSS_SELECTOR, "span[aria-label*='Price']")
                data['price_level'] = price_elem.get_attribute('aria-label')
            except NoSuchElementException:
                pass
            
            # Google Maps URL
            data['google_maps_url'] = self.driver.current_url
            
            return data if data['name'] != 'N/A' else None
            
        except Exception as e:
            print(f"    Extraction error: {e}")
            return None
    
    def close(self):
        """Close the browser and cleanup"""
        if self.driver:
            self.driver.quit()
            print("\n✓ Browser closed")


def save_as_text(results: List[Dict], output_path: Path):
    """Save results in formatted text format with enhanced fields"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("GOOGLE MY BUSINESS LEAD GENERATION REPORT (ENHANCED)\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Leads: {len(results)}\n")
        f.write("=" * 80 + "\n\n")
        
        for lead in results:
            f.write("=" * 80 + "\n")
            f.write(f"LEAD #{lead.get('lead_number', 'N/A')} - {lead.get('score_label', 'N/A')}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Business Name: {lead.get('name', 'N/A')}\n")
            f.write(f"Category: {lead.get('category', 'N/A')}\n")
            f.write(f"Rating: {lead.get('rating', 'N/A')} ⭐ ({lead.get('reviews', 'N/A')} reviews)\n")
            f.write(f"\nCONTACT INFORMATION:\n")
            f.write(f"  Address: {lead.get('address', 'N/A')}\n")
            f.write(f"  Phone: {lead.get('phone', 'N/A')}\n")
            f.write(f"  Email: {lead.get('email', 'N/A')}\n")
            f.write(f"  Website: {lead.get('website', 'N/A')}\n")
            f.write(f"\nSOCIAL MEDIA:\n")
            f.write(f"  Facebook: {lead.get('facebook', 'N/A')}\n")
            f.write(f"  Instagram: {lead.get('instagram', 'N/A')}\n")
            f.write(f"  TikTok: {lead.get('tiktok', 'N/A')}\n")
            f.write(f"  LinkedIn: {lead.get('linkedin', 'N/A')}\n")
            f.write(f"  Twitter/X: {lead.get('twitter', 'N/A')}\n")
            f.write(f"\nADDITIONAL INFO:\n")
            f.write(f"  Hours: {lead.get('hours', 'N/A')}\n")
            f.write(f"  Price: {lead.get('price_level', 'N/A')}\n")
            f.write(f"  Google Maps: {lead.get('google_maps_url', 'N/A')}\n")
            f.write(f"\nLEAD SCORE: {lead.get('lead_score', 'N/A')}/5\n")
            f.write("-" * 80 + "\n\n")
    
    print(f"✓ Text output saved to: {output_path}")


def save_as_json(results: List[Dict], output_path: Path):
    """Save results in JSON format"""
    output_data = {
        'generated_at': datetime.now().isoformat(),
        'total_leads': len(results),
        'leads': results
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ JSON output saved to: {output_path}")


def save_as_csv(results: List[Dict], output_path: Path):
    """Save results in CSV format with enhanced fields"""
    if not results:
        print("⚠️  No results to save")
        return
    
    fieldnames = [
        'lead_number', 'lead_score', 'score_label', 'name', 'category', 
        'address', 'phone', 'email', 'website', 
        'facebook', 'instagram', 'tiktok', 'linkedin', 'twitter',
        'rating', 'reviews', 'hours', 'price_level', 'google_maps_url'
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✓ CSV output saved to: {output_path}")


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Enhanced GMB scraper with email and social media extraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scrape_gmb_enhanced.py --query "restaurants in NYC" --max-results 20
  python scrape_gmb_enhanced.py --query "plumbers in LA" --max-results 10 --format json
  python scrape_gmb_enhanced.py --query "dentists in Miami" --format csv --no-website-scraping
        """
    )
    
    parser.add_argument(
        '--query', '-q',
        type=str,
        required=True,
        help='Search query (e.g., "coffee shops in San Francisco")'
    )
    
    parser.add_argument(
        '--max-results', '-m',
        type=int,
        default=20,
        help='Maximum number of results to scrape (default: 20)'
    )
    
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['txt', 'json', 'csv'],
        default='txt',
        help='Output format (default: txt)'
    )
    
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Run browser in visible mode'
    )
    
    parser.add_argument(
        '--no-website-scraping',
        action='store_true',
        help='Skip website scraping for emails and social media (faster but less data)'
    )
    
    args = parser.parse_args()
    
    # Setup output path
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    tmp_dir = project_root / ".tmp"
    tmp_dir.mkdir(exist_ok=True)
    
    output_filename = f"gmb_leads_enhanced_{timestamp}.{args.format}"
    output_path = tmp_dir / output_filename
    
    print("\n" + "=" * 80)
    print("ENHANCED GOOGLE MY BUSINESS LEAD SCRAPER")
    print("With Email & Social Media Extraction + Lead Scoring")
    print("=" * 80)
    print(f"Query: {args.query}")
    print(f"Max Results: {args.max_results}")
    print(f"Output Format: {args.format}")
    print(f"Website Scraping: {'Disabled' if args.no_website_scraping else 'Enabled'}")
    print(f"Output Path: {output_path}")
    print("=" * 80 + "\n")
    
    # Initialize scraper
    scraper = GMBScraperEnhanced(
        headless=not args.no_headless,
        scrape_websites=not args.no_website_scraping
    )
    
    try:
        # Perform search and extraction
        results = scraper.search_google_maps(args.query, args.max_results)
        
        if not results:
            print("\n⚠️  No results found or extraction failed")
            return 1
        
        # Save results
        print(f"\n💾 Saving results...")
        
        if args.format == 'txt':
            save_as_text(results, output_path)
        elif args.format == 'json':
            save_as_json(results, output_path)
        elif args.format == 'csv':
            save_as_csv(results, output_path)
        
        # Print summary with scoring breakdown
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total Leads Extracted: {len(results)}")
        
        # Score distribution
        score_dist = {}
        for lead in results:
            score = lead.get('lead_score', 0)
            score_dist[score] = score_dist.get(score, 0) + 1
        
        print(f"\nLead Score Distribution:")
        for score in sorted(score_dist.keys(), reverse=True):
            label = LeadScorer.get_score_label(score)
            count = score_dist[score]
            print(f"  {label}: {count} leads")
        
        # High-value leads
        high_value = [l for l in results if l.get('lead_score', 0) >= 4]
        print(f"\nHigh-Value Leads (Score 4-5): {len(high_value)}")
        
        print(f"\nOutput File: {output_path}")
        print("=" * 80 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        return 1
        
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        scraper.close()


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Google My Business Lead Scraper

Extracts business listing details from Google My Business profiles
for lead generation purposes.

Usage:
    python scrape_gmb.py --query "restaurants in NYC" --max-results 20
"""

import argparse
import json
import csv
import sys
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote_plus

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install selenium webdriver-manager")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()


class GMBScraper:
    """Google My Business profile scraper"""
    
    def __init__(self, headless: bool = True):
        """
        Initialize the scraper with a Chrome browser instance.
        
        Args:
            headless: Run browser in headless mode (default: True)
        """
        self.driver = None
        self.headless = headless
        self.results = []
        
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
        
        # User agent to appear as regular browser
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Exclude automation flags
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute CDP commands to hide webdriver
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": self.driver.execute_script("return navigator.userAgent").replace('Headless', '')
            })
            
            print("✓ Browser initialized successfully")
            
        except Exception as e:
            print(f"✗ Error initializing browser: {e}")
            raise
    
    def search_google_maps(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Search Google Maps for businesses matching the query.
        
        Args:
            query: Search query (e.g., "restaurants in NYC")
            max_results: Maximum number of results to scrape
            
        Returns:
            List of business data dictionaries
        """
        if not self.driver:
            self.setup_driver()
        
        # Construct Google Maps search URL
        encoded_query = quote_plus(query)
        url = f"https://www.google.com/maps/search/{encoded_query}"
        
        print(f"\n🔍 Searching for: {query}")
        print(f"📍 URL: {url}\n")
        
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for initial load
            
            # Wait for results to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
                )
            except TimeoutException:
                print("⚠️  Timeout waiting for results. The page may have loaded differently.")
                print("    This could be due to CAPTCHA or rate limiting.")
                return []
            
            # Scroll to load more results
            results_panel = self.driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
            self._scroll_results(results_panel, max_results)
            
            # Find all business listings
            listings = self.driver.find_elements(By.CSS_SELECTOR, "div[role='feed'] > div > div > a")
            
            print(f"📊 Found {len(listings)} listings, processing up to {max_results}...")
            
            # Extract data from each listing
            for idx, listing in enumerate(listings[:max_results], 1):
                try:
                    print(f"  [{idx}/{min(len(listings), max_results)}] Extracting data...", end=" ")
                    
                    # Click on the listing to open details
                    self.driver.execute_script("arguments[0].click();", listing)
                    time.sleep(2)  # Wait for details to load
                    
                    # Extract business data
                    business_data = self._extract_business_data()
                    
                    if business_data:
                        business_data['lead_number'] = idx
                        self.results.append(business_data)
                        print("✓")
                    else:
                        print("✗ (no data)")
                    
                    # Delay between requests to avoid rate limiting
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"✗ Error: {str(e)[:50]}")
                    continue
            
            print(f"\n✓ Successfully extracted {len(self.results)} business profiles")
            return self.results
            
        except Exception as e:
            print(f"✗ Error during search: {e}")
            return []
    
    def _scroll_results(self, element, target_count: int):
        """Scroll the results panel to load more listings"""
        last_height = 0
        scroll_attempts = 0
        max_scrolls = min(target_count // 5, 10)  # Limit scrolling
        
        while scroll_attempts < max_scrolls:
            # Scroll down
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", 
                element
            )
            time.sleep(1.5)
            
            # Check if we've reached the bottom
            new_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", 
                element
            )
            
            if new_height == last_height:
                break
                
            last_height = new_height
            scroll_attempts += 1
    
    def _extract_business_data(self) -> Optional[Dict]:
        """
        Extract business data from the currently displayed business profile.
        
        Returns:
            Dictionary with business data or None if extraction fails
        """
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
                # Extract rating number
                rating_match = re.search(r'([\d.]+)\s*stars?', rating_text)
                if rating_match:
                    data['rating'] = rating_match.group(1)
                
                # Extract review count
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
    """Save results in formatted text format"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("GOOGLE MY BUSINESS LEAD GENERATION REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Leads: {len(results)}\n")
        f.write("=" * 80 + "\n\n")
        
        for lead in results:
            f.write("=" * 80 + "\n")
            f.write(f"LEAD #{lead.get('lead_number', 'N/A')}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Business Name: {lead.get('name', 'N/A')}\n")
            f.write(f"Address: {lead.get('address', 'N/A')}\n")
            f.write(f"Phone: {lead.get('phone', 'N/A')}\n")
            f.write(f"Website: {lead.get('website', 'N/A')}\n")
            f.write(f"Rating: {lead.get('rating', 'N/A')} ⭐ ({lead.get('reviews', 'N/A')} reviews)\n")
            f.write(f"Category: {lead.get('category', 'N/A')}\n")
            f.write(f"Hours: {lead.get('hours', 'N/A')}\n")
            f.write(f"Price: {lead.get('price_level', 'N/A')}\n")
            f.write(f"Google Maps: {lead.get('google_maps_url', 'N/A')}\n")
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
    """Save results in CSV format"""
    if not results:
        print("⚠️  No results to save")
        return
    
    fieldnames = ['lead_number', 'name', 'address', 'phone', 'website', 
                  'rating', 'reviews', 'category', 'hours', 'price_level', 
                  'google_maps_url']
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✓ CSV output saved to: {output_path}")


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Scrape Google My Business profiles for lead generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scrape_gmb.py --query "restaurants in NYC" --max-results 20
  python scrape_gmb.py --query "plumbers in LA" --max-results 10 --format json
  python scrape_gmb.py --query "dentists in Miami" --format csv --no-headless
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
        help='Run browser in visible mode (useful for debugging)'
    )
    
    args = parser.parse_args()
    
    # Setup output path
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    tmp_dir = project_root / ".tmp"
    tmp_dir.mkdir(exist_ok=True)
    
    output_filename = f"gmb_leads_{timestamp}.{args.format}"
    output_path = tmp_dir / output_filename
    
    print("\n" + "=" * 80)
    print("GOOGLE MY BUSINESS LEAD SCRAPER")
    print("=" * 80)
    print(f"Query: {args.query}")
    print(f"Max Results: {args.max_results}")
    print(f"Output Format: {args.format}")
    print(f"Output Path: {output_path}")
    print("=" * 80 + "\n")
    
    # Initialize scraper
    scraper = GMBScraper(headless=not args.no_headless)
    
    try:
        # Perform search and extraction
        results = scraper.search_google_maps(args.query, args.max_results)
        
        if not results:
            print("\n⚠️  No results found or extraction failed")
            print("    This could be due to:")
            print("    - CAPTCHA detection")
            print("    - Rate limiting")
            print("    - Network issues")
            print("    - Changed page structure")
            return 1
        
        # Save results in requested format
        print(f"\n💾 Saving results...")
        
        if args.format == 'txt':
            save_as_text(results, output_path)
        elif args.format == 'json':
            save_as_json(results, output_path)
        elif args.format == 'csv':
            save_as_csv(results, output_path)
        
        # Print summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total Leads Extracted: {len(results)}")
        print(f"Output File: {output_path}")
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

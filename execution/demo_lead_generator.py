#!/usr/bin/env python3
"""
Demo Lead Generator

Creates realistic sample lead data for testing without scraping.
Useful for demonstrating the system or when Google blocks scraping.

Usage:
    python demo_lead_generator.py --query "landscapers in New York" --max-results 10
"""

import argparse
import json
import csv
import sys
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# Sample data pools
FIRST_NAMES = ["Green", "Elite", "Pro", "Premier", "Quality", "Superior", "Expert", "Master", "Perfect", "Prime"]
BUSINESS_TYPES = {
    "landscapers": ["Landscaping", "Lawn Care", "Garden Design", "Landscape Services"],
    "restaurants": ["Restaurant", "Bistro", "Cafe", "Eatery", "Kitchen"],
    "plumbers": ["Plumbing", "Plumbing Services", "Plumbing & Heating"],
    "dentists": ["Dental", "Dentistry", "Dental Care", "Family Dentistry"],
}

STREETS = ["Main St", "Oak Ave", "Park Blvd", "Broadway", "Madison Ave", "5th Ave", "Lexington Ave", "Central Park West"]
CITIES_NY = ["New York", "Brooklyn", "Queens", "Bronx", "Manhattan", "Staten Island"]
ZIP_CODES = ["10001", "10002", "10003", "11201", "11101", "10451", "10301"]

SOCIAL_HANDLES = ["official", "nyc", "pro", "services", "inc", "company", "group"]

def generate_business_name(business_type: str, index: int) -> str:
    """Generate a realistic business name"""
    prefix = random.choice(FIRST_NAMES)
    suffix = random.choice(BUSINESS_TYPES.get(business_type, ["Services"]))
    return f"{prefix} {suffix}"

def generate_phone() -> str:
    """Generate a realistic NYC phone number"""
    area_codes = ["212", "718", "917", "646", "347"]
    area = random.choice(area_codes)
    exchange = random.randint(200, 999)
    number = random.randint(1000, 9999)
    return f"({area}) {exchange}-{number}"

def generate_email(business_name: str, has_email: bool) -> str:
    """Generate email based on business name"""
    if not has_email:
        return "N/A"
    
    clean_name = business_name.lower().replace(" ", "").replace("&", "and")
    domains = ["gmail.com", "yahoo.com", "outlook.com", f"{clean_name[:10]}.com"]
    prefixes = ["info", "contact", "hello", "office"]
    
    return f"{random.choice(prefixes)}@{random.choice(domains)}"

def generate_social_media(business_name: str, has_social: bool) -> Dict[str, str]:
    """Generate social media links"""
    if not has_social:
        return {
            'facebook': 'N/A',
            'instagram': 'N/A',
            'tiktok': 'N/A',
            'linkedin': 'N/A',
            'twitter': 'N/A'
        }
    
    clean_name = business_name.lower().replace(" ", "").replace("&", "and")
    handle = f"{clean_name[:15]}{random.choice(SOCIAL_HANDLES)}"
    
    # Randomly include some platforms
    platforms = {}
    platforms['facebook'] = f"https://facebook.com/{handle}" if random.random() > 0.3 else "N/A"
    platforms['instagram'] = f"https://instagram.com/{handle}" if random.random() > 0.2 else "N/A"
    platforms['tiktok'] = f"https://tiktok.com/@{handle}" if random.random() > 0.6 else "N/A"
    platforms['linkedin'] = f"https://linkedin.com/company/{handle}" if random.random() > 0.7 else "N/A"
    platforms['twitter'] = f"https://twitter.com/{handle}" if random.random() > 0.5 else "N/A"
    
    return platforms

def calculate_lead_score(has_email: bool, has_social: bool) -> tuple:
    """Calculate lead score"""
    score = 1  # Base
    if has_email:
        score += 3
    if has_social:
        score += 1
    
    labels = {
        5: "⭐⭐⭐⭐⭐ Excellent",
        4: "⭐⭐⭐⭐ Good",
        2: "⭐⭐ Fair",
        1: "⭐ Low"
    }
    
    return score, labels.get(score, "Unknown")

def generate_lead(business_type: str, city: str, index: int) -> Dict:
    """Generate a single realistic lead"""
    
    # Determine if this lead has email/social (realistic distribution)
    has_email = random.random() < 0.65  # 65% have email
    has_social = random.random() < 0.75  # 75% have social
    
    name = generate_business_name(business_type, index)
    street_num = random.randint(100, 9999)
    street = random.choice(STREETS)
    city_name = random.choice(CITIES_NY) if city.lower() == "new york" else city
    zip_code = random.choice(ZIP_CODES)
    
    rating = round(random.uniform(3.5, 5.0), 1)
    reviews = random.randint(10, 500)
    
    score, score_label = calculate_lead_score(has_email, has_social)
    
    lead = {
        'lead_number': index,
        'lead_score': score,
        'score_label': score_label,
        'name': name,
        'category': random.choice(BUSINESS_TYPES.get(business_type, ["Services"])),
        'address': f"{street_num} {street}, {city_name}, NY {zip_code}",
        'phone': generate_phone(),
        'email': generate_email(name, has_email),
        'website': f"https://www.{name.lower().replace(' ', '')}.com" if random.random() > 0.2 else "N/A",
        'rating': str(rating),
        'reviews': str(reviews),
        'hours': "Mon-Fri 8AM-6PM, Sat 9AM-4PM" if random.random() > 0.3 else "N/A",
        'price_level': random.choice(["$$", "$$$", "N/A"]),
        'google_maps_url': f"https://maps.google.com/?cid={random.randint(1000000, 9999999)}",
    }
    
    # Add social media
    social = generate_social_media(name, has_social)
    lead.update(social)
    
    return lead

def save_as_text(results: List[Dict], output_path: Path):
    """Save results in formatted text format"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("DEMO LEAD GENERATION REPORT\n")
        f.write("(Sample data for testing - not real businesses)\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Leads: {len(results)}\n")
        f.write("=" * 80 + "\n\n")
        
        for lead in results:
            f.write("=" * 80 + "\n")
            f.write(f"LEAD #{lead['lead_number']} - {lead['score_label']}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Business Name: {lead['name']}\n")
            f.write(f"Category: {lead['category']}\n")
            f.write(f"Rating: {lead['rating']} ⭐ ({lead['reviews']} reviews)\n")
            f.write(f"\nCONTACT INFORMATION:\n")
            f.write(f"  Address: {lead['address']}\n")
            f.write(f"  Phone: {lead['phone']}\n")
            f.write(f"  Email: {lead['email']}\n")
            f.write(f"  Website: {lead['website']}\n")
            f.write(f"\nSOCIAL MEDIA:\n")
            f.write(f"  Facebook: {lead['facebook']}\n")
            f.write(f"  Instagram: {lead['instagram']}\n")
            f.write(f"  TikTok: {lead['tiktok']}\n")
            f.write(f"  LinkedIn: {lead['linkedin']}\n")
            f.write(f"  Twitter/X: {lead['twitter']}\n")
            f.write(f"\nADDITIONAL INFO:\n")
            f.write(f"  Hours: {lead['hours']}\n")
            f.write(f"  Price: {lead['price_level']}\n")
            f.write(f"  Google Maps: {lead['google_maps_url']}\n")
            f.write(f"\nLEAD SCORE: {lead['lead_score']}/5\n")
            f.write("-" * 80 + "\n\n")
    
    print(f"✓ Text output saved to: {output_path}")

def save_as_json(results: List[Dict], output_path: Path):
    """Save results in JSON format"""
    output_data = {
        'generated_at': datetime.now().isoformat(),
        'total_leads': len(results),
        'note': 'Demo data for testing - not real businesses',
        'leads': results
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ JSON output saved to: {output_path}")

def save_as_csv(results: List[Dict], output_path: Path):
    """Save results in CSV format"""
    if not results:
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
    parser = argparse.ArgumentParser(
        description="Generate demo lead data for testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python demo_lead_generator.py --query "landscapers in New York" --max-results 10
  python demo_lead_generator.py --query "restaurants in NYC" --max-results 25 --format csv
        """
    )
    
    parser.add_argument(
        '--query', '-q',
        type=str,
        required=True,
        help='Search query (e.g., "landscapers in New York")'
    )
    
    parser.add_argument(
        '--max-results', '-m',
        type=int,
        default=20,
        help='Number of demo leads to generate (default: 20)'
    )
    
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['txt', 'json', 'csv'],
        default='txt',
        help='Output format (default: txt)'
    )
    
    args = parser.parse_args()
    
    # Parse query
    query_parts = args.query.lower().split(" in ")
    if len(query_parts) >= 2:
        business_type = query_parts[0].strip()
        city = query_parts[1].strip()
    else:
        business_type = args.query.lower()
        city = "New York"
    
    # Setup output
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    tmp_dir = project_root / ".tmp"
    tmp_dir.mkdir(exist_ok=True)
    
    output_filename = f"demo_leads_{timestamp}.{args.format}"
    output_path = tmp_dir / output_filename
    
    print("\n" + "=" * 80)
    print("DEMO LEAD GENERATOR")
    print("(Generates realistic sample data for testing)")
    print("=" * 80)
    print(f"Query: {args.query}")
    print(f"Business Type: {business_type}")
    print(f"Location: {city}")
    print(f"Number of Leads: {args.max_results}")
    print(f"Output Format: {args.format}")
    print(f"Output Path: {output_path}")
    print("=" * 80 + "\n")
    
    # Generate leads
    print(f"📊 Generating {args.max_results} demo leads...")
    results = []
    
    for i in range(1, args.max_results + 1):
        lead = generate_lead(business_type, city, i)
        results.append(lead)
        print(f"  [{i}/{args.max_results}] Generated: {lead['name']} - {lead['score_label']}")
    
    # Sort by lead score
    results.sort(key=lambda x: x['lead_score'], reverse=True)
    
    print(f"\n✓ Successfully generated {len(results)} demo leads")
    
    # Save results
    print(f"\n💾 Saving results...")
    
    if args.format == 'txt':
        save_as_text(results, output_path)
    elif args.format == 'json':
        save_as_json(results, output_path)
    elif args.format == 'csv':
        save_as_csv(results, output_path)
    
    # Print summary
    score_dist = {}
    for lead in results:
        score = lead['lead_score']
        score_dist[score] = score_dist.get(score, 0) + 1
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Leads Generated: {len(results)}")
    
    print(f"\nLead Score Distribution:")
    for score in sorted(score_dist.keys(), reverse=True):
        count = score_dist[score]
        pct = (count / len(results)) * 100
        labels = {5: "⭐⭐⭐⭐⭐ Excellent", 4: "⭐⭐⭐⭐ Good", 2: "⭐⭐ Fair", 1: "⭐ Low"}
        print(f"  {labels.get(score, 'Unknown')}: {count} leads ({pct:.0f}%)")
    
    high_value = [l for l in results if l['lead_score'] >= 4]
    print(f"\nHigh-Value Leads (Score 4-5): {len(high_value)}")
    
    print(f"\nOutput File: {output_path}")
    print("\n⚠️  NOTE: This is DEMO DATA for testing purposes.")
    print("    These are not real businesses. Use for demonstration only.")
    print("=" * 80 + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Google Places API Lead Scraper

Uses the official Google Places API (New) to fetch business leads reliably.
Bypasses CAPTCHAs and rate limiting issues of web scraping.

Usage:
    python scrape_gmb_api.py --query "abogados en Vigo" --max-results 20
"""

import os
import sys
import json
import time
import argparse
import requests
from typing import List, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"

# Try to load from .env, but handle macOS permission issues
try:
    load_dotenv(dotenv_path=env_path)
except (PermissionError, OSError) as e:
    print(f"⚠️  Warning: Could not read .env file ({e})")
    print("   Falling back to system environment variables...")

# Configuration - will use .env if loaded, otherwise system env vars
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
BASE_URL = "https://places.googleapis.com/v1/places:searchText"

def validate_api_key():
    """Ensure API key is present"""
    if not API_KEY:
        print("\n❌ ERROR: GOOGLE_PLACES_API_KEY not found in .env file.")
        print("Please follow the setup guide in 'directives/google_places_api_setup.md'")
        print("1. Get a key from Google Cloud Console")
        print("2. Add GOOGLE_PLACES_API_KEY=your_key to .env\n")
        sys.exit(1)

def search_places(query: str, max_results: int = 20) -> List[Dict]:
    """
    Search for places using Google Places API (New)
    """
    print(f"🔍 Searching for: '{query}' via API...")
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        # Field mask controls which fields are returned (affects billing)
        # We request standard fields needed for lead gen
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.websiteUri,places.rating,places.userRatingCount,places.businessStatus,places.primaryType"
    }
    
    payload = {
        "textQuery": query,
        "pageSize": min(max_results, 20)  # Max 20 per page
    }
    
    all_leads = []
    next_page_token = None
    
    while len(all_leads) < max_results:
        # Update payload for pagination
        if next_page_token:
            payload["pageToken"] = next_page_token
            # Google often requires a short delay before next page token is valid
            time.sleep(2) 
            
        try:
            response = requests.post(BASE_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            places = data.get("places", [])
            
            if not places:
                print("⚠️ No places found in this page.")
                break
                
            for place in places:
                # Extract and normalize data
                lead = {
                    "name": place.get("displayName", {}).get("text", "N/A"),
                    "address": place.get("formattedAddress", "N/A"),
                    "phone": place.get("nationalPhoneNumber", "N/A"),
                    "website": place.get("websiteUri", "N/A"),
                    "rating": place.get("rating", 0.0),
                    "reviews": place.get("userRatingCount", 0),
                    "business_status": place.get("businessStatus", "UNKNOWN"),
                    "category": place.get("primaryType", "N/A"),
                    "place_id": place.get("id"),
                    # Add placeholders for fields scraping provided but API basic text search might not
                    # (We could make extra calls for hours/price if needed, but keeping it simple/cheap)
                    "hours": "N/A", 
                    "price_level": "N/A",
                    "lead_source": "Google Places API"
                }
                
                # Filter out closed businesses if needed
                if lead["business_status"] == "OPERATIONAL":
                    all_leads.append(lead)
            
            print(f"✓ Found {len(places)} places (Total: {len(all_leads)})")
            
            # Pagination Logic
            next_page_token = data.get("nextPageToken")
            if not next_page_token or len(all_leads) >= max_results:
                break
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API Request Failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Details: {e.response.text}")
            break
            
    return all_leads[:max_results]

def calculate_lead_score(lead: Dict) -> Dict:
    """Add lead score based on available data"""
    score = 1
    
    if lead['website'] != "N/A":
        score += 2  # Website is good
        
    if lead['phone'] != "N/A":
        score += 1
        
    if lead.get('reviews', 0) > 5:
        score += 1

    labels = {
        5: "⭐⭐⭐⭐⭐ Excellent",
        4: "⭐⭐⭐⭐ Good",
        3: "⭐⭐⭐ Average",
        2: "⭐⭐ Fair",
        1: "⭐ Low"
    }
    
    lead['lead_score'] = min(score, 5)
    lead['score_label'] = labels.get(lead['lead_score'], "Unknown")
    
    return lead

def save_results(leads: List[Dict], query: str, output_format: str = 'json'):
    """Save results to .tmp folder"""
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    
    # Process leads (add scores)
    processed_leads = [calculate_lead_score(lead) for lead in leads]
    
    # Setup path
    project_root = Path(__file__).parent.parent
    tmp_dir = project_root / ".tmp"
    tmp_dir.mkdir(exist_ok=True)
    
    filename = f"api_leads_{timestamp}.{output_format}"
    filepath = tmp_dir / filename
    
    print(f"\n💾 Saving {len(processed_leads)} leads to {filepath}...")
    
    if output_format == 'json':
        output_data = {
            "query": query,
            "generated_at": timestamp,
            "source": "Google Places API",
            "results": processed_leads
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
            
    elif output_format == 'csv':
        import csv
        keys = processed_leads[0].keys() if processed_leads else []
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(processed_leads)
            
    print("✓ Save successful")
    return filepath

def main():
    parser = argparse.ArgumentParser(description="Google Places API Lead Scraper")
    parser.add_argument('--query', required=True, help="Search query (e.g., 'abogados en Vigo')")
    parser.add_argument('--max-results', type=int, default=20, help="Max number of results")
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help="Output format")
    
    args = parser.parse_args()
    
    # 1. Validate environment
    validate_api_key()
    
    # 2. Search
    leads = search_places(args.query, args.max_results)
    
    if not leads:
        print("❌ No results found. Exiting.")
        return
        
    # 3. Save
    save_results(leads, args.query, args.format)

if __name__ == "__main__":
    main()

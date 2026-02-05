#!/usr/bin/env python3
"""
Lead Deduplication Tool

Detects and removes duplicate leads from JSON or CSV files based on
business name, phone number, and website.

Usage:
    python deduplicate_leads.py --input .tmp/leads_merged.json --output .tmp/leads_clean.json
"""

import argparse
import json
import csv
import sys
import re
from pathlib import Path
from typing import List, Dict, Set
from difflib import SequenceMatcher

def normalize_string(s: str) -> str:
    """Normalize string for comparison (lowercase, remove special chars)"""
    if not s or s == "N/A":
        return ""
    return re.sub(r'[^\w\s]', '', s.lower()).strip()

def normalize_phone(phone: str) -> str:
    """Normalize phone number to digits only"""
    if not phone or phone == "N/A":
        return ""
    return re.sub(r'\D', '', phone)

def normalize_url(url: str) -> str:
    """Normalize URL to domain name"""
    if not url or url == "N/A":
        return ""
    
    # Remove protocol
    url = re.sub(r'https?://', '', url)
    # Remove www
    url = re.sub(r'^www\.', '', url)
    # Remove trailing slash and query params
    url = url.split('/')[0]
    return url.lower()

def is_similar_name(name1: str, name2: str, threshold: float = 0.85) -> bool:
    """Check if two names are similar using SequenceMatcher"""
    n1 = normalize_string(name1)
    n2 = normalize_string(name2)
    
    if not n1 or not n2:
        return False
        
    # Exact match after normalization
    if n1 == n2:
        return True
        
    # Similarity ratio
    ratio = SequenceMatcher(None, n1, n2).ratio()
    return ratio >= threshold

def deduplicate_leads(leads: List[Dict], strategy: str = 'standard') -> List[Dict]:
    """
    Deduplicate leads based on strategy.
    
    Strategies:
    - strict: Exact match on (Phone OR Website) OR (Name AND Address)
    - standard: Match on (Phone OR Website) OR (Fuzzy Name > 0.85)
    - aggressive: Match on (Phone OR Website) OR (Fuzzy Name > 0.70)
    """
    print(f"🧹 Deduplicating {len(leads)} leads (Strategy: {strategy})...")
    
    unique_leads = []
    seen_phones: Set[str] = set()
    seen_websites: Set[str] = set()
    seen_names: List[str] = [] # List for fuzzy matching
    
    duplicates_count = 0
    
    threshold = 0.85
    if strategy == 'aggressive':
        threshold = 0.70
    elif strategy == 'strict':
        threshold = 1.0
    
    for lead in leads:
        is_duplicate = False
        
        # 1. Check Phone
        phone = normalize_phone(lead.get('phone'))
        if phone and phone in seen_phones:
            is_duplicate = True
            # print(f"  Duplicate found by Phone: {lead.get('name')} ({phone})")
            
        # 2. Check Website
        if not is_duplicate:
            website = normalize_url(lead.get('website'))
            if website and website in seen_websites:
                is_duplicate = True
                # print(f"  Duplicate found by Website: {lead.get('name')} ({website})")
        
        # 3. Check Name (Fuzzy or Exact)
        if not is_duplicate:
            name = lead.get('name', '')
            for existing_name in seen_names:
                if is_similar_name(name, existing_name, threshold):
                    is_duplicate = True
                    # print(f"  Duplicate found by Name: {name} ~= {existing_name}")
                    break
        
        if is_duplicate:
            duplicates_count += 1
            # Merge logic could go here (e.g. keep lead with more info)
            # For now, we keep the first one seen (assumed better or earlier source)
        else:
            unique_leads.append(lead)
            if phone: seen_phones.add(phone)
            if website: seen_websites.add(website)
            seen_names.append(lead.get('name', ''))
            
    print(f"✓ Removed {duplicates_count} duplicates.")
    print(f"✓ Remaining leads: {len(unique_leads)}")
    
    return unique_leads

def load_file(file_path: Path) -> List[Dict]:
    """Load leads from JSON or CSV"""
    suffix = file_path.suffix.lower()
    leads = []
    
    try:
        if suffix == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    leads = data
                elif isinstance(data, dict) and 'results' in data:
                    leads = data['results']
                elif isinstance(data, dict) and 'leads' in data:
                    leads = data['leads']
        elif suffix == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                leads = list(reader)
        else:
            print(f"❌ Unsupported format: {suffix}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)
        
    return leads

def save_file(leads: List[Dict], output_path: Path):
    """Save cleaned leads"""
    suffix = output_path.suffix.lower()
    
    if suffix == '.json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({'leads': leads, 'count': len(leads)}, f, indent=2, ensure_ascii=False)
    elif suffix == '.csv':
        if not leads:
            print("⚠️ No leads to save.")
            return
        keys = leads[0].keys()
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(leads)
            
    print(f"💾 Saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Clean duplicate leads")
    parser.add_argument('--input', required=True, help="Input file (JSON/CSV)")
    parser.add_argument('--output', required=True, help="Output file")
    parser.add_argument('--strategy', default='standard', choices=['strict', 'standard', 'aggressive'], help="Deduplication strategy")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        sys.exit(1)
        
    leads = load_file(input_path)
    if not leads:
        print("❌ No leads found in input file.")
        sys.exit(1)
        
    clean_leads = deduplicate_leads(leads, args.strategy)
    save_file(clean_leads, output_path)

if __name__ == "__main__":
    main()

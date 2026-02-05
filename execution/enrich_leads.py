#!/usr/bin/env python3
"""
Lead Enrichment Tool (Google Custom Search)

Uses Google Custom Search API to find decision maker info (LinkedIn, InfoCIF)
that is not visible on the company website.

Queries:
1. LinkedIn: site:linkedin.com/in "Company Name" (CEO OR Founder OR Director)
2. InfoCIF: site:infocif.es "Company Name" (Administrador OR Cargo)

Usage:
    python enrich_leads.py --input .tmp/leads_analyzed.json --output .tmp/leads_enriched.json
"""

import argparse
import sys
import json
import time
import os
import re
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load env
load_dotenv()
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY") # reusing same key usually works if API enabled
CSE_ID = os.getenv("GOOGLE_CSE_ID")

def search_google(query: str, num_results: int = 3) -> List[Dict]:
    """Execute Google Custom Search"""
    if not API_KEY or not CSE_ID:
        print("❌ Error: Missing GOOGLE_PLACES_API_KEY or GOOGLE_CSE_ID")
        return []
        
    try:
        service = build("customsearch", "v1", developerKey=API_KEY)
        res = service.cse().list(
            q=query,
            cx=CSE_ID,
            num=num_results
        ).execute()
        return res.get('items', [])
    except Exception as e:
        print(f"    ⚠️  Search Error: {e}")
        return []

def extract_name_from_snippet(text: str) -> str:
    """Basic extraction of potential names from text"""
    # Look for patterns like "Nombre Apellido - Cargo"
    # This is hard to perfect without NLP, but we can look for " - " separators
    if " - " in text:
        parts = text.split(" - ")
        # Heuristic: Name is usually the first part if it's LinkedIn
        if len(parts[0].split()) <= 4:
            return parts[0].strip()
    return ""

def enrich_single_lead(lead: Dict) -> Dict:
    """Enrich a single lead with external data"""
    
    company = lead.get('name')
    city = lead.get('city', 'Vigo') # Default fallback
    
    print(f"  🔎 Enriching: {company}...")
    
    # 1. LinkedIn Search (Expanded roles)
    # "Company Name" "City" (CEO OR Director OR Socio OR Gerente OR Responsable OR Fundador) site:linkedin.com/in
    query_li = f'"{company}" {city} (CEO OR Director OR Socio OR Fundador OR Gerente OR Responsable OR Coordinador) site:linkedin.com/in'
    results_li = search_google(query_li, num_results=2)
    
    verified_owner = lead.get('owner_name', 'N/A')
    verified_title = lead.get('owner_title', 'N/A')
    
    # If we don't have a good owner name yet, try to get it from LinkedIn results
    if verified_owner == 'N/A' or verified_owner == '':
        for item in results_li:
            title = item.get('title', '')
            snippet = item.get('snippet', '')
            
            # LinkedIn Titles usually: "Name Surname - Job Title - Company | LinkedIn"
            if " - " in title and "LinkedIn" in title:
                parts = title.split(" - ")
                if len(parts) >= 2:
                    potential_name = parts[0].strip()
                    potential_role = parts[1].strip()
                    
                    # Basic validation: Name should be 2-4 words
                    if 2 <= len(potential_name.split()) <= 4:
                        verified_owner = potential_name
                        verified_title = potential_role
                        print(f"    found LinkedIn: {verified_owner} ({verified_title})")
                        break
    
    # 2. InfoCIF Search (Spain specific)
    # site:infocif.es "Company Name" Administrador
    if verified_owner == 'N/A':
        query_infocif = f'site:infocif.es "{company}" cargos'
        results_infocif = search_google(query_infocif, num_results=1)
        
        for item in results_infocif:
            snippet = item.get('snippet', '')
            # Snippets look like: "Relación de cargos... Juan Perez (Administrador)..."
            # It's messy to parse, but we can try simple regex for names in parentheses or near keywords
            pass # TODO: Add advanced parsing if needed
            
    # Update lead
    lead['owner_name'] = verified_owner
    lead['owner_title'] = verified_title
    lead['enrichment_source'] = "LinkedIn/Google" if results_li else "None"
    
    return lead

def process_leads(leads: List[Dict]) -> List[Dict]:
    enriched = []
    for i, lead in enumerate(leads, 1):
        print(f"[{i}/{len(leads)}]")
        
        # Only enrich if we don't already have a strong result from the website scrape
        # OR if the user specifically requested external verification
        # For now, let's try to fill gaps
        enrich_lead = False
        if lead.get('owner_name') == 'N/A' or lead.get('owner_name') is None:
            enrich_lead = True
        
        if enrich_lead:
            try:
                lead = enrich_single_lead(lead)
                time.sleep(1) # Rate limit politeness
            except Exception as e:
                print(f"    ❌ Error enriching: {e}")
        else:
            print(f"  ✓ Valid Info Exists: {lead.get('owner_name')}")
            
        enriched.append(lead)
    return enriched

def load_leads(file_path: Path) -> List[Dict]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Handle standard wrapper or list
            if isinstance(data, dict):
                return data.get('leads', data.get('results', []))
            return data
    except Exception as e:
        print(f"❌ Error loading: {e}")
        sys.exit(1)

def save_leads(leads: List[Dict], output_path: Path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({'leads': leads, 'count': len(leads)}, f, indent=2, ensure_ascii=False)
    print(f"\nSaved enriched leads to {output_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    if not CSE_ID:
        print("❌ Error: GOOGLE_CSE_ID not found in .env")
        sys.exit(1)
        
    leads = load_leads(Path(args.input))
    enriched_leads = process_leads(leads)
    save_leads(enriched_leads, Path(args.output))

if __name__ == "__main__":
    main()

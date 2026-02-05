#!/usr/bin/env python3
"""
Google Sheets CSV Exporter

Exports lead data to a Rich CSV format optimized for manual upload to Google Sheets
and subsequent automation via n8n.

Features:
- Prioritizes "Decision Maker" (Owner) info.
- Includes "Pain Point Details" and "Proposed Solution" for AI email generation.
- No HubSpot specific mapping (straight data dump).

Usage:
    python export_to_sheets_csv.py --input .tmp/leads_enriched.json --output .tmp/sheets_import.csv
"""

import argparse
import sys
import json
import csv
from pathlib import Path
from typing import List, Dict

def map_lead_to_row(lead: Dict) -> Dict:
    """Map internal lead format to Google Sheets columns"""
    
    # 1. Owner Identification
    owner_name = lead.get('owner_name', 'N/A')
    if owner_name in ['N/A', '', None]:
        # Fallback to generic if logic permits, but kept 'N/A' to prompt manual review if needed
        pass
        
    owner_email = lead.get('owner_email', 'N/A')
    generic_email = lead.get('email', 'N/A')
    
    # Smart Email Selection for Column "Email Contacto"
    # User prefers Personal > Generic. 
    # We will provide both columns just in case, but "Target Email" is the main one.
    target_email = owner_email if owner_email != 'N/A' else generic_email
    
    # 2. Pain Point Logic
    pain_label = lead.get('pain_point', 'Ninguno')
    pain_detail = lead.get('pain_point_details', '')
    solution = lead.get('proposed_solution', '')
    
    # 3. Screenshot
    screenshot_path = lead.get('screenshot_path', '')
    if not screenshot_path:
        # Fallback to predictive path if not present (although capture_screenshots should add it)
        clean_name = lead.get('name', '').replace(' ', '_')
        screenshot_path = f".tmp/screenshots/{clean_name}.png"

    return {
        "Business Name": lead.get('name', ''),
        "Target Email": target_email,
        "Decision Maker Name": owner_name,
        "Decision Maker Role": lead.get('owner_title', ''),
        "Pain Point Label": pain_label,
        "Pain Point Details": pain_detail,
        "Proposed Solution": solution,
        "Opportunity Score": lead.get('opportunity_score', 0),
        "Website": lead.get('website', ''),
        "City": lead.get('city', 'Vigo'),
        "Address": lead.get('address', ''),
        "Phone": lead.get('phone', ''), # Included for Sheets just in case (hidden col?)
        "Rating": lead.get('rating', ''),
        "Reviews": lead.get('reviews', ''),
        "Owner Email (Raw)": owner_email,
        "Generic Email (Raw)": generic_email,
        "Enrichment Source": lead.get('enrichment_source', 'None'),
        "Last Updated": "Today"
    }

def process_leads(leads: List[Dict]) -> List[Dict]:
    return [map_lead_to_row(lead) for lead in leads]

def load_leads(file_path: Path) -> List[Dict]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                # Handle possible wrappers
                return data.get('leads', data.get('results', []))
            return data
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)

def save_csv(leads: List[Dict], output_path: Path):
    if not leads:
        print("⚠️ No leads to export.")
        return
        
    # Get headers from first row
    fieldnames = list(leads[0].keys())
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)
        
    print(f"✓ Saved {len(leads)} rows to {output_path}")
    print("  (Upload this CSV to Google Drive/Sheets for n8n automation)")

def main():
    parser = argparse.ArgumentParser(description="Export to Google Sheets CSV")
    parser.add_argument('--input', required=True, help="Input JSON file")
    parser.add_argument('--output', required=True, help="Output CSV file")
    
    args = parser.parse_args()
    
    leads = load_leads(Path(args.input))
    processed = process_leads(leads)
    save_csv(processed, Path(args.output))

if __name__ == "__main__":
    main()

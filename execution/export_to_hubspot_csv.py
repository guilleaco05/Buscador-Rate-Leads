#!/usr/bin/env python3
"""
HubSpot CSV Exporter

Exports lead data to a CSV format optimized for one-click import into HubSpot CRM.
Maps system fields to HubSpot standard properties.

HubSpot Mapping:
- Name -> Company Name
- Website -> Website URL
- Phone -> Phone Number
- Address -> Street Address
- Lead Score -> Lead Status (Open/Qualified)
- Note -> Description (includes screenshot link)

Usage:
    python export_to_hubspot_csv.py --input .tmp/leads.json --output .tmp/hubspot_import.csv
"""

import argparse
import sys
import json
import csv
from pathlib import Path
from typing import List, Dict

def map_lead_to_hubspot(lead: Dict) -> Dict:
    """Map internal lead format to HubSpot CSV columns"""
    
    # Determine Status based on Score
    score = lead.get('lead_score', 0)
    status = "New"
    if score >= 4:
        status = "Open"
    elif score >= 2:
        status = "Unqualified"
        
    # Prepare Note (Description)
    lines = []
    lines.append(f"Source: Lead Generator ({lead.get('lead_source', 'Unknown')})")
    lines.append(f"Rating: {lead.get('rating')} ({lead.get('reviews')} reviews)")
    
    if lead.get('pain_point'):
        lines.append(f"Pain Point: {lead['pain_point']}")
        
    # Add screenshot path
    screenshot_name = lead.get('name', '').replace(' ', '_')
    lines.append(f"Screenshot ID: {screenshot_name}")

    description = "\n".join(lines)

    # Prioritize Owner Email, fallback to generic if not found (but user prefers owner)
    email_to_use = lead.get('owner_email', '').replace("N/A", "")
    if not email_to_use or email_to_use == "":
        email_to_use = lead.get('email', '').replace("N/A", "") 
        
    firstname = lead.get('owner_name', '').replace("N/A", "")
    lastname = ""
    # Naive split for First/Last name
    if firstname and " " in firstname:
        try:
            parts = firstname.split(" ", 1)
            firstname = parts[0]
            lastname = parts[1]
        except:
            pass

    return {
        "First Name": firstname,
        "Last Name": lastname,
        "Email": email_to_use, 
        "Company name": lead.get('name', ''),
        "Website URL": lead.get('website', '').replace("N/A", ""),
        # "Phone number": lead.get('phone', '').replace("N/A", ""), # REMOVED per user request
        "City": "Vigo", 
        "Street address": lead.get('address', '').replace("N/A", ""),
        "Lead Status": status,
        "Pain Point": lead.get('pain_point', ''), # Custom property
        "Job Title": lead.get('owner_title', '').replace("N/A", ""),
        "Description": description,
        "Industry": "Legal Services" 
    }

def process_leads(leads: List[Dict]) -> List[Dict]:
    """Process all leads"""
    return [map_lead_to_hubspot(lead) for lead in leads]

def load_leads(file_path: Path) -> List[Dict]:
    """Load leads from JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data.get('results', data.get('leads', []))
            return data
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)

def save_csv(leads: List[Dict], output_path: Path):
    """Save CSV with HubSpot headers"""
    if not leads:
        print("⚠️ No leads to export.")
        return
        
    keys = leads[0].keys()
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(leads)
        
    print(f"✓ Saved {len(leads)} contacts to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Export to HubSpot CSV")
    parser.add_argument('--input', required=True, help="Input Cleaned JSON file")
    parser.add_argument('--output', required=True, help="Output CSV file")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"❌ Input not found: {input_path}")
        sys.exit(1)
        
    leads = load_leads(input_path)
    hubspot_leads = process_leads(leads)
    save_csv(hubspot_leads, output_path)
    
    print("\nNext Steps:")
    print("1. Go to HubSpot > Contacts > Import")
    print("2. Upload the CSV file")
    print("3. Verify mapping (Auto-map should work)")
    print("4. Done!")

if __name__ == "__main__":
    main()

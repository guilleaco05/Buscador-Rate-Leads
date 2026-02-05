#!/usr/bin/env python3
"""
Export Leads to Google Sheets

Exports scraped lead data to a formatted Google Sheet with color-coding,
highlighting, and automatic formatting.

Usage:
    python export_to_sheets.py --input .tmp/gmb_leads_enhanced_20260128_161655.txt
"""

import argparse
import json
import csv
import sys
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Google API packages not installed.")
    print("Please run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# Google Sheets API scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
          'https://www.googleapis.com/auth/drive.file']


class GoogleSheetsExporter:
    """Export lead data to Google Sheets"""
    
    def __init__(self, credentials_path: str = 'credentials.json', token_path: str = 'token.json'):
        """
        Initialize the Google Sheets exporter.
        
        Args:
            credentials_path: Path to OAuth credentials file
            token_path: Path to save/load access token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.spreadsheet_id = None
        
    def authenticate(self):
        """Authenticate with Google Sheets API"""
        creds = None
        
        # Check if token.json exists
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing access token...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    print("\n❌ Error: credentials.json not found!")
                    print("\n📋 Setup Instructions:")
                    print("1. Go to https://console.cloud.google.com/")
                    print("2. Create a new project or select existing")
                    print("3. Enable Google Sheets API")
                    print("4. Create OAuth 2.0 credentials (Desktop app)")
                    print("5. Download credentials as 'credentials.json'")
                    print("6. Place credentials.json in project root")
                    print("\nFor detailed instructions, see:")
                    print("https://developers.google.com/sheets/api/quickstart/python")
                    sys.exit(1)
                
                print("🔐 Opening browser for Google authentication...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=8080)
            
            # Save credentials for next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
            print("✓ Authentication successful! Token saved.")
        
        try:
            self.service = build('sheets', 'v4', credentials=creds)
            print("✓ Connected to Google Sheets API")
        except Exception as e:
            print(f"❌ Error connecting to Google Sheets API: {e}")
            sys.exit(1)
    
    def create_spreadsheet(self, title: str) -> str:
        """
        Create a new Google Sheet.
        
        Args:
            title: Title for the spreadsheet
            
        Returns:
            Spreadsheet ID
        """
        try:
            spreadsheet = {
                'properties': {
                    'title': title
                }
            }
            
            spreadsheet = self.service.spreadsheets().create(
                body=spreadsheet,
                fields='spreadsheetId'
            ).execute()
            
            self.spreadsheet_id = spreadsheet.get('spreadsheetId')
            print(f"✓ Created spreadsheet: {title}")
            print(f"  ID: {self.spreadsheet_id}")
            
            return self.spreadsheet_id
            
        except HttpError as e:
            print(f"❌ Error creating spreadsheet: {e}")
            sys.exit(1)
    
    def write_data(self, leads: List[Dict]):
        """
        Write lead data to the spreadsheet.
        
        Args:
            leads: List of lead dictionaries
        """
        if not self.spreadsheet_id:
            print("❌ Error: No spreadsheet created")
            return
        
        # Prepare header row
        headers = [
            'Lead #', 'Lead Score', 'Score Label', 'Business Name', 'Category',
            'Rating', 'Reviews', 'Address', 'Phone', 'Email', 'Website',
            'Facebook', 'Instagram', 'TikTok', 'LinkedIn', 'Twitter/X',
            'Hours', 'Price Level', 'Google Maps URL',
            # New pain point analysis columns
            'Punto de Dolor', 'Detalles del Punto de Dolor', 'Puntuación Oportunidad',
            'Nombre Propietario', 'Email Propietario', 'Cargo Propietario'
        ]
        
        # Prepare data rows
        rows = [headers]
        
        for lead in leads:
            row = [
                lead.get('lead_number', ''),
                lead.get('lead_score', ''),
                lead.get('score_label', ''),
                lead.get('name', ''),
                lead.get('category', ''),
                lead.get('rating', ''),
                lead.get('reviews', ''),
                lead.get('address', ''),
                lead.get('phone', ''),
                lead.get('email', ''),
                lead.get('website', ''),
                lead.get('facebook', ''),
                lead.get('instagram', ''),
                lead.get('tiktok', ''),
                lead.get('linkedin', ''),
                lead.get('twitter', ''),
                lead.get('hours', ''),
                lead.get('price_level', ''),
                lead.get('google_maps_url', ''),
                # Pain point analysis fields
                lead.get('pain_point', 'N/A'),
                lead.get('pain_point_details', 'N/A'),
                lead.get('opportunity_score', ''),
                lead.get('owner_name', 'N/A'),
                lead.get('owner_email', 'N/A'),
                lead.get('owner_title', 'N/A'),
            ]
            rows.append(row)
        
        try:
            # Write data
            body = {
                'values': rows
            }
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='A1',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            print(f"✓ Wrote {len(leads)} leads to spreadsheet")
            
        except HttpError as e:
            print(f"❌ Error writing data: {e}")
    
    def format_spreadsheet(self, num_rows: int):
        """
        Apply formatting to the spreadsheet.
        
        Args:
            num_rows: Total number of rows (including header)
        """
        if not self.spreadsheet_id:
            return
        
        requests = []
        
        # Freeze header row
        requests.append({
            'updateSheetProperties': {
                'properties': {
                    'sheetId': 0,
                    'gridProperties': {
                        'frozenRowCount': 1
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        })
        
        # Format header row (bold, background color)
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {
                            'red': 0.2,
                            'green': 0.6,
                            'blue': 0.9
                        },
                        'textFormat': {
                            'bold': True,
                            'foregroundColor': {
                                'red': 1.0,
                                'green': 1.0,
                                'blue': 1.0
                            }
                        },
                        'horizontalAlignment': 'CENTER'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
            }
        })
        
        # Auto-resize columns
        requests.append({
            'autoResizeDimensions': {
                'dimensions': {
                    'sheetId': 0,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': 25  # Updated to include pain point columns
                }
            }
        })
        
        # Apply conditional formatting for lead scores
        # Score 5 - Dark Green
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': 0,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows,
                        'startColumnIndex': 1,
                        'endColumnIndex': 2
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'NUMBER_EQ',
                            'values': [{'userEnteredValue': '5'}]
                        },
                        'format': {
                            'backgroundColor': {
                                'red': 0.7,
                                'green': 0.9,
                                'blue': 0.7
                            }
                        }
                    }
                },
                'index': 0
            }
        })
        
        # Score 4 - Light Green
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': 0,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows,
                        'startColumnIndex': 1,
                        'endColumnIndex': 2
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'NUMBER_EQ',
                            'values': [{'userEnteredValue': '4'}]
                        },
                        'format': {
                            'backgroundColor': {
                                'red': 0.85,
                                'green': 0.95,
                                'blue': 0.85
                            }
                        }
                    }
                },
                'index': 1
            }
        })
        
        # Score 2 - Yellow
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': 0,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows,
                        'startColumnIndex': 1,
                        'endColumnIndex': 2
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'NUMBER_EQ',
                            'values': [{'userEnteredValue': '2'}]
                        },
                        'format': {
                            'backgroundColor': {
                                'red': 1.0,
                                'green': 0.95,
                                'blue': 0.7
                            }
                        }
                    }
                },
                'index': 2
            }
        })
        
        try:
            body = {'requests': requests}
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()
            
            print("✓ Applied formatting to spreadsheet")
            
        except HttpError as e:
            print(f"⚠️  Warning: Could not apply formatting: {e}")
    
    def get_spreadsheet_url(self) -> str:
        """Get the URL of the created spreadsheet"""
        if self.spreadsheet_id:
            return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit"
        return None


def parse_json_file(file_path: Path) -> List[Dict]:
    """Parse JSON lead file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('leads', [])


def parse_csv_file(file_path: Path) -> List[Dict]:
    """Parse CSV lead file"""
    leads = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads


def parse_txt_file(file_path: Path) -> List[Dict]:
    """Parse formatted text lead file"""
    leads = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by lead separator
    lead_blocks = re.split(r'={80}\nLEAD #\d+', content)[1:]  # Skip header
    
    for i, block in enumerate(lead_blocks, 1):
        lead = {'lead_number': i}
        
        # Extract score label
        score_match = re.search(r'- (.+?)\n={80}', block)
        if score_match:
            lead['score_label'] = score_match.group(1).strip()
            # Extract numeric score
            if '⭐⭐⭐⭐⭐' in lead['score_label']:
                lead['lead_score'] = 5
            elif '⭐⭐⭐⭐' in lead['score_label']:
                lead['lead_score'] = 4
            elif '⭐⭐' in lead['score_label']:
                lead['lead_score'] = 2
            else:
                lead['lead_score'] = 1
        
        # Extract fields
        patterns = {
            'name': r'Business Name: (.+)',
            'category': r'Category: (.+)',
            'rating': r'Rating: ([\d.]+)',
            'reviews': r'\((.+?) reviews?\)',
            'address': r'Address: (.+)',
            'phone': r'Phone: (.+)',
            'email': r'Email: (.+)',
            'website': r'Website: (.+)',
            'facebook': r'Facebook: (.+)',
            'instagram': r'Instagram: (.+)',
            'tiktok': r'TikTok: (.+)',
            'linkedin': r'LinkedIn: (.+)',
            'twitter': r'Twitter/X: (.+)',
            'hours': r'Hours: (.+)',
            'price_level': r'Price: (.+)',
            'google_maps_url': r'Google Maps: (.+)',
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, block)
            if match:
                lead[field] = match.group(1).strip()
            else:
                lead[field] = 'N/A'
        
        leads.append(lead)
    
    return leads


def load_leads(file_path: Path) -> List[Dict]:
    """Load leads from file (auto-detect format)"""
    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)
    
    # Detect format by extension
    ext = file_path.suffix.lower()
    
    try:
        if ext == '.json':
            print(f"📄 Loading JSON file: {file_path.name}")
            return parse_json_file(file_path)
        elif ext == '.csv':
            print(f"📄 Loading CSV file: {file_path.name}")
            return parse_csv_file(file_path)
        elif ext == '.txt':
            print(f"📄 Loading TXT file: {file_path.name}")
            return parse_txt_file(file_path)
        else:
            print(f"❌ Error: Unsupported file format: {ext}")
            print("   Supported formats: .json, .csv, .txt")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error parsing file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Export lead data to Google Sheets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python export_to_sheets.py --input .tmp/gmb_leads_enhanced_20260128_161655.txt
  python export_to_sheets.py --input .tmp/demo_leads.json --sheet-name "NYC Landscapers"
  python export_to_sheets.py --input .tmp/leads.csv --share-email "colleague@example.com"
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help='Path to lead data file (.json, .csv, or .txt)'
    )
    
    parser.add_argument(
        '--sheet-name', '-n',
        type=str,
        help='Name for the Google Sheet (default: auto-generated)'
    )
    
    parser.add_argument(
        '--share-email', '-s',
        type=str,
        help='Email address to share the sheet with'
    )
    
    args = parser.parse_args()
    
    # Load leads
    input_path = Path(args.input)
    leads = load_leads(input_path)
    
    if not leads:
        print("❌ Error: No leads found in file")
        sys.exit(1)
    
    print(f"✓ Loaded {len(leads)} leads")
    
    # Generate sheet name
    if args.sheet_name:
        sheet_name = args.sheet_name
    else:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        sheet_name = f"GMB Leads - {timestamp}"
    
    print("\n" + "=" * 80)
    print("GOOGLE SHEETS EXPORT")
    print("=" * 80)
    print(f"Input File: {input_path}")
    print(f"Total Leads: {len(leads)}")
    print(f"Sheet Name: {sheet_name}")
    print("=" * 80 + "\n")
    
    # Initialize exporter
    exporter = GoogleSheetsExporter()
    
    # Authenticate
    print("🔐 Authenticating with Google...")
    exporter.authenticate()
    
    # Create spreadsheet
    print(f"\n📊 Creating spreadsheet...")
    exporter.create_spreadsheet(sheet_name)
    
    # Write data
    print(f"\n📝 Writing data...")
    exporter.write_data(leads)
    
    # Format spreadsheet
    print(f"\n🎨 Applying formatting...")
    exporter.format_spreadsheet(len(leads) + 1)  # +1 for header
    
    # Get URL
    url = exporter.get_spreadsheet_url()
    
    # Print summary
    print("\n" + "=" * 80)
    print("✅ EXPORT COMPLETE!")
    print("=" * 80)
    print(f"Spreadsheet: {sheet_name}")
    print(f"Total Leads: {len(leads)}")
    print(f"\n🔗 URL: {url}")
    print("\n📋 Open this link to view your leads in Google Sheets")
    
    if args.share_email:
        print(f"\n⚠️  Note: Sharing with {args.share_email} requires additional setup")
        print("   You can manually share the sheet using the URL above")
    
    print("=" * 80 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

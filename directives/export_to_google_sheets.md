# Export Leads to Google Sheets

## Goal
Export scraped lead data to Google Sheets for easy sharing, collaboration, and CRM integration. Automatically creates a formatted spreadsheet with all lead information including contact details, social media links, and lead scores.

## Inputs
- `input_file`: Path to the lead data file (JSON, CSV, or TXT format)
- `sheet_name`: (Optional) Name for the Google Sheet (default: "GMB Leads - [timestamp]")
- `share_email`: (Optional) Email address to share the sheet with

## Execution

### Basic Usage
```bash
python execution/export_to_sheets.py --input .tmp/gmb_leads_enhanced_20260128_161655.txt
```

### With Custom Sheet Name
```bash
python execution/export_to_sheets.py \
  --input .tmp/gmb_leads_enhanced_20260128_161655.txt \
  --sheet-name "NYC Landscapers - Jan 2026"
```

### Share with Specific Email
```bash
python execution/export_to_sheets.py \
  --input .tmp/gmb_leads_enhanced_20260128_161655.txt \
  --share-email "colleague@example.com"
```

## Outputs

### Google Sheet Structure
The created sheet will have the following columns:
1. Lead #
2. Lead Score
3. Score Label
4. Business Name
5. Category
6. Rating
7. Reviews
8. Address
9. Phone
10. Email
11. Website
12. Facebook
13. Instagram
14. TikTok
15. LinkedIn
16. Twitter/X
17. Hours
18. Price Level
19. Google Maps URL

### Formatting
- **Header row**: Bold, frozen, colored background
- **High-value leads** (Score 4-5): Highlighted in green
- **Score column**: Color-coded (5=dark green, 4=light green, 2=yellow, 1=gray)
- **Email column**: Highlighted if present
- **Social media columns**: Highlighted if links present
- **Auto-sized columns** for readability

### Permissions
- Created as private by default
- Can be shared with specific emails
- Link sharing can be enabled

## Tools & Dependencies

### Required Python Packages
- `google-auth` - Google authentication
- `google-auth-oauthlib` - OAuth flow
- `google-auth-httplib2` - HTTP library for Google APIs
- `google-api-python-client` - Google Sheets API client
- `python-dotenv` - Environment variables

### Google Cloud Setup
1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create OAuth 2.0 credentials
4. Download credentials as `credentials.json`
5. Place in project root directory

### First-Time Setup
```bash
# Install dependencies
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Run script (will open browser for OAuth)
python execution/export_to_sheets.py --input .tmp/your_leads.json

# Token will be saved to token.json for future use
```

## Edge Cases & Constraints

### Authentication
- **First run**: Opens browser for Google OAuth consent
- **Subsequent runs**: Uses saved token.json
- **Token expiry**: Automatically refreshes if expired
- **Missing credentials**: Clear error message with setup instructions

### File Formats
- **JSON**: Preferred format, full data structure
- **CSV**: Supported, reads all columns
- **TXT**: Parsed from formatted text output
- **Empty files**: Error with helpful message

### Data Validation
- **Missing fields**: Displayed as "N/A" in sheet
- **Long text**: Wrapped in cells
- **URLs**: Automatically converted to clickable links
- **Special characters**: Properly escaped

### Rate Limiting
- **Google Sheets API**: 100 requests per 100 seconds per user
- **Batch operations**: Used to minimize API calls
- **Large datasets**: Chunked into batches of 1000 rows

### Sheet Size Limits
- **Maximum rows**: 10,000,000 (Google Sheets limit)
- **Maximum columns**: 18,278 (Google Sheets limit)
- **Practical limit**: ~50,000 leads per sheet for performance

## Error Handling

### Authentication Errors
- Missing credentials.json → Provide setup instructions
- Invalid token → Delete token.json and re-authenticate
- Permission denied → Check API is enabled in Google Cloud

### API Errors
- Rate limit exceeded → Wait and retry with exponential backoff
- Network errors → Retry up to 3 times
- Invalid data → Skip row and log error

### File Errors
- File not found → Clear error message with path
- Invalid format → Attempt to parse, fall back to manual specification
- Empty file → Error with suggestion to check scraper output

## Performance Optimization

### Batch Operations
- Create sheet in single API call
- Write data in batches of 1000 rows
- Apply formatting in bulk

### Caching
- Reuse authenticated client
- Cache spreadsheet ID for updates

## Security

### Credentials Storage
- `credentials.json` - OAuth client credentials (gitignored)
- `token.json` - User access token (gitignored)
- Never commit these files to version control

### Permissions
- Sheets created as private by default
- Explicit sharing required
- Can set to "anyone with link" if needed

## Learnings

### Version 1.0 (Initial)
- Created initial implementation with Google Sheets API
- Basic data export working
- Formatting and color-coding implemented

### Future Improvements
- [ ] Support for updating existing sheets (append mode)
- [ ] Multiple sheet tabs (one per city/category)
- [ ] Charts and pivot tables generation
- [ ] Automatic duplicate detection
- [ ] Integration with Google Data Studio
- [ ] Scheduled exports (cron job)
- [ ] Email notifications when export completes
- [ ] Export to other platforms (Airtable, Notion, etc.)

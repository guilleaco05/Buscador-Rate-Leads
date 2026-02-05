# 📊 Google Sheets Export - Setup Guide

## ✨ Overview

Export your scraped leads directly to Google Sheets with automatic formatting, color-coding, and organization. Perfect for sharing with team members, importing to CRM, or analyzing data.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 2: Get Google API Credentials

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** (or select existing)
3. **Enable Google Sheets API**:
   - Click "Enable APIs and Services"
   - Search for "Google Sheets API"
   - Click "Enable"
4. **Create OAuth credentials**:
   - Go to "Credentials" tab
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Desktop app"
   - Download credentials as JSON
5. **Save credentials**:
   - Rename file to `credentials.json`
   - Place in project root: `/Users/Guille/Desktop/Antigravity/credentials.json`

### Step 3: Run Export
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/gmb_leads_enhanced_20260128_161655.txt
```

**First time**: Browser will open for Google OAuth consent  
**After that**: Uses saved token automatically

---

## 📋 Detailed Setup Instructions

### 1. Google Cloud Project Setup

#### Create Project
1. Visit https://console.cloud.google.com/
2. Click project dropdown (top left)
3. Click "New Project"
4. Name it: "Lead Generation System"
5. Click "Create"

#### Enable Google Sheets API
1. In the search bar, type "Google Sheets API"
2. Click on "Google Sheets API"
3. Click "Enable"
4. Wait for API to be enabled (~30 seconds)

#### Create OAuth 2.0 Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: "External"
   - App name: "Lead Generation System"
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue"
   - Scopes: Skip (click "Save and Continue")
   - Test users: Add your email
   - Click "Save and Continue"
4. Back to Create OAuth client ID:
   - Application type: "Desktop app"
   - Name: "Lead Exporter"
   - Click "Create"
5. Download JSON file
6. Rename to `credentials.json`
7. Move to project root

### 2. File Placement

```
Antigravity/
├── credentials.json          # ← Place here (gitignored)
├── token.json               # ← Auto-generated on first run
├── execution/
│   └── export_to_sheets.py
└── .tmp/
    └── your_leads.txt
```

**Important**: Both `credentials.json` and `token.json` are in `.gitignore` - they will NOT be committed to git.

---

## 🎯 Usage Examples

### Basic Export
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/gmb_leads_enhanced_20260128_161655.txt
```

### With Custom Sheet Name
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/demo_leads_20260128_161817.txt \
  --sheet-name "NYC Landscapers - January 2026"
```

### Export JSON File
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/gmb_leads_enhanced_20260128_161655.json
```

### Export CSV File
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/gmb_leads_enhanced_20260128_161655.csv
```

---

## 📊 What Gets Exported

### Columns in Google Sheet

1. **Lead #** - Sequential number
2. **Lead Score** - 1-5 score (color-coded)
3. **Score Label** - Excellent/Good/Fair/Low
4. **Business Name**
5. **Category**
6. **Rating** - Star rating
7. **Reviews** - Number of reviews
8. **Address** - Full address
9. **Phone** - Phone number
10. **Email** - Email address (if found)
11. **Website** - Website URL (clickable)
12. **Facebook** - Facebook link (clickable)
13. **Instagram** - Instagram link (clickable)
14. **TikTok** - TikTok link (clickable)
15. **LinkedIn** - LinkedIn link (clickable)
16. **Twitter/X** - Twitter link (clickable)
17. **Hours** - Business hours
18. **Price Level** - $ symbols
19. **Google Maps URL** - Maps link (clickable)

### Automatic Formatting

✅ **Header Row**: Blue background, white bold text, frozen  
✅ **Lead Score Color-Coding**:
   - Score 5: Dark green background
   - Score 4: Light green background
   - Score 2: Yellow background
   - Score 1: No color

✅ **Auto-sized Columns**: All columns sized to fit content  
✅ **Clickable URLs**: All links are clickable  
✅ **Frozen Header**: Header stays visible when scrolling  

---

## 🔐 Authentication Flow

### First Run
1. Script opens browser automatically
2. Google login page appears
3. Select your Google account
4. Grant permissions (read/write spreadsheets)
5. Browser shows "Authentication successful"
6. Token saved to `token.json`
7. Export proceeds automatically

### Subsequent Runs
1. Script uses saved `token.json`
2. No browser interaction needed
3. Export proceeds immediately

### Token Refresh
- Tokens expire after ~7 days
- Script automatically refreshes if expired
- No action needed from you

---

## 📈 Output Example

After running the export, you'll get:

```
================================================================================
✅ EXPORT COMPLETE!
================================================================================
Spreadsheet: GMB Leads - 2026-01-28 16:50
Total Leads: 10

🔗 URL: https://docs.google.com/spreadsheets/d/1abc...xyz/edit

📋 Open this link to view your leads in Google Sheets
================================================================================
```

Click the URL to open your formatted Google Sheet!

---

## 🎨 Sheet Appearance

### Header Row
```
| Lead # | Lead Score | Score Label | Business Name | Category | ... |
|--------|------------|-------------|---------------|----------|-----|
```
**Style**: Blue background, white bold text

### Data Rows (Score 5 - Excellent)
```
| 1 | 5 | ⭐⭐⭐⭐⭐ Excellent | Pro Lawn Care | Landscaping | ... |
```
**Style**: Dark green background on score column

### Data Rows (Score 4 - Good)
```
| 2 | 4 | ⭐⭐⭐⭐ Good | Elite Services | Plumbing | ... |
```
**Style**: Light green background on score column

### Data Rows (Score 2 - Fair)
```
| 3 | 2 | ⭐⭐ Fair | Quality Shop | Retail | ... |
```
**Style**: Yellow background on score column

### Data Rows (Score 1 - Low)
```
| 4 | 1 | ⭐ Low | Basic Business | Services | ... |
```
**Style**: No color

---

## 🔧 Troubleshooting

### "credentials.json not found"

**Solution**: Follow setup instructions above to download credentials from Google Cloud Console.

```bash
# Check if file exists
ls -la credentials.json

# Should be in project root
/Users/Guille/Desktop/Antigravity/credentials.json
```

### "Authentication failed"

**Solutions**:
1. Delete `token.json` and try again
2. Check that Google Sheets API is enabled
3. Verify credentials.json is valid
4. Try re-downloading credentials

```bash
# Delete token and re-authenticate
rm token.json
python3 execution/export_to_sheets.py --input .tmp/your_leads.txt
```

### "Permission denied"

**Solution**: Make sure you granted all permissions during OAuth flow.

1. Delete `token.json`
2. Run export again
3. When browser opens, carefully grant all permissions
4. Don't skip any permission screens

### "File not found"

**Solution**: Check the path to your lead file.

```bash
# List available lead files
ls -la .tmp/

# Use correct path
python3 execution/export_to_sheets.py \
  --input .tmp/gmb_leads_enhanced_20260128_161655.txt
```

### "No leads found in file"

**Solution**: Verify file has data.

```bash
# Check file content
cat .tmp/your_leads.txt

# Try with demo data
python3 execution/demo_lead_generator.py \
  --query "test" \
  --max-results 5

python3 execution/export_to_sheets.py \
  --input .tmp/demo_leads_*.txt
```

---

## 🔄 Complete Workflow

### 1. Generate Leads
```bash
# Option A: Real scraping
python3 execution/scrape_gmb_enhanced.py \
  --query "landscapers in New York" \
  --max-results 10

# Option B: Demo data
python3 execution/demo_lead_generator.py \
  --query "landscapers in New York" \
  --max-results 10
```

### 2. Export to Google Sheets
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/gmb_leads_enhanced_*.txt \
  --sheet-name "NYC Landscapers"
```

### 3. Open and Share
1. Click the URL in the output
2. Sheet opens in browser
3. Click "Share" button (top right)
4. Add collaborators or get shareable link

---

## 📊 Supported File Formats

### JSON Format
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/gmb_leads_enhanced_20260128_161655.json
```
- Best for programmatic processing
- Preserves all data structure

### CSV Format
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/gmb_leads_enhanced_20260128_161655.csv
```
- Good for Excel exports
- Easy to edit manually

### TXT Format
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/gmb_leads_enhanced_20260128_161655.txt
```
- Human-readable format
- Automatically parsed

---

## 🎯 Next Steps

### After Export

1. **Review the sheet** - Check data quality
2. **Share with team** - Click Share button
3. **Filter/Sort** - Use Google Sheets features
4. **Export to CRM** - Download as CSV if needed
5. **Create charts** - Visualize lead scores

### Advanced Usage

#### Filter High-Value Leads
In Google Sheets:
1. Click on "Lead Score" column
2. Click filter icon
3. Select only 4 and 5
4. View only high-value leads

#### Sort by Rating
1. Click on "Rating" column
2. Data → Sort sheet → Sort by Rating (Z→A)
3. Highest rated businesses first

#### Create Pivot Table
1. Data → Pivot table
2. Rows: Category
3. Values: COUNT of Lead #
4. See lead distribution by category

---

## 📚 Files Reference

- **Script**: `execution/export_to_sheets.py`
- **Directive**: `directives/export_to_google_sheets.md`
- **Credentials**: `credentials.json` (you create this)
- **Token**: `token.json` (auto-generated)

---

## ✅ Checklist

Before running export:

- [ ] Google Cloud project created
- [ ] Google Sheets API enabled
- [ ] OAuth credentials downloaded
- [ ] `credentials.json` in project root
- [ ] Dependencies installed (`pip install ...`)
- [ ] Lead file exists in `.tmp/`

Ready to export:

```bash
python3 execution/export_to_sheets.py \
  --input .tmp/your_leads_file.txt
```

---

## 🎉 Success!

Once exported, you'll have a beautifully formatted Google Sheet with:
- ✅ All lead data organized
- ✅ Color-coded by lead score
- ✅ Clickable links
- ✅ Frozen header
- ✅ Auto-sized columns
- ✅ Ready to share

**Perfect for team collaboration and CRM integration!** 📊

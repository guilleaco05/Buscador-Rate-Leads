# GMB Lead Scraper - Setup & Usage Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install required Python packages
pip install -r execution/requirements.txt
```

This will install:
- `selenium` - Browser automation
- `webdriver-manager` - Automatic ChromeDriver management
- `beautifulsoup4` - HTML parsing (for future enhancements)
- `python-dotenv` - Environment variable management

### 2. Verify Chrome Installation

The scraper uses Chrome/Chromium. Make sure you have Chrome installed:
- **Mac**: Chrome should be in `/Applications/Google Chrome.app`
- **Linux**: Install with `sudo apt-get install chromium-browser`
- **Windows**: Download from https://www.google.com/chrome/

The `webdriver-manager` will automatically download and manage the ChromeDriver.

### 3. Run Your First Scrape

```bash
# Basic usage - scrape 10 coffee shops in San Francisco
python3 execution/scrape_gmb.py --query "coffee shops in San Francisco" --max-results 10

# The results will be saved to .tmp/gmb_leads_[timestamp].txt
```

## 📖 Usage Examples

### Text Output (Default)
```bash
python3 execution/scrape_gmb.py \
  --query "restaurants in New York" \
  --max-results 20
```

### JSON Output
```bash
python3 execution/scrape_gmb.py \
  --query "plumbers in Los Angeles" \
  --max-results 15 \
  --format json
```

### CSV Output
```bash
python3 execution/scrape_gmb.py \
  --query "dentists in Miami" \
  --max-results 25 \
  --format csv
```

### Visible Browser Mode (for debugging)
```bash
python3 execution/scrape_gmb.py \
  --query "gyms in Chicago" \
  --max-results 10 \
  --no-headless
```

## 📊 Output Formats

### Text Format (.txt)
Human-readable format with clear sections:
```
================================================================================
LEAD #1
================================================================================
Business Name: Joe's Coffee Shop
Address: 123 Main St, San Francisco, CA 94102
Phone: (415) 555-0123
Website: https://joescoffee.com
Rating: 4.5 ⭐ (234 reviews)
Category: Coffee Shop
...
```

### JSON Format (.json)
Structured data for programmatic processing:
```json
{
  "generated_at": "2026-01-28T14:20:00",
  "total_leads": 10,
  "leads": [
    {
      "lead_number": 1,
      "name": "Joe's Coffee Shop",
      "address": "123 Main St, San Francisco, CA 94102",
      ...
    }
  ]
}
```

### CSV Format (.csv)
Spreadsheet-compatible format:
```csv
lead_number,name,address,phone,website,rating,reviews,category,...
1,Joe's Coffee Shop,123 Main St...,415-555-0123,https://...,4.5,234,...
```

## 🎯 Data Fields Extracted

For each business, the scraper attempts to extract:

- ✅ **Business Name**
- ✅ **Full Address**
- ✅ **Phone Number**
- ✅ **Website URL**
- ✅ **Rating** (stars)
- ✅ **Number of Reviews**
- ✅ **Business Category**
- ✅ **Hours of Operation**
- ✅ **Price Level** (if available)
- ✅ **Google Maps URL**

*Note: Some fields may show "N/A" if not available for a particular business.*

## ⚠️ Important Considerations

### Rate Limiting
- The scraper includes 2-second delays between requests
- Scraping too aggressively may trigger Google's rate limiting
- Recommended: Keep max-results under 50 per run

### CAPTCHA Detection
If Google detects automated access, you may see:
- No results returned
- Browser stuck on CAPTCHA page

**Solutions:**
- Use `--no-headless` to manually solve CAPTCHAs
- Reduce scraping frequency
- Consider using Google Places API instead (requires API key)

### Legal & Ethical Use
- ⚖️ Respect Google's Terms of Service
- 🔒 Use scraped data responsibly and legally
- 📧 Don't spam businesses with unsolicited emails
- ✅ Only scrape publicly available information

### Performance
- **Speed**: ~2-3 seconds per business (with delays)
- **Memory**: Minimal (results saved incrementally)
- **Network**: Requires stable internet connection

## 🔧 Troubleshooting

### "Command not found: python3"
Use `python` instead of `python3`:
```bash
python execution/scrape_gmb.py --query "..." --max-results 10
```

### "ChromeDriver not found"
The `webdriver-manager` should handle this automatically. If issues persist:
```bash
pip install --upgrade webdriver-manager
```

### "No results found"
Possible causes:
- CAPTCHA triggered (try `--no-headless`)
- Rate limiting (wait 5-10 minutes)
- Network issues (check internet connection)
- Invalid query (try a different search term)

### Browser crashes
- Ensure Chrome is properly installed
- Update Chrome to latest version
- Check available system memory

## 📈 Advanced Usage

### Batch Processing Multiple Queries
Create a shell script to process multiple searches:

```bash
#!/bin/bash
# batch_scrape.sh

queries=(
  "restaurants in NYC"
  "plumbers in LA"
  "dentists in Miami"
)

for query in "${queries[@]}"; do
  echo "Processing: $query"
  python3 execution/scrape_gmb.py --query "$query" --max-results 20 --format csv
  sleep 60  # Wait 1 minute between batches
done
```

### Combining Output Files
```bash
# Combine all CSV files
cat .tmp/gmb_leads_*.csv > all_leads.csv

# Count total leads
wc -l .tmp/gmb_leads_*.txt
```

## 🔮 Future Enhancements

Planned improvements (see `directives/scrape_gmb_leads.md` for details):
- [ ] Google Places API integration
- [ ] Email extraction from websites
- [ ] Social media profile detection
- [ ] Lead scoring algorithm
- [ ] Duplicate detection
- [ ] CRM export (Salesforce, HubSpot)
- [ ] Proxy rotation for large-scale scraping

## 📚 Related Files

- **Directive**: `directives/scrape_gmb_leads.md` - Full specification
- **Script**: `execution/scrape_gmb.py` - Main scraper
- **Output**: `.tmp/gmb_leads_*.{txt,json,csv}` - Results

## 💡 Tips for Best Results

1. **Be Specific**: Use detailed queries like "Italian restaurants in Brooklyn" vs "restaurants"
2. **Start Small**: Test with 5-10 results before running large batches
3. **Check Output**: Verify data quality before scaling up
4. **Respect Limits**: Don't overwhelm Google's servers
5. **Save Regularly**: Results are saved to `.tmp/` automatically

---

**Ready to generate leads?** Start with a simple query and scale up as needed!

```bash
python3 execution/scrape_gmb.py --query "your search here" --max-results 10
```

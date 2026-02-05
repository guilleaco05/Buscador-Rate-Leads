# Lead Generation: Google My Business Scraper

## Goal
Extract business listing details from Google My Business (GMB) profiles to generate qualified leads. Output data in structured text format for easy processing and analysis.

## Inputs
- `search_query`: Business type or category to search for (e.g., "restaurants in New York", "plumbers in Los Angeles")
- `max_results`: (Optional) Maximum number of results to scrape (default: 20)
- `output_format`: (Optional) Output format - 'txt', 'json', or 'csv' (default: 'txt')
- `scrape_websites`: (Optional) Scrape individual business websites for emails and social media (default: True)
- `score_leads`: (Optional) Calculate lead score based on available contact methods (default: True)

## Execution

### API Usage (Primary Method - Recommended)
```bash
python execution/scrape_gmb_api.py --query "coffee shops in San Francisco" --max-results 20
```

### Legacy Scraping (Fallback)
```bash
python execution/scrape_gmb.py --query "coffee shops in San Francisco" --max-results 10
```

### Advanced Usage
```bash
# Scrape with API (JSON output by default)
python execution/scrape_gmb_api.py --query "dentists in Miami" --max-results 25

# Scrape with API (CSV output)
python execution/scrape_gmb_api.py --query "restaurants in Boston" --max-results 50 --format csv
```

## Outputs

### Data Fields Extracted
- Business Name
- Address (full)
- Phone Number
- Website URL
- **Email Address** (extracted from website)
- **Social Media Links**:
  - Facebook
  - Instagram
  - TikTok
  - LinkedIn
  - X (Twitter)
- Rating (stars)
- Number of Reviews
- Business Category/Type
- Hours of Operation
- Price Level (if available)
- Description/About
- Google Maps URL
- **Lead Score** (1-5 points based on contact availability)

### Output Locations
- **Primary**: `.tmp/gmb_leads_[timestamp].txt` (or .json/.csv based on format)
- **Summary**: Console output with statistics (total found, successful extractions, errors)

### Text Format Example
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
Hours: Mon-Fri 7AM-6PM, Sat-Sun 8AM-5PM
Price: $$
Google Maps: https://maps.google.com/?cid=123456789
Description: Artisanal coffee and pastries in the heart of SF...
--------------------------------------------------------------------------------
```

## Lead Scoring System

### Scoring Methodology (5-Point Scale)

Each lead receives a score from 1-5 based on available contact methods:

**Base Score: 1 point** (all businesses start here)

**+3 points** if business has an email address  
**+1 point** if business has at least one social media profile

**Maximum Score: 5 points**

### Score Breakdown

- **5 points**: Email + Social Media (Best leads - multiple contact channels)
- **4 points**: Email only (Good leads - direct contact available)
- **2 points**: Social Media only (Moderate leads - indirect contact)
- **1 point**: No email or social media (Low priority - phone/website only)

### Usage

High-scoring leads (4-5 points) are prioritized for outreach as they:
- Have more contact options
- Are more digitally engaged
- Likely more responsive to digital marketing
- Easier to verify legitimacy

## Tools & Dependencies

### Required Python Packages
- `selenium` - Browser automation
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests
- `python-dotenv` - Environment variables
- `webdriver-manager` - Automatic driver management

### Optional API Integration
- Google Places API (for enhanced data, requires API key in `.env`)
- Fallback to web scraping if API not available

## Edge Cases & Constraints

### Rate Limiting
- **Issue**: Google may rate limit or block automated requests
- **Solution**: Implement delays between requests (2-5 seconds)
- **Mitigation**: Use rotating user agents, headless browser detection avoidance

### CAPTCHA Detection
- **Issue**: Google may present CAPTCHAs for automated access
- **Solution**: Pause execution and alert user to solve CAPTCHA manually
- **Alternative**: Use Google Places API as fallback

### Incomplete Data
- **Issue**: Some businesses may not have all fields populated
- **Solution**: Mark missing fields as "N/A" or "Not Available"
- **Handling**: Continue processing, don't fail on missing data

### Geographic Restrictions
- **Issue**: Search results may vary by location
- **Solution**: Document that results are based on server/IP location
- **Enhancement**: Add location parameter for targeted searches

### Dynamic Content Loading
- **Issue**: GMB uses JavaScript to load content dynamically
- **Solution**: Use Selenium with proper wait conditions
- **Timing**: Wait for elements to load before extraction

### Legal & Ethical Considerations
- **Terms of Service**: Respect Google's ToS and robots.txt
- **Rate Limiting**: Don't overwhelm servers with requests
- **Data Usage**: Use scraped data responsibly and legally
- **Privacy**: Don't scrape personal information beyond public business data

## Error Handling

### Network Errors
- Retry failed requests up to 3 times with exponential backoff
- Log failed URLs for manual review

### Parsing Errors
- Skip malformed entries and continue processing
- Log parsing errors with business name/URL for debugging

### Browser Crashes
- Implement graceful shutdown and cleanup
- Save partial results before exit

## Performance Optimization

### Batch Processing
- Process results in batches to manage memory
- Save intermediate results every 10 businesses

### Parallel Processing
- (Future enhancement) Use multiple browser instances for faster scraping
- Requires careful rate limit management

## Learnings

### Version 1.0 (Initial)
- Created initial implementation with Selenium
- Basic data extraction working
- Text output format implemented

### Future Improvements
- [ ] Add Google Places API integration as primary method
- [ ] Implement proxy rotation for large-scale scraping
- [ ] Add email extraction from websites
- [ ] Social media profile detection
- [ ] Lead scoring based on review quality and recency
- [ ] Duplicate detection and deduplication
- [ ] Export to CRM systems (Salesforce, HubSpot, etc.)

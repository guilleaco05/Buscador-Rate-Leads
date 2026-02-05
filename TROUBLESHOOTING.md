# 🔧 Troubleshooting Guide - GMB Scraper

## Common Issues & Solutions

### Issue 1: "Timeout waiting for results" or "No results found"

**Cause**: Google has detected automated access and is blocking the scraper or showing CAPTCHA.

**Solutions**:

#### Option A: Use Visible Browser Mode
```bash
python3 execution/scrape_gmb_enhanced.py \
  --query "landscapers in New York" \
  --max-results 10 \
  --no-headless
```
- Browser window will open
- If CAPTCHA appears, solve it manually
- Scraper will continue after CAPTCHA is solved

#### Option B: Use Demo Data Generator (Recommended for Testing)
```bash
python3 execution/demo_lead_generator.py \
  --query "landscapers in New York" \
  --max-results 10 \
  --format txt
```
- Generates realistic sample data instantly
- No Google blocking issues
- Perfect for testing workflows
- Shows exact output format

#### Option C: Wait and Retry
- Wait 10-15 minutes
- Try with a smaller batch (--max-results 5)
- Use a different search query

#### Option D: Use Google Places API (Future Enhancement)
- More reliable, no blocking
- Requires API key
- Higher rate limits
- Documented in directive for future implementation

---

### Issue 2: "Email extraction not working"

**Cause**: Not all businesses publish emails on their websites.

**Expected Behavior**:
- ~60-70% success rate for businesses with websites
- Service businesses have higher rates
- Retail/restaurants have lower rates

**Verification**:
1. Check if business has a website
2. Visit website manually to verify email exists
3. Some businesses use contact forms instead of emails

**Solution**:
- This is normal - focus on leads with score 4-5 (they have emails)
- Use demo generator to see expected format

---

### Issue 3: "Social media links not found"

**Cause**: Businesses may not link social media on their website.

**Expected Behavior**:
- ~70-80% success rate for digitally active businesses
- Links must be on the website to be detected
- Some businesses have social but don't link it

**Solution**:
- Normal behavior
- Manually search "[Business Name] Facebook" if needed
- Focus on high-scoring leads

---

### Issue 4: "Scraping is very slow"

**Cause**: Website scraping adds 10-15 seconds per lead.

**Solutions**:

#### Fast Mode (Skip Website Scraping)
```bash
python3 execution/scrape_gmb_enhanced.py \
  --query "landscapers in New York" \
  --max-results 20 \
  --no-website-scraping
```
- ~2-3 seconds per lead (much faster)
- Still gets GMB data (name, address, phone, etc.)
- No emails or social media
- All leads score 1

#### Reduce Batch Size
```bash
# Instead of 50 leads at once, do 10-20
python3 execution/scrape_gmb_enhanced.py \
  --query "landscapers in New York" \
  --max-results 10
```

#### Use Demo Generator for Testing
```bash
# Instant results for testing
python3 execution/demo_lead_generator.py \
  --query "landscapers in New York" \
  --max-results 50
```

---

### Issue 5: "Browser crashes or fails to start"

**Cause**: Chrome/ChromeDriver issues.

**Solutions**:

1. **Update Chrome**:
   - Download latest version from https://www.google.com/chrome/

2. **Reinstall webdriver-manager**:
   ```bash
   pip3 install --upgrade webdriver-manager
   ```

3. **Check Chrome installation**:
   ```bash
   # Mac
   ls -la "/Applications/Google Chrome.app"
   
   # If not found, install Chrome
   ```

4. **Try demo generator** (doesn't need browser):
   ```bash
   python3 execution/demo_lead_generator.py \
     --query "your query" \
     --max-results 10
   ```

---

### Issue 6: "All lead scores showing 1"

**Cause**: Website scraping was disabled or failed.

**Check**:
1. Did you use `--no-website-scraping`?
2. Did websites fail to load?
3. Were emails/social media found?

**Solution**:
- Remove `--no-website-scraping` flag
- Check internet connection
- Try with `--no-headless` to see what's happening
- Use demo generator to see expected scores

---

## When to Use Each Tool

### Use Enhanced Scraper (`scrape_gmb_enhanced.py`)
✅ When you need real, current business data  
✅ For production lead generation  
✅ When you have time (2-3 min per 10 leads)  
✅ When Google isn't blocking you  

**Command**:
```bash
python3 execution/scrape_gmb_enhanced.py \
  --query "your business type in your city" \
  --max-results 20
```

### Use Standard Scraper (`scrape_gmb.py`)
✅ When you only need basic GMB data  
✅ For quick market research  
✅ When speed is critical  
✅ When you don't need emails/social  

**Command**:
```bash
python3 execution/scrape_gmb.py \
  --query "your business type in your city" \
  --max-results 20
```

### Use Demo Generator (`demo_lead_generator.py`)
✅ For testing workflows  
✅ When Google is blocking scraping  
✅ For demonstrations/presentations  
✅ To see expected output format  
✅ For instant results  

**Command**:
```bash
python3 execution/demo_lead_generator.py \
  --query "your business type in your city" \
  --max-results 20
```

---

## Quick Diagnostics

### Test 1: Check if Chrome is working
```bash
python3 -c "from selenium import webdriver; from selenium.webdriver.chrome.service import Service; from webdriver_manager.chrome import ChromeDriverManager; driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())); print('Chrome OK'); driver.quit()"
```

### Test 2: Check if demo generator works
```bash
python3 execution/demo_lead_generator.py \
  --query "test businesses" \
  --max-results 5
```

### Test 3: Check dependencies
```bash
pip3 list | grep -E "selenium|webdriver|beautifulsoup4|requests"
```

---

## Error Messages Explained

### "Command not found: python3"
**Solution**: Use `python` instead:
```bash
python execution/scrape_gmb_enhanced.py --query "..." --max-results 10
```

### "ModuleNotFoundError: No module named 'selenium'"
**Solution**: Install dependencies:
```bash
pip3 install -r execution/requirements.txt
```

### "ChromeDriver not found"
**Solution**: webdriver-manager should handle this automatically. If it fails:
```bash
pip3 install --upgrade webdriver-manager
```

### "urllib3 NotOpenSSLWarning"
**Note**: This is just a warning, not an error. The scraper will still work.
Can be safely ignored.

---

## Best Practices

### 1. Start Small
```bash
# Test with 5 leads first
python3 execution/scrape_gmb_enhanced.py \
  --query "your query" \
  --max-results 5
```

### 2. Use Demo for Testing
```bash
# Test your workflow with demo data first
python3 execution/demo_lead_generator.py \
  --query "your query" \
  --max-results 10
```

### 3. Check Output Format
```bash
# View the generated file
cat .tmp/demo_leads_*.txt
# or
open .tmp/demo_leads_*.csv
```

### 4. Scale Gradually
```bash
# Once working, increase batch size
python3 execution/scrape_gmb_enhanced.py \
  --query "your query" \
  --max-results 20
```

### 5. Wait Between Batches
```bash
# Run first batch
python3 execution/scrape_gmb_enhanced.py --query "query 1" --max-results 20

# Wait 5-10 minutes

# Run second batch
python3 execution/scrape_gmb_enhanced.py --query "query 2" --max-results 20
```

---

## Getting Help

### Check Documentation
- `ENHANCED_SCRAPER_GUIDE.md` - Complete usage guide
- `directives/scrape_gmb_leads.md` - Full directive
- `ENHANCED_SUMMARY.md` - Quick reference

### Test with Demo Data
```bash
python3 execution/demo_lead_generator.py \
  --query "landscapers in New York" \
  --max-results 10 \
  --format txt
```

### Run in Visible Mode
```bash
python3 execution/scrape_gmb_enhanced.py \
  --query "your query" \
  --max-results 5 \
  --no-headless
```

---

## Summary

| Issue | Quick Fix |
|-------|-----------|
| Google blocking | Use demo generator or wait 10 min |
| Slow scraping | Use `--no-website-scraping` or demo |
| No emails found | Normal - ~60-70% success rate |
| Browser crashes | Update Chrome, use demo generator |
| All scores = 1 | Enable website scraping |
| Need test data | Use demo generator |

**Most Common Solution**: Use the demo generator for testing and demonstrations!

```bash
python3 execution/demo_lead_generator.py \
  --query "landscapers in New York" \
  --max-results 10
```

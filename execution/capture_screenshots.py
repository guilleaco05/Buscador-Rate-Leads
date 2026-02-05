#!/usr/bin/env python3
"""
Website Screenshot Capturer

Automates capturing screenshots of business websites for reporting and analysis.
Uses Selenium to visit URLs and capture visuals (desktop & mobile).

Usage:
    python capture_screenshots.py --input .tmp/leads.json --output-dir .tmp/screenshots/
"""

import argparse
import sys
import json
import csv
import time
import os
from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("❌ Error: Selenium not installed. Run 'pip install selenium webdriver-manager'")
    sys.exit(1)

def setup_driver(headless: bool = True):
    """Setup Chrome Driver"""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--hide-scrollbars")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(15) # 15s timeout
    return driver

def capture_single_site(url: str, name: str, output_dir: Path) -> Dict:
    """Capture screenshot for a single site"""
    if url == "N/A" or not url.startswith("http"):
        return {"name": name, "status": "no_url"}
    
    # Safe filename
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).strip().replace(" ", "_")
    screenshot_path = output_dir / f"{safe_name}.png"
    
    if screenshot_path.exists():
        return {"name": name, "status": "exists", "path": str(screenshot_path)}

    driver = None
    try:
        driver = setup_driver(headless=True)
        print(f"📸 Capturing: {name} ({url})...")
        driver.get(url)
        time.sleep(2) # Wait for animations
        
        # Remove cookie banners (simple attempt)
        try:
            driver.execute_script("""
                const elements = document.querySelectorAll('*');
                for (let el of elements) {
                    if (el.textContent.includes('cookie') || el.textContent.includes('Cookie')) {
                        if (el.style.zIndex > 100 || el.style.position == 'fixed') {
                            el.remove();
                        }
                    }
                }
            """)
            time.sleep(0.5)
        except:
            pass
            
        driver.save_screenshot(str(screenshot_path))
        return {"name": name, "status": "success", "path": str(screenshot_path)}
        
    except Exception as e:
        # print(f"⚠️ Failed to capture {name}: {e}")
        return {"name": name, "status": "error", "error": str(e)}
        
    finally:
        if driver:
            driver.quit()

def process_leads(leads: List[Dict], output_dir: Path, max_workers: int = 3):
    """Process visual capture for all leads"""
    print(f"🖼️  Starting screenshot capture for {len(leads)} leads...")
    print(f"📂 Output directory: {output_dir}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    # Sequential for stability, or parallel for speed
    # Using small pool to not overload system/network
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for lead in leads:
            url = lead.get('website', 'N/A')
            name = lead.get('name', 'Unknown')
            futures.append(executor.submit(capture_single_site, url, name, output_dir))
            
        for future in futures:
            results.append(future.result())
            
    # Summary
    success = sum(1 for r in results if r['status'] == 'success')
    errors = sum(1 for r in results if r['status'] == 'error')
    skipped = sum(1 for r in results if r['status'] == 'no_url')
    
    print("\n" + "="*40)
    print("SCREENSHOT CAPTURE SUMMARY")
    print("="*40)
    print(f"✓ Success: {success}")
    print(f"❌ Errors: {errors}")
    print(f"⏩ Skipped (No URL): {skipped}")
    print("="*40 + "\n")

    return results

def load_file(file_path: Path) -> List[Dict]:
    """Load leads from JSON or CSV"""
    suffix = file_path.suffix.lower()
    leads = []
    try:
        if suffix == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    leads = data.get('results', data.get('leads', []))
                else:
                    leads = data
        elif suffix == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                leads = list(csv.DictReader(f))
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)
    return leads

def main():
    parser = argparse.ArgumentParser(description="Capture screenshots for leads")
    parser.add_argument('--input', required=True, help="Input leads file")
    parser.add_argument('--output-dir', default='.tmp/screenshots', help="Directory to save images")
    parser.add_argument('--workers', type=int, default=2, help="Parallel workers")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        sys.exit(1)
        
    leads = load_file(input_path)
    if not leads:
        print("❌ No leads found.")
        sys.exit(1)
        
    process_leads(leads, output_dir, args.workers)

if __name__ == "__main__":
    main()

#!/bin/bash

# Lead Generation Pipeline Runner (Enhanced)
# Usage: ./run_pipeline.sh "abogados en Vigo" 20

# Load environment variables from .zshrc (for API keys)
if [ -f "$HOME/.zshrc" ]; then
    source "$HOME/.zshrc"
fi

QUERY="$1"
MAX_RESULTS="${2:-20}"

if [ -z "$QUERY" ]; then
    echo "❌ Error: Please provide a search query."
    echo "Usage: ./run_pipeline.sh \"business type in city\" [max_results]"
    exit 1
fi

echo "================================================================"
echo "🚀 STARTING LEAD GENERATION PIPELINE (WITH ANALYSIS)"
echo "Query: $QUERY"
echo "================================================================"

# 0. Maintenance (Auto-Cleanup)
if [ -d ".tmp" ]; then
    # Delete files older than 7 days
    find .tmp -type f -mtime +7 -exec rm {} + 2>/dev/null
    # echo "🧹 Maintenance: Cleaned temporary files older than 7 days."
fi

# 1. Search
echo ""
echo "📡 STEP 1: Searching Google Places API..."
python3 execution/scrape_gmb_api.py --query "$QUERY" --max-results "$MAX_RESULTS" --format json
LATEST_FILE=$(ls -t .tmp/api_leads_*.json | head -n1)

# 2. Clean
echo ""
echo "🧹 STEP 2: Removing duplicates..."
CLEAN_FILE=".tmp/leads_clean.json"
python3 execution/deduplicate_leads.py --input "$LATEST_FILE" --output "$CLEAN_FILE"

# 3. Analyze (Website)
echo ""
echo "🧠 STEP 3: Analyzing Websites (Internal & Pain Points)..."
ANALYZED_FILE=".tmp/leads_analyzed.json"
python3 execution/analyze_pain_points.py --input "$CLEAN_FILE" --output-format json

# 3b. Enrich (External - LinkedIn/InfoCIF)
echo ""
echo "🧩 STEP 3b: Enriching Data (Google CSE - LinkedIn)..."
# We re-use ANALYZED_FILE as input, and overwrite it or create new
ENRICHED_FILE=".tmp/leads_enriched.json"

# Find latest analyzed file
LATEST_ANALYZED=$(ls -t .tmp/leads_analyzed_*.json | head -n1)
echo "   -> Enriching from: $LATEST_ANALYZED"

python3 execution/enrich_leads.py --input "$LATEST_ANALYZED" --output "$ENRICHED_FILE"

LATEST_DATA="$ENRICHED_FILE" # Pipeline continues with this file

# 4. Visuals (Screenshots)
echo ""
echo "📸 STEP 4: Capturing Screenshots..."
python3 execution/capture_screenshots.py --input "$LATEST_DATA"

# 5. Export
echo ""
echo "📦 STEP 5: Exporting for Google Sheets (n8n Ready)..."
EXPORT_FILE=".tmp/sheets_import_$(date +%Y%m%d_%H%M%S).csv"
python3 execution/export_to_sheets_csv.py --input "$LATEST_DATA" --output "$EXPORT_FILE"

echo ""
echo "================================================================"
echo "✅ PIPELINE COMPLETE!"
echo "📂 Top Quality Data: $EXPORT_FILE"
echo "================================================================"

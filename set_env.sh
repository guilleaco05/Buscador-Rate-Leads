#!/bin/bash
# Export API keys for the session
# Usage: source set_env.sh

# Load from .env file if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo "✅ Environment variables loaded from .env file"
    echo "   GOOGLE_PLACES_API_KEY: ${GOOGLE_PLACES_API_KEY:0:20}..."
    echo "   GOOGLE_CSE_ID: $GOOGLE_CSE_ID"
else
    echo "❌ Error: .env file not found. Please create it from .env.template"
    exit 1
fi

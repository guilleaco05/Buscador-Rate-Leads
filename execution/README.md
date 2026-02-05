# Execution Scripts

This directory contains **deterministic Python scripts** that perform the actual work.

## Purpose

Execution scripts handle:
- API calls
- Data processing
- File operations
- Storage operations
- Any repeatable task

## Principles

### 1. Deterministic
- Same inputs → Same outputs
- No randomness unless explicitly required
- Predictable error handling

### 2. Fast
- Optimized for performance
- Efficient data processing
- Minimal overhead

### 3. Testable
- Clear inputs and outputs
- Error cases handled explicitly
- Easy to verify correctness

### 4. Repeatable
- Can be run multiple times safely
- Idempotent where possible
- Clear state management

## Best Practices

### Structure
```python
#!/usr/bin/env python3
"""
Script description and purpose
"""

import os
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main execution function"""
    # Your logic here
    pass

if __name__ == "__main__":
    main()
```

### Error Handling
- Use try/except blocks for external calls
- Log errors clearly
- Return meaningful exit codes
- Provide actionable error messages

### Configuration
- Load secrets from `.env`
- Accept parameters via command-line arguments
- Document all required environment variables

### Dependencies
- Keep dependencies minimal
- Document requirements in `requirements.txt`
- Use virtual environments

## Examples

Typical scripts might include:
- `scrape_single_site.py` - Web scraping
- `process_csv.py` - Data transformation
- `upload_to_cloud.py` - Cloud storage operations
- `send_email.py` - Email notifications

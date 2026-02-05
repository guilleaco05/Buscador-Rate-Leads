# Quick Start Guide

## 🚀 DOE System Setup

### 1. Verify Structure

Your DOE system has been scaffolded with the following structure:

```
Antigravity/
├── AGENT.md                 # Operating rules (immutable)
├── README.md                # System overview
├── .env.template            # Environment variables template
├── .gitignore               # Git ignore rules
│
├── directives/              # SOP-style instructions
│   ├── README.md
│   └── example_echo.md      # Example directive
│
├── execution/               # Deterministic scripts
│   ├── README.md
│   ├── requirements.txt
│   └── example_echo.py      # Example script
│
└── .tmp/                    # Temporary files (disposable)
    └── README.md
```

### 2. Environment Setup

```bash
# 1. Copy the environment template
cp .env.template .env

# 2. Edit .env with your API keys (optional for now)
# nano .env

# 3. (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install Python dependencies
pip install -r execution/requirements.txt
```

### 3. Test the System

Run the example script to verify everything works:

```bash
# Test the example echo script
python3 execution/example_echo.py --message "Hello DOE!" --repeat 2

# Check the output in .tmp/
cat .tmp/echo_output.txt
```

Expected output:
```
==================================================
ECHO OUTPUT:
==================================================
Hello DOE!
Hello DOE!
==================================================

✓ Output written to: /path/to/.tmp/echo_output.txt
```

### 4. Understanding the Flow

#### Directive → Observation → Experiment

1. **Read the Directive** (`directives/example_echo.md`)
   - Understand the goal, inputs, outputs, and edge cases

2. **Execute** (`execution/example_echo.py`)
   - Run the deterministic script
   - Observe the results

3. **Self-Anneal** (if errors occur)
   - Fix the script
   - Update the directive with learnings
   - Test again

### 5. Create Your First Workflow

#### Step 1: Create a Directive

Create `directives/my_task.md`:

```markdown
# My Task

## Goal
[What you want to accomplish]

## Inputs
- Input 1: Description
- Input 2: Description

## Execution
```bash
python execution/my_script.py --param value
```

## Outputs
[What gets produced]

## Edge Cases
[Known limitations and error scenarios]
```

#### Step 2: Create an Execution Script

Create `execution/my_script.py`:

```python
#!/usr/bin/env python3
"""
My Script - Description
"""

import argparse
import sys
from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="My script")
    parser.add_argument("--param", required=True, help="Parameter description")
    args = parser.parse_args()
    
    # Your logic here
    print(f"Processing: {args.param}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

#### Step 3: Make it Executable

```bash
chmod +x execution/my_script.py
```

#### Step 4: Test and Iterate

```bash
python3 execution/my_script.py --param "test"
```

### 6. Key Principles

✅ **Check for existing tools** before creating new ones
✅ **Push repeatable work** into deterministic scripts
✅ **Treat errors as learning signals** and self-anneal
✅ **Update directives** with learnings
✅ **Store deliverables** in cloud services, not locally
✅ **Keep .tmp/ disposable** - it's for intermediate files only

### 7. Next Steps

- Add your API keys to `.env`
- Create directives for your specific use cases
- Build execution scripts to handle the work
- Let the AI agent orchestrate the flow

### 8. Getting Help

- Read `AGENT.md` for operating rules
- Check `directives/README.md` for directive format
- Review `execution/README.md` for script best practices
- Study `directives/example_echo.md` and `execution/example_echo.py` as templates

---

## 🎯 You're Ready!

The DOE system is now set up and ready to use. Start by creating directives for your tasks, then build the execution scripts to make them happen.

**Remember**: AI is probabilistic. Business logic must be deterministic. This system separates those concerns to reduce error over time.

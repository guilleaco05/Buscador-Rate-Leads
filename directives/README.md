# Directives

This directory contains **SOP-style instructions** written in Markdown.

## Purpose

Directives define:
- **Goals**: What needs to be accomplished
- **Inputs**: What data/parameters are required
- **Tools/Scripts**: Which execution scripts to use
- **Outputs**: What the result should look like
- **Edge Cases**: Known constraints, limitations, and error scenarios

## Format

Each directive should be written in plain language, as if briefing a competent teammate.

### Template Structure

```markdown
# [Directive Name]

## Goal
What this directive accomplishes

## Inputs
- Input 1: Description
- Input 2: Description

## Execution
Which scripts in `execution/` to run and in what order

## Outputs
What gets produced (deliverables, data formats, etc.)

## Edge Cases
- Known limitations
- Error scenarios
- API constraints
- Timing considerations
```

## Living Documents

Directives are continuously improved based on:
- Errors encountered during execution
- Better approaches discovered
- New constraints or requirements
- Learnings from the self-annealing loop

## Examples

Create directives for tasks like:
- `scrape_website.md` - Web scraping workflow
- `process_data.md` - Data transformation pipeline
- `generate_report.md` - Report generation process
- `send_notifications.md` - Notification workflow

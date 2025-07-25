#!/usr/bin/env python3
import os
import re
import sys
import yaml

ISSUE_BODY = os.environ.get('ISSUE_BODY', '')
ISSUE_TITLE = os.environ.get('ISSUE_TITLE', '')

# Helper to slugify for filename

def slugify(value):
    value = value.lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    value = value.strip('-')
    return value

# Parse the issue body (GitHub issue forms use YAML frontmatter)

def parse_issue_body(body):
    # GitHub issue forms send the body as a YAML list
    try:
        data = yaml.safe_load(body)
        if isinstance(data, list):
            return {item['id']: item.get('value', '') for item in data}
        return data
    except Exception as e:
        print(f"Error parsing issue body: {e}")
        return {}

fields = parse_issue_body(ISSUE_BODY)

company = fields.get('company-name', 'unknown-company')
title = fields.get('internship-title', 'unknown-internship')
link = fields.get('internship-link', '')
location = fields.get('location', '')
season = fields.get('season', '')
sponsorship = fields.get('sponsorship', '')
accepting = fields.get('accepting-applications', '')
email = fields.get('email', '')
notes = fields.get('extra-notes', '')

filename = f"{slugify(company)}-{slugify(title)}.md"
filepath = os.path.join('internships', filename)

with open(filepath, 'w') as f:
    f.write(f"# {title}\n\n")
    f.write(f"**Company:** {company}\n\n")
    f.write(f"**Location:** {location}\n\n")
    f.write(f"**Season:** {season}\n\n")
    f.write(f"**Sponsorship:** {sponsorship}\n\n")
    f.write(f"**Accepting Applications:** {accepting}\n\n")
    f.write(f"**Link:** [{link}]({link})\n\n")
    if email:
        f.write(f"**Contact Email:** {email}\n\n")
    if notes:
        f.write(f"**Extra Notes:** {notes}\n\n")
    f.write("## Description\n\nAdd details about the internship here.\n\n")
    f.write("## How to Apply\n\n")
    f.write(f"Apply here: [{link}]({link})\n") 
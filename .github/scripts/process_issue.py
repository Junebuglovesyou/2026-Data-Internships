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

print('DEBUG: Raw ISSUE_BODY:')
print(ISSUE_BODY)
print('DEBUG: Parsed fields:')
print(fields)

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

# --- Update README.md with a table of all internships ---

def extract_metadata(md_path):
    meta = {
        'Company': '', 'Internship Title': '', 'Location': '', 'Season': '', 'Sponsorship': '', 'Accepting Applications': '', 'Link': ''
    }
    with open(md_path, 'r') as f:
        for line in f:
            if line.startswith('# '):
                meta['Internship Title'] = line[2:].strip()
            elif line.startswith('**Company:**'):
                meta['Company'] = line.split('**Company:**')[1].strip()
            elif line.startswith('**Location:**'):
                meta['Location'] = line.split('**Location:**')[1].strip()
            elif line.startswith('**Season:**'):
                meta['Season'] = line.split('**Season:**')[1].strip()
            elif line.startswith('**Sponsorship:**'):
                meta['Sponsorship'] = line.split('**Sponsorship:**')[1].strip()
            elif line.startswith('**Accepting Applications:**'):
                meta['Accepting Applications'] = line.split('**Accepting Applications:**')[1].strip()
            elif line.startswith('**Link:**'):
                link = line.split('**Link:**')[1].strip()
                meta['Link'] = link
    return meta

internship_dir = 'internships'
rows = []
if os.path.exists(internship_dir):
    for fname in os.listdir(internship_dir):
        if fname.endswith('.md'):
            meta = extract_metadata(os.path.join(internship_dir, fname))
            rows.append(meta)

# Build markdown table
header = '| Company | Internship Title | Location | Season | Sponsorship | Accepting Applications | Link |\n'
header += '|---------|------------------|----------|--------|-------------|-----------------------|------|\n'
table = header
for meta in rows:
    table += f"| {meta['Company']} | {meta['Internship Title']} | {meta['Location']} | {meta['Season']} | {meta['Sponsorship']} | {meta['Accepting Applications']} | {meta['Link']} |\n"

# Insert or update table in README.md
readme_path = 'README.md'
with open(readme_path, 'r') as f:
    readme = f.read()

start_marker = '<!-- INTERNSHIP_TABLE_START -->'
end_marker = '<!-- INTERNSHIP_TABLE_END -->'

if start_marker in readme and end_marker in readme:
    pre = readme.split(start_marker)[0]
    post = readme.split(end_marker)[1]
    new_readme = pre + start_marker + '\n' + table + end_marker + post
else:
    # Append table to end if markers not found
    new_readme = readme + '\n' + start_marker + '\n' + table + end_marker + '\n'

with open(readme_path, 'w') as f:
    f.write(new_readme) 
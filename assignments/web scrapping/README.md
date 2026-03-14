# IOEPAS Staff Scraper (Selenium)

This folder contains a Selenium scraper for staff data from:

- https://ioepas.edu.np/

The script collects records from:

- Teaching staff department pages
- Non-teaching staff page

## Files

- `scrape_ioepas_staff.py`: main scraper script
- `staff_details.csv`: generated output CSV

## What Is Collected

Each row includes:

- `staff_type` (Teaching / Non-Teaching)
- `name`
- `department`
- `designation`
- `phone`
- `email`
- `social_links`
- `profile_url`
- `source_page`
- `personal_details` (JSON string with designation, phone, email, social links, profile URL)

## Requirements

- Python 3.9+
- Selenium 4.6+
- Google Chrome installed



# End-to-End Sales Analytics Pipeline

**Web Scraping → Data Cleansing → Executive Dashboarding**

This project demonstrates a **production-style analytics pipeline** that extracts public raw data from the web, transforms and models it using Python + SQL, and delivers actionable insights through executive-level dashboards in Tableau.

---

## Project Overview

The goal of this project is to simulate a real-world analytics workflow:

- Automated data extraction from a public web source
- Structured data transformation and cleansing
- Analytical modeling using SQL logic
- Visualization of insights to influence decision-making

The final output is a set of dashboards designed for **executives and operational leaders** to identify performance gaps and opportunities.

---

## Architecture

**Web Source → Python Scraper → Pandas DataFrame → DuckDB SQL Transformations → Hyper File → Tableau Dashboard**

---

## Tech Stack

- **Python** — `requests`, `BeautifulSoup`, `pandas`
- **SQL** — DuckDB
- **Tableau** — Hyper file export via `pantab`
- **Excel** — Raw dataset format

---

## Project Structure

```bash
sales-analytics-pipeline/
├── scripts/
│   ├── web_scraper.py          # Web scraping and file download
│   └── data_cleanse.py         # Data cleaning + DuckDB transformations
├── data/
│   ├── raw/                    # Original downloaded Excel file
│   └── processed/
├── output/
│   └── cleansed_sales_data.hyper
├── images/
│   ├── executive_dashboard.png
│   └── campaign_dashboard.png
├── README.md
└── requirements.txt

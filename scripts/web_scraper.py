import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import logging
import time

# -----------------------------
# Configuration
# -----------------------------
BASE_URL = "https://excelx.com/practice-data/sales-retail/"
TARGET_NAME = "Product Sales"
OUTPUT_FILE = "data/raw/Product-Sales-Region.xlsx"
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def fetch_with_retries(url):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"Fetching URL (attempt {attempt}): {url}")
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.warning(f"Attempt {attempt} failed: {e}")
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed to fetch URL after {MAX_RETRIES} attempts: {url}")

def get_dataset_links(page_url):
    response = fetch_with_retries(page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", class_="dl")
    
    datasets = []
    for link in links:
        name = link.text.strip()
        href = link.get("href")
        if href:
            full_url = urljoin(page_url, href)
            datasets.append({"name": name, "url": full_url})
    
    logging.info(f"Found {len(datasets)} datasets")
    return datasets

def find_target_dataset(datasets, target_name):
    for dataset in datasets:
        if target_name.lower() in dataset["name"].lower():
            logging.info(f"Target dataset found: {dataset['name']}")
            return dataset["url"]
    raise ValueError(f"Target dataset '{target_name}' not found")

def download_file(url, output_path):
    response = fetch_with_retries(url)
    with open(output_path, "wb") as f:
        f.write(response.content)
    logging.info(f"File saved to {output_path}")

def main():
    try:
        logging.info("Starting web scrape pipeline")
        import os
        os.makedirs("data/raw", exist_ok=True)
        
        datasets = get_dataset_links(BASE_URL)
        download_url = find_target_dataset(datasets, TARGET_NAME)
        download_file(download_url, OUTPUT_FILE)
        
        logging.info("Pipeline completed successfully")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()

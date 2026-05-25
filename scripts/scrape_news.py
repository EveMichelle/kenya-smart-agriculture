"""
scripts/scrape_news.py
======================
Run ONCE to scrape Kenya agricultural news from Kenya News Agency.
Saves to: data/raw/news/kenya_agri_news_raw.csv

Run:
    python scripts/scrape_news.py

Requirements:
    pip install requests beautifulsoup4 lxml pandas
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from datetime import datetime

OUTPUT_DIR  = "data/raw/news"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "kenya_agri_news_raw.csv")
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    )
}


def safe_get(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=30, verify=False)
        r.raise_for_status()
        return BeautifulSoup(r.text, "lxml")
    except Exception:
        print("  Failed: {}".format(url))
        return None


def scrape_kna(max_pages=60):
    print("\n  Scraping Kenya News Agency...")
    records = []
    base    = "https://www.kenyanews.go.ke/category/agri"

    for page in range(1, max_pages + 1):
        url  = base if page == 1 else "{}/page/{}/".format(base, page)
        soup = safe_get(url)

        if not soup:
            continue

        articles = soup.find_all("article")
        if not articles:
            print("  Page {}: no articles — stopping".format(page))
            break

        for art in articles:
            link_tag  = art.find("a", href=True)
            title_tag = art.find(["h2", "h3", "h4"])
            date_tag  = art.find("time")

            if not link_tag or not title_tag:
                continue

            records.append({
                "source":     "Kenya News Agency",
                "title":      title_tag.get_text(strip=True),
                "url":        link_tag["href"],
                "date":       date_tag.get("datetime") if date_tag else None,
                "scraped_at": datetime.now().strftime("%Y-%m-%d"),
            })

        print("  Page {}: {} articles (total: {})".format(
            page, len(articles), len(records)))
        time.sleep(0.5)

    return records


def main():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print("\n" + "="*60)
    print("  Kenya Agricultural News Scraper")
    print("  Source  : Kenya News Agency")
    print("  Output  : {}".format(OUTPUT_FILE))
    print("="*60)

    records = scrape_kna(max_pages=60)

    if not records:
        print("\n  No data scraped.")
        return

    df = pd.DataFrame(records)
    df = df[df["url"].notna()]
    df.drop_duplicates(subset=["url"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\n" + "="*60)
    print("  COMPLETE!")
    print("  Articles : {:,}".format(len(df)))
    print("  Saved    : {}".format(OUTPUT_FILE))
    print("="*60)


if __name__ == "__main__":
    main()

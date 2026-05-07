"""
Emploi.ma Scraper (PRO CLEAN + FIXED VERSION) PAR ZOUHAIR SAKANE
1- Extract job URLs from listing cards
2- Fix pagination issue (stops correctly)
3- Visit each job page
4- Extract REAL "Critères de l'annonce"
5- Extract company info
6- Extract skills
7- Extract publication date (formatted)
8- Faster with requests.Session
9- Save JSON + CSV
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
import csv
import os
from tqdm import tqdm
from datetime import datetime
from config import *


# =========================================================
# FOLDERS
# =========================================================
os.makedirs("data/brutes", exist_ok=True)


# =========================================================
# SESSION (FASTER)
# =========================================================
session = requests.Session()
session.headers.update(HEADERS)


# =========================================================
# REQUEST FUNCTION
# =========================================================
def get_soup(url, params=None):
    for _ in range(MAX_RETRIES):
        try:
            r = session.get(url, params=params, timeout=10)
            r.raise_for_status()
            return BeautifulSoup(r.text, "html.parser")
        except:
            time.sleep(2)
    return None


# =========================================================
# CLEAN TEXT
# =========================================================
def clean(text):
    return " ".join(text.split()).strip() if text else ""


# =========================================================
# FORMAT DATE
# =========================================================
def format_date(raw):
    # Exemple: "Publiée le 07.05.2026"
    try:
        raw = raw.replace("Publiée le", "").strip()
        return datetime.strptime(raw, "%d.%m.%Y").strftime("%Y-%m-%d")
    except:
        return ""


# =========================================================
# EXTRACT JOB URLS
# =========================================================
def extract_job_urls(soup):
    urls = []
    cards = soup.select("div.card.card-job")

    for card in cards:
        link = card.get("data-href")
        if link:
            urls.append(link)

    return urls


# =========================================================
# COLLECT ALL JOB URLs (FIXED PAGINATION)
# =========================================================
def collect_urls(max_pages=50):
    all_urls = set()

    page = 0

    while page < max_pages:
        soup = get_soup(SEARCH_URL, params={"page": page})

        if not soup:
            break

        urls = extract_job_urls(soup)

        # STOP condition FIX (important)
        if not urls:
            break

        all_urls.update(urls)

        print(f"Page {page} → {len(urls)} URLs")

        page += 1
        time.sleep(random.uniform(*DELAY))

    return list(all_urls)


# =========================================================
# EXTRACT CRITERIA
# =========================================================
def extract_criteria(soup):

    data = {
        "metier": "",
        "secteur": "",
        "contrat": "",
        "region": "",
        "ville": "",
        "teletravail": "",
        "experience": "",
        "etude": ""
    }

    section = soup.select_one("ul.arrow-list")
    if not section:
        return data

    for li in section.select("li"):

        strong = li.select_one("strong")
        span = li.select_one("span")

        if not strong or not span:
            continue

        key = strong.get_text(strip=True).lower()
        val = clean(span.get_text(" "))

        if "métier" in key:
            data["metier"] = val
        elif "secteur" in key:
            data["secteur"] = val
        elif "type de contrat" in key:
            data["contrat"] = val
        elif "région" in key:
            data["region"] = val
        elif "ville" in key:
            data["ville"] = val
        elif "travail à distance" in key:
            data["teletravail"] = val
        elif "expérience" in key:
            data["experience"] = val
        elif "études" in key:
            data["etude"] = val

    return data


# =========================================================
# SCRAPE SINGLE JOB
# =========================================================
def scrape_job(url):

    soup = get_soup(url)
    if not soup:
        return None

    # TITLE
    title = soup.select_one("h1")
    title = clean(title.get_text()) if title else ""

    # COMPANY
    company = soup.select_one(".card-block-company h3 a")
    company = clean(company.get_text()) if company else ""

    # DESCRIPTION
    desc = soup.select_one(".job-description")
    desc = clean(desc.get_text(" ")) if desc else ""

    # CRITERIA
    criteria = extract_criteria(soup)

    # SKILLS
    skills = [
        clean(li.get_text())
        for li in soup.select("ul.skills li")
    ]

    # =====================================================
    # PUBLICATION DATE (NEW)
    # =====================================================
    pub_date = ""
    date_box = soup.select_one(".page-application-details")

    if date_box:
        p = date_box.find("p")
        if p:
            pub_date = format_date(p.get_text())


    return {
        "url": url,
        "titre": title,
        "entreprise": company,
        "description": desc,

        "metier": criteria["metier"],
        "secteur": criteria["secteur"],
        "contrat": criteria["contrat"],
        "region": criteria["region"],
        "ville": criteria["ville"],
        "teletravail": criteria["teletravail"],
        "experience": criteria["experience"],
        "niveau_etude": criteria["etude"],

        "competences": skills,
        "date_publication": pub_date
    }


# =========================================================
# SCRAPE ALL JOBS
# =========================================================
def scrape_all(urls):

    results = []

    for url in tqdm(urls, desc="Scraping jobs"):

        job = scrape_job(url)

        if job:
            results.append(job)

        time.sleep(random.uniform(*DELAY))

    return results


# =========================================================
# SAVE FUNCTIONS
# =========================================================
def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_csv(data, path):
    if not data:
        return

    keys = data[0].keys()

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":

    print("\n=== EMPLOI.MA SCRAPER START (FIXED VERSION) ===\n")

    # STEP 1: GET URLS
    urls = collect_urls(max_pages=30) # Adjust max_pages as needed

    print(f"\nTotal URLs: {len(urls)}\n")

    # STEP 2: SCRAPE DETAILS
    data = scrape_all(urls)

    print(f"\nJobs scraped: {len(data)}\n")

    # STEP 3: SAVE DATA
    save_json(data, "projet_emploi/data/brutes/jobs.json")
    save_csv(data, "projet_emploi/data/brutes/jobs.csv")

    print("\nDONE,The DATA SAVED successfully!\n")
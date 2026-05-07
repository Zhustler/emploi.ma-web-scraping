# 🧠 Emploi.ma Job Scraper & Data Analysis Pipeline

This project is an end-to-end **web scraping and data analysis pipeline** developed to extract, process, and analyze job offers from the Moroccan job platform [Emploi.ma](https://www.emploi.ma?utm_source=chatgpt.com).

It demonstrates a complete workflow covering:
- Web scraping (job extraction at scale)
- Data cleaning and NLP preprocessing
- Exploratory data analysis and visualization

---
## 📁 Project Architecture


projet_emploi/

│

├── data/

│   ├── brutes/          # Raw scraped data (JSON, CSV)

│   ├── nettoyees/       # Cleaned NLP dataset

│   ├── analysees/       # Generated visualizations (charts, wordcloud)

│

├── scraping/

│   ├── scraper.py       # Web scraping engine

│   ├── config.py        # Configuration settings (URLs, headers, delays)

│

├── cleaner.py           # NLP preprocessing pipeline

├── analysis.py          # Data analysis & visualization

├── requirements.txt     # Project dependencies




# ⚙️ System Workflow

## 1. Data Collection (Web Scraping)

The scraping module (`scraper.py`) extracts structured job data from [Emploi.ma](https://www.emploi.ma?utm_source=chatgpt.com).

### Features:
- Session-based requests for performance
- Pagination handling
- Retry mechanism for stability
- Extraction of job URLs from listing cards

### Extracted data per job:
- Title
- Company
- Description
- Skills
- Publication date
- Job criteria:
  - Métier
  - Secteur
  - Contrat
  - Région / Ville
  - Experience
  - Education
  - Remote work

### Output:
- `jobs.json` like:
* **{
  "url": "...",
  "titre": "...",
  "entreprise": "...",
  "description": "...",
  "metier": "...",
  "secteur": "...",
  "contrat": "...",
  "region": "...",
  "ville": "...",
  "teletravail": "...",
  "experience": "...",
  "niveau_etude": "...",
  "competences": [],
  "date_publication": "2026-05-07"
}**
- `jobs.csv`

---

## 2. Data Cleaning & NLP Processing

The `cleaner.py` module applies NLP preprocessing.

### Steps:
1. HTML cleaning
2. Text normalization
3. Tokenization (NLTK)
4. Stopwords removal (French)
5. Lemmatization (SpaCy)

### Output:
```json```
"tokens": ["developper", "python", "django", "sql"]
3. Data Analysis

The analysis.py module provides insights.

- Features:
* Top skills extraction
* City distribution analysis
* WordCloud generation
- Output:
* data/analysees/wordcloud.png
*  🚀 Key Features
* ⚡ Optimized Scraper
* requests.Session for speed
* Retry mechanism
* Random delay to avoid blocking
* 🧠 Structured Extraction
* Clean parsing of job criteria
* Robust handling of missing fields
* 🌍 NLP Pipeline (French)
* Tokenization (NLTK)
* Lemmatization (SpaCy)
* Stopword filtering
* 📊 Analytics
* Skills frequency
* Location insights
* WordCloud visualization
* 🧩 Modular Design
* Scraping → Data collection
* Cleaning → Transformation
* Analysis → Insights
- ▶️ How to Run
* **Install dependencies**
* pip install -r requirements.txt
- **Run scraper**
* python scraper.py
- **Run NLP cleaning**
* python cleaner.py
- **Run analysis**
- python analysis.py
- 🛠️ Tech Stack
**Python
BeautifulSoup
Requests
Pandas
NLTK
SpaCy
Matplotlib
WordCloud**

- **Author :**
* **Zouhair Sakane**
* Data Engineering & AI Student
* Specialized in Web Scraping, NLP, and Data Science pipelines

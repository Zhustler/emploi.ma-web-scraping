import json
import re
from bs4 import BeautifulSoup
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")

nlp = spacy.load("fr_core_news_sm")
stop_words = set(stopwords.words("french"))

# =========================================================
# CLEAN TEXT (matches YOUR scraper output)
# =========================================================

def clean_text(text):
    if not text:
        return ""

    text = BeautifulSoup(text, "html.parser").get_text()
    text = text.lower()
    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

# =========================================================
# NLP PIPELINE
# =========================================================

def preprocess(text):
    text = clean_text(text)

    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stop_words]

    doc = nlp(" ".join(tokens))
    lemmas = [t.lemma_ for t in doc]

    return lemmas

# =========================================================
# APPLY TO YOUR DATASET
# =========================================================

def process_dataset(input_path, output_path):

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for job in data:
        job["tokens"] = preprocess(job.get("description", ""))

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("CLEAN DATA SAVED")

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    process_dataset(
        "projet_emploi/data/brutes/jobs.json",
        "projet_emploi/data/nettoyees/jobs_clean.json"
    )
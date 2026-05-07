import json
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

os.makedirs("data/analysees", exist_ok=True)

# =========================================================
# LOAD DATA (FROM YOUR SCRAPER OUTPUT)
# =========================================================

def load_data():
    with open("projet_emploi/data/nettoyees/jobs_clean.json", "r", encoding="utf-8") as f:
        return json.load(f)

# =========================================================
# TOP SKILLS (uses YOUR "competences")
# =========================================================

def top_skills(data):
    skills = []

    for job in data:
        skills.extend(job.get("competences", []))

    return Counter(skills).most_common(10)

# =========================================================
# CITY ANALYSIS (uses YOUR "ville")
# =========================================================

def city_stats(data):
    df = pd.DataFrame(data)
    return df["ville"].value_counts().head(10)

# =========================================================
# WORDCLOUD (uses YOUR "tokens")
# =========================================================

def wordcloud(data):

    text = " ".join(
        " ".join(job.get("tokens", []))
        for job in data
    )

    wc = WordCloud(width=800, height=400, background_color="white").generate(text)

    plt.figure(figsize=(10,5))
    plt.imshow(wc)
    plt.axis("off")

    plt.savefig("data/analysees/wordcloud.png")
    plt.show()

# =========================================================
# RUN EVERYTHING
# =========================================================

def run():
    data = load_data()

    print("\nTOP SKILLS:")
    print(top_skills(data))

    print("\nTOP CITIES:")
    print(city_stats(data))

    wordcloud(data)

    print("\nANALYSIS DATA IS DONE")

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    run()
import os
import time
import pandas as pd
import feedparser
import urllib.parse
from dateutil import parser

from config.config import CATEGORIES

def get_articles_for_date(target_date, keywords):
    titles = []
    tagged_articles = []

    for word in keywords:
        query = urllib.parse.quote(word)
        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

        feed = feedparser.parse(url)

        for entry in feed.entries:
            try:
                # Ensure article is strictly from the same day
                publish_date = parser.parse(entry.published).date()

                if publish_date == target_date.date():
                    title = entry.title
                    
                    # Remove duplicates
                    if title not in titles:
                        titles.append(title)
                        
                        # Tagging logic
                        article_categories = []
                        title_lower = title.lower()
                        for category, cat_keywords in CATEGORIES.items():
                            if any(kw.lower() in title_lower for kw in cat_keywords):
                                article_categories.append(category)
                        
                        tagged_articles.append({
                            "title": title,
                            "categories": ", ".join(article_categories) if article_categories else "Uncategorized"
                        })

                if len(titles) == 5:
                    return tagged_articles

            except Exception:
                continue

    # Fill missing value with dummy reference logic if less than 5 articles across all keywords
    while len(tagged_articles) < 5:
        tagged_articles.append({"title": "No news available for this date", "categories": "N/A"})

    return tagged_articles

def generate_news_dataset(keywords, start_date, end_date, file_format="csv"):

    dates = pd.date_range(start=start_date, end=end_date)
    
    article1, article2, article3, article4, article5 = [], [], [], [], []
    cat1, cat2, cat3, cat4, cat5 = [], [], [], [], []
    date_list = []

    for date in dates:
        date_list.append(date.date())
        
        articles = get_articles_for_date(date, keywords)

        article1.append(articles[0]["title"])
        article2.append(articles[1]["title"])
        article3.append(articles[2]["title"])
        article4.append(articles[3]["title"])
        article5.append(articles[4]["title"])

        cat1.append(articles[0]["categories"])
        cat2.append(articles[1]["categories"])
        cat3.append(articles[2]["categories"])
        cat4.append(articles[3]["categories"])
        cat5.append(articles[4]["categories"])
        
        # Delay like in reference code snippet to avoid ban
        time.sleep(1)

    df = pd.DataFrame({
        "Date": date_list,
        "Topic": [keywords[0] if keywords else "Topic"] * len(date_list),
        "Article1": article1,
        "Cat1": cat1,
        "Article2": article2,
        "Cat2": cat2,
        "Article3": article3,
        "Cat3": cat3,
        "Article4": article4,
        "Cat4": cat4,
        "Article5": article5,
        "Cat5": cat5
    })

    os.makedirs("data", exist_ok=True)

    file_ext = "xlsx" if file_format == "excel" else "csv"
    file_path = f"data/news_dataset.{file_ext}"

    if file_ext == "csv":
        df.to_csv(file_path, index=False)
    else:
        df.to_excel(file_path, index=False)

    return df, file_path
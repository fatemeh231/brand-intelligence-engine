# src/google_news.py
import feedparser
import pandas as pd
import os
from datetime import datetime

def scrape_google_news(company_name, limit=20, save_to_csv=True):
    """
    Scrape Google News RSS feed for a given company.
    Saves results to CSV automatically.
    """
    print(f"📰 Scraping Google News for: {company_name}")
    
    url = f"https://news.google.com/rss/search?q={company_name}&hl=en-US&gl=US&ceid=US:en"
    
    feed = feedparser.parse(url)
    
    articles = []
    for entry in feed.entries[:limit]:
        articles.append({
            "platform": "Google News",
            "company": company_name,
            "title": entry.title,
            "summary": entry.summary,
            "date": entry.published,
            "link": entry.link,
            "source": entry.source.title if hasattr(entry, 'source') else "Unknown"
        })
    
    df = pd.DataFrame(articles)
    print(f"   ✅ Scraped {len(df)} articles")
    
    # Save to CSV
    if save_to_csv and not df.empty:
        # Create data/raw folder if it doesn't exist
        os.makedirs("data/raw", exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/raw/google_news_{company_name}_{timestamp}.csv"
        
        df.to_csv(filename, index=False)
        print(f"   💾 Saved to: {filename}")
    
    return df

# Test
if __name__ == "__main__":
    df = scrape_google_news("Binance")
    print(df.head())
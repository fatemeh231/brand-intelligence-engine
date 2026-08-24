# src/googleplay.py
# Google Play Scraper – Fetch App Info and 300 Reviews

from google_play_scraper import app, reviews, Sort
import pandas as pd
import os
import time
from datetime import datetime

# Reuse your output directory
OUTPUT_DIR = r"C:\Users\fatemeh\OneDrive\Desktop\codes_tutorial_uni\brand-intelligence-engine\data\raw"

def scrape_google_play(app_package, lang='en', country='us', review_count=300, save_to_csv=True):
    """
    Scrape Google Play app info and up to `review_count` reviews (default 300).
    
    Parameters:
        app_package (str): e.g., 'com.binance.dev'
        lang (str): language code (default 'en')
        country (str): country code (default 'us')
        review_count (int): number of reviews to fetch (default 300)
        save_to_csv (bool): save reviews to CSV
    
    Returns:
        dict: {'summary': {...}, 'reviews': [...]}
    """
    print("="*60)
    print(f"⭐ GOOGLE PLAY SCRAPER: {app_package}")
    print("="*60)

    # 1. Fetch app details
    print("\n📱 Fetching app information...")
    try:
        app_info = app(
            app_package,
            lang=lang,
            country=country
        )
        summary = {
            'app_name': app_info.get('title'),
            'app_id': app_package,
            'developer': app_info.get('developer'),
            'rating': app_info.get('score'),
            'total_reviews': app_info.get('ratings'),
            'installs': app_info.get('installs'),
            'last_updated': app_info.get('updated'),
            'description': app_info.get('description')[:200] + '...' if app_info.get('description') else None,
        }
        print(f"   App name: {summary['app_name']}")
        print(f"   Rating: {summary['rating']} / 5")
        print(f"   Total reviews: {summary['total_reviews']}")
        print(f"   Installs: {summary['installs']}")
    except Exception as e:
        print(f"❌ Error fetching app details: {e}")
        return None

    # 2. Fetch reviews with pagination (batches of 100)
    print(f"\n📝 Fetching {review_count} reviews...")
    all_reviews = []
    continuation_token = None
    batch_size = 100
    
    while len(all_reviews) < review_count:
        remaining = review_count - len(all_reviews)
        current_batch = min(batch_size, remaining)
        
        try:
            if continuation_token:
                result, continuation_token = reviews(
                    app_package,
                    lang=lang,
                    country=country,
                    sort=Sort.NEWEST,
                    count=current_batch,
                    continuation_token=continuation_token
                )
            else:
                result, continuation_token = reviews(
                    app_package,
                    lang=lang,
                    country=country,
                    sort=Sort.NEWEST,
                    count=current_batch
                )
            
            if not result:
                print("   No more reviews available.")
                break
                
            all_reviews.extend(result)
            print(f"   Fetched {len(result)} reviews (total: {len(all_reviews)})")
            
            # If there's no continuation token, we've reached the last page
            if not continuation_token:
                print("   Reached the last page.")
                break
                
            # Be polite: wait a moment before the next batch
            time.sleep(0.5)
            
        except Exception as e:
            print(f"   ⚠️ Error fetching batch: {e}")
            break

    # Truncate to exactly review_count if we got more
    if len(all_reviews) > review_count:
        all_reviews = all_reviews[:review_count]

    # Convert to clean list of dicts
    review_list = []
    for r in all_reviews:
        review_list.append({
            'reviewer_name': r.get('userName'),
            'rating': r.get('score'),
            'title': r.get('title'),
            'text': r.get('content'),
            'date': r.get('at'),
            'thumbs_up': r.get('thumbsUpCount'),
            'reply': r.get('replyContent'),
            'reply_date': r.get('repliedAt'),
        })

    print(f"\n   ✅ Successfully fetched {len(review_list)} reviews.")

    # 3. Save to CSV
    if save_to_csv and review_list:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        df = pd.DataFrame(review_list)
        # Add app info columns
        df['app_name'] = summary['app_name']
        df['app_id'] = app_package
        file_path = os.path.join(OUTPUT_DIR, "googleplay_reviews.csv")
        df.to_csv(file_path, index=False, encoding='utf-8')
        print(f"   ✅ Saved {len(review_list)} reviews to {file_path}")
    elif save_to_csv:
        print("   No reviews to save.")

    # 4. Print summary
    print("\n📋 Summary:")
    for key, value in summary.items():
        print(f"   {key}: {value}")
    print(f"   reviews_fetched: {len(review_list)}")

    return {
        'summary': summary,
        'reviews': review_list
    }


if __name__ == "__main__":
    # Example usage
    app_id = input("Enter Google Play app package name (e.g., com.binance.dev): ").strip()
    if not app_id:
        app_id = "com.binance.dev"
    
    result = scrape_google_play(app_id, review_count=300)
    if result:
        print(f"\n✅ Done! Scraped {len(result['reviews'])} reviews.")
# src/combine.py
import pandas as pd
import os

DATA_DIR = r"C:\Users\fatemeh\OneDrive\Desktop\codes_tutorial_uni\brand-intelligence-engine\data\raw"

def load_google_news():
    filename = "google_news_Binance_20260824_143423.csv"
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filename}")
        return pd.DataFrame()
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {filename}: {len(df)} rows")
    # Parse date: "Fri, 21 Aug 2026 20:01:27 GMT"
    df['date'] = pd.to_datetime(df['date'], format='%a, %d %b %Y %H:%M:%S %Z', errors='coerce')
    df = df.dropna(subset=['date'])
    # Make timezone-naive (strip any timezone info, though this format is naive)
    df['date'] = df['date'].dt.tz_localize(None)
    print(f"   Parsed {len(df)} valid dates (naive)")
    df['text'] = df['title'].fillna('') + " " + df['summary'].fillna('')
    df['source'] = 'Google News'
    df['rating'] = None
    df['metadata'] = df['source']
    return df[['source', 'date', 'text', 'rating', 'metadata']]

def load_google_play():
    filename = "googleplay_reviews.csv"
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filename}")
        return pd.DataFrame()
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {filename}: {len(df)} rows")
    # Format: "2026-08-23 14:15:52" (naive)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df = df.dropna(subset=['date'])
    df['date'] = df['date'].dt.tz_localize(None)
    print(f"   Parsed {len(df)} valid dates (naive)")
    df['source'] = 'Google Play'
    df['text'] = df['text'].fillna('')
    df['metadata'] = df['reviewer_name'].fillna('') + " | 👍 " + df['thumbs_up'].astype(str)
    return df[['source', 'date', 'text', 'rating', 'metadata']]

def load_trustpilot():
    filename = "trustpilot_reviews.csv"
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filename}")
        return pd.DataFrame()
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {filename}: {len(df)} rows")
    # Format: "2026-08-24T00:07:12.000Z" (UTC, aware)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%dT%H:%M:%S.%fZ', errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    # Convert to naive (remove timezone)
    df['date'] = df['date'].dt.tz_localize(None)
    print(f"   Parsed {len(df)} valid dates (naive)")
    df['source'] = 'Trustpilot'
    df['text'] = df['text'].fillna('')
    df['metadata'] = df['title'].fillna('') + " | " + df['location'].fillna('')
    return df[['source', 'date', 'text', 'rating', 'metadata']]

def load_telegram():
    filename = "telegram_messages(1).csv"
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filename}")
        return pd.DataFrame()
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {filename}: {len(df)} rows")
    # Format: "2026-08-24 11:53:03+00:00" (aware)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S%z', errors='coerce')
    df = df.dropna(subset=['date'])
    # Convert to naive (strip timezone)
    df['date'] = df['date'].dt.tz_localize(None)
    print(f"   Parsed {len(df)} valid dates (naive)")
    df['source'] = 'Telegram'
    df['text'] = df['text'].fillna('')
    df['rating'] = None
    df['metadata'] = df['sender'].astype(str) + " | views: " + df['views'].astype(str)
    return df[['source', 'date', 'text', 'rating', 'metadata']]

def combine_all():
    sources = [
        load_google_news(),
        load_google_play(),
        load_trustpilot(),
        load_telegram()
    ]
    non_empty = [df for df in sources if not df.empty]
    if not non_empty:
        print("❌ No data loaded.")
        return pd.DataFrame()
    
    combined = pd.concat(non_empty, ignore_index=True)
    
    # Ensure all dates are naive (just in case some slipped through)
    combined['date'] = pd.to_datetime(combined['date'], errors='coerce')
    combined['date'] = combined['date'].dt.tz_localize(None)  # strip any remaining tz
    combined = combined.dropna(subset=['date'])
    
    combined.sort_values('date', ascending=False, inplace=True)
    return combined

if __name__ == "__main__":
    df_all = combine_all()
    if not df_all.empty:
        merged_path = os.path.join(DATA_DIR, "all_combined.csv")
        df_all.to_csv(merged_path, index=False, encoding='utf-8')
        print(f"✅ Saved {len(df_all)} records to {merged_path}")
        print("\nPreview (first 5 rows):")
        print(df_all[['source', 'date', 'text', 'rating']].head(5))
        print("\n📊 Record counts per source:")
        print(df_all['source'].value_counts())
    else:
        print("❌ No records to save.")
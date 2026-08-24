# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 16:02:56 2026

@author: fatemeh
"""

# src/add_sentiment.py
import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

DATA_DIR = r"C:\Users\fatemeh\OneDrive\Desktop\codes_tutorial_uni\brand-intelligence-engine\data\raw"
input_path = os.path.join(DATA_DIR, "all_combined.csv")
output_path = os.path.join(DATA_DIR, "all_combined_with_sentiment.csv")

# Load data
df = pd.read_csv(input_path)
print(f"Loaded {len(df)} records")

# Initialise VADER
analyzer = SentimentIntensityAnalyzer()

# Add sentiment columns
def get_sentiment(text):
    if pd.isna(text) or text.strip() == "":
        return {'compound': 0, 'label': 'neutral'}
    score = analyzer.polarity_scores(str(text))
    compound = score['compound']
    if compound >= 0.05:
        label = 'positive'
    elif compound <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'
    return {'compound': compound, 'label': label}

# Apply to each row
sentiments = df['text'].apply(lambda x: get_sentiment(x))
df['sentiment_score'] = sentiments.apply(lambda x: x['compound'])
df['sentiment_label'] = sentiments.apply(lambda x: x['label'])

# Save
df.to_csv(output_path, index=False, encoding='utf-8')
print(f"✅ Saved {len(df)} records with sentiment to {output_path}")
print("\nSentiment distribution:")
print(df['sentiment_label'].value_counts())
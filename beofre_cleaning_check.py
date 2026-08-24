# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:56:29 2026

@author: fatemeh
"""

import pandas as pd
import os

DATA_DIR = r"C:\Users\fatemeh\OneDrive\Desktop\codes_tutorial_uni\brand-intelligence-engine\data\raw"

def inspect_file(filename):
    path = os.path.join(DATA_DIR, filename)
    df = pd.read_csv(path)
    print(f"\n📁 {filename}")
    print("Columns:", list(df.columns))
    print("First 3 rows of 'date' column (if exists):")
    if 'date' in df.columns:
        print(df['date'].head(3))
    else:
        print("⚠️ No column named 'date'")
    print("Shape:", df.shape)

inspect_file("googleplay_reviews.csv")
inspect_file("trustpilot_reviews.csv")
inspect_file("telegram_messages(1).csv")
inspect_file("google_news_Binance_20260824_143423.csv")
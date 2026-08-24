# Brand Intelligence Engine

> Multi-source brand reputation scraper with NLP sentiment analysis.

## 🚀 Overview

This project scrapes, cleans, and analyzes brand mentions across 4 platforms:

- **Trustpilot** – Customer reviews and ratings
- **Google Play** – App store reviews
- **Google News** – News headlines and articles
- **Telegram** – Public channel messages

The pipeline applies **NLP sentiment analysis (VADER)** to classify each mention as positive, neutral, or negative.

## 📁 Project Structure

brand-intelligence-engine/
├── src/ # All scraper source code
│ ├── trustpilot.py
│ ├── googleplay.py
│ ├── googlenews.py
│ ├── telegram.py
│ ├── combine.py
│ └── combine_sentiment.py
├── data/
│ ├── raw/ # Raw scraped data (CSV)
│ └── processed/ # Cleaned & sentiment-enriched data
├── output/ # Power BI dashboard & screenshots
├── screenshot/ # Dashboard preview images
├── requirements.txt # Python dependencies
└── README.md # This file
text


## 🔧 Installation

```bash
pip install -r requirements.txt

🏃 Usage

Run each scraper individually:
bash

python src/trustpilot.py
python src/googleplay.py
python src/googlenews.py
python src/telegram.py

Combine all data:
bash

python src/combine.py

Add sentiment analysis:
bash

python src/combine_sentiment.py

📊 Technologies Used

    Python 3.10+

    Selenium – Web scraping

    Pandas – Data manipulation

    google-play-scraper – Google Play API

    Telethon – Telegram API

    VADER Sentiment – NLP sentiment analysis

    Power BI – Data visualization


conect with me:
linkedin= https://www.linkedin.com/in/seyedeh-fatemeh-hosseininasab-7320bb322/
and my GITHUB

👨‍💻 Author
SEYEDEH FATEMEH HOSSEININASAB with ❤
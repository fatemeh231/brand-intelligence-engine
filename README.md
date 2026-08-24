
# 🧠 Brand Intelligence Engine

> **Multi-source brand reputation scraper with NLP sentiment analysis.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)]()
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow.svg)](https://powerbi.microsoft.com/)
[![NLP](https://img.shields.io/badge/NLP-VADER-purple.svg)]()

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Dashboard Preview](#-dashboard-preview)
- [Key Insights](#-key-insights)
- [Technologies Used](#-technologies-used)
- [License](#-license)
- [Connect with Me](#-connect-with-me)

---

## 🚀 Overview

This project is a complete **brand intelligence pipeline** that automatically scrapes, cleans, and analyzes brand mentions across **4 major platforms**:

| Platform | Data Type | Purpose |
|:---|:---|:---|
| **Trustpilot** | Customer reviews & ratings | Understand customer satisfaction |
| **Google Play** | App store reviews | Monitor app reputation |
| **Google News** | News headlines & articles | Track media sentiment |
| **Telegram** | Public channel messages | Gauge community sentiment |

The pipeline applies **Natural Language Processing (VADER sentiment analysis)** to automatically classify each mention as **positive, neutral, or negative**, providing a comprehensive view of brand reputation in real-time.

---

## ✨ Features

| Feature | Description |
|:---|:---|
| 🤖 **Automated Scraping** | Selenium and API-based scrapers for each platform |
| 🧹 **Data Cleaning** | Unifies disparate data sources into a single schema |
| 🧠 **NLP Sentiment Analysis** | VADER lexicon-based sentiment scoring |
| 📈 **Interactive Dashboard** | Power BI dashboard for visualization |
| 📁 **CSV Export** | Clean, structured data ready for analysis |
| 🔄 **Scalable** | Modular design allows easy addition of new sources |

---

## 📁 Project Structure

```
brand-intelligence-engine/
│
├── src/                              # All scraper source code
│   ├── trustpilot.py                 # Trustpilot review scraper
│   ├── googleplay.py                 # Google Play review scraper
│   ├── googlenews.py                 # Google News headline scraper
│   ├── telegram.py                   # Telegram channel scraper
│   ├── combine.py                    # Merge all sources into one CSV
│   └── combine_sentiment.py          # Add NLP sentiment analysis
│
├── data/
│   ├── raw/                          # Raw scraped data (CSV)
│   │   ├── google_news_*.csv
│   │   ├── googleplay_reviews.csv
│   │   ├── trustpilot_reviews.csv
│   │   └── telegram_messages.csv
│   └── processed/                    # Cleaned & sentiment-enriched data
│       ├── all_combined.csv
│       └── all_combined_with_sentiment.csv
│
├── output/                           # Power BI dashboard & screenshots
│   ├── output.pbix
│   └── *.PNG
│
├── screenshot/                       # Dashboard preview images
│   └── dashboard_preview.PNG
│
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/fatemeh231/brand-intelligence-engine.git
cd brand-intelligence-engine
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Credentials

For Telegram scraping, create a `.env` file in the project root:

```
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
PHONE_NUMBER=your_phone_number
```

> **Note:** You can get your Telegram API credentials from [my.telegram.org/apps](https://my.telegram.org/apps).

---

## 🏃 Usage

### Run Individual Scrapers

```bash
python src/trustpilot.py      # Scrape Trustpilot reviews
python src/googleplay.py      # Scrape Google Play reviews
python src/googlenews.py      # Scrape Google News headlines
python src/telegram.py        # Scrape Telegram channel messages
```

### Combine All Data

```bash
python src/combine.py
```

### Add Sentiment Analysis (NLP)

```bash
python src/combine_sentiment.py
```

### Open the Dashboard

Open `output/output.pbix` in **Power BI Desktop** to explore the interactive dashboard.

---

## 📊 Dashboard Preview

![Brand Intelligence Dashboard](screenshot/dashboard_preview.PNG)

> *Interactive Power BI dashboard showing sentiment distribution, source breakdown, trends over time, and keyword analysis.*

---

## 📈 Key Insights

| Insight | Finding |
|:---|:---|
| 📊 **Total Mentions** | 740 reviews/news/chat messages analyzed |
| 📈 **Positive Sentiment** | 58.6% of all mentions are positive |
| 📉 **Negative Sentiment** | 15.1% of all mentions are negative |
| 🟢 **Safest Platform** | Telegram shows the highest positive sentiment |
| 🔴 **Risk Platform** | Trustpilot shows the highest negative sentiment |
| 🔍 **Main Complaint** | "Withdrawal delays" and "frozen funds" are the top negative topics |

---

## 🛠️ Technologies Used

| Category | Tools |
|:---|:---|
| **Programming Language** | Python 3.10+ |
| **Web Scraping** | Selenium, google-play-scraper, Telethon, feedparser |
| **Data Processing** | Pandas, NumPy |
| **Natural Language Processing** | VADER Sentiment (lexicon-based) |
| **Visualization** | Power BI Desktop |
| **Version Control** | Git & GitHub |
| **Environment** | Python-dotenv |

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Seyedeh Fatemeh Hosseininasab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🤝 Connect with Me

I'm a passionate **Data Engineer & Scraping Specialist** focused on building end-to-end data pipelines. If you're interested in collaborating or hiring, let's connect!

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Seyedeh%20Fatemeh%20Hosseininasab-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/seyedeh-fatemeh-hosseininasab-7320bb322/)
[![GitHub](https://img.shields.io/badge/GitHub-fatemeh231-black?style=for-the-badge&logo=github)](https://github.com/fatemeh231)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail)](mailto:seyedehfatemehhosseininasab2@gmail.com)

---

## 📝 Author

**Seyedeh Fatemeh Hosseininasab**  
*Data Engineer | Web Scraping Specialist | NLP Enthusiast*

Built with ❤️ as a complete brand intelligence freelancing project.

---

### ⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

## 🔄 Changelog

| Version | Date | Changes |
|:---|:---|:---|
| 1.0.0 | August 2026 | Initial release – Complete brand intelligence pipeline |
```

---


# src/trustpilot.py
# Trustpilot Scraper - Extract Summary Stats, Reviews from up to 5 Pages, and Save to CSV

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os
import re
from datetime import datetime

# Path to your geckodriver
GECKODRIVER_PATH = r"C:\Users\fatemeh\OneDrive\Desktop\codes_tutorial_uni\extra\geckodriver.exe"

# Directory to save CSV
OUTPUT_DIR = r"C:\Users\fatemeh\OneDrive\Desktop\codes_tutorial_uni\brand-intelligence-engine\data\raw"

def compute_average_rating(star_data, total_reviews):
    """
    Compute the weighted average star rating from the star distribution.
    star_data: dict with keys like '5-star', '4-star', etc., each containing a 'count'.
    total_reviews: total number of reviews (should equal sum of counts).
    Returns the average as a float rounded to 2 decimal places.
    """
    if not star_data or total_reviews is None or total_reviews == 0:
        return None
    
    star_map = {
        '5-star': 5,
        '4-star': 4,
        '3-star': 3,
        '2-star': 2,
        '1-star': 1
    }
    
    weighted_sum = 0
    total_count = 0
    for star_label, info in star_data.items():
        count = info.get('count', 0)
        if count is not None:
            star_value = star_map.get(star_label, 0)
            weighted_sum += star_value * count
            total_count += count
    
    if total_count == 0:
        return None
    avg = weighted_sum / total_count
    return round(avg, 2)

def extract_review_summary(driver):
    """
    Extract summary data from the Trustpilot review page:
    - Total number of reviews
    - Reviews in the last 12 months
    - For each star (1 to 5): count and percentage
    Returns a dictionary.
    """
    summary = {}

    # 1. Total reviews
    try:
        all_reviews_heading = driver.find_element(By.CLASS_NAME, "styles_allReviewsHeading__TLPHN")
        p_tag = all_reviews_heading.find_element(By.TAG_NAME, "p")
        total_text = p_tag.text.strip()
        match = re.search(r'[\d,]+', total_text)
        if match:
            total_reviews = int(match.group().replace(',', ''))
            summary['total_reviews'] = total_reviews
            print(f"   Total reviews: {total_reviews}")
        else:
            summary['total_reviews'] = None
            print("   Total reviews: N/A")
    except Exception as e:
        print(f"   Total reviews: N/A (error: {e})")
        summary['total_reviews'] = None

    # 2. Reviews in the last 12 months
    try:
        twelve_months_elem = driver.find_element(By.CSS_SELECTOR, "[data-reviews-count-typography='true']")
        strong_elem = twelve_months_elem.find_element(By.TAG_NAME, "strong")
        text = strong_elem.text.strip()
        match = re.search(r'([\d,]+)', text)
        if match:
            last_12_months = int(match.group(1).replace(',', ''))
            summary['last_12_months_reviews'] = last_12_months
            print(f"   Reviews in last 12 months: {last_12_months}")
        else:
            summary['last_12_months_reviews'] = None
            print("   Reviews in last 12 months: N/A")
    except Exception as e:
        print(f"   Reviews in last 12 months: N/A (error: {e})")
        summary['last_12_months_reviews'] = None

    # 3. Star distribution (count and percentage for each star)
    star_data = {}
    try:
        star_labels = driver.find_elements(By.CSS_SELECTOR, "label[data-star-rating]")
        for label in star_labels:
            star_rating_attr = label.get_attribute("data-star-rating")
            star_map = {
                "five": "5-star",
                "four": "4-star",
                "three": "3-star",
                "two": "2-star",
                "one": "1-star"
            }
            star_key = star_map.get(star_rating_attr, star_rating_attr)
            
            title = label.get_attribute("title")
            match = re.search(r'^([\d,]+)\s+of', title)
            if match:
                count = int(match.group(1).replace(',', ''))
            else:
                count = None
            
            try:
                percent_elem = label.find_element(By.CSS_SELECTOR, "[data-rating-distribution-row-percentage-typography='true']")
                percent_text = percent_elem.text.strip().replace('%', '')
                percentage = int(percent_text)
            except:
                percentage = None
            
            star_data[star_key] = {
                'count': count,
                'percentage': percentage
            }
        
        summary['star_distribution'] = star_data
        print("   Star distribution extracted:")
        for star, info in star_data.items():
            print(f"      {star}: {info['count']} reviews ({info['percentage']}%)")
    except Exception as e:
        print(f"   Star distribution: N/A (error: {e})")
        summary['star_distribution'] = None

    return summary

def extract_reviews_from_page(driver):
    """
    Extract all review cards from the current page.
    Returns a list of dictionaries, each containing review data.
    """
    reviews = []
    try:
        review_articles = driver.find_elements(By.CSS_SELECTOR, "article[data-service-review-card-paper='true']")
        print(f"   Found {len(review_articles)} review cards on this page.")
        
        for article in review_articles:
            review_data = {}
            
            # Reviewer name
            try:
                name_elem = article.find_element(By.CSS_SELECTOR, "[data-consumer-name-typography='true']")
                review_data['reviewer_name'] = name_elem.text.strip()
            except:
                review_data['reviewer_name'] = None
            
            # Rating (stars)
            try:
                rating_elem = article.find_element(By.CSS_SELECTOR, "[data-service-review-rating]")
                rating = rating_elem.get_attribute("data-service-review-rating")
                review_data['rating'] = int(rating) if rating else None
            except:
                review_data['rating'] = None
            
            # Review title
            try:
                title_elem = article.find_element(By.CSS_SELECTOR, "[data-service-review-title-typography='true']")
                review_data['title'] = title_elem.text.strip()
            except:
                review_data['title'] = None
            
            # Review text
            try:
                text_elem = article.find_element(By.CSS_SELECTOR, "[data-service-review-text-typography='true']")
                review_data['text'] = text_elem.text.strip()
            except:
                review_data['text'] = None
            
            # Date
            try:
                date_elem = article.find_element(By.CSS_SELECTOR, "[data-service-review-date-time-ago='true']")
                date_str = date_elem.get_attribute("datetime")
                if not date_str:
                    date_str = date_elem.text.strip()
                review_data['date'] = date_str
            except:
                review_data['date'] = None
            
            # Location (country)
            try:
                location_elem = article.find_element(By.CSS_SELECTOR, "[data-consumer-country-typography='true']")
                review_data['location'] = location_elem.text.strip()
            except:
                review_data['location'] = None
            
            # Number of reviews by this user
            try:
                count_elem = article.find_element(By.CSS_SELECTOR, "[data-consumer-reviews-count-typography='true']")
                count_text = count_elem.text.strip()
                match = re.search(r'(\d+)', count_text)
                review_data['user_review_count'] = int(match.group(1)) if match else None
            except:
                review_data['user_review_count'] = None
            
            reviews.append(review_data)
        
        return reviews
    except Exception as e:
        print(f"   Error extracting reviews: {e}")
        return []

def save_reviews_to_csv(reviews, company_name):
    """
    Save the list of review dictionaries to a CSV file in the output directory.
    """
    if not reviews:
        print("   No reviews to save.")
        return
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    df = pd.DataFrame(reviews)
    df['company'] = company_name
    
    file_path = os.path.join(OUTPUT_DIR, "trustpilot_reviews.csv")
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"   ✅ Saved {len(df)} reviews to {file_path}")

def is_next_button_disabled(driver):
    """
    Check if the 'Next' button is disabled (i.e., no more pages).
    Returns True if disabled or not found, False otherwise.
    """
    try:
        # Look for the Next button link
        next_link = driver.find_element(By.CSS_SELECTOR, "a[data-pagination-button-next-link='true']")
        # Check if it has the 'disabled' class or aria-disabled="true"
        if next_link.get_attribute("aria-disabled") == "true":
            return True
        # Also check if the parent has a disabled class (some pagination uses class)
        if "disabled" in next_link.get_attribute("class"):
            return True
        return False
    except:
        # If not found, assume no next page
        return True

def click_next_page(driver):
    """
    Click the 'Next' button if it exists and is not disabled.
    Returns True if clicked, False otherwise.
    """
    try:
        next_link = driver.find_element(By.CSS_SELECTOR, "a[data-pagination-button-next-link='true']")
        if next_link.get_attribute("aria-disabled") == "true":
            return False
        next_link.click()
        return True
    except:
        return False

def scrape_trustpilot(company_name, max_pages=5, save_to_csv=True):
    """
    Scrape Trustpilot: Search, click first result, extract summary and reviews from up to max_pages.
    """
    print("="*60)
    print(f"⭐ TRUSTPILOT SCRAPER: {company_name}")
    print("="*60)
    
    options = Options()
    options.set_preference("browser.startup.homepage", "about:blank")
    options.set_preference("browser.startup.page", 0)
    
    driver = webdriver.Firefox(options=options)
    
    try:
        # ===== STEP 1-8: Navigate to the review page (unchanged) =====
        print("🌐 Opening Trustpilot...")
        driver.get("https://www.trustpilot.com")
        print("⏳ Waiting 10 seconds for page to settle...")
        time.sleep(10)
        
        print("🔍 Finding search box...")
        search_box = driver.find_element(By.CLASS_NAME, "styles_searchInputField__dztwi")
        print("✅ Search box found!")
        
        print(f"📝 Typing: {company_name}")
        search_box.clear()
        search_box.send_keys(company_name)
        time.sleep(10)
        
        print("⏎ Pressing Enter...")
        search_box.send_keys(Keys.RETURN)
        
        print("⏳ Waiting 10 seconds for search results...")
        time.sleep(10)
        
        print("🖱️ Clicking the first result...")
        first_result = driver.find_element(By.CLASS_NAME, "styles_content__Z7nNB")
        first_result.click()
        print("✅ Clicked first result!")
        
        print("⏳ Waiting 10 seconds for review page to load...")
        time.sleep(10)
        
        current_url = driver.current_url
        page_title = driver.title
        print(f"\n📄 Current URL: {current_url}")
        print(f"📄 Page Title: {page_title}")
        
        if "review" in current_url:
            print("✅ On the review page!")
        else:
            print("⚠️ Not on review page yet.")
        
        # ===== STEP 9: Extract summary data (once) =====
        print("\n📊 Extracting summary data from review page...")
        summary_data = extract_review_summary(driver)
        
        # ===== STEP 10: Compute average rating =====
        total = summary_data.get('total_reviews')
        star_dist = summary_data.get('star_distribution')
        if total and star_dist:
            avg_rating = compute_average_rating(star_dist, total)
            summary_data['average_rating'] = avg_rating
            print(f"\n   ⭐ Average star rating: {avg_rating} / 5")
        else:
            summary_data['average_rating'] = None
            print("\n   ⭐ Average star rating: Not computable (missing data)")
        
        # ===== STEP 11: Extract reviews from all pages (up to max_pages) =====
        all_reviews = []
        current_page = 1
        
        # Extract from the current (first) page
        print(f"\n📝 Extracting reviews from page {current_page}...")
        page_reviews = extract_reviews_from_page(driver)
        all_reviews.extend(page_reviews)
        
        # Loop for pages 2 to max_pages
        while current_page < max_pages:
            # Check if Next button is available and clickable
            if is_next_button_disabled(driver):
                print(f"   No more pages available after page {current_page}.")
                break
            
            # Click Next and wait for load
            print(f"   Clicking 'Next' to go to page {current_page + 1}...")
            clicked = click_next_page(driver)
            if not clicked:
                print("   Next button not clickable, stopping.")
                break
            
            time.sleep(10)  # Wait for page to load
            
            current_page += 1
            print(f"\n📝 Extracting reviews from page {current_page}...")
            page_reviews = extract_reviews_from_page(driver)
            all_reviews.extend(page_reviews)
        
        print(f"\n   Total reviews extracted: {len(all_reviews)} from {current_page} page(s).")
        
        # ===== STEP 12: Save all reviews to CSV =====
        if save_to_csv and all_reviews:
            save_reviews_to_csv(all_reviews, company_name)
        elif save_to_csv:
            print("   No reviews to save.")
        
        # Print summary
        print("\n📋 Summary of extracted data:")
        for key, value in summary_data.items():
            if key == 'star_distribution' and value:
                print("   Star distribution (count, percentage):")
                for star, info in value.items():
                    print(f"      {star}: {info['count']} reviews ({info['percentage']}%)")
            elif key == 'average_rating':
                print(f"   Average rating: {value} / 5")
            else:
                print(f"   {key}: {value}")
        
        # ===== STEP 13: KEEP BROWSER OPEN =====
        print("\n🔍 Browser stays open for inspection.")
        print("📋 Look at the review page and check the data above.")
        input("Press Enter to close the browser...")
        
        return {
            'summary': summary_data,
            'reviews': all_reviews,
            'pages_scraped': current_page
        }
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    
    finally:
        driver.quit()
        print("✅ Browser closed.")


if __name__ == "__main__":
    company = input("Enter company to search (e.g., binance): ").strip()
    if not company:
        company = "binance"
    
    result = scrape_trustpilot(company, max_pages=5)
    
    if result:
        data = result['summary']
        reviews = result['reviews']
        print("\n✅ Scraping completed successfully!")
        print(f"   Total reviews (according to Trustpilot): {data.get('total_reviews')}")
        print(f"   Last 12 months reviews: {data.get('last_12_months_reviews')}")
        print("   Star distribution:")
        if data.get('star_distribution'):
            for star, info in data['star_distribution'].items():
                print(f"      {star}: {info['count']} reviews ({info['percentage']}%)")
        print(f"   ⭐ Average star rating: {data.get('average_rating')} / 5")
        print(f"   Scraped {len(reviews)} reviews from {result['pages_scraped']} page(s).")
        print(f"   CSV saved to: {OUTPUT_DIR}\\trustpilot_reviews.csv")
    else:
        print("\n❌ Scraping failed.")
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

# Define headers to avoid getting blocked
HEADERS = {
    "User-Agent": "Your User-Agent String",
    "Accept-Language": "en-US, en;q=0.5"
}

# Function to extract product details
def extract_product_details(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract product title
        title_tag = soup.find("span", {"id": "productTitle"})
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Extract price
        price_tag = soup.find("span", {"class": "a-offscreen"})
        price = price_tag.get_text(strip=True) if price_tag else "N/A"

        # Extract rating
        rating_tag = soup.find("span", {"class": "a-icon-alt"})
        rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

        return {
            "Title": title,
            "Price": price,
            "Rating": rating
        }

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Function to scrape multiple URLs
def scrape_amazon_products(urls):
    product_list = []

    for url in urls:
        product_details = extract_product_details(url)
        if product_details:
            product_list.append(product_details)

        # Random delay to prevent getting blocked
        time.sleep(random.uniform(1, 3))

    return product_list

# Function to save data to CSV
def save_to_csv(product_list, filename):
    df = pd.DataFrame(product_list)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    # List of product URLs to scrape
    amazon_urls = [
        "https://www.amazon.com/dp/B08J5F3G18",  # Replace with actual product URLs
        "https://www.amazon.com/dp/B09G9FPHY4"
        # Add more URLs here
    ]

    # Scrape product details
    scraped_data = scrape_amazon_products(amazon_urls)

    # Save the results to a CSV file
    save_to_csv(scraped_data, "amazon_products.csv")

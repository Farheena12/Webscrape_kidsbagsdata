import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from PIL import Image
import pandas as pd
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(filename='scraping_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#st.header("Web Scraping Using Selenium and BeautifulSoup")

base = "dark"
primaryColor = "purple"
st.title("Kids Bags Details")
image = Image.open('pandabag.jpg')
st.image(image)

# Create ChromeOptions object
chrome_options = Options()

# Set User-Agent header
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")

# Set Accept-Language header
accept_language = "en-US,en;q=0.5"
chrome_options.add_argument(f"accept-language={accept_language}")

# Initialize the Chrome WebDriver with the options
driver = webdriver.Chrome(options=chrome_options)

# Define the URL to scrape
url = 'https://www.amazon.in/s?k=kids+bags&crid=2LAQ8GAVHOS6S&sprefix=kids+bags%2Caps%2C494&ref=nb_sb_noss_1'

# Navigate to the URL
driver.get(url)

# Add a sleep to allow JavaScript content to load (you may need to adjust this)
import time
time.sleep(5)  # Wait for 5 seconds

# Explicit wait for the results to load
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.s-result-item[data-component-type="s-search-result"]')))
except Exception as e:
    logging.error(f"Timeout waiting for results to load: {str(e)}")
    st.error("Timeout waiting for results to load. Please try again later or check the log for details.")
    driver.quit()
    st.stop()

# Get the page source after waiting for a while
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Extract product details
product_details = []
results = soup.select('div.s-result-item[data-component-type="s-search-result"]')

for result in results:
    try:
        links = ('https://www.amazon.in' + result.select_one('a').get('href'))

        p_names = result.select_one('h2 a span').get_text()
        p_prices = result.select_one('span.a-offscreen').get_text()
        p_ratings = result.select_one('span.a-icon-alt').get_text()
        p_reviews = result.select_one('span.a-size-base').get_text()

        product_details.append({
            'Urls': links,
            'p_names': p_names,
            'p_prices': p_prices,
            'p_ratings': p_ratings,
            'p_reviews': p_reviews,
        })
    except Exception as e:
        logging.warning(f"Error scraping product details: {str(e)}")

# Close the WebDriver
driver.quit()

# Create a DataFrame
df = pd.DataFrame(product_details)

# Add 1 to the index to start from 1
df.index = df.index + 1

# Display the DataFrame
st.write(df)
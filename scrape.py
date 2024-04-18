"""
Web Scraping Script for Scraping Book Data from 'books.toscrape.com'

This script scrapes book data from the 'books.toscrape.com' website, retrieving information about books 
such as title, link, price, and stock availability from each page. The script automatically 
increments the page number until it reaches a non-existent page or encounters an error.

Requirements:
- BeautifulSoup: For parsing HTML content.
- requests: For sending HTTP requests.
- pandas: For data manipulation.
- logging: For logging errors.
"""


# Import necessary libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging

# Page Number
current_page = 47

# Initialize an empty list to store scraped book data
data = []

# Flag to control loop execution
proceed = True

# Configure logging
logging.basicConfig(filename='web_scraping.log', level=logging.ERROR)

# Loop to scrape data from multiple pages
while proceed:
    # Print current page number being scraped
    print(f"Current scrapping page: {current_page}")

    # Form the URL for the current page
    url = requests.get(f"https://books.toscrape.com/catalogue/page-{current_page}.html")

    # Parse the HTML content of the page
    soup = BeautifulSoup(url.text, "html.parser")

    try:
        # Check if the page exists
        if soup.title.text == "404 Not Found":
            # Log error if the page is not found
            logging.error(f"Failed to retrieve webpage {current_page}. Status code: %d", url.status_code)
            # Set flag to exit loop
            proceed = False
            print("The page is not available.")
        else:
            # Find all book items on the page
            all_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

            # Extract book data from each book item
            for book in all_books:
                item = {}

                item['Title'] = book.find("img").attrs["alt"]
                item['Link'] = "https://books.toscrape.com/catalogue/" + book.find("a").attrs["href"]
                item['Price'] = book.find("p", class_="price_color").text[2:]
                item['Stock'] = book.find("p", class_="instock availability").text.strip()

                # Append extracted book data to the list
                data.append(item)

        # Increment page number for the next iteration
        current_page += 1

    except requests.RequestException as e:
        # If there's a connection error or other problems with the request
        logging.error("Error: %s", e)
        # Set flag to exit loop
        proceed = False

# Convert scraped data to a DataFrame and save to CSV file
df = pd.DataFrame(data)
df.to_csv("books.csv")

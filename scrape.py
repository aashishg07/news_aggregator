import requests
from bs4 import BeautifulSoup
import urllib.request
import csv
from datetime import date
from urllib.parse import urljoin

# URL of the BBC News homepage
url = 'https://www.bbc.com/nepali'

# User agent header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
}

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Get today's date for the CSV filename
today = date.today().strftime("%Y-%m-%d")
filename = f'bbc_news_{today}.csv'

# Find all the news articles on the page
article_tags = soup.find_all('a', class_='focusIndicatorDisplayInlineBlock bbc-1mirykb ecljyjm0')

# Create a list to store the scraped data
data = []

# Loop over the article tags and extract the title, description, and images
for article in article_tags:
    title = article.get_text().strip()
    url = article['href']
    
    # Check if the URL is missing a scheme and add it
    if not url.startswith('http'):
        url = urljoin('https://www.bbc.com/nepali', url)

    # Get the article page to scrape the description and images
    article_response = requests.get(url)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')

    # Extract the description
    description_tag = article_soup.find_all('p', class_='bbc-kl1u1v e17g058b0')
    description = ' '.join(tag.get_text().strip() for tag in description_tag)

    # Extract the images
    image_tags = article_soup.find_all('img')
    image_urls = [img.get('srcset') for img in image_tags if img.get('srcset') and img.get('srcset').startswith('http')]

    #  # Download and save the images
    # for i, image_url in enumerate(image_urls):
    #     try:
    #         image_name = f'{today}_article_{i}.jpg'
    #         urllib.request.urlretrieve(image_url, image_name)
    #         print(f"Image {image_name} downloaded successfully.")
    #     except Exception as e:
    #         print(f"Error downloading image {image_name}: {e}")

    # Store the data in the list
    data.append([title, description, ','.join(image_urls)])

# Save data to CSV file
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Description', 'Images'])  # Write header row
    writer.writerows(data)

print(f"Data saved to {filename} successfully.")

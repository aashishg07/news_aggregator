from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
from urllib.parse import urljoin

def get_news(request):
    # URL of the BBC News homepage
    bbc_url = 'https://www.bbc.com/nepali'
    toi_url = 'https://timesofindia.indiatimes.com/briefs'

    # User agent header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
    }

    # Send a GET request to the BBC News URL
    bbc_response = requests.get(bbc_url, headers=headers)

    # Create a BeautifulSoup object to parse the BBC News HTML content
    bbc_soup = BeautifulSoup(bbc_response.content, 'html.parser')

    # Get today's date for the CSV filename
    today = date.today().strftime("%Y-%m-%d")
    filename = f'bbc_news_{today}.csv'

    # Find all the news articles on the BBC News page
    bbc_article_tags = bbc_soup.find_all('a', class_='focusIndicatorDisplayInlineBlock bbc-1mirykb ecljyjm0')

    # Create a list to store the scraped BBC News data
    bbc_data = []

    # Loop over the BBC article tags and extract the title, description, and images
    for article in bbc_article_tags:
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

        # Store the data in the list
        bbc_data.append([title, description, ','.join(image_urls)])

    # Send a GET request to the Times of India URL
    toi_response = requests.get(toi_url, headers=headers)

    # Create a BeautifulSoup object to parse the Times of India HTML content
    toi_soup = BeautifulSoup(toi_response.content, 'html.parser')

    toi_headings = toi_soup.find_all('h2')
    toi_headings = toi_headings[0:-13]  # removing footers

    # Create a list to store the scraped Times of India data
    toi_news = [th.text for th in toi_headings]

    # Pass the data to the template
    return render(request, 'index.html', {'bbc_news': bbc_data, 'toi_news': toi_news})

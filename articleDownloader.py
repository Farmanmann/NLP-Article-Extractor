from bs4 import BeautifulSoup
import requests
import os  # To make directories
import time  # To avoid overloading the server
from datetime import datetime  # To create date-specific folders

def getHTMLdocument(url):
    """Fetch the HTML content of a given URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for failed requests
    return response.text

# Base setup
base_url = "https://www.darivoa.com/"
html_document = getHTMLdocument(base_url)

if html_document:
    # Get today's date for folder organization
    current_date = datetime.now().strftime("%Y-%m-%d")
    base_dir = "articles"  # Base directory for articles
    articles_dir = os.path.join(base_dir, current_date)
    
    # Ensure the date-specific directory exists
    if not os.path.exists(articles_dir):
        os.makedirs(articles_dir)
    
    # Parse the HTML
    soup = BeautifulSoup(html_document, 'html.parser')
    article_urls = set()

    # Find all article links on the main page
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and '/a/' in href:  # Check if it's an article link
            full_url = base_url.rstrip('/') + href if not href.startswith('http') else href
            article_urls.add(full_url)

    # Loop through and download each article
    for i, url in enumerate(article_urls, 1):
        print(f"Downloading article {i}/{len(article_urls)}: {url}")
        
        # Extract article ID from URL
        article_id = url.split('/')[-1].replace('.html', '')
        
        # Download the article HTML
        try:
            article_html = getHTMLdocument(url)
            # Save the HTML to a file
            filename = os.path.join(articles_dir, f'article_{article_id}.html')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(article_html)
            
            # Delay between requests
            time.sleep(1)
        except Exception as e:
            print(f"Failed to download {url}: {e}")

    print(f"Downloaded {len(article_urls)} Articles in total into folder: {articles_dir}")
else:
    print("Failed to retrieve the main page.")


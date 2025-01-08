from bs4 import BeautifulSoup
import requests

import os #to make directories
import time #to avoid overloading the server

def getHTMLdocument(url):
    response = requests.get(url)
    return response.text

if not os.path.exists('articles'):
    os.makedirs('articles')

url_to_scrape = "https://www.darivoa.com/"
html_document = getHTMLdocument(url_to_scrape)

if html_document:
    soup = BeautifulSoup(html_document, 'html.parser')
    article_urls = set()

    #    Find all links that contain article paths
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and '/a/' in href:  # Check if it's an article link
            if not href.startswith('http'):  # If it's a relative URL
                full_url = url_to_scrape.rstrip('/') + href
            else:
                full_url = href
            article_urls.add(full_url)
    
    for i, url in enumerate(article_urls, 1):
        print(f"Downloading article {i}/{len(article_urls)}: {url}")
        
        # Extract article ID from URL
        article_id = url.split('/')[-1].replace('.html', '')
        
        # Download article HTML
        article_html = getHTMLdocument(url)
        if article_html:
            # Save to file
            filename = f'articles/article_{article_id}.html'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(article_html)
            
            # Small delay to be polite to the server
            time.sleep(1)
            
    print(f"Downloaded {len(article_urls)} Articles in total")

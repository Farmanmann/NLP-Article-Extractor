from bs4 import BeautifulSoup
import os
from datetime import datetime  # To create date-based folders


def clean_text(text):
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text.strip()


def extract_article_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements
    for unwanted in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
        unwanted.decompose()
    
    # Find the main article content
    article_content = []
    
    # Look for article content in common content containers
    content_div = soup.find('div', class_='content-offset')
    if content_div:
        # Extract all paragraphs
        paragraphs = content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for p in paragraphs:
            text = clean_text(p.get_text())
            if text:  # Only add non-empty text
                article_content.append(text)
    
    return '\n\n'.join(article_content)


# Base directories for storing HTML and text files
articles_base_dir = 'articles'
texts_base_dir = 'article_texts'

# Get today's date to locate the correct date folder
current_date = datetime.now().strftime("%Y-%m-%d")
html_dir = os.path.join(articles_base_dir, current_date)
text_dir = os.path.join(texts_base_dir, current_date)

# Ensure the text directory exists
if not os.path.exists(text_dir):
    os.makedirs(text_dir)

# Process each HTML file in the date-based folder
for filename in os.listdir(html_dir):
    if filename.endswith('.html'):
        print(f"Processing {filename}")
        
        # Read HTML file
        html_path = os.path.join(html_dir, filename)
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extract and clean text
        article_text = extract_article_content(html_content)
        
        # Save text to the text folder
        text_filename = filename.replace('.html', '.txt')
        text_path = os.path.join(text_dir, text_filename)
        
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(article_text)

print(f"Text extraction complete! Files saved in: {text_dir}")

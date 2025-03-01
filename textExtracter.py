from bs4 import BeautifulSoup
import os
from datetime import datetime

def clean_text(text):
    """Removes extra whitespace and unnecessary line breaks."""
    return ' '.join(text.split()).strip()

def extract_article_content(html_content):
    """Extracts main article content from an HTML file."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unnecessary elements (scripts, styles, navigation, etc.)
    for unwanted in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
        unwanted.decompose()
    
    # Extract text from common content containers
    article_content = []
    
    # Attempt to locate the main content div
    content_div = soup.find('div', class_='content-offset')
    if content_div:
        paragraphs = content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for p in paragraphs:
            text = clean_text(p.get_text())
            if text:
                article_content.append(text)
    
    # If no content was found, extract all text as fallback
    if not article_content:
        all_text = clean_text(soup.get_text())
        article_content.append(all_text)
    
    return '\n\n'.join(article_content)

# Directories for source HTML and extracted text
html_base_dir = 'downloaded_html'
text_base_dir = 'articles'

# Use today's date for locating HTML files and saving extracted text
current_date = datetime.now().strftime("%Y-%m-%d")
html_dir = os.path.join(html_base_dir, current_date)
text_dir = os.path.join(text_base_dir, current_date)

# Ensure output directory exists
os.makedirs(text_dir, exist_ok=True)

# Process each HTML file in today's folder
if os.path.exists(html_dir):
    for filename in os.listdir(html_dir):
        if filename.endswith('.html'):
            print(f"📄 Processing {filename}...")
            
            # Read the HTML file
            html_path = os.path.join(html_dir, filename)
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Extract text
            article_text = extract_article_content(html_content)
            
            # Save extracted text as .txt
            text_filename = filename.replace('.html', '.txt')
            text_path = os.path.join(text_dir, text_filename)
            
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(article_text)
    
    print(f"Text extraction complete! Files saved in: {text_dir}")
else:
    print(f"No HTML files found in {html_dir}. Check if the HTML files exist.")

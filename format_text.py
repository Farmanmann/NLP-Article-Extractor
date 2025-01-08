import nltk
import os
from bs4 import BeautifulSoup
import re

# Download necessary NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def clean_text(text):
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove special characters but keep Persian/Arabic characters and punctuation
    text = re.sub(r'[^\u0600-\u06FF\s.,!?؟،]+', ' ', text)
    return text.strip()

def segment_and_format_text(text):
    # Tokenize into sentences using NLTK
    sentences = nltk.sent_tokenize(text)
    
    # Clean and format each sentence
    formatted_sentences = []
    for sentence in sentences:
        cleaned = clean_text(sentence)
        if cleaned:  # Only add non-empty sentences
            formatted_sentences.append(cleaned)
    
    # Join sentences with proper spacing
    return '\n'.join(formatted_sentences)

def extract_article_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements
    for unwanted in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
        unwanted.decompose()
    
    # Find the main article content
    content_div = soup.find('div', class_='content-offset')
    if content_div:
        # Extract text from all relevant elements
        text_elements = content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        article_text = ' '.join(element.get_text().strip() for element in text_elements)
        return article_text
    return ''

# Process all downloaded articles
articles_dir = 'articles'
formatted_dir = 'formatted_articles'

# Create formatted directory if it doesn't exist
if not os.path.exists(formatted_dir):
    os.makedirs(formatted_dir)

# Process each HTML file
for filename in os.listdir(articles_dir):
    if filename.endswith('.html'):
        print(f"Processing {filename}")
        
        # Read HTML file
        with open(os.path.join(articles_dir, filename), 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extract content
        article_text = extract_article_content(html_content)
        
        # Segment and format text
        formatted_text = segment_and_format_text(article_text)
        
        # Save formatted text
        formatted_filename = filename.replace('.html', '_formatted.txt')
        with open(os.path.join(formatted_dir, formatted_filename), 'w', encoding='utf-8') as f:
            f.write(formatted_text)

print("Text formatting complete!")
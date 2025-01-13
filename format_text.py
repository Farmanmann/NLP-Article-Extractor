import nltk
import os
from bs4 import BeautifulSoup
import re
from datetime import datetime

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

# Define base directories
articles_texts_base_dir = 'article_texts'
formatted_articles_base_dir = 'formatted_articles'

# Get today's date to locate and save in the correct folder
current_date = datetime.now().strftime("%Y-%m-%d")
articles_texts_dir = os.path.join(articles_texts_base_dir, current_date)
formatted_articles_dir = os.path.join(formatted_articles_base_dir, current_date)

# Create directory for formatted articles if it doesn't exist
if not os.path.exists(formatted_articles_dir):
    os.makedirs(formatted_articles_dir)

# Process each text file in the articles_texts directory
for filename in os.listdir(articles_texts_dir):
    if filename.endswith('.txt'):
        print(f"Processing {filename}")
        
        # Read article text file
        text_path = os.path.join(articles_texts_dir, filename)
        with open(text_path, 'r', encoding='utf-8') as f:
            article_text = f.read()
        
        # Segment and format text
        formatted_text = segment_and_format_text(article_text)
        
        # Save the formatted text to the formatted_articles directory
        formatted_filename = filename.replace('.txt', '_formatted.txt')
        formatted_text_path = os.path.join(formatted_articles_dir, formatted_filename)
        
        with open(formatted_text_path, 'w', encoding='utf-8') as f:
            f.write(formatted_text)

print(f"Text formatting complete! Files saved in: {formatted_articles_dir}")

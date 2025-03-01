import nltk
import os
import re
from datetime import datetime

# Ensure necessary NLTK tokenizer is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def clean_text(text):
    """Remove extra whitespace and keep only Persian/Arabic characters and punctuation."""
    text = ' '.join(text.split())  # Remove extra spaces
    text = re.sub(r'[^\u0600-\u06FF\s.,!?؟،]+', ' ', text)  # Keep Persian/Arabic + punctuation
    return text.strip()

def segment_and_format_text(text):
    """Tokenizes text into sentences and cleans each one."""
    sentences = nltk.sent_tokenize(text)
    formatted_sentences = [clean_text(sentence) for sentence in sentences if clean_text(sentence)]
    return '\n'.join(formatted_sentences)

# Base directories
articles_base_dir = 'articles'        # Source: Raw extracted text
formatted_base_dir = 'article_texts'  # Destination: Processed & formatted text

# Get today's date for correct directory usage
current_date = datetime.now().strftime("%Y-%m-%d")
articles_dir = os.path.join(articles_base_dir, current_date)
formatted_dir = os.path.join(formatted_base_dir, current_date)

# Ensure output directory exists
os.makedirs(formatted_dir, exist_ok=True)

# Process each text file in today's articles directory
if os.path.exists(articles_dir):
    for filename in os.listdir(articles_dir):
        if filename.endswith('.txt'):
            print(f"📄 Processing {filename}...")

            # Read original text
            text_path = os.path.join(articles_dir, filename)
            with open(text_path, 'r', encoding='utf-8') as f:
                article_text = f.read().strip()
            
            # Skip empty files
            if not article_text:
                print(f"⚠️ Skipping {filename} (empty file).")
                continue

            # Process and format text
            formatted_text = segment_and_format_text(article_text)
            
            # Skip saving empty formatted text
            if not formatted_text:
                print(f"⚠️ No meaningful text extracted from {filename}, skipping.")
                continue
            
            # Save to formatted directory
            formatted_filename = filename.replace('.txt', '_formatted.txt')
            formatted_text_path = os.path.join(formatted_dir, formatted_filename)
            
            with open(formatted_text_path, 'w', encoding='utf-8') as f:
                f.write(formatted_text)

    print(f"✅ Text formatting complete! Files saved in: {formatted_dir}")
else:
    print(f"⚠️ No text files found in {articles_dir}. Check your extracted articles.")

from bs4 import BeautifulSoup
import os

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

# Process all downloaded articles
articles_dir = 'articles'
text_dir = 'article_texts'

# Create text directory if it doesn't exist
if not os.path.exists(text_dir):
    os.makedirs(text_dir)

# Process each HTML file
for filename in os.listdir(articles_dir):
    if filename.endswith('.html'):
        print(f"Processing {filename}")
        
        # Read HTML file
        with open(os.path.join(articles_dir, filename), 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extract and clean text
        article_text = extract_article_content(html_content)
        
        # Save text to new file
        text_filename = filename.replace('.html', '.txt')
        with open(os.path.join(text_dir, text_filename), 'w', encoding='utf-8') as f:
            f.write(article_text)

print("Text extraction complete!")
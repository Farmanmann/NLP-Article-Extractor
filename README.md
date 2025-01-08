# VOA Dari Web Scraper

A Python-based web scraping project for extracting and processing articles from darivoa.com. The project includes tools for downloading articles, extracting clean text content, and formatting text with proper handling of Persian/Arabic text.

## Project Structure

The project consists of three main scripts:
- `articleDownloader.py`: Downloads article HTML from the website
- `textExtracter.py`: Extracts clean text content from HTML files
- `format_text.py`: Formats and segments the extracted text

## Setup

### Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Requirements
Create a `requirements.txt` file with the following dependencies:
```
beautifulsoup4==4.12.3
nltk==3.8.1
requests==2.31.0
```

## Component Details

### Article Downloader
`articleDownloader.py` handles the initial web scraping:
- Creates 'articles' directory if it doesn't exist
- Collects unique article URLs from darivoa.com
- Downloads HTML content for each article
- Saves files with UTF-8 encoding for Persian text
- Includes error handling and request delays
- Shows download progress
- Names files using article IDs

### Text Extractor
`textExtracter.py` processes the downloaded HTML:
- Creates 'article_texts' directory for cleaned content
- Processes HTML files from 'articles' directory
- Removes unwanted elements (scripts, styles, nav menus)
- Extracts text from relevant HTML tags
- Cleans whitespace and formatting
- Saves cleaned text to separate files

### Text Formatter
`format_text.py` provides final text processing:
- Uses NLTK for sentence segmentation
- Preserves Persian/Arabic characters (Unicode range \u0600-\u06FF)
- Maintains punctuation in both English and Persian
- Removes unwanted special characters
- Formats text with one sentence per line
- Preserves proper spacing and formatting

## Usage

1. Set up the virtual environment and install requirements
2. Run the scripts in sequence:
```bash
python articleDownloader.py
python textExtracter.py
python format_text.py
```

## Output Structure
```
project/
├── articles/                 # Raw HTML files
│   └── article_[ID].html
├── article_texts/           # Extracted text content
│   └── article_[ID].txt
└── formatted_texts/         # Final formatted text
    └── article_[ID]_formatted.txt
```

## Important Notes
- The scripts include delays between requests to avoid overwhelming the server
- All text is processed with UTF-8 encoding for proper Persian text handling
- The NLTK library will download required data on first run
- Make sure you have proper permissions to create directories and files

# VOA Dari Web Scraper

A Python-based web scraping project for extracting and processing articles from darivoa.com. The project includes tools for downloading articles, extracting clean text content, and formatting text with proper handling of Persian/Arabic text.

## Project Structure

The project consists of four main scripts:
- `articleDownloader.py`: Downloads article HTML from the given list
- `textExtracter.py`: Extracts clean text content from HTML files
- `format_text.py`: Formats and segments the extracted text
- `wayback_fetcher.py`: (Debugging tool) Used to check the availability of Wayback Machine snapshots without downloading them

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

## Component Details

### Article Downloader
`articleDownloader.py` Downloads the archived HTML from the wayback machine
- Creates 'downloaded_html/date' directory to store raw HTML files
- Iterates over snapshot URLs from wayback_fetcher.py
- Downloads each HTML file, retrying up to 3 times if there are connection issues
- Saves each file in UTF-8 encoding for Persian text
- Logs successful and failed downloads
- Implements timeouts and delays to prevent server overload

### Text Extractor
`textExtracter.py` processes the downloaded HTML:
- Creates 'article_texts' directory for cleaned content
- Processes HTML files from 'downloaded_html/date' directory
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

### Wayback Machine Fetcher
`wayback_fetcher.py` Queries the wayback machine for availible snapshots
- Queries Wayback Machine for archived URLs.
- Lists found snapshots and their HTTP status codes.
- Does NOT download any files (for debugging purposes only).

## Usage

1. Set up the virtual environment and install requirements
2. Run the scripts in sequence:
```bash
python wayback_fetcher.py    # Fetches available snapshots
python articleDownloader.py  # Downloads HTML from wayback machine
python textExtracter.py      # Extracts clean article text
python format_text.py        # Formats the extracted text
```

## Output Structure
```
NLP-Article-Extractor/
├── downloaded_html/    # Raw HTML files from Wayback Machine
│   └── YYYY-MM-DD/
│       └── article_timestamp.html
├── articles/           # Extracted clean text from HTML
│   └── YYYY-MM-DD/
│       └── article_timestamp.txt
├── article_texts/      # Fully formatted and segmented text
│   └── YYYY-MM-DD/
│       └── article_timestamp_formatted.txt
└── scripts/            # Python scripts for each processing step
```

## Features and Enhancements
- Wayback Machine Support: Fetches and downloads archived versions of articles.
- Filters only HTTP 200 snapshots to avoid broken downloads.
- Error Handling: Implements retry logic for failed downloads.
- Batch Processing: Organizes files by date for efficient storage and access.
- Persian/Arabic Text Processing: Ensures proper text extraction and formatting.

## Important Notes
- The scripts include delays between requests to avoid overwhelming the server.
- All text is processed with UTF-8 encoding for proper Persian text handling.
- The NLTK library will download required data on first run.
- Ensure you have proper permissions to create directories and files.

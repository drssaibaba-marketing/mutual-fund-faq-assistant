import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from datetime import datetime
import time

# 2.1 URL Curation
URLS = [
    {"url": "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth", "name": "HDFC Mid-Cap Opportunities Fund"},
    {"url": "https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth", "name": "HDFC Small Cap Fund"},
    {"url": "https://groww.in/mutual-funds/hdfc-gold-etf-fund-of-fund-direct-plan-growth", "name": "HDFC Gold ETF Fund of Fund"},
    {"url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth", "name": "HDFC Top 100 Fund"},
    {"url": "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth", "name": "HDFC ELSS Tax Saver Fund"}
]

# 2.2 Web Scraping Module
def scrape_url(url):
    """Scrapes the text content from the given URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script, style, header, footer, nav elements to get cleaner text
        for script in soup(["script", "style", "header", "footer", "nav", "noscript"]):
            script.extract()
            
        # Get text and clean it up
        text = soup.get_text(separator=' ', strip=True)
        # Basic cleanup for excessive whitespaces
        text = ' '.join(text.split())
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def load_and_chunk_data():
    """Scrapes data, chunks it, and adds metadata."""
    documents = []
    
    # 2.3 Text Chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    for item in URLS:
        print(f"Scraping: {item['name']} from {item['url']}")
        text = scrape_url(item['url'])
        
        if text:
            chunks = text_splitter.split_text(text)
            
            # 2.4 Metadata Tagging
            for chunk in chunks:
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source_url": item['url'],
                        "scheme_name": item['name'],
                        "last_updated": current_date
                    }
                )
                documents.append(doc)
        time.sleep(1) # Be polite to the server
                
    print(f"Total chunks created: {len(documents)}")
    return documents

if __name__ == "__main__":
    docs = load_and_chunk_data()
    if docs:
        print(f"Sample chunk:\n{docs[0].page_content[:200]}...\nMetadata: {docs[0].metadata}")

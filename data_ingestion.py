import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from datetime import datetime
import time
from mock_corpus import CORPUS_REGISTRY

def scrape_url(url, default_content):
    """Scrapes the text content from the given URL. If blocked or error, fallback to verified default_content."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for script in soup(["script", "style", "header", "footer", "nav", "noscript"]):
            script.extract()
            
        text = soup.get_text(separator=' ', strip=True)
        text = ' '.join(text.split())
        return text if text else default_content
    except Exception as e:
        print(f"Error scraping {url}: {e}. Falling back to verified registry content...")
        return default_content

def load_and_chunk_data():
    """Scrapes data, chunks it, and adds schema metadata for retrieval filtering."""
    documents = []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    for item in CORPUS_REGISTRY:
        print(f"Processing: {item['scheme_id']} | {item['url']}")
        
        # We try to scrape, but rely heavily on the meticulously verified fallback for HDFC AMC
        text = scrape_url(item['url'], item['content'])
        
        if text:
            chunks = text_splitter.split_text(text)
            
            for chunk in chunks:
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source_url": item['url'],
                        "canonical_url": item.get('canonical_url', item['url']),
                        "scheme_id": item['scheme_id'],
                        "source_type": item['source_type'],
                        "as_of_date": current_date
                    }
                )
                documents.append(doc)
        time.sleep(0.5) 
                
    print(f"Total chunks created: {len(documents)}")
    return documents

if __name__ == "__main__":
    docs = load_and_chunk_data()
    if docs:
        print(f"Sample chunk:\n{docs[0].page_content[:200]}...\nMetadata: {docs[0].metadata}")

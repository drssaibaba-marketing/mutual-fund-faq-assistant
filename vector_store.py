import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from data_ingestion import load_and_chunk_data

# Vector Database directory
DB_DIR = "./chroma_db_v8"

# 3.1 Embedding Model Integration & 3.2 Vector DB Initialization
def get_vector_store():
    """Initializes and returns the Chroma vector store with embeddings."""
    # Using a free, high-quality local embedding model
    print("Initializing embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
        print("Loading existing vector database...")
        vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    else:
        print("Vector database not found. Starting data ingestion...")
        # 3.3 Data Indexing
        docs = load_and_chunk_data()
        if not docs:
            raise ValueError("No documents were loaded. Check the data ingestion pipeline.")
            
        print("Indexing documents into Chroma vector database...")
        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=DB_DIR
        )
        print("Indexing complete.")
        
    return vectorstore

if __name__ == "__main__":
    vs = get_vector_store()
    
    # 3.4 Retrieval Testing (Sanity Check)
    print("\n--- Running Sanity Check Retrieval ---")
    queries = [
        "What is the expense ratio?",
        "What is the exit load?",
        "minimum sip amount"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = vs.similarity_search(query, k=2)
        
        for i, res in enumerate(results):
            print(f"  Result {i+1} [Source: {res.metadata.get('scheme_name')}]:")
            content_preview = res.page_content.replace('\n', ' ')[:150]
            # Handle unicode characters like the Rupee symbol for Windows console printing
            safe_preview = content_preview.encode('ascii', 'ignore').decode('ascii')
            print(f"    {safe_preview}...")

# Mutual Fund FAQ Assistant

A facts-only, RAG-based (Retrieval-Augmented Generation) Chatbot designed to answer objective, verifiable queries about specific HDFC Mutual Fund schemes. The assistant strictly adheres to factual responses based on official sources and gracefully refuses any requests for investment advice.

## 🏢 Selected AMC & Schemes

**Asset Management Company (AMC):** HDFC Mutual Fund

**Selected Schemes:**
1. HDFC Mid-Cap Opportunities Fund
2. HDFC Small Cap Fund
3. HDFC Gold ETF Fund of Fund
4. HDFC Top 100 Fund (Large Cap)
5. HDFC ELSS Tax Saver Fund

*(Note: Data is sourced using Groww links as proxy reference points to ensure reliable scraping, while maintaining factual integrity).*

## 🏗️ Architecture Overview

The project follows a standard Retrieval-Augmented Generation (RAG) architecture:
1. **Data Ingestion (`data_ingestion.py`)**: Scrapes text data from the provided URLs, cleans the HTML, and chunks the content using `RecursiveCharacterTextSplitter`. Metadata (URL, Scheme Name, Date) is appended to each chunk.
2. **Vector Store (`vector_store.py`)**: Uses the `sentence-transformers` library and the `all-MiniLM-L6-v2` HuggingFace embedding model to encode the text chunks and stores them locally in a `Chroma` database.
3. **Guardrails (`guardrails.py`)**: A lightweight regex-based ruleset that intercepts user queries. If advisory/opinionated patterns are detected, it blocks the query and redirects the user to official educational resources.
4. **RAG Pipeline (`rag_pipeline.py`)**: Leverages LangChain and Groq API (`mixtral-8x7b-32768`) with a strict System Prompt. It forces the LLM to use *only* retrieved context, limit responses to 3 sentences, and cite its sources.
5. **User Interface (`app.py`)**: A minimalistic Streamlit application that ties the backend components together into a user-friendly chat interface.

## 🚀 Setup & Run Instructions

### Prerequisites
- Python 3.9+
- A valid [Groq API Key](https://console.groq.com/keys)

### 1. Clone the repository and navigate to the project root
```bash
git clone <repository_url>
cd RAG_Chatbot_Project
```

### 2. Set up the virtual environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install sentence-transformers
```

### 4. Configure Environment Variables
Open the `.env` file in the root directory and add your Groq API Key:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 5. Build the Vector Database
Initialize the Chroma database by running the vector store script (this will scrape the data and generate embeddings locally):
```bash
python vector_store.py
```

### 6. Run the Application
Launch the Streamlit user interface:
```bash
streamlit run app.py
```

## ⚠️ Known Limitations
- **Data Freshness**: The system relies on static scraping at the time of database initialization. To update NAVs or expense ratios, `vector_store.py` (with the `chroma_db` folder deleted) must be re-run.
- **Scraping Protections**: Official AMC websites (like HDFC) often have strict anti-bot measures returning 403 Forbidden. Proxy URLs (like Groww) are used to simulate data ingestion.
- **LLM Hallucinations**: While strict prompts (Temperature=0) heavily mitigate hallucinations, LLMs can occasionally misinterpret context. The mandatory source citation ensures users can verify the facts.
- **Guardrail Bypasses**: The rule-based regex guardrail is extremely fast and effective for common phrases, but it can potentially be bypassed by highly sophisticated or obfuscated advisory prompts.

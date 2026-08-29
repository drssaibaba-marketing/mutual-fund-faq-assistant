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

*(Note: Groww is the selected product context, but all information is sourced exclusively from official HDFC, SEBI, and AMFI pages to ensure factual integrity).*

## 🏗️ Architecture Overview

The project has been refactored into a separated Backend/Frontend architecture:
1. **Frontend (Vanilla HTML/CSS/JS)**: A static frontend mirroring the premium dark mode UI, designed to be deployed instantly on Vercel.
2. **Backend (FastAPI)**: Serves the RAG logic via REST API, designed for deployment on platforms like Railway.
3. **Data Ingestion & Vector Store**: Scrapes canonical text and stores embeddings locally in a `Chroma` database.
4. **Guardrails & RAG Pipeline**: Ensures queries are strictly factual using `qwen/qwen3.8-27b` via Groq.

## 🚀 Setup & Run Instructions

### Prerequisites
- Python 3.9+
- A valid [Groq API Key](https://console.groq.com/keys)

### 1. Clone the repository
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

### 6. Run the Application Locally

**Start the Backend:**
```bash
uvicorn main:app --reload --port 8000
```

**Start the Frontend:**
Open a new terminal, navigate to the `frontend/` folder, and start a local HTTP server:
```bash
cd frontend
python -m http.server 3000
```
Then visit `http://localhost:3000` in your browser.

## ⚠️ Known Limitations
- **Data Freshness**: The system relies on static scraping at the time of database initialization.
- **Scraping Protections**: Official AMC websites (like HDFC) often have strict anti-bot measures returning 403 Forbidden. We simulate data ingestion using verified mock corpus.
- **LLM Hallucinations**: While strict prompts heavily mitigate hallucinations, LLMs can occasionally misinterpret context. 
- **Guardrail Bypasses**: The rule-based regex guardrail is extremely fast and effective for common phrases, but it can potentially be bypassed by highly sophisticated or obfuscated advisory prompts.

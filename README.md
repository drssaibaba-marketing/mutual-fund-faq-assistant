# Mutual Fund FAQ Assistant

A facts-only, RAG-based (Retrieval-Augmented Generation) Chatbot designed to answer objective, verifiable queries about specific HDFC Mutual Fund schemes. 

**Disclaimer:**
> Facts-only. No investment advice.

## 🏢 Selected Product & AMC

- **Selected Product:** Groww
- **Selected AMC:** HDFC Mutual Fund

**Selected Schemes:**
1. HDFC Mid-Cap Opportunities Fund
2. HDFC Small Cap Fund
3. HDFC Gold ETF Fund of Fund
4. HDFC Top 100 Fund (Large Cap)
5. HDFC ELSS Tax Saver Fund

## 🏗️ Architecture Overview

The project is built with a separated Backend/Frontend architecture:
1. **Frontend (Vanilla HTML/CSS/JS)**: A static frontend mirroring the premium dark mode UI.
2. **Backend (FastAPI)**: Serves the RAG logic via REST API, designed for deployment on platforms like Railway.
3. **Data Ingestion & Vector Store**: Scrapes canonical text and stores embeddings locally in a `Chroma` database.
4. **Guardrails & RAG Pipeline**: Ensures queries are strictly factual using LLM capabilities with stringent advisory guardrails.

## 🌐 Public Deployed Prototype URL
- **Backend API:** `https://mutual-fund-faq-assistant-production.up.railway.app/api/chat`
*(Please deploy the `frontend/` statically on Vercel/Netlify or run locally via HTTP server as per instructions below)*

## 📚 Source List
The application exclusively utilizes the following 15 public URLs (Primary and Secondary sources verified for facts):

**HDFC AMC (Primary Sources):**
1. https://www.hdfcfund.com/explore/mutual-funds/hdfc-mid-cap-opportunities-fund
2. https://www.hdfcfund.com/explore/mutual-funds/hdfc-small-cap-fund
3. https://www.hdfcfund.com/explore/mutual-funds/hdfc-gold-etf-fund-of-fund
4. https://www.hdfcfund.com/explore/mutual-funds/hdfc-top-100-fund
5. https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund

**HDFC AMC (Secondary Sources):**
6. https://www.hdfcfund.com/statutory-disclosure/nav-and-idcw
7. https://www.hdfcfund.com/investor-services/download-statements/account-statement
8. https://www.hdfcfund.com/investor-services/download-statements/capital-gains-statement
9. https://www.hdfcfund.com/investor-services/kyc
10. https://www.hdfcfund.com/about-us/corporate-governance
11. https://www.hdfcfund.com/investor-services/downloads/forms

**AMFI / SEBI (Secondary Sources):**
12. https://www.amfiindia.com/
13. https://investor.sebi.gov.in/
14. https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doFaq=yes
15. https://www.sebi.gov.in/legal/master-circulars/may-2023/master-circular-for-mutual-funds_71438.html

## 💬 Sample Q&A

**Q1: What is the expense ratio of HDFC Mid Cap Fund?**
**A1:** The expense ratio for the HDFC Mid-Cap Opportunities Fund Direct plan is 0.85%. [Source](https://www.hdfcfund.com/explore/mutual-funds/hdfc-mid-cap-opportunities-fund/regular)

**Q2: What is the lock-in period of HDFC ELSS Tax Saver Fund?**
**A2:** The lock-in period for the HDFC ELSS Tax Saver Fund is 3 years. [Source](https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/regular)

**Q3: How can I download my capital gains statement?**
**A3:** To download your capital gains statement, visit the HDFC Mutual Fund website and enter your PAN and folio number under the 'Capital Gains Statement' section. You must then select the relevant financial year to generate the PDF. [Source](https://www.hdfcfund.com/investor-services/download-statements/capital-gains-statement)

**Q4: Should I invest in HDFC Mid Cap Fund?**
**A4:** I can only provide factual information about HDFC mutual funds based on approved sources. I cannot provide investment advice or recommendations.

**Q5: What is the minimum SIP amount for HDFC Small Cap Fund?**
**A5:** The minimum SIP amount for the HDFC Small Cap Fund is Rs. 100. [Source](https://www.hdfcfund.com/explore/mutual-funds/hdfc-small-cap-fund/regular)

**Q6: What is the riskometer classification of HDFC Gold ETF Fund of Fund?**
**A6:** The riskometer classification for HDFC Gold ETF Fund of Fund is High. [Source](https://www.hdfcfund.com/explore/mutual-funds/hdfc-gold-etf-fund-of-fund/regular)

## 🚀 Setup & Run Instructions

### Prerequisites
- Python 3.9+
- A valid [Groq API Key](https://console.groq.com/keys)

### 1. Clone the repository
```bash
git clone https://github.com/drssaibaba-marketing/mutual-fund-faq-assistant.git
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

## 🔄 Automated Knowledge Refresh

The knowledge base is automatically refreshed every day at 10:00 AM IST using a GitHub Actions scheduler. The workflow runs the ingestion pipeline to fetch updated NAVs and documents, builds the new ChromaDB vector index, and pushes the updated index to the repository. This guarantees that the live deployed application always has the latest verified data without causing startup delays or facing WAF blocks during production operation.

To run the refresh manually, you can trigger the **Daily RAG Knowledge Base Update** workflow via the GitHub Actions `workflow_dispatch` interface.

## ⚠️ Known Limitations
- **Data Freshness**: The system relies on static scraping at the time of database initialization.
- **Scraping Protections**: Official AMC websites (like HDFC) often have strict anti-bot measures returning 403 Forbidden. We simulate data ingestion using verified mock corpus.
- **LLM Hallucinations**: While strict prompts heavily mitigate hallucinations, LLMs can occasionally misinterpret context. 
- **Guardrail Bypasses**: The rule-based regex guardrail is extremely fast and effective for common phrases, but it can potentially be bypassed by highly sophisticated or obfuscated advisory prompts.

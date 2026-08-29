# Phase-Wise Implementation Plan: Mutual Fund FAQ Assistant

This document outlines the step-by-step implementation plan for building the RAG-based Mutual Fund FAQ Assistant, based on the provided problem statement and architecture.

---

## Phase 1: Project Setup and Environment Configuration
**Goal:** Initialize the repository, set up the development environment, and configure dependencies.

*   **1.1 Repository Initialization:** Create the project directory and initialize version control (Git).
*   **1.2 Environment Setup:** Create a virtual environment (e.g., Python `venv` or `conda`).
*   **1.3 Dependency Installation:** Install required libraries (e.g., `langchain`, `llama-index`, `chromadb` or `pinecone`, `langchain-groq`, `streamlit`, `beautifulsoup4`, `requests`).
*   **1.4 API Keys & Secrets Management:** Set up a `.env` file to securely store API keys for the chosen LLM and Vector DB.

---

## Phase 2: Data Ingestion and Processing Pipeline
**Goal:** Scrape, parse, and structure data from the selected HDFC Mutual Fund sources.

*   **2.1 URL Curation:** Define the list of 5 target HDFC fund URLs.
*   **2.2 Web Scraping Module:** Develop a scraper/loader to extract text content and relevant data (e.g., expense ratios, exit loads) from the official AMC pages.
*   **2.3 Text Chunking:** Implement a chunking strategy (e.g., RecursiveCharacterTextSplitter) to break extracted text into semantically cohesive, manageable chunks.
*   **2.4 Metadata Tagging:** Ensure every chunk is appended with `source_url`, `last_updated`, and `scheme_name`.

---

## Phase 3: Vector Database Setup and Embedding Generation
**Goal:** Convert text chunks into embeddings and store them in a vector database for efficient retrieval.

*   **3.1 Embedding Model Integration:** Connect to the embedding model API (e.g., OpenAI `text-embedding-3-small`).
*   **3.2 Vector DB Initialization:** Set up the chosen Vector Database (e.g., local ChromaDB instance).
*   **3.3 Data Indexing:** Run the ingestion pipeline to embed all document chunks and store them in the Vector DB alongside their metadata.
*   **3.4 Retrieval Testing (Sanity Check):** Perform basic similarity searches to verify that relevant chunks are correctly returned for simple queries.

---

## Phase 4: Retrieval and Generation Pipeline (RAG) Setup
**Goal:** Build the core RAG logic that processes user queries and generates answers using the LLM.

*   **4.1 Query Embedding & Retrieval:** Implement the logic to embed user queries and fetch the top `K` most relevant chunks from the Vector DB.
*   **4.2 Prompt Engineering:** Design a strict system prompt enforcing the constraints:
    *   Use *only* the retrieved context.
    *   Maximum length of 3 sentences.
    *   Include exactly one citation link.
*   **4.3 LLM Integration:** Connect the LLM via Groq API to generate responses based on the prompt.
*   **4.4 Post-Processing:** Format the output to ensure the footer `Last updated from sources: <date>` is appended reliably.

---

## Phase 5: Refusal Handling and Guardrails
**Goal:** Implement mechanisms to detect and reject advisory or non-factual queries.

*   **5.1 Intent Classification:** Implement a lightweight guardrail (using rules, NLP, or an initial fast LLM check) to determine if a query is factual or advisory.
*   **5.2 Refusal Logic:** Create standard polite refusal responses for advisory queries (e.g., "Which is better?", "Should I invest?").
*   **5.3 Educational Redirection:** Append an AMFI or SEBI educational link to the refusal responses.

---

## Phase 6: User Interface Development
**Goal:** Build a minimalistic frontend for users to interact with the assistant.

*   **6.1 UI Framework Setup:** Initialize a Streamlit (or basic React) application.
*   **6.2 Core UI Elements:** Add the welcome message, chat window, and the visible disclaimer: *"Facts-only. No investment advice."*
*   **6.3 Example Questions Integration:** Add 3 clickable pre-defined questions to guide user interactions.
*   **6.4 Pipeline Integration:** Connect the frontend chat window to the backend RAG and Guardrail pipelines.

---

## Phase 7: Testing and Refinement
**Goal:** Validate the system against the success criteria and refine constraints.

*   **7.1 Factual Query Testing:** Test with various data points (expense ratio, minimum SIP, lock-in period) to ensure accurate retrieval and 3-sentence limit compliance.
*   **7.2 Advisory Query Testing:** Attempt to bypass the guardrails with investment advice requests to ensure the Refusal Handler triggers correctly.
*   **7.3 Citation Verification:** Ensure every factual response includes one working source link and the correct footer date.

---

## Phase 8: Final Deliverables and Documentation
**Goal:** Finalize the project and prepare the final outputs.

*   **8.1 README Creation:** Write the `README.md` containing:
    *   Setup and run instructions.
    *   List of selected AMC and schemes.
    *   Architecture overview.
    *   Known limitations.
*   **8.2 Code Cleanup:** Refactor and comment code for readability and maintainability.
*   **8.3 Final Review:** Confirm all constraints from `problemstatment.md` are strictly met.

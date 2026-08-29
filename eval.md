# Evaluation Framework: Mutual Fund FAQ Assistant

This document establishes the evaluation criteria and testing methodology for the RAG-based FAQ Assistant, aligning with the requirements in [implementation-plan.md](file:///d:/GenAITrg-NEXTLEAP/RAG_Chatbot_Project/implementation-plan.md). 

---

## 1. RAG Evaluation Metrics (RAGAS Framework)

To ensure the accuracy and reliability of the assistant, we will evaluate both the **Retrieval** and **Generation** components using standard RAG evaluation methodologies.

### A. Retrieval Evaluation
* **Context Relevance (Precision):** Measures how relevant the retrieved chunks are to the user's query. High relevance means the Vector DB is not fetching useless information.
* **Context Recall:** Measures if all the necessary information to answer the query was successfully retrieved. If the answer exists in the ingested documents but isn't retrieved, recall is low.

### B. Generation Evaluation
* **Faithfulness (No Hallucinations):** Measures whether the generated answer is strictly derived from the retrieved context. If the LLM brings in outside knowledge, this score fails.
* **Answer Relevance:** Measures how directly the generated answer addresses the user's query, avoiding generic or evasive responses.

---

## 2. System Constraint Evaluation (Pass/Fail)

These are strict business rules that the LLM must follow 100% of the time. We will use a suite of test queries to verify these constraints.

| Constraint | Evaluation Criteria | Testing Method |
| :--- | :--- | :--- |
| **Facts-Only Refusal** | Does the system refuse advisory queries (e.g., "Should I buy?")? | Submit 10 advisory queries. 100% must trigger the Refusal Handler. |
| **Conciseness** | Is the response 3 sentences or fewer? | Submit 20 factual queries. Programmatically count sentences in the output. |
| **Citation Requirement** | Does the response include exactly one valid source link? | Check if a valid URL from the `source_url` metadata is present in the response. |
| **Footer Inclusion** | Is the `"Last updated from sources: <date>"` footer present? | String matching on the final output string. |

---

## 3. Test Query Dataset

A curated dataset of queries should be used to baseline and continuously evaluate the model.

### 3.1 Factual Queries (Expected: Accurate Answer)
1. "What is the exit load for the HDFC Mid-Cap Opportunities Fund?"
2. "What is the benchmark index for the HDFC Small Cap Fund?"
3. "What is the minimum SIP amount for the HDFC ELSS Tax Saver Fund?"
4. "How long is the lock-in period for the ELSS fund?"
5. "What is the riskometer classification for the HDFC Gold ETF Fund of Fund?"

### 3.2 Advisory / Rule-Breaking Queries (Expected: Refusal)
1. "Is HDFC Top 100 a good investment for my retirement?"
2. "Which fund should I choose between HDFC Small Cap and Mid Cap?"
3. "Can you compare the historical returns of these funds?"
4. "What is your opinion on investing in Gold ETFs right now?"
5. "I have 1 lakh rupees, where should I invest it?"

### 3.3 Edge Case Queries (Expected: Graceful Handling)
1. "What is the expense ratio for the SBI Magnum Midcap Fund?" *(Expected: "I do not have this information.")*
2. "Tell me about the exit load." *(Expected: Ask for clarification on which fund, or list exit loads briefly if within constraints.)*

---

## 4. Human-in-the-Loop (HITL) Validation

While programmatic evaluation is crucial for speed, human review is required for nuance.

* **Blind Testing:** Reviewers are presented with the user query, retrieved context, and generated answer. They must blindly rate:
  1. Did the system follow the constraints?
  2. Is the tone neutral and non-advisory?
  3. Is the grammar and formatting correct?
* **Citation Verification:** A human reviewer must periodically click the generated citation links to ensure they are not dead links and actually lead to the correct AMC/SEBI/AMFI page.

---

## 5. Performance Metrics
* **End-to-End Latency:** Time taken from the user hitting "Send" to the final response rendering on the UI. Target: `< 3 seconds` (leveraging Groq's fast inference).
* **API Error Rate:** Tracking timeouts, rate limits, or 500 errors from the Groq API or Vector Database. Target: `< 1%`.

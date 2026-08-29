# Problem Statement: Mutual Fund FAQ Assistant (Facts-Only Q&A)

## Overview
The objective of this project is to build a facts-only FAQ assistant for mutual fund schemes, using Groww as the reference product context. The assistant will answer objective, verifiable queries related to mutual funds by retrieving information exclusively from official public sources, such as AMC (Asset Management Company) websites, AMFI, and SEBI.

The system must strictly avoid providing investment advice, opinions, or recommendations. Every response must include a single, clear source link and adhere to defined constraints around clarity, accuracy, and compliance.

---

## Objective
Design and implement a lightweight Retrieval-Augmented Generation (RAG)-based assistant that:
* Answers factual queries about mutual fund schemes supported by available data
* Uses Groww purely as the selected product/reference context for the project
* Uses a curated corpus of official documents (HDFC AMC, SEBI, AMFI) as the absolute sources of truth
* Provides concise, source-backed responses
* Cites exactly one official source containing/supporting the fact

---

## Target Users
* Retail investors comparing mutual fund schemes
* Customer support and content teams handling repetitive mutual fund queries

---

## Scope of Work

### 1. Corpus Definition
* Select one Asset Management Company (AMC)
* Choose 3–5 mutual fund schemes, ensuring category diversity (e.g., large-cap, flexi-cap, ELSS)
  * HDFC Mid-Cap Opportunities Fund
  * HDFC Small Cap Fund
  * HDFC Gold ETF Fund of Fund
  * HDFC Top 100 Fund (Large Cap)
  * HDFC ELSS Tax Saver Fund

### 2. FAQ Assistant Requirements
The assistant must answer **any factual scheme-specific question supported by the approved corpus**. The following categories are mandatory acceptance tests, but they are NOT a whitelist:
* Expense ratio of a scheme
* Exit load details
* Minimum SIP / investment amount
* ELSS lock-in period
* Riskometer classification
* Benchmark index
* Process to download statements or capital gains reports
* NAV and AUM
* Fund Manager and Investment Objective

Ensure:
* Each response is purely factual and limited to a maximum of 3 sentences
* Each response includes exactly one clearly identified official source citation link
* For dynamic facts (such as NAV), the date of the fact is identified in the response
* Each response includes a footer: _“Last updated from sources: <date>”_

### 3. Refusal Handling
The assistant must refuse non-factual or advisory queries, such as:
* “Should I invest in this fund?”
* “Which fund is better?”

Refusal responses should:
* Be polite and clearly worded
* Reinforce the facts-only limitation
* Provide a relevant educational link (e.g., AMFI or SEBI resource)

### 4. User Interface (Minimal)
The solution should include a simple interface with:
* A welcome message
* Three example questions
* A visible disclaimer: _“Facts-only. No investment advice.”_

---

## Constraints

### Data and Sources
* Groww is the selected product/reference context, but must NOT be used as an information source
* HDFC AMC, AMFI, and SEBI must be the only authoritative sources
* Do not use unrelated third-party websites
* Never invent information (hallucinate)

### Privacy and Security
* Do not collect, store, or process:
  * PAN or Aadhaar numbers
  * Account numbers
  * OTPs
  * Email addresses or phone numbers

### Content Restrictions
* No investment advice or recommendations
* No performance comparisons or return calculations
* For performance-related queries, provide a link to the official factsheet only

### Transparency
* Responses must be short, factual, and verifiable
* Every answer must include a single official source link
* Dates must be specified for dynamic facts (like NAV)

---

## Expected Deliverables

1. **README Document**
   * Setup instructions
   * Selected AMC and schemes
   * Architecture overview (RAG approach)
   * Known limitations
2. **Disclaimer Snippet**
   * _“Facts-only. No investment advice.”_

---

## Success Criteria
* Accurate retrieval of factual mutual fund information
* Strict adherence to facts-only responses
* Consistent inclusion of valid source citations
* Proper refusal of advisory queries
* Clean, minimal, and user-friendly interface

---

## Summary
The goal is to build a trustworthy, transparent, and compliant mutual fund FAQ assistant that prioritizes accuracy over intelligence. The system should ensure that users receive only verified, source-backed financial information, without any advisory bias or speculative content.

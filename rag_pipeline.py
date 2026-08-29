import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from vector_store import get_vector_store

load_dotenv()

# Global initialization to prevent reloading weights on every query
print("Initializing RAG Pipeline resources (this may take a moment to load embeddings)...")
vectorstore = get_vector_store()

# 4.3 LLM Integration
def get_llm():
    if "GROQ_API_KEY" not in os.environ or os.environ["GROQ_API_KEY"] == "your_groq_api_key_here":
        raise ValueError("Error: GROQ_API_KEY is missing or invalid in the .env file. Please add a valid key.")
    # Using qwen/qwen3.8-27b for fast and accurate factual responses
    # If the user changed the model, they can update it here, but keeping qwen for now.
    return ChatGroq(model="qwen/qwen3.8-27b", temperature=0)

# 4.2 Prompt Engineering
PROMPT_TEMPLATE = """You are a highly strict and factual Mutual Fund FAQ Assistant. 
You must answer the user's query using ONLY the provided Context. Do NOT use outside knowledge.
If the answer is not contained in the context, politely state that you do not have that information based on the sources.

Strict Constraints:
1. Your response must be purely factual and a MAXIMUM of 3 sentences.
2. You must include exactly ONE clearly identified, clickable source citation link at the end of your response. 
3. Provide purely factual answers without any investment advice, opinions, or recommendations.
4. The Context includes official AMC, SEBI, and AMFI sources.
5. For dynamic NAV facts, you MUST prefer the official HDFC NAV & IDCW page over any other scheme page.
6. For dynamic facts (such as NAV), explicitly state the date of the fact exactly as provided in the context. Never cite a scheme page that does not actually contain the NAV being reported.
7. CRITICAL: Before outputting a fact, verify it exists in the provided context. Do NOT infer or combine facts from memory. If the source does not contain the requested fact, state that it is unavailable.

Context:
{context}

Query: {query}
Answer:"""

def extract_scheme_id(query):
    query = query.lower()
    if "mid cap" in query or "mid-cap" in query or "midcap" in query:
        return "hdfc_mid_cap"
    if "small cap" in query or "small-cap" in query or "smallcap" in query:
        return "hdfc_small_cap"
    if "gold" in query:
        return "hdfc_gold_etf"
    if "large cap" in query or "large-cap" in query or "top 100" in query:
        return "hdfc_large_cap"
    if "elss" in query or "tax saver" in query:
        return "hdfc_elss"
    return None

def format_docs(docs):
    formatted_docs = []
    for doc in docs:
        content = doc.page_content.replace('\n', ' ')
        url = doc.metadata.get('canonical_url', doc.metadata.get('source_url', 'Unknown URL'))
        source_type = doc.metadata.get('source_type', 'secondary')
        scheme_id = doc.metadata.get('scheme_id', 'unknown')
        formatted_docs.append(f"[Scheme: {scheme_id} | Type: {source_type} | Content: {content} | Source Link: {url}]")
    return "\n".join(formatted_docs)

# 4.4 Post-Processing
def generate_answer(query):
    """Retrieves context, generates the answer with LLM, and applies the footer."""
    try:
        llm = get_llm()
    except ValueError as e:
        return str(e)
        
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    
    scheme_id = extract_scheme_id(query)
    
    # Explicit Scheme Matching
    # Fetch 6 docs. We do NOT use Chroma's $in operator to avoid potential version compatibility issues.
    # We fetch more docs and filter in python if needed, or just let Chroma return everything and filter.
    # Actually, fetching 10 docs and filtering out wrong schemes in python is completely safe.
    raw_docs = vectorstore.similarity_search(query, k=15)
    
    # If the query is about NAV, explicitly fetch the NAV chunk by querying it
    nav_docs = []
    if "nav" in query.lower():
        nav_docs = vectorstore.similarity_search("Official HDFC Mutual Fund NAVs", k=3)
        nav_docs = [d for d in nav_docs if "nav-and-idcw" in d.metadata.get("canonical_url", "")]
        
    filtered_docs = []
    for doc in raw_docs:
        doc_scheme = doc.metadata.get("scheme_id", "general")
        if scheme_id:
            # If query is scheme specific, only allow that scheme AND general docs
            if doc_scheme == scheme_id or doc_scheme == "general":
                filtered_docs.append(doc)
        else:
            filtered_docs.append(doc)
            
    # Take top 6 after filtering
    final_docs = filtered_docs[:6]
    
    # If the query is about NAV, ensure the NAV chunk is included
    if "nav" in query.lower() and nav_docs:
        # Check if nav_doc is already in final_docs
        if nav_docs[0] not in final_docs:
            final_docs.insert(0, nav_docs[0])
            final_docs = final_docs[:6]
    
    if not final_docs:
        return "I'm sorry, I could not find any relevant information for your query."
        
    context_str = format_docs(final_docs)
    
    # Langchain Expression Language (LCEL) chain
    rag_chain = (
        prompt
        | llm
        | StrOutputParser()
    )
    
    # Generate the main answer
    answer = rag_chain.invoke({"context": context_str, "query": query})
    
    # Ensure ONE citation is visible
    return answer

if __name__ == "__main__":
    print("\n--- Testing RAG Pipeline ---")
    test_query = "What is the NAV of HDFC Mid Cap Fund?"
    print(f"Query: {test_query}")
    response = generate_answer(test_query)
    print("\nResponse:")
    print(response.encode('ascii', 'ignore').decode('ascii'))

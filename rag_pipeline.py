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
# 4.1 Query Embedding & Retrieval
# Retrieve top 3 most relevant chunks
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 4.3 LLM Integration
def get_llm():
    if "GROQ_API_KEY" not in os.environ or os.environ["GROQ_API_KEY"] == "your_groq_api_key_here":
        raise ValueError("Error: GROQ_API_KEY is missing or invalid in the .env file. Please add a valid key.")
    # Using Llama 3.1 for fast and accurate factual responses
    return ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# 4.2 Prompt Engineering
PROMPT_TEMPLATE = """You are a highly strict and factual Mutual Fund FAQ Assistant. 
You must answer the user's query using ONLY the provided Context. Do NOT use outside knowledge.
If the answer is not contained in the context, politely state that you do not have that information based on the sources.

Strict Constraints:
1. Your response must be a MAXIMUM of 3 sentences.
2. You must include exactly one source citation link from the context at the end of your response.
3. Provide purely factual answers without any investment advice, opinions, or recommendations.

Context:
{context}

Query: {query}
Answer:"""

def format_docs(docs):
    formatted_docs = []
    for doc in docs:
        content = doc.page_content.replace('\n', ' ')
        url = doc.metadata.get('source_url', 'Unknown URL')
        formatted_docs.append(f"[Content: {content} | Source Link: {url}]")
    return "\n".join(formatted_docs)

# 4.4 Post-Processing
def generate_answer(query):
    """Retrieves context, generates the answer with LLM, and applies the footer."""
    try:
        llm = get_llm()
    except ValueError as e:
        return str(e)
        
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    
    # Langchain Expression Language (LCEL) chain
    rag_chain = (
        {"context": retriever | format_docs, "query": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Retrieve documents to extract metadata for the footer
    docs = retriever.invoke(query)
    if not docs:
        return "I'm sorry, I could not find any relevant information for your query."
        
    last_updated = docs[0].metadata.get("last_updated", "Unknown Date")
    
    # Generate the main answer
    answer = rag_chain.invoke(query)
    
    # Enforce footer format
    footer = f"\n\nLast updated from sources: {last_updated}"
    
    return answer + footer

if __name__ == "__main__":
    print("\n--- Testing RAG Pipeline ---")
    test_query = "What is the exit load for HDFC Mid-Cap Opportunities Fund?"
    print(f"Query: {test_query}")
    response = generate_answer(test_query)
    print("\nResponse:")
    print(response.encode('ascii', 'ignore').decode('ascii'))

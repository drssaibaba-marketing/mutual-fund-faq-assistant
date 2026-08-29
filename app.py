import streamlit as st
from guardrails import handle_query_guardrails
from rag_pipeline import generate_answer
import os

# 6.1 UI Framework Setup
st.set_page_config(page_title="Mutual Fund FAQ Assistant", page_icon="📈", layout="centered")

# 6.2 Core UI Elements
st.title("📈 Mutual Fund FAQ Assistant")
st.markdown("**Disclaimer:** *Facts-only. No investment advice.*")

st.markdown(
    "Welcome! I can answer factual questions about select HDFC Mutual Fund schemes. "
    "Please note that I cannot provide performance comparisons, recommendations, or financial advice."
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6.3 Example Questions Integration
st.markdown("### Example Questions")
# Create columns for buttons
col1, col2, col3 = st.columns(3)

# Handle button clicks by saving the selected question to session state
if col1.button("Expense ratio of Mid-Cap?"):
    st.session_state.example_q = "What is the expense ratio for HDFC Mid-Cap Opportunities Fund?"
if col2.button("Minimum SIP for Tax Saver?"):
    st.session_state.example_q = "What is the minimum SIP amount for HDFC ELSS Tax Saver Fund?"
if col3.button("Exit load of Small Cap?"):
    st.session_state.example_q = "What is the exit load of HDFC Small Cap Fund?"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6.4 Pipeline Integration
# Get prompt from either the chat input or the example question buttons
prompt = st.chat_input("Ask a factual question about the mutual funds...")
if "example_q" in st.session_state:
    prompt = st.session_state.example_q
    del st.session_state.example_q

if prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Searching official sources..."):
            # Check if GROQ_API_KEY is missing before doing anything
            if "GROQ_API_KEY" not in os.environ or os.environ["GROQ_API_KEY"] == "your_groq_api_key_here":
                response = "⚠️ **Configuration Error**: `GROQ_API_KEY` is not set in the `.env` file. Please configure it to use this assistant."
            else:
                # 1. Check Guardrails
                refusal = handle_query_guardrails(prompt)
                if refusal:
                    response = refusal
                else:
                    # 2. Fetch RAG response
                    try:
                        response = generate_answer(prompt)
                    except Exception as e:
                        response = f"An error occurred: {str(e)}"
            
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

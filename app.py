import streamlit as st
from guardrails import handle_query_guardrails
from rag_pipeline import generate_answer
import os

# 6.1 UI Framework Setup
st.set_page_config(page_title="Mutual Fund FAQ Assistant", page_icon="📈", layout="centered")

# Custom CSS for Premium Dark Mode UI
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Outfit', sans-serif;
}

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    color: #f1f5f9;
}

/* Header typography */
h1 {
    font-weight: 700 !important;
    background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

h2, h3 {
    font-weight: 600 !important;
    color: #e2e8f0 !important;
}

/* Disclaimer text */
.stMarkdown p > strong {
    color: #f87171 !important;
}

/* Chat Messages container */
[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(12px);
}

/* Chat text readability */
[data-testid="stChatMessage"] .stMarkdown,
[data-testid="stChatMessage"] .stMarkdown p {
    color: #f8fafc !important;
    font-size: 1rem;
    line-height: 1.6;
}

/* Secondary text and timestamps */
[data-testid="stChatMessage"] [data-testid="stCaptionContainer"],
[data-testid="stChatMessage"] small,
.stMarkdown small {
    color: #cbd5e1 !important;
    font-size: 0.85rem !important;
}

/* Links (e.g., Source links) */
[data-testid="stChatMessage"] a, .stMarkdown a {
    color: #38bdf8 !important;
    text-decoration: none !important;
    font-weight: 500 !important;
    border-bottom: 1px solid rgba(56, 189, 248, 0.3);
    transition: all 0.2s ease;
}

[data-testid="stChatMessage"] a:hover, .stMarkdown a:hover {
    color: #bae6fd !important;
    border-bottom: 1px solid #bae6fd;
}

/* Buttons */
.stButton > button {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 20px !important;
    color: #f8fafc !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(5px) !important;
    width: 100%;
}

.stButton > button:hover {
    background: rgba(56, 189, 248, 0.15) !important;
    border-color: #38bdf8 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2) !important;
    color: #ffffff !important;
}

/* Chat Input Container */
[data-testid="stChatInput"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 16px !important;
}

/* Force transparent background on inner text areas/inputs and set text color */
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] input {
    background-color: transparent !important;
    color: #1e293b !important;
    -webkit-text-fill-color: #1e293b !important;
    caret-color: #1e293b !important;
}
[data-testid="stChatInput"] div[data-baseweb] {
    background-color: #f1f5f9 !important;
    border-radius: 12px;
}

/* Increase placeholder visibility */
[data-testid="stChatInput"] textarea::placeholder,
[data-testid="stChatInput"] input::placeholder {
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
    opacity: 1 !important;
}

/* Ensure send button is clearly visible */
[data-testid="stChatInput"] button svg {
    fill: #1e293b !important;
    color: #1e293b !important;
}

/* Custom Spinner */
.stSpinner > div > div {
    border-color: #38bdf8 transparent transparent transparent !important;
}
</style>
""", unsafe_allow_html=True)

# 6.2 Core UI Elements
st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <svg width="45" height="45" viewBox="0 0 45 45" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 15px;">
            <rect width="45" height="45" rx="10" fill="rgba(56, 189, 248, 0.1)"/>
            <path d="M12 30L20 22L26 28L34 16" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M28 16H34V22" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1 style="margin: 0; padding: 0;">Mutual Fund FAQ Assistant</h1>
    </div>
""", unsafe_allow_html=True)
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

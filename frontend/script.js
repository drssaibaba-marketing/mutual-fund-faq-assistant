const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://127.0.0.1:8000/api/chat' 
    : 'https://' + window.location.hostname.replace('frontend', 'backend') + '/api/chat'; // Change this placeholder with actual production backend URL once deployed on Railway

// Configure marked.js options for security and styling
marked.setOptions({
    breaks: true, // translate newlines to <br>
});

const chatContainer = document.getElementById('chat-container');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

let chatHistory = [];

function setQuery(query) {
    chatInput.value = query;
    chatInput.focus();
}

function appendMessage(role, content) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message ${role}`;
    
    let avatarContent = role === 'user' ? 'U' : 'AI';
    let avatarClass = role === 'user' ? 'user-avatar' : 'assistant-avatar';
    
    // Parse markdown if it's the assistant
    let displayContent = role === 'assistant' ? marked.parse(content) : content;
    // For user, escape HTML to prevent XSS
    if (role === 'user') {
        const temp = document.createElement('div');
        temp.textContent = displayContent;
        displayContent = temp.innerHTML;
    }
    
    msgDiv.innerHTML = `
        <div class="chat-avatar ${avatarClass}">${avatarContent}</div>
        <div class="chat-content">${displayContent}</div>
    `;
    
    chatContainer.appendChild(msgDiv);
    // Smooth scroll to bottom
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
}

function appendLoading() {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message assistant loading-message`;
    msgDiv.id = 'loading-message';
    
    msgDiv.innerHTML = `
        <div class="chat-avatar assistant-avatar">AI</div>
        <div class="chat-content">
            <div class="loading-indicator">
                <div class="spinner"></div>
                Searching official sources...
            </div>
        </div>
    `;
    
    chatContainer.appendChild(msgDiv);
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
}

function removeLoading() {
    const loadingMsg = document.getElementById('loading-message');
    if (loadingMsg) {
        loadingMsg.remove();
    }
}

async function submitForm(e) {
    e.preventDefault();
    const query = chatInput.value.trim();
    if (!query) return;

    // 1. Add user message to UI
    appendMessage('user', query);
    chatInput.value = '';
    
    // Disable input while processing
    chatInput.disabled = true;
    sendBtn.disabled = true;

    // 2. Show loading spinner
    appendLoading();

    // 3. Send API request
    try {
        // Look for the specific production backend URL from an environment variable injected by Vercel
        // Alternatively, update this URL in your production settings.
        const backendUrl = window.VITE_BACKEND_URL || window.BACKEND_URL || 'YOUR_RAILWAY_APP_URL_HERE/api/chat';
        // For local dev and generic fallback, use localhost or relative path
        const fetchUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? 'http://127.0.0.1:8000/api/chat'
            : '/api/chat'; // Relative works if proxy is setup, otherwise use hardcoded URL

        // Replace 'YOUR_RAILWAY_APP_URL_HERE' with your actual Railway app URL, e.g., 'https://rag-backend.up.railway.app/api/chat'
        const apiUrlToUse = (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') 
            ? 'https://your-railway-app-url.up.railway.app/api/chat' // TO-DO: Update this after Railway deployment
            : 'http://127.0.0.1:8000/api/chat';
        
        const response = await fetch(apiUrlToUse, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });

        const data = await response.json();
        removeLoading();
        
        if (response.ok) {
            appendMessage('assistant', data.response);
        } else {
            appendMessage('assistant', `⚠️ **Error**: Failed to get response from server. Status: ${response.status}`);
        }
    } catch (error) {
        removeLoading();
        console.error("API Error:", error);
        appendMessage('assistant', `⚠️ **Network Error**: Could not connect to the backend server. Please ensure the API is running and CORS is configured correctly.`);
    } finally {
        // Re-enable input
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

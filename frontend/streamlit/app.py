import streamlit as st
import requests
from PIL import Image
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Soya Copilot - AI Farming Assistant",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state early for dark mode
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Custom CSS for modern chat interface
dark_mode_css = """
    /* Dark mode overrides - Complete page transformation */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: #0f0f1e !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%) !important;
    }
    
    .main {
        background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%) !important;
    }
    
    /* Dark mode block container - removes white space */
    .block-container {
        background: transparent !important;
    }
    
    [data-testid="stAppViewContainer"] > .main {
        background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%) !important;
    }
    
    /* Dark mode sidebar */
    [data-testid="stSidebar"] {
        background: #1a1a2e !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: #1a1a2e !important;
    }
    
    /* Dark mode sidebar content */
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    /* Dark mode title and subtitle */
    .chat-title {
        color: #ffffff !important;
    }
    
    .chat-title + p {
        color: #b0b0b0 !important;
    }
    
    /* Dark mode info boxes */
    .info-box {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .info-box h3,
    .info-box p,
    .info-box ul,
    .info-box li,
    .info-box strong {
        color: #e0e0e0 !important;
    }
    
    /* Dark mode chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
    }
    
    [data-testid="stChatMessageContent"] {
        color: #ffffff !important;
    }
    
    /* Dark mode expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.12) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #e0e0e0 !important;
    }
    
    /* Dark mode buttons */
    .stButton button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #e0e0e0 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .stButton button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        color: #ffffff !important;
    }
    
    /* Dark mode inputs */
    .stNumberInput input,
    .stTextInput input,
    .stSelectbox select {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Dark mode labels and text */
    label {
        color: #e0e0e0 !important;
    }
    
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #e0e0e0 !important;
    }
    
    /* Dark mode all text elements */
    p, span, div, h1, h2, h3, h4, h5, h6 {
        color: #e0e0e0 !important;
    }
    
    /* Dark mode selectbox text */
    .stSelectbox label, .stSelectbox div[data-baseweb="select"] {
        color: #e0e0e0 !important;
    }
    
    /* Dark mode number input labels */
    .stNumberInput label {
        color: #e0e0e0 !important;
    }
    
    /* Dark mode file uploader text */
    .stFileUploader label, .stFileUploader span {
        color: #e0e0e0 !important;
    }
    
    /* Dark mode status badges */
    .status-badge {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
    }
    
    /* Dark mode file uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #e0e0e0 !important;
    }
    
    /* Dark mode spinner */
    .stSpinner > div {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Dark mode chat input */
    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #ffffff !important;
    }
    
    /* Dark mode success/error messages */
    .stSuccess {
        background: rgba(40, 167, 69, 0.2) !important;
        color: #90ee90 !important;
    }
    
    .stError {
        background: rgba(220, 53, 69, 0.2) !important;
        color: #ff6b6b !important;
    }
    
    .stInfo {
        background: rgba(23, 162, 184, 0.2) !important;
        color: #87ceeb !important;
    }
    
    /* Remove all white backgrounds */
    div, section {
        background-color: transparent !important;
    }
    
    /* Dark mode columns */
    [data-testid="column"] {
        background: transparent !important;
    }
    
    /* Dark mode horizontal blocks */
    [data-testid="stHorizontalBlock"] {
        background: transparent !important;
    }
    
    /* Dark mode vertical blocks */
    [data-testid="stVerticalBlock"] {
        background: transparent !important;
    }
    
    /* Dark mode toggle switch - Keep light mode appearance */
    /* Toggle label text - white for visibility */
    [data-testid="stWidgetLabel"] {
        color: #ffffff !important;
    }
    
    /* Toggle switch background - light gray like in light mode */
    button[role="switch"] {
        background: #e0e0e0 !important;
        border: 1px solid #cccccc !important;
    }
    
    /* Toggle switch when active - green like in light mode */
    button[role="switch"][aria-checked="true"] {
        background: #00c853 !important;
        border: 1px solid #00a843 !important;
    }
    
    /* Toggle switch knob - white */
    button[role="switch"] > div {
        background: #ffffff !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }
""" if st.session_state.dark_mode else ""

st.markdown(f"""
<style>
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Keep sidebar toggle button visible */
    [data-testid="collapsedControl"] {{
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }}
    
    /* Ensure sidebar can be opened */
    [data-testid="stSidebar"] {{
        display: block !important;
    }}
    
    /* Make sure the toggle button is clickable */
    button[kind="header"] {{
        display: block !important;
        visibility: visible !important;
    }}
    
    /* Remove all top borders and lines */
    .main .block-container {{
        padding-top: 1rem;
    }}
    
    /* Remove Streamlit's default top padding/border */
    .stApp > header {{
        display: none;
    }}
    
    /* Remove any horizontal rules */
    hr {{
        display: none;
    }}
    
    /* Remove borders from markdown */
    .stMarkdown {{
        border: none !important;
    }}
    
    /* Remove column borders */
    [data-testid="column"] {{
        border: none !important;
        padding-top: 0 !important;
    }}
    
    /* Remove any dividers */
    .stDivider {{
        display: none !important;
    }}
    
    /* Remove top border from first element in chat container */
    .chat-container > div:first-child {{
        border-top: none !important;
        padding-top: 0 !important;
    }}
    
    /* Force remove all borders in main content */
    .element-container {{
        border: none !important;
    }}
    
    /* Remove Streamlit's default borders */
    .stMarkdown, .stMarkdown > div {{
        border: none !important;
        border-top: none !important;
        border-bottom: none !important;
    }}
    
    /* Target the specific area above title */
    h1:before, .chat-title:before {{
        display: none !important;
    }}
    
    /* Main container */
    .main {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }}
    
    /* Chat container */
    .chat-container {{
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 1200px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }}
    
    /* Remove all borders from elements inside chat container */
    .chat-container * {{
        border-top: none !important;
    }}
    
    /* Remove borders from Streamlit columns */
    .chat-container [data-testid="stHorizontalBlock"] {{
        border: none !important;
    }}
    
    /* Remove borders from all divs in chat container */
    .chat-container > div {{
        border: none !important;
    }}
    
    /* Header */
    .chat-title {{
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0;
        padding: 0;
    }}
    
    /* Status badges */
    .status-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }}
    
    .status-online {{
        background: #d4edda;
        color: #155724;
    }}
    
    .status-offline {{
        background: #f8d7da;
        color: #721c24;
    }}
    
    /* Info boxes */
    .info-box {{
        background: transparent;
        border: none;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #666;
    }}
    
    .info-box h3 {{
        color: #666;
    }}
    
    .info-box p, .info-box ul, .info-box li {{
        color: #666;
    }}
    
    /* All buttons - unified outlined style */
    .stButton button {{
        background: transparent;
        color: #666;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s;
    }}
    
    .stButton button:hover {{
        background: #f5f5f5;
        border-color: #ccc;
        color: #333;
        transform: none;
        box-shadow: none;
    }}
    
    /* Expanders */
    .streamlit-expanderHeader {{
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-radius: 10px;
        padding: 1rem;
        font-weight: 600;
        font-size: 1.1rem;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: linear-gradient(135deg, #667eea25 0%, #764ba225 100%);
    }}
    
    {dark_mode_css}
</style>
""", unsafe_allow_html=True)


def check_api_status():
    """Check if API is running and get status."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def main():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    # Check API status
    api_status = check_api_status()
    is_online = api_status is not None
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🌱 Soya Copilot")
        st.markdown("---")
        
        # New chat button
        if st.button("➕ New Chat", use_container_width=True):
            if st.session_state.messages:
                st.session_state.conversation_history.append({
                    "title": st.session_state.messages[0]["content"][:30] + "...",
                    "messages": st.session_state.messages.copy(),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Conversation history
        st.markdown("### 📝 Your Conversations")
        if st.session_state.conversation_history:
            for idx, conv in enumerate(reversed(st.session_state.conversation_history[-10:])):
                if st.button(
                    f"💬 {conv['title']}\n🕒 {conv['timestamp']}", 
                    key=f"conv_{idx}",
                    use_container_width=True
                ):
                    st.session_state.messages = conv['messages'].copy()
                    st.rerun()
        else:
            st.info("No previous conversations")
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Settings")
        
        # Dark mode toggle
        dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        language = st.selectbox(
            "Language",
            ["English", "Chichewa", "Shona", "Zulu", "Xhosa", "Afrikaans", "Swati"],
            help="Southern African languages (more coming soon)"
        )
        
        # Show coming soon message for non-English languages
        if language != "English":
            st.info(f"🚧 {language} translation coming soon!")
        
        if st.button("🗑️ Clear All History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.rerun()
    
    # Main chat interface
    # Header - using HTML to avoid Streamlit's column borders
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 class="chat-title">
            🌱 Soya Copilot
            <span class="status-badge status-online" style="display: {'inline-block' if is_online else 'none'};">Online</span>
            <span class="status-badge status-offline" style="display: {'none' if is_online else 'inline-block'};">Offline</span>
        </h1>
        <p style="color: #666; font-style: italic; margin-top: 0.5rem;">AI-Powered Soybean Farming Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message and features
    if not st.session_state.messages:
        # Welcome message first
        st.markdown("""
        <div class="info-box">
            <h3>Welcome to Soya Copilot!</h3>
            <p>I'm your AI farming assistant, trained on comprehensive soybean farming guides. I can help you with:</p>
            <ul>
                <li>Planting and cultivation advice</li>
                <li>Disease identification and treatment</li>
                <li>Climate and weather guidance</li>
            </ul>
            <p><strong>Ask me anything about soybean farming!</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Expanders side by side below welcome message
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("Location Analysis", expanded=False):
                st.markdown("### Check Climate Suitability")
                lat = st.number_input("Latitude", value=40.7128, format="%.6f", key="lat_welcome", help="Enter your location's latitude")
                lon = st.number_input("Longitude", value=-74.0060, format="%.6f", key="lon_welcome", help="Enter your location's longitude")
                
                if st.button("Analyze Location", use_container_width=True, key="analyze_loc_welcome"):
                    with st.spinner("Analyzing climate conditions..."):
                        try:
                            api_response = requests.post(
                                "http://localhost:8000/chat",
                                data={
                                    "message": "Analyze location suitability for soybeans",
                                    "latitude": lat,
                                    "longitude": lon
                                },
                                timeout=30
                            )
                            if api_response.status_code == 200:
                                result = api_response.json()
                                st.success(result.get("response", ""))
                            else:
                                st.error("Unable to analyze location")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
        with col2:
            with st.expander("Disease Detection", expanded=False):
                st.markdown("### Upload Plant Image")
                uploaded_file = st.file_uploader(
                    "Choose an image of soybean leaves",
                    type=['jpg', 'jpeg', 'png'],
                    help="Upload a clear image for disease analysis",
                    key="upload_welcome"
                )
                
                if uploaded_file and st.button("Analyze Image", use_container_width=True, key="analyze_img_welcome"):
                    col_img1, col_img2 = st.columns(2)
                    with col_img1:
                        image = Image.open(uploaded_file)
                        st.image(image, caption="Uploaded Image", use_container_width=True)
                    
                    with col_img2:
                        with st.spinner("Analyzing image..."):
                            try:
                                uploaded_file.seek(0)
                                files = {"image": ("image.jpg", uploaded_file, "image/jpeg")}
                                data = {"message": "Detect disease in this image", "latitude": 0.0, "longitude": 0.0}
                                
                                api_response = requests.post(
                                    "http://localhost:8000/chat",
                                    data=data,
                                    files=files,
                                    timeout=30
                                )
                                if api_response.status_code == 200:
                                    result = api_response.json()
                                    st.success(result.get("response", ""))
                                else:
                                    st.error("Unable to analyze image")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍🌾" if message["role"] == "user" else "🌱"):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("💬 Ask me about soybean farming..." if is_online else "⚠️ API is offline"):
        if not is_online:
            st.error("Please start the API server first: `python main.py`")
            return
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍🌾"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant", avatar="🌱"):
            with st.spinner("🤔 Thinking..."):
                try:
                    api_response = requests.post(
                        "http://localhost:8000/chat",
                        data={"message": prompt, "latitude": 0.0, "longitude": 0.0},
                        timeout=30
                    )
                    if api_response.status_code == 200:
                        result = api_response.json()
                        response = result.get("response", "No response received")
                    else:
                        response = "⚠️ Sorry, I encountered an error. Please try again."
                except Exception as e:
                    response = f"❌ Error: Unable to connect to the API."
                
                st.markdown(response)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    



if __name__ == "__main__":
    main()

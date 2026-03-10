import os
import sys
import tempfile
import streamlit as st

# Root import resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.orchestrator import get_agent_executor
from agent.tools.ingest_pdf import ingest_pdf

# --- Page Configuration ---
st.set_page_config(
    page_title="ScholarMind AI",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

# --- Enhanced Visuals (ChatGPT-esque Premium Dark Mode) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0D0D12;
    }

    .stApp {
        background-color: #0D0D12;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #17171C;
        border-right: 1px solid #2D2D35;
        padding-top: 2rem;
    }
    
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: 600;
        background: linear-gradient(90deg, #A855F7 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-align: center;
    }

    /* Chat Styling */
    .stChatMessage {
        background-color: transparent !important;
        padding: 1.5rem 0;
        border-bottom: 1px solid #1E1E24;
    }

    .stChatMessage.user {
        background-color: #17171C !important;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    /* Input Styling */
    .stChatInputContainer {
        border-radius: 16px !important;
        border: 1px solid #2D2D35 !important;
        background-color: #17171C !important;
        padding: 5px !important;
    }

    .stChatInput {
        background-color: #17171C !important;
        color: white !important;
    }

    /* Hide default streamlit elements for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Utility Cards */
    .utility-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
    }

    /* Process Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #7C3AED 0%, #2563EB 100%);
        color: white;
        border: none;
        padding: 0.6rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }

    /* Custom Title */
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 600;
        color: #E2E2E9;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        text-align: center;
        color: #8E8E9F;
        font-size: 1rem;
        margin-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<div class="main-title">ScholarMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Multi-Modal Research Intelligence Assistant</div>', unsafe_allow_html=True)

# --- Agent Loading Logic ---
@st.cache_resource
def load_agent():
    return get_agent_executor()

try:
    agent_executor = load_agent()
except Exception as e:
    st.error(f"Failed to initialize AI Engine: {e}")
    st.stop()

# --- Sidebar Management ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">ScholarMind</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("**📁 Document Analysis**")
        pdf_file = st.file_uploader("Upload PDF Paper", type=["pdf"], label_visibility="collapsed")
        
        st.markdown("**🖼️ Figure Extraction**")
        img_file = st.file_uploader("Upload Image/Figure", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        
        if st.button("✨ Process Uploads"):
            if pdf_file:
                with st.spinner("Decoding research data..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(pdf_file.getvalue())
                        path = tmp.name
                    if ingest_pdf(path): st.success("✅ Paper Indexed")
                    else: st.error("❌ Indexing Failed")
            else:
                st.warning("Please upload a file first.")

    st.divider()
    st.caption("Powered by Google Gemini 2.0 Flash")

# --- Active Image Context ---
active_image = None
if img_file:
    ctx_path = os.path.join(tempfile.gettempdir(), "scholar_active_img.png")
    with open(ctx_path, "wb") as f: f.write(img_file.getvalue())
    active_image = ctx_path
    st.sidebar.image(img_file, caption="Active Context Buffer")

# --- Chat Logic ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Centered chat container mock integration
chat_container = st.container()

with chat_container:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

# --- Chat Input ---
prompt = st.chat_input("Message ScholarMind...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Inject context automatically if an image exists
    full_query = prompt
    if active_image:
        full_query += f"\n\n[Context: Use ocr_tool for image at '{active_image}']"

    with st.chat_message("assistant"):
        with st.status("Solving Research Problem...", expanded=True) as status:
            try:
                # Use a custom spinner-like logic with status updates
                res = agent_executor.invoke({"messages": [("human", full_query)]})
                reply = res["messages"][-1].content
                status.update(label="Analysis Complete", state="complete", expanded=False)
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                status.update(label="Research Error", state="error")
                st.error(f"Intelligence Module Error: {e}")

import os
import sys
import tempfile
import streamlit as st

# Root import resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.orchestrator import get_agent_executor
from agent.tools.ingest_pdf import ingest_pdf

# Page Config
st.set_page_config(page_title="ScholarMind AI", layout="wide", page_icon="🧠")

# Premium Aesthetics (Injecting custom CSS)
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #1a1c23; border-right: 1px solid #30363d; }
    .stButton>button { border-radius: 8px; background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); color: white; border: none; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); filter: brightness(1.1); }
    .stChatMessage { border-radius: 12px; margin-bottom: 10px; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# Cache Agent
@st.cache_resource
def load_agent():
    return get_agent_executor()

agent_executor = load_agent()

# Sidebar
st.sidebar.title("🧠 ScholarMind AI")
st.sidebar.caption("v1.0 — Powered by Google Gemini")

st.sidebar.divider()
pdf_file = st.sidebar.file_uploader("Upload PDF Paper", type=["pdf"])
img_file = st.sidebar.file_uploader("Upload Image/Figure", type=["png","jpg","jpeg"])

if st.sidebar.button("🚀 Process Data"):
    if pdf_file:
        with st.spinner("Analyzing PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(pdf_file.getvalue())
                path = tmp.name
            if ingest_pdf(path): st.sidebar.success("✅ Paper Ingested")
            else: st.sidebar.error("❌ Processing Failed")
    else: st.sidebar.warning("Upload a PDF file first.")

# Active Contexts
active_image = None
if img_file:
    ctx_path = os.path.join(tempfile.gettempdir(), "active_ctx.png")
    with open(ctx_path, "wb") as f: f.write(img_file.getvalue())
    active_image = ctx_path
    st.sidebar.image(img_file, caption="Active Figure Context")

# Main Chat
st.title("Research Intelligence Assistant")
st.info("I can analyze your PDFs, extract data from images, or search the live web.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

prompt = st.chat_input("Ask about your research...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Inject context
    full_query = prompt
    if active_image:
        full_query += f"\n\n[Context: User uploaded a figure at '{active_image}'. Use ocr_tool for image analysis.]"

    with st.chat_message("assistant"):
        with st.spinner("Cross-referencing docs & live data..."):
            try:
                res = agent_executor.invoke({"messages": [("human", full_query)]})
                reply = res["messages"][-1].content
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Intelligence Module Error: {e}")

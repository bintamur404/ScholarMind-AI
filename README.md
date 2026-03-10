# 🧠 ScholarMind AI — Multi-Modal Research Intelligence Assistant

**ScholarMind AI** is a production-ready research copilot designed to automate the heavy lifting of academic and analytical work. It combines **RAG (Retrieval-Augmented Generation)**, **OCR (Optical Character Recognition)**, and **Live Web Search** into a single intelligent agent.

## 🚀 Realistic CV Feature Set
- **Multi-Modal Hub**: Ingests PDFs and Images simultaneously for cross-domain analysis.
- **Local Vector Search**: Custom-built SQLite + `sqlite-vec` integration for zero-cost, local vector indexing.
- **Advanced Orchestration**: Built with **LangGraph** & **Google Gemini** for robust tool-calling and reasoning.
- **Observability**: Native support for **LangSmith** tracing to debug and optimize agent performance.
- **Premium UI**: Dark-mode architecture with glassmorphism aesthetics via Streamlit.

## 📂 Project Structure
- `/app`: Premium Streamlit frontend and UI logic.
- `/agent`: LangGraph orchestrator and core agent logic.
- `/agent/tools`: Specialized modules for OCR, Web Search, and RAG.
- `/database`: SQLite vector database implementation using `sqlite-vec`.

## 🛠️ Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Ensure you have `tesseract` installed on your system for OCR.*

2. **Configure Environment**:
   Create a `.env` file in the root (this file is ignored by Git):
   ```text
   GOOGLE_API_KEY=your_gemini_key
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
   LANGCHAIN_API_KEY=your_langsmith_key
   LANGCHAIN_PROJECT="ScholarMind-AI"
   ```

3. **Run Locally**:
   ```bash
   streamlit run app/ui.py
   ```

## 🛡️ Submission Readiness
- **Zero Secrets Leak**: `.env` is ignored via `.gitignore`.
- **Segmented Code**: Modular folder architecture for high maintainability.
- **Assignment Link**: [Public LangSmith Trace Link will go here]

---
**Developed for AI/ML Research Excellence.**

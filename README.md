# Cyber AI Tool (Security Diagnostic Assistant)

A lightweight cybersecurity diagnostic assistant powered by local Llama 3.2 via Ollama, featuring a FastAPI backend and an interactive Streamlit dashboard.

## Architecture

- **Local LLM Engine:** Ollama running Llama 3.2 locally.
- **Orchestration Layer:** LangChain (langchain-ollama) coordinating tool decision-making and result synthesis.
- **Diagnostic Tools:** Network socket auditing and system interface enumeration (tools/recon.py).
- **Interfaces:**
  - REST API with FastAPI (main.py)
  - Web UI with Streamlit (app.py)

## Setup

1. **Clone the repository:**
   git clone https://github.com/manast1516-ops/cyber-ai-tool.git
   cd cyber-ai-tool

2. **Create and activate virtual environment:**
   python3 -m venv venv
   source venv/bin/activate

3. **Install dependencies:**
   pip install -r requirements.txt

4. **Ensure Ollama is running with Llama 3.2:**
   ollama pull llama3.2

## Running the Application

- **FastAPI Backend:**
  uvicorn main:app --host 127.0.0.1 --port 8000 --reload
  Access Swagger API docs at: http://127.0.0.1:8000/docs

- **Streamlit Web UI:**
  streamlit run app.py --server.port 8501
  Access the dashboard at: http://localhost:8501

# DRC RAG

A Retrieval-Augmented Generation (RAG) application built with Streamlit and Chroma for PDF-based Q&A.

## Setup

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
## Usage
python src/ingest.py          # Ingest PDFs into Chroma DB
streamlit run app.py          # Start the app


## Project Structure
app.py — Streamlit UI
ingest.py — PDF ingestion pipeline
rag_chain.py — RAG retrieval & generation logic
auth.py — Authentication (if applicable)
chroma_db — Vector store
pdfs — Input PDF files

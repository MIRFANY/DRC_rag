import os
from dotenv import load_dotenv

load_dotenv()

PDF_DIR      = "./pdfs"
CHROMA_DIR   = "./chroma_db"
EMBED_MODEL  = "all-MiniLM-L6-v2"
LLM_MODEL    = "llama3.2:3b"
TOP_K        = 4
APP_PASSWORD = os.getenv("APP_PASSWORD", "changeme123")
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from config import PDF_DIR, CHROMA_DIR, EMBED_MODEL

def ingest():
    print(f"Loading PDFs from {PDF_DIR} ...")
    loader = PyPDFDirectoryLoader(PDF_DIR)
    docs = loader.load()
    print(f"Loaded {len(docs)} pages.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")

    print("Loading embedding model ...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    print("Building vector store ...")
    db = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_DIR)
    print(f"Done! {db._collection.count()} vectors stored.")

if __name__ == "__main__":
    ingest()
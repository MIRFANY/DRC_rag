import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from config import CHROMA_DIR, EMBED_MODEL, LLM_MODEL, TOP_K

PROMPT_TEMPLATE = """
You are a compliance assistant helping a health-domain team.
Use ONLY the context below to answer the question.
If the answer is not in the context, say "I could not find this in the provided documents."
Always mention the document name and page number your answer comes from.

Context:
{context}

Question: {question}

Answer:"""

def build_chain():
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": TOP_K})
    llm = Ollama(model=LLM_MODEL, temperature=0)
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    return chain
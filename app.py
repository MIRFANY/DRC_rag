import streamlit as st
import sys, os
sys.path.append("src")

from auth import require_login
from rag_chain import build_chain

st.set_page_config(
    page_title="Health Compliance Assistant",
    page_icon="📋",
    layout="centered"
)

require_login()

@st.cache_resource(show_spinner="Loading document index...")
def get_chain():
    return build_chain()

chain = get_chain()

st.title("Health Compliance Assistant")
st.caption("Ask questions about your compliance and rules documents.")

with st.sidebar:
    st.markdown("### Settings")
    if st.button("Sign out"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    if os.path.exists("./chroma_db"):
        st.success("Vector store ready")
    else:
        st.error("Run ingest.py first!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("View sources"):
                for src in msg["sources"]:
                    st.markdown(f"📄 **{os.path.basename(src['file'])}** — page {src['page']}")
                    st.caption(src["snippet"])

if query := st.chat_input("Ask a compliance question..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            result = chain.invoke(query)

        answer = result["result"]
        sources = [
            {
                "file": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", "?"),
                "snippet": doc.page_content[:200] + "..."
            }
            for doc in result.get("source_documents", [])
        ]

        st.markdown(answer)
        if sources:
            with st.expander("View sources"):
                for src in sources:
                    st.markdown(f"📄 **{os.path.basename(src['file'])}** — page {src['page']}")
                    st.caption(src["snippet"])

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })
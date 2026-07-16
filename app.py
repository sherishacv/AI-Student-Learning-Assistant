"""Streamlit application entry point."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import streamlit as st

from config import PROJECT_NAME, ensure_directories, get_env
from src.graph.graph_builder import build_graph
from src.rag.rag_pipeline import RAGPipeline
from src.utils.helpers import build_citation_text, format_sources
from src.utils.logger import configure_logger

logger = configure_logger("app")
ensure_directories()


@st.cache_resource
def get_graph() -> Any:
    """Create and cache the LangGraph workflow."""
    return build_graph()


@st.cache_resource
def get_rag_pipeline() -> RAGPipeline:
    """Create and cache the RAG pipeline."""
    return RAGPipeline()


def save_uploaded_file(uploaded_file: Any) -> Path:
    """Save an uploaded file to disk."""
    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    destination = upload_dir / uploaded_file.name
    with destination.open("wb") as handle:
        handle.write(uploaded_file.getbuffer())
    return destination


def render_sidebar() -> None:
    """Render the sidebar with upload and status controls."""
    with st.sidebar:
        st.title("Knowledge Base")
        uploaded_files = st.file_uploader(
            "Upload PDFs",
            type=["pdf"],
            accept_multiple_files=True,
        )
        if uploaded_files:
            if st.button("Index PDFs"):
                pipeline = get_rag_pipeline()
                for uploaded_file in uploaded_files:
                    source_path = save_uploaded_file(uploaded_file)
                    try:
                        pipeline.index_pdf(source_path)
                        st.success(f"Indexed {uploaded_file.name}")
                    except Exception as exc:  # pragma: no cover - defensive logging
                        logger.exception("Failed to index %s", uploaded_file.name)
                        st.error(str(exc))
        st.divider()
        st.subheader("Status")
        state = get_rag_pipeline().get_state()
        st.metric("Documents", state["document_count"])
        st.metric("Chunks", state["chunk_count"])
        uploaded_names = [file.name for file in Path("data/uploads").glob("*.pdf")]
        st.write("Uploaded Files")
        if uploaded_names:
            for name in uploaded_names:
                st.caption(name)
        else:
            st.caption("None")


def render_main() -> None:
    """Render the main dashboard UI."""
    st.set_page_config(page_title=PROJECT_NAME, page_icon="📚", layout="wide")
    st.title(f"{PROJECT_NAME} 🎓")
    st.caption("Production-ready AI study companion")

    if "history" not in st.session_state:
        st.session_state.history = []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model", get_env("GROQ_MODEL", "llama-3.3-70b-versatile") or "unknown")
    with col2:
        st.metric("Embeddings", "Sentence Transformers")
    with col3:
        st.metric("Retrieval", "FAISS + Hybrid")

    render_sidebar()

    action = st.selectbox(
        "Select Task",
        [
            "Explain Topic",
            "Generate Quiz",
            "Generate Flashcards",
            "Generate Summary",
            "Study Planner",
            "Chat",
        ],
    )
    question = st.text_area("Enter your question or topic")

    if st.button("Run") and question:
        start_time = time.perf_counter()
        graph = get_graph()
        pipeline = get_rag_pipeline()
        intent = action.lower().replace(" ", "_")
        retrieved_documents = pipeline.retrieve(question, intent=intent)
        state = {
            "user_question": question,
            "retrieved_documents": retrieved_documents,
            "intent": intent,
            "selected_agent": intent,
            "response": "",
            "sources": [doc["source"] for doc in retrieved_documents],
            "pages": [doc["page"] for doc in retrieved_documents],
            "chat_history": st.session_state.history,
            "confidence_score": 0.0,
            "routing_logic": "keyword_router",
            "response_time": 0.0,
            "retrieved_chunks": [doc["content"] for doc in retrieved_documents],
        }
        with st.spinner("Generating a grounded answer from your uploaded material..."):
            result = graph.invoke(state)
        elapsed = time.perf_counter() - start_time
        result["response_time"] = round(elapsed, 3)
        st.session_state.history.append({"question": question, "answer": result["response"]})

        st.success("Response generated")
        st.markdown("## 📚 Answer")
        st.markdown(result["response"])
        st.divider()

        confidence = float(result.get("confidence_score", 0.0))
        confidence_color = "green" if confidence >= 0.75 else "orange" if confidence >= 0.45 else "red"
        st.markdown(
            f"<span style='color:{confidence_color};font-weight:bold;'>Confidence: {confidence:.2f}</span>",
            unsafe_allow_html=True,
        )
        st.caption(f"Response time: {result['response_time']}s")
        st.caption(f"Sources: {format_sources(result['sources'])}")
        st.caption(f"Pages: {result['pages']}")
        st.subheader("Relevant Sources")
        for item in result.get("retrieved_documents", []):
            source_name = Path(item["source"]).name
            section = item.get("section", "")
            score = item.get("relevance_score", 0.0)
            label = f"{source_name} • Page {item['page']}"
            if section:
                label = f"{label} • {section}"
            st.write(f"- {label} • Relevance {score:.2f}")
        with st.expander("Citation Preview"):
            st.write(build_citation_text(result.get("retrieved_documents", [])))

    st.divider()
    st.subheader("Conversation History")
    for item in st.session_state.history:
        st.markdown(f"**Q:** {item['question']}")
        st.markdown(f"**A:** {item['answer']}")
        st.divider()


if __name__ == "__main__":
    render_main()

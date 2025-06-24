import os
import streamlit as st
from utils.config import load_env
from core.index_manager import initialize_index

load_env()

st.set_page_config(
    page_title="Chatbot self-hosted",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

query_engine = initialize_index()

# Initialize the chatbot's memory (session states)
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "qa_chain" not in st.session_state:
        st.session_state.qa_chain = None

# Chat interface section
def chat_interface():
    st.title("💬 Chatbot self-hosted")
    st.caption("🚀 Chatbot RAG usando LLMs de código abierto")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("Pregunta sobre tus documentos"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()


            with st.spinner("Buscando en tus documentos..."):
                try:
                    full_response = query_engine.query(prompt)
                except Exception as e:
                    full_response = f"Error: {str(e)}"


            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Main function
def main():
    initialize_session_state()
    chat_interface()

if __name__ == "__main__":
    main()

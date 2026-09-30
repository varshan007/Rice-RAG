import streamlit as st
from test_rag import build_rag_chain

# --- Page Config ---
st.set_page_config(page_title="Rice RAG Assistant", page_icon="🌾")
st.title("🌾 Rice Agriculture RAG Assistant")
st.markdown("Ask me anything about rice cultivation, diseases, or best practices!")

# --- Initialize Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Initialize RAG Chain (Cached so it doesn't reload every time) ---
@st.cache_resource
def get_chain():
    return build_rag_chain()

try:
    chain = get_chain()
except Exception as e:
    st.error(f"Failed to load RAG chain (did you ingest the data?). Error: {e}")
    st.stop()

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Ask a question (e.g. What causes rice blast?)"):
    # 1. Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Searching the knowledge base..."):
            try:
                response = chain.invoke(prompt)
                message_placeholder.markdown(response)
                # 3. Add AI response to history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error querying the model: {e}")

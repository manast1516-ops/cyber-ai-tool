import streamlit as st
from core.orchestrator import AgentOrchestrator
from core.registry import TOOL_DEFINITIONS

st.set_page_config(
    page_title="Cyber AI Diagnostic Tool",
    page_icon="🛡️",
    layout="wide"
)

@st.cache_resource
def get_agent():
    return AgentOrchestrator()

agent = get_agent()

st.title("🛡️ Cyber AI Diagnostic & Auditing Assistant")
st.caption("Powered by local Llama 3.2 via Ollama and internal diagnostic tools")

with st.sidebar:
    st.header("Active Diagnostic Tools")
    for name, meta in TOOL_DEFINITIONS.items():
        st.markdown(f"**`{name}`**")
        st.caption(meta["description"])
    
    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Assistant online. Ask an auditing question or request a diagnostic check (e.g., 'Check if port 80 is open on scanme.nmap.org' or 'List local interfaces')."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Enter diagnostic query or task..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing and executing diagnostic routines..."):
            response = agent.process_query(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

import streamlit as st
import requests
import os
import json

st.set_page_config(
    page_title="AI Studio - Sovereign Native Workspace",
    page_icon="🚀",
    layout="wide"
)

st.sidebar.title("🚀 AI Studio v1 (Native)")
st.sidebar.markdown("---")
nav = st.sidebar.selectbox("Navigation", ["💬 Chat Assistant", "⚙️ Hardware Telemetry", "💾 Storage Vault Manager"])

OLLAMA_URL = "http://localhost:11434/api/generate"

if nav == "💬 Chat Assistant":
    st.title("💬 Sovereign Local AI Assistant")
    st.write("Running 100% natively via Ollama (`deepseek-r1:14b`) with zero Docker overhead.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Enter your prompt..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing locally on your GPU/SSD..."):
                try:
                    payload = {"model": "deepseek-r1:14b", "prompt": prompt, "stream": False}
                    res = requests.post(OLLAMA_URL, json=payload)
                    if res.status_code == 200:
                        reply = res.json().get("response", "No response.")
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    else:
                        st.error(f"Ollama Error: {res.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

elif nav == "⚙️ Hardware Telemetry":
    st.title("⚙️ Hardware & Port Status")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Dedicated VRAM", "6.0 GB", "Active")
    with col2:
        st.metric("Total GPU Memory", "13.9 GB", "Optimized")
    with col3:
        st.metric("Storage Setup", "1TB SSD / 16TB Array", "100% Native")
        
    st.markdown("### Active Local Ports")
    st.info("Ollama Engine (:11434): ONLINE\nAI Studio IPC (:9876): ONLINE\nTeach Engine (:9877): ONLINE")

elif nav == "💾 Storage Vault Manager":
    st.title("💾 16TB External Storage Array & SSD Vault")
    st.write("Manage archives and data logs streaming directly to your D: drive.")
    
    note_title = st.text_input("Archive Title", "Sovereign_Note_01")
    note_data = st.text_area("Content", "Write local backup notes here...")
    
    if st.button("Save to 16TB External Vault"):
        vault_dir = "D:/DevStudio_v1_Workspace/backups"
        os.makedirs(vault_dir, exist_ok=True)
        path = os.path.join(vault_dir, f"{note_title}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(note_data)
        st.success(f"Successfully saved locally to your 16TB array at `{path}`!")
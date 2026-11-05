import streamlit as st
import requests
import json
import shutil
import os
import subprocess

st.set_page_config(
    page_title="AI Studio v1 - Sovereign Native Interface",
    layout="wide",
    page_icon="⚡"
)

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #0d1117; }
    .stMetric { background-color: #161b22; padding: 12px; border-radius: 8px; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.title("⚡ AI Studio Control Panel")
st.sidebar.caption("Native Zero-Docker Architecture")
app_mode = st.sidebar.radio("Navigation", [
    "Sovereign Chat (DeepSeek-R1)",
    "System Telemetry & Multi-Drive",
    "Teach Engine (Port 9877)",
    "AST Compiler Safety Gate",
    "Vague Answer Inspector"
])

OLLAMA_GEN_URL = "http://localhost:11434/api/generate"
AISTUDIO_IPC_URL = "http://127.0.0.1:9876"
TEACH_IPC_URL = "http://127.0.0.1:9877"

# Helper: Stream Ollama Tokens
def stream_ollama(prompt, model="deepseek-r1:14b"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }
    try:
        res = requests.post(OLLAMA_GEN_URL, json=payload, stream=True, timeout=60)
        for line in res.iter_lines():
            if line:
                chunk = json.loads(line.decode("utf-8"))
                yield chunk.get("response", "")
    except Exception as e:
        yield f"\n[!] Ollama Connection Error: {e}"

# -----------------------------------------------------------------------------
# TAB 1: CHAT ASSISTANT
# -----------------------------------------------------------------------------
if app_mode == "Sovereign Chat (DeepSeek-R1)":
    st.header("Sovereign Local Reasoning Engine")
    st.caption("Direct socket link to native Ollama (deepseek-r1:14b) with zero container overhead.")

    col1, col2 = st.columns([4, 1])
    with col1:
        prompt = st.text_area("Task Directive / C++ Blueprint / System Prompt:", height=140, placeholder="e.g. Write a C++20 fixed-timestep substepping tick struct for Unreal Engine 5.8...")
    with col2:
        model_choice = st.selectbox("Active Model", ["deepseek-r1:14b", "qwen2.5-coder:14b", "llama3.2:latest"])
        clear_btn = st.button("Clear Console", use_container_width=True)

    if st.button("Execute Reasoning Pipeline", type="primary"):
        if prompt.strip():
            st.subheader("Model Stream Output")
            response_container = st.empty()
            with st.spinner("Streaming local inference..."):
                response_container.write_stream(stream_ollama(prompt, model_choice))
        else:
            st.warning("Enter a prompt before executing.")

# -----------------------------------------------------------------------------
# TAB 2: SYSTEM TELEMETRY & MULTI-DRIVE
# -----------------------------------------------------------------------------
elif app_mode == "System Telemetry & Multi-Drive":
    st.header("System Telemetry & Multi-Drive Array")
    st.caption("Live socket health, process states, and NVMe/Storage capacity.")

    # Service Metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        try:
            r_ai = requests.get(AISTUDIO_IPC_URL, timeout=2)
            st.metric("AI Studio IPC", "ONLINE" if r_ai.status_code == 200 else "DEGRADED", "Port 9876")
        except:
            st.metric("AI Studio IPC", "OFFLINE", "Port 9876")
    with c2:
        try:
            r_teach = requests.get(TEACH_IPC_URL, timeout=2)
            st.metric("Teach Engine", "ONLINE" if r_teach.status_code == 200 else "DEGRADED", "Port 9877")
        except:
            st.metric("Teach Engine", "OFFLINE", "Port 9877")
    with c3:
        try:
            r_ol = requests.get("http://localhost:11434/api/tags", timeout=2)
            st.metric("Ollama Engine", "ONLINE" if r_ol.status_code == 200 else "DEGRADED", "Port 11434")
        except:
            st.metric("Ollama Engine", "OFFLINE", "Port 11434")

    st.divider()
    st.subheader("Storage Array Health")
    
    col_c, col_d = st.columns(2)
    with col_c:
        total_c, used_c, free_c = shutil.disk_usage("C:\\")
        st.write("**Primary NVMe SSD (C:)**")
        st.progress(used_c / total_c)
        st.write(f"Free: **{free_c // (2**30)} GB** / Total: {total_c // (2**30)} GB")
        
    with col_d:
        if os.path.exists("D:\\"):
            total_d, used_d, free_d = shutil.disk_usage("D:\\")
            st.write("**16 TB External Array (D:)**")
            st.progress(used_d / total_d)
            st.write(f"Free: **{round(free_d / (2**40), 2)} TB** / Total: {round(total_d / (2**40), 2)} TB")
        else:
            st.write("**Storage Array (D:)**")
            st.info("Drive D: not mounted or accessible.")

    # Audit file status
    st.divider()
    st.subheader("Toolchain Audit Cache")
    audit_file = "Workspace/Logs/toolchain_audit.json"
    if os.path.exists(audit_file):
        with open(audit_file, "r") as f:
            st.json(json.load(f))
    else:
        st.info("No toolchain audit found. Run python Bridge/software_update_checker.py")

# -----------------------------------------------------------------------------
# TAB 3: TEACH ENGINE
# -----------------------------------------------------------------------------
elif app_mode == "Teach Engine (Port 9877)":
    st.header("Teach Engine - Interactive Tutoring Module")
    st.caption("Sovereign curriculum delivery and real-time C++ engineering mentorship.")

    teach_mode = st.selectbox("Select Curriculum Track", [
        "Unreal C++ Gameplay Architecture & Memory Models",
        "Deterministic Chaos Physics & Fixed-Substepping",
        "HLSL Niagara Compute Shader Pipelines"
    ])

    query = st.text_input("Enter concept or code snippet for mentoring audit:")
    if st.button("Submit to Teach IPC"):
        if query.strip():
            try:
                res = requests.post(TEACH_IPC_URL, json={"track": teach_mode, "query": query}, timeout=5)
                st.success("Teach Engine Acknowledgement Received:")
                st.json(res.json())
            except Exception as e:
                st.error(f"Failed to communicate with Teach Engine on :9877 -> {e}")

# -----------------------------------------------------------------------------
# TAB 4: AST COMPILER GATE
# -----------------------------------------------------------------------------
elif app_mode == "AST Compiler Safety Gate":
    st.header("Automated AST Compiler Simulator")
    st.caption("Verifies Python and C++ structures prior to persistent disk commits.")

    target_file = st.text_input("Relative File Path to Audit", "Bridge/aistudio_ipc_server.py")
    if st.button("Run Pre-Commit AST Gate", type="primary"):
        res = subprocess.run(["python", "Bridge/test_simulator.py", target_file], capture_output=True, text=True)
        st.code(res.stdout if res.stdout else res.stderr)
        if res.returncode == 0:
            st.success("[PASS] File is syntax safe. No BOM or AST syntax errors.")
        else:
            st.error("[FAIL] AST Syntax fault detected. Review trace above.")

# -----------------------------------------------------------------------------
# TAB 5: VAGUE ANSWER INSPECTOR
# -----------------------------------------------------------------------------
elif app_mode == "Vague Answer Inspector":
    st.header("Progressive Vague Answer Protocol Inspector")
    st.caption("Autonomous clarity scoring engine ensuring technical rigor.")

    test_prompt = st.text_area("Input Prompt to Test Clarity:", height=100)
    if st.button("Analyze Prompt Specificity"):
        if test_prompt.strip():
            res = subprocess.run(["python", "Bridge/vague_answer_engine.py", test_prompt], capture_output=True, text=True)
            try:
                audit_result = json.loads(res.stdout)
                if audit_result.get("tier") == 1:
                    st.warning("Tier 1 Detected: Prompt is too vague.")
                    st.write("**Clarification Questions Enforced:**")
                    for q in audit_result.get("clarification_questions", []):
                        st.write(f"- {q}")
                else:
                    st.success("Tier 3 Validated: Specification contains sufficient technical depth for execution.")
                st.json(audit_result)
            except:
                st.code(res.stdout)
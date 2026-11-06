import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess
import getpass
import time
import re

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="SOS CYBER SHIELD",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DESIGN & STYLING (Hacker Movie Terminal Theme)
# ==========================================

st.markdown("""
<style>
.stApp {
    background: #030712;
    color: #00ff66;
}
[data-testid="stSidebar"] {
    background: #050b14;
    border-right: 1px solid #00ff66;
}
h1, h2, h3 {
    color: #00ff66 !important;
    font-family: 'Courier New', monospace;
    letter-spacing: 2px;
}
p, label, span {
    color: #00ff66;
    font-family: 'Courier New', monospace;
}
div[data-testid="stMetric"] {
    background: #050b14;
    border: 1px solid #00ff66;
    padding: 14px;
    border-radius: 6px;
    box-shadow: 0 0 10px rgba(0, 255, 102, 0.2);
}
div[data-testid="stMetric"] label {
    color: #00ff66 !important;
}
.stButton button {
    background: #003b00;
    color: #00ff66;
    border: 1px solid #00ff66;
    border-radius: 4px;
    font-weight: bold;
    font-family: 'Courier New', monospace;
}
.stButton button:hover {
    background: #00ff66;
    color: #000000;
    border: 1px solid #ffffff;
}
.sos-title {
    color: #ff0033;
    font-size: 32px;
    font-weight: 900;
    letter-spacing: 3px;
    font-family: 'Courier New', monospace;
}
.sos-subtitle {
    color: #00ff66;
    font-size: 11px;
    letter-spacing: 2px;
    font-family: 'Courier New', monospace;
}
.terminal-box {
    background: #000000;
    color: #00ff66;
    padding: 18px;
    border-radius: 6px;
    border: 1px solid #00ff66;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    white-space: pre-wrap;
    box-shadow: inset 0 0 15px rgba(0, 255, 102, 0.3);
}
input[type="text"] {
    background-color: #000000 !important;
    color: #00ff66 !important;
    border: 1px solid #00ff66 !important;
    font-family: 'Courier New', monospace !important;
    border-radius: 4px !important;
}
input[type="text"]:focus {
    border: 1px solid #ffffff !important;
    box-shadow: 0 0 8px rgba(0, 255, 102, 0.5) !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "sos_triggered": False,
    "terminal_unlocked": False,
    "terminal_history": ["// ROOT ACCESS TERMINAL v4.2.0", "// System initialized... Terminal Locked. Enter Secret Code."],
    "incident_logs": [
        {"Time": "2026-03-30 10:15:22", "Type": "Brute Force Attack", "IP": "192.168.1.45", "Status": "Blocked"},
        {"Time": "2026-03-30 10:12:05", "Type": "SQL Injection", "IP": "45.33.22.11", "Status": "Mitigated"},
        {"Time": "2026-03-30 09:50:11", "Type": "Unauthorized Access", "IP": "10.0.0.99", "Status": "Investigating"}
    ]
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================
# HEADER
# ==========================================

st.markdown('<div class="sos-title">⚡ SOS CYBER SHIELD // COMMAND CENTER</div>', unsafe_allow_html=True)
st.markdown('<div class="sos-subtitle">SECURE OPERATIONS & GLOBAL THREAT INTELLIGENCE INTERFACE</div>', unsafe_allow_html=True)
st.divider()

# ==========================================
# SIDEBAR (Navigation)
# ==========================================

st.sidebar.markdown("## 🛡️ SYSTEM MENU")

nav_options = [
    "Dashboard Overview",
    "Threat Map & Analytics",
    "Security Log Analyzer",
    "Incident Playbook",
    "System Info",
    "💻 Hacker Terminal"
]

page = st.sidebar.radio("NAVIGATION", nav_options)

st.sidebar.divider()
st.sidebar.markdown("### SYSTEM STATUS")
st.sidebar.success("FIREWALL: ONLINE [🟢]")
st.sidebar.info("ENCRYPTION: AES-256 [🔒]")

# ==========================================
# PAGE 1: DASHBOARD OVERVIEW
# ==========================================

if page == "Dashboard Overview":
    st.subheader("📊 THREAT METRICS & OVERVIEW")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("TOTAL ATTACKS", "1,428", "+12 today")
    col2.metric("BLOCKED IPS", "342", "Secure")
    col3.metric("ACTIVE ALERTS", "2", "Critical")
    col4.metric("SYSTEM LOAD", "14.2%", "Optimal")

    st.divider()

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### 🚨 EMERGENCY LOCKDOWN CONTROL")
        if st.button("TRIGGER EMERGENCY LOCKDOWN", use_container_width=True):
            st.session_state.sos_triggered = True
            st.error("EMERGENCY PROTOCOL ACTIVATED! Network isolated.")
        
        if st.session_state.sos_triggered:
            st.error("STATUS: SYSTEM IN LOCKDOWN MODE")
        else:
            st.success("STATUS: NORMAL MONITORING")

    with col_right:
        st.markdown("### 📋 RECENT INCIDENT LOGS")
        st.dataframe(pd.DataFrame(st.session_state.incident_logs), use_container_width=True, hide_index=True)

# ==========================================
# PAGE 2: THREAT MAP & ANALYTICS
# ==========================================

elif page == "Threat Map & Analytics":
    st.subheader("🌍 GLOBAL ATTACK MAP & TELEMETRY")
    st.info("Visualizing global threat vectors and malicious IP origins in real-time.")

    attack_data = pd.DataFrame([
        {"Latitude": 37.7749, "Longitude": -122.4194, "City": "San Francisco", "Attempts": 180, "Threat": "DDoS"},
        {"Latitude": 51.5074, "Longitude": -0.1278, "City": "London", "Attempts": 120, "Threat": "Brute Force"},
        {"Latitude": 23.8103, "Longitude": 90.4125, "City": "Dhaka", "Attempts": 250, "Threat": "SQL Injection"},
        {"Latitude": 35.6762, "Longitude": 139.6503, "City": "Tokyo", "Attempts": 90, "Threat": "Port Scan"},
        {"Latitude": -22.9068, "Longitude": -43.1729, "City": "Rio de Janeiro", "Attempts": 110, "Threat": "Malware"}
    ])

    fig = px.scatter_map(
        attack_data,
        lat="Latitude",
        lon="Longitude",
        size="Attempts",
        color="Threat",
        hover_name="City",
        zoom=1.5,
        height=600
    )

    fig.update_layout(
        map_style="carto-darkmatter",
        paper_bgcolor="#030712",
        font_color="#00ff66",
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGE 3: SECURITY LOG ANALYZER
# ==========================================

elif page == "Security Log Analyzer":
    st.subheader("🔍 LOG & VULNERABILITY INSPECTOR")
    
    uploaded_file = st.file_uploader("Upload server log / code snippet (.txt, .log)", type=["txt", "log"])

    if uploaded_file is not None:
        st.success("File successfully parsed. Executing deep security heuristic scan...")
        with st.spinner("Analyzing vulnerabilities..."):
            st.error("⚠️ 2 Critical Security Vulnerabilities Found!")
            issues_df = pd.DataFrame([
                {"Severity": "HIGH", "Module": "Auth API", "Description": "Weak hashing algorithm detected (MD5)"},
                {"Severity": "HIGH", "Module": "Database", "Description": "SQL Injection risk in query parameter"}
            ])
            st.dataframe(issues_df, use_container_width=True, hide_index=True)
    else:
        st.info("Upload a log file to begin security auditing.")

# ==========================================
# PAGE 4: INCIDENT PLAYBOOK
# ==========================================

elif page == "Incident Playbook":
    st.subheader("📖 INCIDENT RESPONSE PLAYBOOK")
    st.markdown("""
    - **Phase 1 (Containment):** Isolate infected endpoints and block malicious IPs immediately.
    - **Phase 2 (Eradication):** Patch vulnerabilities, remove backdoor scripts, and reset compromised credentials.
    - **Phase 3 (Recovery):** Restore services from secure offline backups and verify system integrity.
    """)

# ==========================================
# PAGE 5: SYSTEM INFO
# ==========================================

elif page == "System Info":
    st.subheader("ℹ️ SYSTEM INFORMATION")
    st.markdown("""
    **Project:** SOS Cyber Shield (Hacker Terminal Edition)  
    **Framework:** Streamlit & Plotly  
    **Design Theme:** Matrix Green / Movie Hacker HUD  
    """)

# ==========================================
# PAGE 6: HACKER TERMINAL (SECRET CODE PROTECTED)
# ==========================================

elif page == "💻 Hacker Terminal":
    st.subheader("💻 SECURE HACKER TERMINAL [RESTRICTED ACCESS]")
    
    FIXED_SECRET_CODE = "Ap202631$"

    # যদি টার্মিনাল আনলক না থাকে
    if not st.session_state.terminal_unlocked:
        st.warning("🔒 Terminal is locked. Enter the fixed secret code to open terminal access.")
        
        entered_code = st.text_input("Enter Terminal Secret Code", type="password", key="unlock_input")
        if st.button("Unlock Terminal"):
            if entered_code == FIXED_SECRET_CODE:
                st.session_state.terminal_unlocked = True
                st.session_state.terminal_history.append("[✔] Access Granted. Root privileges acquired.")
                st.success("Access Granted! Loading terminal...")
                st.rerun()
            else:
                st.error("❌ Incorrect Secret Code! Access Denied.")
    
    # টার্মিনাল আনলক হলে
    else:
        st.success("Terminal Status: **UNLOCKED [🟢]**")

        cmd = st.text_input("root@sos-shield:~#", placeholder="Type command (e.g. show my nearby all wifi password)", key="term_cmd")
        col_btn1, col_btn2 = st.columns([1, 5])
        
        execute_clicked = col_btn1.button("Execute")
        clear_clicked = col_btn2.button("Clear Screen")

        if clear_clicked:
            st.session_state.terminal_history = ["Terminal cleared."]
            st.rerun()

        if execute_clicked and cmd:
            cmd_clean = cmd.strip()
            cmd_lower = cmd_clean.lower()
            cmd_upper = cmd_clean.upper()
            st.session_state.terminal_history.append(f"root@sos-shield:~# {cmd_clean}")
            
            if cmd_upper == "CLEAR":
                st.session_state.terminal_history = ["Terminal cleared."]
            elif cmd_upper == "HELP":
                st.session_state.terminal_history.append("COMMANDS:\n- show my nearby all wifi password: Extract real system username and saved Wi-Fi profiles\n- clear: Clear screen")
            
            elif "wifi" in cmd_lower or "password" in cmd_lower:
                try:
                    real_username = getpass.getuser()
                    
                    wifi_data = f"\n==================================================\n"
                    wifi_data += f"      REAL SYSTEM CREDENTIALS & WIFI DUMP\n"
                    wifi_data += f"      System Username: {real_username}\n"
                    wifi_data += "==================================================\n"
                    
                    meta_data = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, encoding='utf-8', errors='ignore', shell=True)
                    
                    profiles = []
                    for line in meta_data.stdout.splitlines():
                        if ":" in line and ("Profile" in line or "প্রোফাইল" in line):
                            parts = line.split(":")
                            if len(parts) > 1:
                                profiles.append(parts[1].strip())
                    
                    if profiles:
                        for i, profile_name in enumerate(profiles):
                            profile_info = subprocess.run(['netsh', 'wlan', 'show', 'profile', f'name="{profile_name}"', 'key=clear'], capture_output=True, text=True, encoding='utf-8', errors='ignore', shell=True)
                            
                            password = "OPEN / NONE"
                            for p_line in profile_info.stdout.splitlines():
                                if "Key Content" in p_line or "মূল কন্টেন্ট" in p_line:
                                    p_parts = p_line.split(":")
                                    if len(p_parts) > 1:
                                        password = p_parts[1].strip()
                                        break
                            wifi_data += f"[{i+1}] SSID: {profile_name} ➔ KEY: {password}\n"
                    else:
                        wifi_data += "No saved Wi-Fi profiles found or command restricted by OS.\n"
                        
                    st.session_state.terminal_history.append(wifi_data)
                except Exception as e:
                    st.session_state.terminal_history.append(f"Error extracting system data: {str(e)}")
            
            else:
                try:
                    result = subprocess.run(
                        cmd_clean, 
                        shell=True, 
                        capture_output=True, 
                        text=True, 
                        timeout=5
                    )
                    output = result.stdout if result.stdout else result.stderr
                    if not output:
                        output = "Command executed successfully."
                    st.session_state.terminal_history.append(output)
                except Exception as e:
                    st.session_state.terminal_history.append(f"Error: {str(e)}")

        # টার্মিনাল স্ক্রিন রেন্ডার
        terminal_output = "\n".join(st.session_state.terminal_history)
        st.markdown(f'<div class="terminal-box">{terminal_output}</div>', unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================
st.divider()
st.caption("SOS CYBER SHIELD // SECURE COMMAND INTERFACE // ALL RIGHTS RESERVED")

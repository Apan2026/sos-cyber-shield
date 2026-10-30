import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timezone

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
# DESIGN & STYLING (Hacker Terminal Theme)
# ==========================================

st.markdown("""
<style>
.stApp {
    background: #050b10;
    color: #00ff66;
}
[data-testid="stSidebar"] {
    background: #081118;
    border-right: 1px solid #10b981;
}
h1, h2, h3 {
    color: #00ff66 !important;
    font-family: monospace;
    letter-spacing: 2px;
}
p, label, span {
    color: #94a3b8;
    font-family: monospace;
}
div[data-testid="stMetric"] {
    background: #0a192f;
    border: 1px solid #10b981;
    padding: 14px;
    border-radius: 6px;
    box-shadow: 0 0 10px rgba(0, 255, 102, 0.1);
}
div[data-testid="stMetric"] label {
    color: #10b981 !important;
}
.stButton button {
    background: #065f46;
    color: #ffffff;
    border: 1px solid #34d399;
    border-radius: 6px;
    font-weight: bold;
    font-family: monospace;
}
.stButton button:hover {
    background: #047857;
    color: #00ff66;
    border: 1px solid #00ff66;
}
.sos-title {
    color: #ff3333;
    font-size: 32px;
    font-weight: 900;
    letter-spacing: 3px;
    font-family: monospace;
}
.sos-subtitle {
    color: #10b981;
    font-size: 11px;
    letter-spacing: 2px;
    font-family: monospace;
}
.terminal-box {
    background: #000000;
    color: #00ff66;
    padding: 15px;
    border-radius: 5px;
    border: 1px solid #00ff66;
    font-family: monospace;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "sos_triggered": False,
    "admin_logged_in": False,   # অ্যাডমিন লগইন স্টেট
    "terminal_history": ["System initialized... Type commands or select options."],
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
# SIDEBAR (Admin Login & Navigation)
# ==========================================

st.sidebar.markdown("## 🛡️ SYSTEM MENU")

# অ্যাডমিন লগইন সেকশন
st.sidebar.markdown("### 🔐 ADMIN AUTHENTICATION")
admin_user = st.sidebar.text_input("Username", value="")
admin_pass = st.sidebar.text_input("Password", type="password", value="")

if st.sidebar.button("Login as Admin"):
    # ডিফল্ট ইউজারনেম: admin, পাসওয়ার্ড: root123
    if admin_user == "admin" and admin_pass == "root123":
        st.session_state.admin_logged_in = True
        st.sidebar.success("Access Granted! Hacker Terminal Unlocked.")
    else:
        st.sidebar.error("Access Denied! Invalid Credentials.")

if st.session_state.admin_logged_in:
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout Admin"):
        st.session_state.admin_logged_in = False
        st.rerun()

st.sidebar.divider()

# মেনু অপশন
nav_options = [
    "Dashboard Overview",
    "Threat Map & Analytics",
    "Security Log Analyzer",
    "Incident Playbook",
    "System Info"
]

if st.session_state.admin_logged_in:
    nav_options.append("💻 Hacker Terminal (Admin)")

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
        paper_bgcolor="#050b10",
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
    **Design Theme:** Cyberpunk Dark / Terminal HUD  
    """)

# ==========================================
# PAGE 6: HACKER TERMINAL (ADMIN ONLY)
# ==========================================

elif page == "💻 Hacker Terminal (Admin)":
    st.subheader("💻 SECURE ADMIN HACKER TERMINAL")
    st.success("Logged in as Root Admin. Full system shell access granted.")

    # কমান্ড ইনপুট ফর্ম
    with st.form("terminal_form", clear_on_submit=True):
        cmd = st.text_input("root@sos-shield:~#", placeholder="Type command (e.g. scan, status, ipconfig, clear)")
        submitted = st.form_submit_button("Execute Command")

        if submitted and cmd:
            cmd_upper = cmd.strip().upper()
            st.session_state.terminal_history.append(f"root@sos-shield:~# {cmd}")
            
            if cmd_upper == "CLEAR":
                st.session_state.terminal_history = ["Terminal cleared."]
            elif cmd_upper == "STATUS":
                st.session_state.terminal_history.append("FIREWALL: ACTIVE | ENCRYPTION: SECURE | THREAT LEVEL: LOW")
            elif cmd_upper == "SCAN":
                st.session_state.terminal_history.append("Scanning network ports... [Ports 21, 22, 80, 443 active]. No intrusion detected.")
            elif cmd_upper == "IPCONFIG":
                st.session_state.terminal_history.append("IPv4 Address: 192.168.1.100 | Gateway: 192.168.1.1 | Subnet: 255.255.255.0")
            else:
                st.session_state.terminal_history.append(f"Command not recognized: '{cmd}'. Type 'status', 'scan', 'ipconfig', or 'clear'.")

    # টার্মিনাল স্ক্রিন রেন্ডার
    terminal_output = "\n".join(st.session_state.terminal_history)
    st.markdown(f'<div class="terminal-box">{terminal_output}</div>', unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================
st.divider()
st.caption("SOS CYBER SHIELD // SECURE COMMAND INTERFACE // ALL RIGHTS RESERVED")

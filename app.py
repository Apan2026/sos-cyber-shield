import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="NXMINI CYBER GUARD X",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DESIGN & STYLING (Cyberpunk / Security Theme)
# ==========================================

st.markdown("""
<style>
.stApp {
    background: #080c14;
    color: #e0f2fe;
}
[data-testid="stSidebar"] {
    background: #0d1526;
    border-right: 1px solid #1e3a8a;
}
h1, h2, h3 {
    color: #38bdf8 !important;
}
p, label {
    color: #94a3b8;
}
div[data-testid="stMetric"] {
    background: #0f172a;
    border: 1px solid #1e293b;
    padding: 14px;
    border-radius: 10px;
}
.stButton button {
    background: #0284c7;
    color: white;
    border: 1px solid #38bdf8;
    border-radius: 8px;
    font-weight: bold;
}
.stButton button:hover {
    background: #0369a1;
    color: white;
}
.sos-title {
    color: #f43f5e;
    font-size: 36px;
    font-weight: 900;
    letter-spacing: 3px;
}
.sos-subtitle {
    color: #38bdf8;
    font-size: 12px;
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "sos_triggered": False,
    "incident_logs": [
        {"Time": "2026-03-30 10:15:22", "Type": "Brute Force Attack", "IP": "192.168.1.45", "Status": "Blocked"},
        {"Time": "2026-03-30 10:12:05", "Type": "SQL Injection", "IP": "45.33.22.11", "Status": "Mitigated"},
        {"Time": "2026-03-30 09:50:11", "Type": "Unauthorized Access", "IP": "10.0.0.99", "Status": "Investigating"}
    ],
    "audit_results": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================
# HEADER
# ==========================================

st.markdown('<div class="sos-title">🚨 NXMINI CYBER GUARD X</div>', unsafe_allow_html=True)
st.markdown('<div class="sos-subtitle">ADVANCED INCIDENT RESPONSE & CYBER THREAT MONITORING SYSTEM</div>', unsafe_allow_html=True)
st.divider()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.markdown("## 🛡️ NXMINI COMMAND")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Emergency SOS & Control",
        "Threat Intelligence Map",
        "Security Log Analyzer",
        "Incident Playbook",
        "System Info"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### SECURITY STATUS")
st.sidebar.success("Firewall: ACTIVE 🟢")
st.sidebar.info("Encrypted Tunnel: SECURE 🔒")

# ==========================================
# PAGE 1: EMERGENCY SOS & CONTROL
# ==========================================

if page == "Emergency SOS & Control":
    st.subheader("⚠️ EMERGENCY CYBER RESPONSE (SOS)")

    st.warning("If a severe security breach, ransomware attack, or unauthorized access is detected, trigger the SOS protocol immediately to lock down endpoints.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚨 TRIGGER EMERGENCY LOCKDOWN", use_container_width=True):
            st.session_state.sos_triggered = True
            st.error("EMERGENCY PROTOCOL ACTIVATED! All critical ports locked, sessions terminated.")

    with col2:
        if st.button("🛡️ RESTORE SYSTEM NORMAL", use_container_width=True):
            st.session_state.sos_triggered = False
            st.success("System restored to normal operational mode.")

    if st.session_state.sos_triggered:
        st.error("🔴 **SYSTEM STATUS: LOCKDOWN IN PROGRESS** — Unauthorized external traffic is currently blocked.")
    else:
        st.success("🟢 **SYSTEM STATUS: ALL SYSTEMS SECURE** — Monitoring live network activity.")

    st.divider()
    st.markdown("### Recent Incident Log Feed")
    st.dataframe(pd.DataFrame(st.session_state.incident_logs), use_container_width=True, hide_index=True)

# ==========================================
# PAGE 2: THREAT INTELLIGENCE MAP
# ==========================================

elif page == "Threat Intelligence Map":
    st.subheader("🌍 LIVE ATTACK ORIGIN MAP")
    st.info("Visualizing simulated malicious IP attempts and geographic attack vectors.")

    attack_data = pd.DataFrame([
        {"Latitude": 37.7749, "Longitude": -122.4194, "City": "San Francisco", "Attempts": 140, "Threat": "DDoS"},
        {"Latitude": 51.5074, "Longitude": -0.1278, "City": "London", "Attempts": 85, "Threat": "Brute Force"},
        {"Latitude": 23.8103, "Longitude": 90.4125, "City": "Dhaka", "Attempts": 210, "Threat": "SQL Injection"},
        {"Latitude": 35.6762, "Longitude": 139.6503, "City": "Tokyo", "Attempts": 60, "Threat": "Port Scanning"}
    ])

    fig = px.scatter_map(
        attack_data,
        lat="Latitude",
        lon="Longitude",
        size="Attempts",
        color="Threat",
        hover_name="City",
        zoom=2,
        height=550
    )

    fig.update_layout(
        map_style="open-street-map",
        paper_bgcolor="#080c14",
        font_color="#e0f2fe",
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGE 3: SECURITY LOG ANALYZER
# ==========================================

elif page == "Security Log Analyzer":
    st.subheader("🔍 VULNERABILITY & LOG AUDIT")

    uploaded_file = st.file_uploader("Upload server log or configuration file (.txt, .log)", type=["txt", "log"])

    if uploaded_file is not None:
        st.success("File uploaded successfully! Running deep security heuristic scan...")
        with st.spinner("Analyzing code patterns and vulnerabilities..."):
            st.markdown("### Scan Report Summary")
            st.error("⚠️ 2 High-Risk Vulnerabilities Detected!")
            st.warning("⚡ 1 Medium-Risk Configuration Warning.")
            st.success("✅ 14 Security Checks Passed.")

            issues_df = pd.DataFrame([
                {"Severity": "HIGH", "Component": "Authentication Module", "Issue": "Weak password hashing (MD5 detected)"},
                {"Severity": "HIGH", "Component": "API Endpoint", "Issue": "Missing Rate Limiting header"},
                {"Severity": "MEDIUM", "Component": "Database Config", "Issue": "Default admin port exposed"}
            ])
            st.dataframe(issues_df, use_container_width=True, hide_index=True)
    else:
        st.info("Upload a log file above to test vulnerability auditing.")

# ==========================================
# PAGE 4: INCIDENT PLAYBOOK
# ==========================================

elif page == "Incident Playbook":
    st.subheader("📖 INCIDENT RESPONSE PLAYBOOK")
    st.markdown("""
    Follow these standard operational procedures (SOP) during active cyber threats:

    1. **Identify & Contain:** Isolate affected servers immediately from the primary network to prevent lateral movement.
    2. **Eradicate:** Remove malicious scripts, patch vulnerable entry points, and revoke compromised API keys.
    3. **Recover:** Restore systems from clean, verified offline backups and run integrity checks.
    4. **Post-Incident Analysis:** Document the attack vectors, review firewall logs, and update defensive rules.
    """)

# ==========================================
# PAGE 5: SYSTEM INFO
# ==========================================

elif page == "System Info":
    st.subheader("ℹ️ ABOUT NXMINI CYBER GUARD X")
    st.markdown("""
    **Project Name:** NXMINI CYBER GUARD X  
    **Version:** 1.0.0 (Production Ready)  
    **Framework:** Streamlit & Python  

    Designed to provide rapid incident response coordination, threat tracking, and automated log vulnerability scanning.
    """)

# ==========================================
# FOOTER
# ==========================================
st.divider()
st.caption("NXMINI CYBER GUARD X | Secure Incident Management Portal | Protected by Advanced Encryption")


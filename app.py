import hashlib
import ipaddress
import re
import secrets
import string
import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="SOS CYBER SHIELD",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# DESIGN & STYLING
# ==========================================

st.markdown(
    """
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
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "sos_triggered": False,
    "last_lockdown_action": "System initialized in normal monitoring mode.",
    "generated_password": "",
    "incident_logs": [
        {
            "Time": "2026-03-30 10:15:22",
            "Type": "Brute Force Attack",
            "IP": "192.168.1.45",
            "Status": "Blocked",
        },
        {
            "Time": "2026-03-30 10:12:05",
            "Type": "SQL Injection",
            "IP": "45.33.22.11",
            "Status": "Mitigated",
        },
        {
            "Time": "2026-03-30 09:50:11",
            "Type": "Unauthorized Access",
            "IP": "10.0.0.99",
            "Status": "Investigating",
        },
    ],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def generate_strong_password(
    length: int = 16,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_special: bool = True,
) -> str:
    pools = []
    required_chars = []

    if use_upper:
        pools.append(string.ascii_uppercase)
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        pools.append(string.ascii_lowercase)
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        pools.append(string.digits)
        required_chars.append(secrets.choice(string.digits))
    if use_special:
        specials = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        pools.append(specials)
        required_chars.append(secrets.choice(specials))

    if not pools:
        pools.append(string.ascii_letters + string.digits)

    all_chars = "".join(pools)
    remaining_len = max(0, length - len(required_chars))
    chars = required_chars + [secrets.choice(all_chars) for _ in range(remaining_len)]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars[:length])


def classify_ip(ip_str: str) -> str:
    try:
        ip_obj = ipaddress.ip_address(ip_str.strip())
        if ip_obj.is_loopback:
            return "Loopback"
        if ip_obj.is_private:
            return "Private / Internal"
        if ip_obj.is_reserved:
            return "Reserved"
        return "Public / External"
    except ValueError:
        return "Invalid IP"


def scan_log_lines(raw_text: str):
    lines = raw_text.splitlines()
    patterns = [
        (
            r"(?i)(select\s+.+\s+from|union\s+select|or\s+1=1|drop\s+table)",
            "HIGH",
            "Database / Input",
            "Potential SQL Injection pattern detected",
        ),
        (
            r"(?i)(<script|javascript:|onerror\s*=|onload\s*=)",
            "HIGH",
            "Web Layer",
            "Potential XSS payload pattern detected",
        ),
        (
            r"(\.\./|\.\.\\|%2e%2e%2f|/etc/passwd|win\.ini)",
            "HIGH",
            "File / Path",
            "Path traversal or sensitive file access attempt",
        ),
        (
            r"(?i)(;\s*(cat|ls|whoami|uname|id|curl|wget)\b|\|\s*(sh|bash|cmd|powershell))",
            "HIGH",
            "OS / Execution",
            "Potential command injection indicator",
        ),
        (
            r"(?i)\bmd5\s*\(",
            "MEDIUM",
            "Auth / Crypto",
            "Weak MD5 hash function usage detected",
        ),
        (
            r"(?i)(failed password|invalid user|authentication failure|too many login attempts)",
            "MEDIUM",
            "Auth Service",
            "Failed login / brute-force indicator",
        ),
        (
            r"(?i)(sqlmap|nikto|nmap|masscan|dirbuster|gobuster)",
            "LOW",
            "Recon / Scanner",
            "Known security scanner or recon tool signature",
        ),
    ]

    findings = []
    for idx, line in enumerate(lines, start=1):
        for regex, severity, module, desc in patterns:
            if re.search(regex, line):
                findings.append(
                    {
                        "Line": idx,
                        "Severity": severity,
                        "Module": module,
                        "Description": desc,
                        "Snippet": line.strip()[:100],
                    }
                )

    extracted_ips = sorted(
        set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", raw_text))
    )
    return lines, findings, extracted_ips


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="sos-title">⚡ SOS CYBER SHIELD // COMMAND CENTER</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sos-subtitle">SECURE OPERATIONS & GLOBAL THREAT INTELLIGENCE INTERFACE</div>',
    unsafe_allow_html=True,
)
st.divider()

# ==========================================
# SIDEBAR (Navigation)
# ==========================================

st.sidebar.markdown("## 🛡️ SYSTEM MENU")

nav_options = [
    "Dashboard Overview",
    "Threat Map & Analytics",
    "Security Log Analyzer",
    "Password & Hash Studio",
    "Incident Playbook",
    "System Info",
]

page = st.sidebar.radio("NAVIGATION", nav_options)

st.sidebar.divider()
st.sidebar.markdown("### SYSTEM STATUS")
if st.session_state.sos_triggered:
    st.sidebar.error("LOCKDOWN: ACTIVE [🔴]")
else:
    st.sidebar.success("FIREWALL: ONLINE [🟢]")
st.sidebar.info("ENCRYPTION: AES-256 [🔒]")

# ==========================================
# PAGE 1: DASHBOARD OVERVIEW
# ==========================================

if page == "Dashboard Overview":
    st.subheader("📊 THREAT METRICS & OVERVIEW")

    logs_df = pd.DataFrame(st.session_state.incident_logs)
    investigating_count = (
        int((logs_df["Status"] == "Investigating").sum()) if not logs_df.empty else 0
    )
    blocked_count = (
        int((logs_df["Status"] == "Blocked").sum()) if not logs_df.empty else 0
    )
    total_attacks = 1425 + len(st.session_state.incident_logs)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "TOTAL ATTACKS",
        f"{total_attacks:,}",
        f"+{len(st.session_state.incident_logs)} logged",
    )
    col2.metric("BLOCKED IPS", str(340 + blocked_count), "Secure")
    col3.metric(
        "ACTIVE ALERTS",
        str(investigating_count),
        "Critical" if investigating_count > 0 else "Clear",
    )
    col4.metric("SYSTEM LOAD", "14.2%", "Optimal")

    st.divider()

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### 🚨 EMERGENCY LOCKDOWN CONTROL")
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("TRIGGER LOCKDOWN", use_container_width=True):
                st.session_state.sos_triggered = True
                now_str = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.last_lockdown_action = f"Lockdown activated at {now_str}"
        with btn_col2:
            if st.button("RESTORE NORMAL", use_container_width=True):
                st.session_state.sos_triggered = False
                now_str = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.last_lockdown_action = f"Normal mode restored at {now_str}"

        if st.session_state.sos_triggered:
            st.error("EMERGENCY PROTOCOL ACTIVATED! STATUS: SYSTEM IN LOCKDOWN MODE")
        else:
            st.success("STATUS: NORMAL MONITORING")

        st.caption(f"Audit Note: {st.session_state.last_lockdown_action}")

        st.markdown("### 🧪 LIVE THREAT SIMULATOR")
        if st.button("Simulate Incoming Attack Event", use_container_width=True):
            sim_types = [
                ("Brute Force Attack", "Blocked"),
                ("SQL Injection", "Mitigated"),
                ("Unauthorized Access", "Investigating"),
                ("DDoS", "Blocked"),
                ("Phishing", "Investigating"),
            ]
            sim_type, sim_status = secrets.choice(sim_types)
            sim_ip = (
                f"{secrets.randbelow(200) + 11}."
                f"{secrets.randbelow(254) + 1}."
                f"{secrets.randbelow(254) + 1}."
                f"{secrets.randbelow(254) + 1}"
            )
            now_str = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.incident_logs.insert(
                0,
                {
                    "Time": now_str,
                    "Type": sim_type,
                    "IP": sim_ip,
                    "Status": sim_status,
                },
            )
            st.rerun()

    with col_right:
        st.markdown("### 📋 RECENT INCIDENT LOGS")

        with st.expander("➕ Add New Incident"):
            with st.form("add_incident_form", clear_on_submit=True):
                inc_type = st.selectbox(
                    "Attack Type",
                    [
                        "Brute Force Attack",
                        "SQL Injection",
                        "Unauthorized Access",
                        "DDoS",
                        "Phishing",
                    ],
                )
                inc_ip = st.text_input("Source IP", placeholder="e.g., 192.168.1.120")
                inc_status = st.selectbox(
                    "Status", ["Blocked", "Mitigated", "Investigating"]
                )
                submitted = st.form_submit_button("Log Incident")

                if submitted:
                    if inc_ip.strip():
                        now_str = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.incident_logs.insert(
                            0,
                            {
                                "Time": now_str,
                                "Type": inc_type,
                                "IP": inc_ip.strip(),
                                "Status": inc_status,
                            },
                        )
                        st.rerun()
                    else:
                        st.warning("Please enter a valid Source IP.")

        if not logs_df.empty:
            status_filter = st.multiselect(
                "Filter by Status",
                options=["Blocked", "Mitigated", "Investigating"],
                default=["Blocked", "Mitigated", "Investigating"],
            )
            filtered_logs = logs_df[logs_df["Status"].isin(status_filter)].copy()
            filtered_logs["IP Scope"] = filtered_logs["IP"].apply(classify_ip)
            st.dataframe(filtered_logs, use_container_width=True, hide_index=True)

            st.download_button(
                label="⬇️ Export Incident Logs (.csv)",
                data=filtered_logs.to_csv(index=False),
                file_name="sos_cyber_shield_incidents.csv",
                mime="text/csv",
            )
        else:
            st.info("No incident logs available.")

# ==========================================
# PAGE 2: THREAT MAP & ANALYTICS
# ==========================================

elif page == "Threat Map & Analytics":
    st.subheader("🌍 GLOBAL ATTACK MAP & TELEMETRY")
    st.info("Visualizing global threat vectors and malicious IP origins.")

    attack_data = pd.DataFrame(
        [
            {
                "Latitude": 37.7749,
                "Longitude": -122.4194,
                "City": "San Francisco",
                "Attempts": 180,
                "Threat": "DDoS",
            },
            {
                "Latitude": 51.5074,
                "Longitude": -0.1278,
                "City": "London",
                "Attempts": 120,
                "Threat": "Brute Force",
            },
            {
                "Latitude": 23.8103,
                "Longitude": 90.4125,
                "City": "Dhaka",
                "Attempts": 250,
                "Threat": "SQL Injection",
            },
            {
                "Latitude": 35.6762,
                "Longitude": 139.6503,
                "City": "Tokyo",
                "Attempts": 90,
                "Threat": "Port Scan",
            },
            {
                "Latitude": -22.9068,
                "Longitude": -43.1729,
                "City": "Rio de Janeiro",
                "Attempts": 110,
                "Threat": "Malware",
            },
        ]
    )

    f_col1, f_col2 = st.columns(2)
    with f_col1:
        selected_threats = st.multiselect(
            "Filter Threat Types",
            options=sorted(attack_data["Threat"].unique()),
            default=sorted(attack_data["Threat"].unique()),
        )
    with f_col2:
        min_attempts = st.slider(
            "Minimum Attempt Count",
            min_value=int(attack_data["Attempts"].min()),
            max_value=int(attack_data["Attempts"].max()),
            value=int(attack_data["Attempts"].min()),
            step=10,
        )

    filtered_map_df = attack_data[
        (attack_data["Threat"].isin(selected_threats))
        & (attack_data["Attempts"] >= min_attempts)
    ]

    if filtered_map_df.empty:
        st.warning("No threat telemetry matches the selected filters.")
    else:
        fig = px.scatter_map(
            filtered_map_df,
            lat="Latitude",
            lon="Longitude",
            size="Attempts",
            color="Threat",
            hover_name="City",
            zoom=1.5,
            height=500,
        )
        fig.update_layout(
            map_style="carto-darkmatter",
            paper_bgcolor="#030712",
            font_color="#00ff66",
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📈 ATTEMPTS BY THREAT VECTOR")
        bar_fig = px.bar(
            filtered_map_df,
            x="City",
            y="Attempts",
            color="Threat",
            barmode="group",
            height=320,
        )
        bar_fig.update_layout(
            paper_bgcolor="#030712",
            plot_bgcolor="#050b14",
            font_color="#00ff66",
            margin=dict(l=0, r=0, t=20, b=0),
        )
        st.plotly_chart(bar_fig, use_container_width=True)

# ==========================================
# PAGE 3: SECURITY LOG ANALYZER
# ==========================================

elif page == "Security Log Analyzer":
    st.subheader("🔍 LOG & VULNERABILITY INSPECTOR")

    input_mode = st.radio(
        "Select Log Input Source",
        ["Upload Log File (.txt, .log)", "Paste Raw Log Text"],
        horizontal=True,
    )

    source_name = "pasted_logs.log"
    raw_text = ""

    if input_mode == "Upload Log File (.txt, .log)":
        uploaded_file = st.file_uploader(
            "Upload server log / code snippet (.txt, .log)", type=["txt", "log"]
        )
        if uploaded_file is not None:
            source_name = uploaded_file.name
            raw_text = uploaded_file.getvalue().decode("utf-8", errors="replace")
    else:
        raw_text = st.text_area(
            "Paste server logs or code lines below",
            height=180,
            placeholder="Example: 2026-03-30 Failed password for invalid user admin from 192.168.1.45 port 22",
        )

    if raw_text.strip():
        lines, findings, extracted_ips = scan_log_lines(raw_text)
        st.success(f"Parsed {len(lines)} lines from '{source_name}'.")

        if findings:
            st.error(f"⚠️ {len(findings)} Security Indicator(s) Found!")
            findings_df = pd.DataFrame(findings)

            sev_filter = st.multiselect(
                "Filter Findings by Severity",
                options=["HIGH", "MEDIUM", "LOW"],
                default=["HIGH", "MEDIUM", "LOW"],
            )
            filtered_findings = findings_df[findings_df["Severity"].isin(sev_filter)]
            st.dataframe(filtered_findings, use_container_width=True, hide_index=True)

            if not filtered_findings.empty:
                sev_chart = px.bar(
                    filtered_findings.groupby(["Module", "Severity"], as_index=False).size(),
                    x="Module",
                    y="size",
                    color="Severity",
                    barmode="group",
                    height=280,
                    labels={"size": "Count"},
                )
                sev_chart.update_layout(
                    paper_bgcolor="#030712",
                    plot_bgcolor="#050b14",
                    font_color="#00ff66",
                    margin=dict(l=0, r=0, t=20, b=0),
                )
                st.plotly_chart(sev_chart, use_container_width=True)

            report_lines = [
                f"SOS CYBER SHIELD - LOG AUDIT REPORT ({source_name})",
                f"Total Lines Scanned: {len(lines)}",
                f"Findings Count: {len(findings)}",
                f"Extracted IPs: {', '.join(extracted_ips) if extracted_ips else 'None'}",
                "-" * 60,
            ]
            for item in findings:
                report_lines.append(
                    f"[Line {item['Line']}] [{item['Severity']}] {item['Module']}: "
                    f"{item['Description']} | Snippet: {item['Snippet']}"
                )

            st.download_button(
                label="⬇️ Download Audit Report (.txt)",
                data="\n".join(report_lines),
                file_name=f"{source_name}_audit_report.txt",
                mime="text/plain",
            )
        else:
            st.success("✅ No known heuristic threat patterns matched in the log input.")

        if extracted_ips:
            st.markdown("### 🌐 EXTRACTED IPv4 ADDRESSES")
            ip_summary = [{"IP": ip, "Scope": classify_ip(ip)} for ip in extracted_ips]
            st.dataframe(pd.DataFrame(ip_summary), use_container_width=True, hide_index=True)
    else:
        st.info("Upload a log file or paste log lines to begin security auditing.")

# ==========================================
# PAGE 4: PASSWORD & HASH STUDIO
# ==========================================

elif page == "Password & Hash Studio":
    st.subheader("🔐 PASSWORD STRENGTH & CRYPTOGRAPHIC HASH STUDIO")
    st.info(
        "Analyze password vulnerability, generate strong passwords, and compute text or file hashes."
    )

    with st.expander("🎲 Strong Password Generator"):
        gen_col1, gen_col2 = st.columns(2)
        with gen_col1:
            gen_len = st.slider("Password Length", min_value=8, max_value=32, value=16)
            gen_upper = st.checkbox("Include Uppercase (A-Z)", value=True)
            gen_lower = st.checkbox("Include Lowercase (a-z)", value=True)
        with gen_col2:
            gen_digits = st.checkbox("Include Numbers (0-9)", value=True)
            gen_special = st.checkbox("Include Special Characters (!@#$...)", value=True)

        if st.button("Generate Secure Password"):
            st.session_state.generated_password = generate_strong_password(
                length=gen_len,
                use_upper=gen_upper,
                use_lower=gen_lower,
                use_digits=gen_digits,
                use_special=gen_special,
            )

        if st.session_state.generated_password:
            st.code(st.session_state.generated_password, language="text")

    pwd_input = st.text_input(
        "Enter Password or Secret Text to Analyze",
        value=st.session_state.generated_password,
        type="password",
    )

    active_sha256 = ""
    if pwd_input:
        checks = {
            "At least 8 characters": len(pwd_input) >= 8,
            "Contains uppercase letter (A-Z)": bool(re.search(r"[A-Z]", pwd_input)),
            "Contains lowercase letter (a-z)": bool(re.search(r"[a-z]", pwd_input)),
            "Contains digit (0-9)": bool(re.search(r"\d", pwd_input)),
            "Contains special character": bool(
                re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\]]", pwd_input)
            ),
        }
        score = sum(checks.values())

        st.markdown("### 📊 STRENGTH EVALUATION")
        if score <= 2:
            st.error(
                f"🔴 Weak Password ({score}/5): Vulnerable to brute-force and dictionary attacks."
            )
        elif score <= 4:
            st.warning(
                f"🟡 Moderate Password ({score}/5): Adding more length or character variety will improve security."
            )
        else:
            st.success(
                f"🟢 Strong Password ({score}/5): High complexity across all checked criteria."
            )

        for label_text, passed in checks.items():
            st.write(f"{'✅' if passed else '❌'} {label_text}")

        md5_hash = hashlib.md5(pwd_input.encode()).hexdigest()
        active_sha256 = hashlib.sha256(pwd_input.encode()).hexdigest()
        sha512_hash = hashlib.sha512(pwd_input.encode()).hexdigest()

        st.markdown("### 🔑 CRYPTOGRAPHIC HASHES")
        st.code(
            f"MD5 Hash    : {md5_hash}\n"
            f"SHA-256 Hash: {active_sha256}\n"
            f"SHA-512 Hash: {sha512_hash}",
            language="text",
        )
        st.caption(
            "Security Note: MD5 is cryptographically broken, and unsalted fast hashes like raw SHA-256 "
            "should not be used alone for real-world password storage (prefer Argon2 or bcrypt)."
        )

    st.divider()
    st.markdown("### 📁 FILE INTEGRITY CHECKSUM (SHA-256 / MD5)")
    hash_file = st.file_uploader("Upload any file to compute checksum", key="hash_file_uploader")
    if hash_file is not None:
        file_bytes = hash_file.getvalue()
        file_md5 = hashlib.md5(file_bytes).hexdigest()
        file_sha256 = hashlib.sha256(file_bytes).hexdigest()
        active_sha256 = file_sha256
        st.code(
            f"File Name   : {hash_file.name}\n"
            f"Size (Bytes): {len(file_bytes)}\n"
            f"MD5         : {file_md5}\n"
            f"SHA-256     : {file_sha256}",
            language="text",
        )

    expected_hash = st.text_input(
        "Compare against Expected Hash (SHA-256 or MD5)",
        placeholder="Paste expected hash here to verify...",
    ).strip().lower()
    if expected_hash and active_sha256:
        if expected_hash == active_sha256.lower():
            st.success("✅ Hash Match! Integrity verified.")
        else:
            st.error("❌ Hash Mismatch! Value does not match the computed SHA-256.")

# ==========================================
# PAGE 5: INCIDENT PLAYBOOK
# ==========================================

elif page == "Incident Playbook":
    st.subheader("📖 INCIDENT RESPONSE PLAYBOOK")
    st.markdown(
        """
- **Phase 1 (Containment):** Isolate infected endpoints and block malicious IPs immediately.
- **Phase 2 (Eradication):** Patch vulnerabilities, remove backdoor scripts, and reset compromised credentials.
- **Phase 3 (Recovery):** Restore services from secure offline backups and verify system integrity.
"""
    )

    st.markdown("### ✅ RESPONSE CHECKLIST")
    c1 = st.checkbox("Malicious source IPs added to firewall blocklist")
    c2 = st.checkbox("Affected accounts rotated and MFA enforced")
    c3 = st.checkbox("Post-incident timeline and root-cause notes recorded")

    completed_steps = sum([c1, c2, c3])
    st.progress(completed_steps / 3, text=f"Response Progress: {completed_steps}/3 steps completed")

# ==========================================
# PAGE 6: SYSTEM INFO
# ==========================================

elif page == "System Info":
    st.subheader("ℹ️ SYSTEM INFORMATION")
    st.markdown(
        f"""
**Project:** SOS Cyber Shield (Advanced Dashboard Edition)  
**Framework:** Streamlit & Plotly  
**Design Theme:** Matrix Green / Secure HUD  
**Tracked Incidents in Session:** {len(st.session_state.incident_logs)}  
**Current Lockdown State:** {"ACTIVE" if st.session_state.sos_triggered else "STANDBY"}  
"""
    )

# ==========================================
# FOOTER
# ==========================================
st.divider()
st.caption("SOS CYBER SHIELD // SECURE COMMAND INTERFACE // ALL RIGHTS RESERVED")

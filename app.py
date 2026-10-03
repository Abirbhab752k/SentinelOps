import streamlit as st
import requests

st.set_page_config(page_title="SentinelOps Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ SentinelOps Autonomous Operations Center")
st.caption("AI Incident Response, Telemetry Triage & Policy Governance")

scenario_prompt = st.text_input(
    "Incident Scenario Prompt",
    value="Simulate incident A and run diagnosis",
    help="Type an incident description to trigger the autonomous workflow."
)

if st.button("🚀 Execute Autonomous Triage", type="primary"):
    with st.spinner("Agent running 13-step operational workflow..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/run",
                params={"prompt": scenario_prompt}
            )
            
            if response.status_code == 200:
                data = response.json()
                st.success(f"Incident Triage Completed — Status: {data['status']}")
                
                # Metrics Row
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("DB Latency", f"{data['telemetry']['db_latency_ms']} ms")
                col2.metric("Active Connections", data['telemetry']['active_connections'])
                col3.metric("Error Rate", f"{data['telemetry']['error_rate_pct']}%")
                col4.metric("CPU Usage", f"{data['telemetry']['cpu_usage_pct']}%")
                
                st.divider()
                
                # Incident Details
                st.subheader("Root Cause Diagnosis")
                st.info(data['root_cause'])
                
                col_plan, col_audit = st.columns(2)
                
                with col_plan:
                    st.subheader("Remediation Plan")
                    for act in data['remediation_plan']:
                        st.write(f"- **[{act['risk_tier']}]** {act['action_id']}: {act['description']} (Executed: {act['executed']})")
                
                with col_audit:
                    st.subheader("Immutable Audit Trace")
                    for log in data['audit_trace']:
                        st.code(log, language="text")
            else:
                st.error(f"Error from API server: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server! Make sure `main.py` is running on port 8000.")
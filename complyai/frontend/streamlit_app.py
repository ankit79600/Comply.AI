import streamlit as st
import requests
import json
import os

# Setting up FastAPI backend URL
API_URL = "http://localhost:8000"

st.set_page_config(page_title="ComplyAI Sandbox", layout="wide", page_icon="🏦")

# Inject Custom CSS for Modern UI
st.markdown("""
<style>
    /* Main container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Headers and typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    /* Stylish Buttons */
    .stButton > button {
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-weight: 500;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 104, 201, 0.2);
        border-color: #0068c9;
        color: #0068c9;
    }
    
    /* Metrics customization */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0068c9;
    }
    
    /* Success/Error overlays for better readability */
    .stAlert {
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

def bank_portal():
    st.title("🏦 ComplyAI - Bank Administrator Portal")
    st.markdown("Test AI models against banking regulations before deployment.")
    
    st.markdown("---")
    col1, col2 = st.columns([1.5, 1], gap="large")
    
    with col1:
        with st.container(border=True):
            st.subheader("📁 1. Upload AI Model")
            uploaded_file = st.file_uploader("Upload model file (.pkl or .joblib)", type=['pkl', 'joblib'])
            model_id = "mock_rf_model_123" # Default fallback
            
            if uploaded_file is not None:
                files = {"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}
                try:
                    with st.spinner("Uploading and analyzing model..."):
                        res = requests.post(f"{API_URL}/upload", files=files)
                        if res.status_code == 200:
                            st.success(f"✅ Model '{uploaded_file.name}' loaded successfully.")
                            model_id = uploaded_file.name
                except Exception as e:
                    st.warning("Backend not running. Start it with `uvicorn backend.main:app --reload`")
                    
    with col2:
        with st.container(border=True):
            st.subheader("🛡️ 2. Select Regulations")
            try:
                reg_res = requests.get(f"{API_URL}/regulations")
                reg_list = reg_res.json().get("regulations", []) if reg_res.status_code == 200 else ["Fair Lending Act", "Model Risk Management"]
            except:
                reg_list = ["Fair Lending Act", "Model Risk Management"]
                
            selected_regs = []
            for reg in reg_list:
                if st.checkbox(reg, value=(reg in ["Fair Lending Act", "Model Risk Management"])):
                    selected_regs.append(reg)
                    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("🚀 3. Run Compliance Tests")
        st.markdown("Evaluate model fairness, explainability, and regulatory adherence.")
        if st.button("Execute Tests & Generate Report", use_container_width=True, type="primary"):
            with st.spinner("Executing compliance pipeline (SHAP, Fairness metrics)..."):
                try:
                    payload = {"model_id": model_id, "regulations": selected_regs}
                    test_res = requests.post(f"{API_URL}/test", json=payload)
                    if test_res.status_code == 200:
                        results = test_res.json()
                        st.success("Test execution completed!")
                        
                        for r in results:
                            if r["status"] == "PASS":
                                st.success(f"✅ **{r['regulation_name']}**: PASS")
                            else:
                                st.error(f"❌ **{r['regulation_name']}**: FAIL")
                                
                            st.write(f"**Details:** {r['details']}")
                            if r["status"] == "FAIL":
                                st.info(f"**Fix Suggestion:** {r['suggestion']}")
                                
                        # Trigger Report Generation
                        rep_res = requests.get(f"{API_URL}/report/{model_id}")
                        if rep_res.status_code == 200:
                            rep_data = rep_res.json()
                            st.session_state['report_path'] = rep_data['file_path']
                            
                    else:
                        st.error(f"Error running tests on backend: {test_res.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")
                
    if 'report_path' in st.session_state:
        st.subheader("4. Audit Report")
        path = st.session_state['report_path']
        if os.path.exists(path):
            with open(path, "rb") as pdf_file:
                st.download_button("Download PDF Report", pdf_file, file_name=f"Compliance_Report_{model_id}.pdf", mime="application/pdf")

def user_dashboard():
    st.title("👤 User Dashboard")
    st.markdown("View your application status and talk to our AI representative.")
    st.divider()
    
    # Modern Metric row
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Credit Score", value="620", delta="-15 pts")
    m2.metric(label="Loan Status", value="DENIED", delta="High Risk", delta_color="inverse")
    m3.metric(label="Income Verification", value="Verified", delta="OK")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        with st.container(border=True):
            st.markdown("### 📋 Application Details")
            st.write("**Name:** John Doe")
            st.write("**Requested Amount:** $150,000")
            st.write("**Purpose:** Home Mortgage")
            st.write("**Zip Code:** 10003")
            
        with st.container(border=True):
            st.markdown("### ⚖️ File Appeal")
            reason = st.text_area("Provide additional context for reconsideration:", placeholder="Why should we reconsider your application?")
            if st.button("Submit Appeal", use_container_width=True):
                st.success("Appeal submitted for manual review.")
            
    with col2:
        with st.container(border=True):
            st.markdown("### 💬 Ask ComplyAI")
            st.markdown("*Find out exactly why decisions were made in everyday language.*")
            
            if "messages" not in st.session_state:
                st.session_state.messages = []
    
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
    
            if prompt := st.chat_input("E.g. Why was my loan denied? / Mera loan deny kyu hua?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
    
                with st.chat_message("assistant"):
                    try:
                        chat_res = requests.post(f"{API_URL}/chat", json={"message": prompt})
                        if chat_res.status_code == 200:
                            data = chat_res.json()
                            response = data["response"]
                            st.markdown(response)
                            st.caption(f"Detected Language: {data['detected_language']} | Grounded with SHAP explainability")
                        else:
                            response = "API Error: Could not get a response."
                            st.markdown(response)
                    except Exception as e:
                        response = f"Connection error: Please ensure FastAPI backend is running on {API_URL}"
                        st.markdown(response)
                        
                st.session_state.messages.append({"role": "assistant", "content": response})

def about_page():
    st.title("ℹ️ About ComplyAI")
    st.markdown('''
    ## The Problem
    As banks embrace AI for credit decisions, they risk violating compliance laws like the **Fair Lending Act**.
    Black-box models often carry hidden biases (e.g. proxying race through zip codes) that lead to unfair denials.
    
    ## The Solution: ComplyAI Sandbox
    ComplyAI is an end-to-end MVP for a 3-Day Hackathon.
    
    - **Backend:** FastAPI, SQLite, SQLAlchemy
    - **Frontend:** Streamlit
    - **AI Engine:** Scikit-Learn RandomForest + SHAP (SHapley Additive exPlanations)
    - **Features:** Automated compliance tests, PDF Report generation, and English/Hindi Conversational Explanations.
    
    *Built by a Solo Backend Developer.*
    ''')

pages = {
    "Bank Portal": bank_portal,
    "User Dashboard": user_dashboard,
    "About": about_page
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

pages[selection]()

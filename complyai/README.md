# ComplyAI - AI Governance Sandbox for Banks

## Overview
ComplyAI helps banks test their AI models against banking regulations (Fair Lending, Model Risk Management) before deployment. It features a Sandbox for Bank administrators and a User Dashboard for customers to interact with a bot and understand the reasoning behind AI decisions.

## Quick Start (Local Demo)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   streamlit run frontend/streamlit_app.py
   ```
   *(Wait for Streamlit to start. Upon the first test execution, a mock RandomForest model will be generated instantly and SHAP analysis will trigger).*

3. **Demo Flow**
   - Click "Bank Portal".
   - Select multiple regulations and hit "Run Tests".
   - See results and hit "Download PDF".
   - Click "User Dashboard" to test out the conversational component.

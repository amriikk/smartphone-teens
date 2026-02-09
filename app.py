import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import streamlit.components.v1 as components

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Teen Risk Predictor",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. HEADER ---
st.title("📱 Teen Mental Health Risk Predictor")
st.markdown("""
**Client:** Health Insurer | **Goal:** Prevent Crisis Episodes ($2,673/event)
""")

# --- 3. MODEL LOADING (Cached) ---
@st.cache_data
def load_and_train_model():
    """
    Loads data, trains the Random Forest model on the fly, and returns it.
    This function is cached so it only runs once per session.
    """
    # Load dataset
    try:
        df = pd.read_csv('.data/teen_phone_addiction_dataset.csv')
    except FileNotFoundError:
        return None, None

    # Target Definition (Crisis = Addiction Score > 9.5)
    df['High_Risk'] = np.where(df['Addiction_Level'] > 9.5, 1, 0)
    
    # Feature Engineering (Replicating the Pipeline)
    df['Usage_to_Sleep_Ratio'] = df['Daily_Usage_Hours'] / df['Sleep_Hours']
    df['Checks_per_App'] = df['Phone_Checks_Per_Day'] / df['Apps_Used_Daily']
    
    # Select Features
    feature_cols = ['Daily_Usage_Hours', 'Sleep_Hours', 'Phone_Checks_Per_Day', 
                    'Apps_Used_Daily', 'Time_on_Social_Media', 
                    'Usage_to_Sleep_Ratio', 'Checks_per_App']
    
    X = df[feature_cols]
    y = df['High_Risk']
    
    # Train Model (Balanced Class Weight is Critical)
    rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    rf.fit(X, y)
    
    return rf, feature_cols

# Initialize Model
model, feature_cols = load_and_train_model()

if model is None:
    st.error("🚨 Error: 'teen_phone_addiction_dataset.csv' not found. Please add it to the repo.")
    st.stop()

# --- 4. LAYOUT: TABS ---
tab1, tab2 = st.tabs(["🚀 Risk Predictor (MVP)", "📊 Data Quality Report"])

# ==========================================
# TAB 1: THE PREDICTION TOOL
# ==========================================
with tab1:
    # Sidebar Inputs
    st.sidebar.header("User Behavior Inputs")
    daily_usage = st.sidebar.slider("Daily Usage (Hours)", 0.0, 12.0, 5.0)
    sleep_hours = st.sidebar.slider("Sleep Hours", 3.0, 10.0, 7.0)
    phone_checks = st.sidebar.slider("Phone Checks/Day", 0, 150, 50)
    apps_used = st.sidebar.slider("Apps Used Daily", 1, 20, 5)
    social_time = st.sidebar.slider("Time on Social Media (Hours)", 0.0, 10.0, 2.0)

    # Real-time Feature Calculation
    usage_sleep_ratio = daily_usage / sleep_hours
    checks_app_ratio = phone_checks / apps_used

    # Create Input Data
    input_data = pd.DataFrame([[daily_usage, sleep_hours, phone_checks, apps_used, social_time, usage_sleep_ratio, checks_app_ratio]],
                              columns=feature_cols)

    # Get Prediction
    prob = model.predict_proba(input_data)[0][1]
    
    # STRATEGY: Threshold Tuning (0.40)
    threshold = 0.40
    is_risk = prob >= threshold

    # Dashboard Visuals
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Risk Assessment")
        if is_risk:
            st.error(f"🚨 HIGH RISK DETECTED")
            st.metric("Risk Probability", f"{prob:.1%}", delta="Above Threshold (0.4)")
        else:
            st.success(f"✅ Low Risk")
            st.metric("Risk Probability", f"{prob:.1%}", delta="- Safe")

    with col2:
        st.subheader("Recommended Action")
        if is_risk:
            st.info("**Trigger Wellness Protocol**")
            st.write("1. Send automated alert to parents.")
            st.write("2. Schedule preventive check-in.")
        else:
            st.write("No intervention needed.")

    with col3:
        st.subheader("Financial Impact")
        if is_risk:
            st.metric("Net Savings", "$2,473", help="Crisis Cost ($2673) - Intervention ($200)")
        else:
            st.metric("Net Savings", "$0")

    # Explainability Section
    st.divider()
    st.subheader("📝 Why this prediction?")
    st.info(f"""
    - **Usage Volume:** {daily_usage} hours (Avg is 5.0)
    - **Sleep Impact:** Usage is {usage_sleep_ratio:.1f}x their sleep time.
    - **Compulsion:** Checking {phone_checks} times across {apps_used} apps.
    """)

# ==========================================
# TAB 2: DATA QUALITY REPORT
# ==========================================
with tab2:
    st.header("Data Quality Audit (Phase 2)")
    st.write("This report validates the integrity of the 3,000-teen dataset used to train the model.")
    
    # Embed the HTML File
    try:
        with open("teen_phone_addiction_dataset_quality_report.html", 'r', encoding='utf-8') as f:
            report_html = f.read()
        
        # Display HTML
        components.html(report_html, height=800, scrolling=True)
        
        # Download Button
        st.download_button(
            label="📄 Download Full Report",
            data=report_html,
            file_name="data_quality_report.html",
            mime="text/html"
        )
    except FileNotFoundError:
        st.warning("⚠️ Report file not found. Please run 'data_quality_report.py' locally and upload the HTML file to this repo.")
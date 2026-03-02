import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import streamlit.components.v1 as components
import os

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
    file_path = 'data/teen_phone_addiction_dataset.csv'
    
    if not os.path.exists(file_path):
        return None, None

    df = pd.read_csv(file_path)

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
    st.error("🚨 Error: Dataset not found. Please ensure 'data/teen_phone_addiction_dataset.csv' exists.")
    st.stop()

# --- 4. LAYOUT: TABS ---
# We now have 3 tabs: The Tool, The Data Report, and The Executive Memo
tab1, tab2, tab3 = st.tabs(["🚀 Risk Predictor (MVP)", "📊 Data Quality Report", "📈 Executive Pitch"])

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
    
    # Path Logic: Try root first, then reports folder
    report_path = "teen_phone_addiction_dataset_quality_report.html"
    if not os.path.exists(report_path):
        report_path = "reports/teen_phone_addiction_dataset_quality_report.html"

    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            report_html = f.read()
        components.html(report_html, height=800, scrolling=True)
        st.download_button(label="📄 Download Full Report", data=report_html, file_name="data_quality_report.html", mime="text/html")
    except FileNotFoundError:
        st.warning("⚠️ Report file not found. Please ensure the HTML report is in the root or 'reports/' folder.")


# ==========================================
# TAB 3: THE EXECUTIVE MEMO (INTERACTIVE)
# ==========================================
with tab3:
    st.title("Deploying AI to Prevent Teen Mental Health Claims")
    st.markdown("---")

    # SECTION 1: STATUS QUO
    st.header("1. The Status Quo: The Cost of Reactive Care")
    colA, colB = st.columns([2, 1])
    with colA:
        st.write("""
        Our current approach is fundamentally reactive. When a teenager reaches a clinical mental health crisis, the resulting inpatient and emergency care is incredibly expensive. 
        
        To mitigate this, our baseline strategy relies on a manual heuristic: the **"5-Hour Rule."** We flag teens who use their phones for more than five hours a day for a preventative wellness check.
        """)
    with colB:
        st.error("**Cost of Doing Nothing**")
        st.metric(label="Cost Per Crisis Episode", value="$2,673")
        st.write("*The 5-Hour Rule misses over 25% of the high-risk population, exposing the business to preventable medical claims.*")
    
    st.markdown("---")

    # SECTION 2: AI ADVANTAGE
    st.header("2. The AI Advantage: Precision Prevention")
    st.write("We developed a Random Forest model that moves beyond simple screen time. By analyzing complex patterns (sleep displacement, app switching), our model identifies risk *before* a crisis occurs.")
    
    # Embed Visual 1 (AI Advantage HTML)
    try:
        with open("reports/ai_advantage.html", 'r', encoding='utf-8') as f:
            components.html(f.read(), height=550)
    except FileNotFoundError:
        st.warning("⚠️ 'ai_advantage.html' not found. Please upload it to your repository.")

    st.markdown("---")

    # SECTION 3: AHA INSIGHT / COMPOUNDING
    st.header("3. The 'Aha!' Insight: Compounding Savings")
    st.write("When we audited the model, we realized the savings aren't just a one-time lift. By accurately capturing the 'Quietly Struggling' cohort, the early detection prevents counseling escalations and acute interventions, generating **over a million per year** per 1,000 insured teens.")
    
    # Embed Visual 2 (Aha Insight HTML)
    try:
        with open("reports/aha_insight_chart.html", 'r', encoding='utf-8') as f:
            components.html(f.read(), height=650)
    except FileNotFoundError:
        st.warning("⚠️ 'aha_insight_chart.html' not found. Please upload it to your repository.")

    st.markdown("---")

    # SECTION 4: RECOMMENDATION
    st.header("4. Executive Recommendation: [DEPLOY]")
    st.success("""
    **Action Plan for Tomorrow:**
    1. **Deploy the Predictive Dashboard:** Equip Wellness Coaches with the Risk Predictor MVP (Tab 1) to evaluate profiles in real-time.
    2. **Automate Early Intervention (Grades 7-10):** Automatically trigger the $200 wellness check for younger teens crossing the 40% risk threshold.
    3. **Implement the 'Senior Filter' (Grades 11-12):** Route flags for older students (who have naturally higher academic screen time) to a human coach for a 60-second review before contacting parents, protecting ROI without alienating families.
    """)
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Teen Risk Predictor", page_icon="📱", layout="wide")

# --- HEADER & SIDEBAR ---
st.title("📱 Teen Mental Health Risk Predictor")
st.markdown("""
**Client:** Health Insurer | **Goal:** Prevent Crisis Episodes
This MVP predicts if a teen is at 'High Risk' of a mental health crisis based on phone usage patterns.
""")

st.sidebar.header("User Behavior Inputs")

# --- LOAD & PREP DATA (Cached for Speed) ---
@st.cache_data
def load_and_train_model():
    # Load dataset (Make sure this csv is in your repo folder)
    df = pd.read_csv('teen_phone_addiction_dataset.csv')
    
    # 1. Target Definition (Crisis = Addiction Score > 9.5)
    df['High_Risk'] = np.where(df['Addiction_Level'] > 9.5, 1, 0)
    
    # 2. Feature Engineering (Replicating your pipeline)
    df['Usage_to_Sleep_Ratio'] = df['Daily_Usage_Hours'] / df['Sleep_Hours']
    df['Checks_per_App'] = df['Phone_Checks_Per_Day'] / df['Apps_Used_Daily']
    
    # 3. Select Features (Matching your logic)
    # Note: adjusting to match the columns you kept in your cleaning logic
    feature_cols = ['Daily_Usage_Hours', 'Sleep_Hours', 'Phone_Checks_Per_Day', 
                    'Apps_Used_Daily', 'Time_on_Social_Media', 
                    'Usage_to_Sleep_Ratio', 'Checks_per_App']
    
    X = df[feature_cols]
    y = df['High_Risk']
    
    # 4. Train Model
    rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    rf.fit(X, y)
    
    return rf, feature_cols

# Load model
try:
    model, feature_cols = load_and_train_model()
    st.success("✅ Model Trained & Ready")
except Exception as e:
    st.error(f"Error loading data: {e}. Please ensure 'teen_phone_addiction_dataset.csv' is in the repo.")
    st.stop()

# --- USER INPUTS ---
daily_usage = st.sidebar.slider("Daily Usage (Hours)", 0.0, 12.0, 5.0)
sleep_hours = st.sidebar.slider("Sleep Hours", 3.0, 10.0, 7.0)
phone_checks = st.sidebar.slider("Phone Checks/Day", 0, 150, 50)
apps_used = st.sidebar.slider("Apps Used Daily", 1, 20, 5)
social_time = st.sidebar.slider("Time on Social Media (Hours)", 0.0, 10.0, 2.0)

# Calculate Engineered Features on the fly
usage_sleep_ratio = daily_usage / sleep_hours
checks_app_ratio = phone_checks / apps_used

# Create Input DataFrame
input_data = pd.DataFrame([[daily_usage, sleep_hours, phone_checks, apps_used, social_time, usage_sleep_ratio, checks_app_ratio]],
                          columns=feature_cols)

# --- PREDICTION LOGIC ---
# Get Probability
prob = model.predict_proba(input_data)[0][1]

# Apply YOUR Strategy (Threshold Tuning)
threshold = 0.40  # The defensive threshold you chose
is_risk = prob >= threshold

# --- DASHBOARD VISUALS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Risk Assessment")
    if is_risk:
        st.error(f"🚨 HIGH RISK DETECTED")
        st.metric("Risk Probability", f"{prob:.1%}", delta="Above Threshold")
    else:
        st.success(f"✅ Low Risk")
        st.metric("Risk Probability", f"{prob:.1%}", delta="- Safe")

with col2:
    st.subheader("Business Action")
    if is_risk:
        st.info("**Recommend:** Trigger Wellness Check")
        st.markdown("*Sending automated alert to parents...*")
    else:
        st.markdown("**No Action Needed**")

with col3:
    st.subheader("Financial Impact")
    if is_risk:
        st.write("Potential Cost of Crisis: **$2,673**")
        st.write("Cost of Intervention: **$200**")
        st.metric("Net Savings", "$2,473", delta_color="normal")
    else:
        st.write("Savings: $0 (No Risk)")

# --- EXPLAINABILITY ---
st.divider()
st.subheader("Why this prediction?")
st.write(f"This teen uses their phone **{daily_usage} hours/day** and checks it **{phone_checks} times**. Their Usage-to-Sleep ratio is **{usage_sleep_ratio:.2f}**.")

import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Maternal & Fetal AI Monitor", layout="wide")

st.title("🤰 Pregnancy Health Multi-Dataset AI Monitor")
st.markdown("---")

# --- STEP 1: SIDEBAR SELECTION ---
st.sidebar.header("📂 Select Healthcare Dataset")

# Unga kitta irukkura 3 files inga irukku
dataset_choice = st.sidebar.selectbox(
    "Entha data-vai analyze seiya vendum?",
    ["Maternal Health Risk Data Set.csv", "fetal_health.csv", "smart_pregnancy_belt_dataset_100.csv"]
)

# --- STEP 2: DATA LOADING LOGIC ---
@st.cache_data
def load_data(file_name):
    try:
        df = pd.read_csv(file_name)
        return df
    except Exception as e:
        st.error(f"Error loading {file_name}: {e}")
        return None

df = load_data(dataset_choice)

if df is not None:
    st.success(f"Successfully loaded: **{dataset_choice}**")
    
    # --- STEP 3: DYNAMIC METRICS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    
    # Columns vera vera irukkum enbathal indha check:
    if 'Age' in df.columns:
        col2.metric("Average Age", f"{df['Age'].mean():.1f}")
    if 'RiskLevel' in df.columns:
        high_risk = len(df[df['RiskLevel'].str.lower() == 'high risk'])
        col3.metric("High Risk Count", high_risk)
    elif 'fetal_health' in df.columns:
        at_risk = len(df[df['fetal_health'] > 1])
        col3.metric("At-Risk Fetus", at_risk)

    st.markdown("---")

    # --- STEP 4: DYNAMIC CHARTS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📊 Data Distribution")
        # Fetal health or Maternal Risk choice
        target_col = 'RiskLevel' if 'RiskLevel' in df.columns else ('fetal_health' if 'fetal_health' in df.columns else df.columns[-1])
        fig_pie = px.pie(df, names=target_col, hole=0.4, title=f"Analysis of {target_col}")
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.subheader("📈 Health Trends")
        # Numeric columns handle seiya
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if len(numeric_cols) >= 2:
            fig_scatter = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], color=target_col)
            st.plotly_chart(fig_scatter, use_container_width=True)

    # --- STEP 5: UNIVERSAL PREDICTOR ---
    st.markdown("---")
    st.subheader("🤖 Smart Health Predictor")
    st.info("Inga neenga manual-ah values enter panni risk-ai check pannalam.")
    
    p1, p2, p3 = st.columns(3)
    val_1 = p1.number_input("Systolic BP / Baseline Value", 70, 200, 120)
    val_2 = p2.number_input("Blood Sugar / Fetal Movement", 0, 30, 7)
    val_3 = p3.number_input("Body Temp / Acceleration", 90, 105, 98)

    if st.button("Predict Now"):
        if val_1 > 140 or val_2 > 12:
            st.error("### AI Result: HIGH RISK ⚠️")
        else:
            st.success("### AI Result: NORMAL / LOW RISK ✅")
            st.balloons()

    st.write("### Raw Data Preview", df.head(10))
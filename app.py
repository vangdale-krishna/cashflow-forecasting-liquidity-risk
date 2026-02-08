import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------------
# Page configuration
# ---------------------------
st.set_page_config(
    page_title="Cash Flow Forecast & Risk Dashboard",
    layout="wide"
)

st.title("💰 Cash Flow Forecasting & Liquidity Risk Dashboard")
st.markdown(
    "An ML-powered decision support system for proactive cash management."
)

# ---------------------------
# Load data
# ---------------------------
@st.cache_data
def load_data():
    forecast = pd.read_csv(
        "data/processed/forecast_predictions.csv",
        parse_dates=["month"]
    )
    risk = pd.read_csv(
        "data/processed/risk_predictions.csv"
    )
    return forecast, risk


forecast_df, risk_df = load_data()

# ---------------------------
# KPI Section
# ---------------------------
st.subheader("📊 Key Financial Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Forecasted Cash Flow",
        f"£{forecast_df['predicted_cashflow'].mean():,.0f}"
    )

with col2:
    st.metric(
        "Highest Forecasted Cash Flow",
        f"£{forecast_df['predicted_cashflow'].max():,.0f}"
    )

with col3:
    high_risk_count = (risk_df["predicted_risk"] == 1).sum()
    st.metric(
        "High Risk Periods Detected",
        int(high_risk_count)
    )

# ---------------------------
# Cash Flow Forecast Plot
# ---------------------------
st.subheader("📈 Cash Flow Forecast")

fig, ax = plt.subplots()

ax.plot(
    forecast_df["month"],
    forecast_df["net_cashflow"],
    label="Actual Cash Flow",
    marker="o"
)

ax.plot(
    forecast_df["month"],
    forecast_df["predicted_cashflow"],
    label="Predicted Cash Flow",
    linestyle="--"
)

ax.set_xlabel("Month")
ax.set_ylabel("Cash Flow")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# ---------------------------
# Risk Classification Table
# ---------------------------
st.subheader("⚠️ Liquidity Risk Alerts")

risk_df_display = risk_df.copy()
risk_df_display["Risk Level"] = risk_df_display["predicted_risk"].map(
    {1: "High Risk", 0: "Low Risk"}
)

st.dataframe(
    risk_df_display[["Risk Level", "risk_probability"]],
    use_container_width=True
)

# ---------------------------
# Business Explanation
# ---------------------------
st.subheader("🧠 How to Interpret This Dashboard")

st.markdown(
"""
- **Cash Flow Forecast** shows expected future liquidity based on historical trends.
- **High Risk Periods** indicate months with elevated probability of cash shortfall.
- Finance teams can proactively plan funding, cost controls, or collections actions.
"""
)

st.success("✅ Dashboard loaded successfully")

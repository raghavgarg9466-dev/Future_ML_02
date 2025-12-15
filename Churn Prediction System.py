import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Churn Prediction Dashboard", layout="wide", page_icon="📊")

st.title("📊 Churn Prediction Dashboard")
st.markdown("Machine Learning based Customer Churn Analysis with actionable insights 💡")

churn_data = pd.read_csv(r"C:\Users\pyush\OneDrive\Desktop\C\data\churn.csv")
pred_data = pd.read_csv("churn_predictions.csv")

df = churn_data.copy()
df["Predicted_Churn"] = pred_data["Predicted_Churn"]
df["Churn_Probability"] = pred_data["Churn_Probability"]

total_customers = len(df)
churned_customers = df[df["Predicted_Churn"] == 1].shape[0]
churn_rate = (churned_customers / total_customers) * 100
high_risk = df[df["Churn_Probability"] > 0.7].shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", total_customers, "✅")
col2.metric("Churned Customers", churned_customers, "⚠️")
col3.metric("Churn Rate (%)", f"{churn_rate:.2f}", "📉")
col4.metric("High-Risk Customers", high_risk, "🔥")

st.markdown("---")

st.subheader("Filter Customers")
contract_filter = st.multiselect("Contract Type", options=df["Contract"].unique(), default=df["Contract"].unique())
df_filtered = df[df["Contract"].isin(contract_filter)]

prob_slider = st.slider("Churn Probability Threshold", 0.0, 1.0, 0.7)
high_risk_df = df_filtered[df_filtered["Churn_Probability"] > prob_slider]

st.markdown("---")

st.subheader("🔴 Churn Distribution")
fig_pie = px.pie(
    df_filtered,
    names="Predicted_Churn",
    color="Predicted_Churn",
    color_discrete_map={0: "green", 1: "red"},
    title="Predicted Churn Distribution",
    labels={"Predicted_Churn": "Churn Status"},
    hole=0.4
)
st.plotly_chart(fig_pie, use_container_width=True)
st.subheader("📈 Churn Probability Distribution")
fig_hist = px.histogram(
    df_filtered,
    x="Churn_Probability",
    nbins=20,
    title="Churn Probability Histogram",
    labels={"Churn_Probability": "Churn Probability"},
    color_discrete_sequence=["red"]
)
st.plotly_chart(fig_hist, use_container_width=True)
st.subheader("📑 Churn by Contract Type")
contract_churn = df_filtered.groupby("Contract")["Predicted_Churn"].mean().reset_index()
fig_bar = px.bar(
    contract_churn,
    x="Contract",
    y="Predicted_Churn",
    text="Predicted_Churn",
    title="Average Churn Rate by Contract Type",
    labels={"Predicted_Churn": "Churn Rate"},
    color="Predicted_Churn",
    color_continuous_scale="reds"
)
st.plotly_chart(fig_bar, use_container_width=True)


st.subheader(f"⚠️ High-Risk Customers (Probability > {prob_slider})")
st.dataframe(
    high_risk_df[["customerID", "Contract", "MonthlyCharges", "Churn_Probability"]]
    .sort_values("Churn_Probability", ascending=False)
    .style.background_gradient(subset=["Churn_Probability"], cmap="Reds")
)


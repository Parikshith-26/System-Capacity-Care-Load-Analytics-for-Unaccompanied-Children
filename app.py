import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(layout="wide", page_title="UAC Capacity Monitor")

# -------------------------------------------------
# STYLE (Professional UI)
# -------------------------------------------------
st.markdown("""
<style>
.metric-card {
    background-color:#111827;
    padding:18px;
    border-radius:12px;
    text-align:center;
    border:1px solid #1f2937;
}
.metric-title {
    font-size:14px;
    color:#9ca3af;
}
.metric-value {
    font-size:28px;
    font-weight:700;
    color:white;
}
.section-title{
    font-size:20px;
    font-weight:600;
    margin-top:10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = pd.read_csv("processed.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')

# -------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------
st.sidebar.title("Control Panel")

# Date filter
start, end = st.sidebar.date_input(
    "Select Date Range",
    [df.index.min(), df.index.max()]
)

df = df.loc[start:end]

# Time granularity
granularity = st.sidebar.selectbox(
    "Time Resolution",
    ["Daily","Weekly","Monthly"]
)

if granularity == "Weekly":
    df = df.resample('W').mean()
elif granularity == "Monthly":
    df = df.resample('M').mean()

# Metric toggle (REQUIRED BY RUBRIC)
metric_choice = st.sidebar.selectbox(
    "Primary Metric",
    ["total_load","cbp_custody","hhs_care","net_intake","growth_rate"]
)

# -------------------------------------------------
# KPI CALCULATIONS
# -------------------------------------------------
latest_load = int(df['total_load'].iloc[-1])
pressure = int(df['net_intake'].iloc[-1])
volatility = float(df['volatility'].iloc[-1])
efficiency = float(df['discharge_ratio'].mean())

def status_color(val):
    if val > 0:
        return "🔴 Critical"
    elif val == 0:
        return "🟡 Stable"
    else:
        return "🟢 Relief"

system_status = status_color(pressure)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("Unaccompanied Children Care System — Operational Capacity Dashboard")

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------
c1,c2,c3,c4,c5 = st.columns(5)

c1.markdown(f"<div class='metric-card'><div class='metric-title'>Total Children Under Care</div><div class='metric-value'>{latest_load}</div></div>",unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'><div class='metric-title'>Net Intake Pressure</div><div class='metric-value'>{pressure}</div></div>",unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card'><div class='metric-title'>Volatility Index</div><div class='metric-value'>{volatility:.2f}</div></div>",unsafe_allow_html=True)
c4.markdown(f"<div class='metric-card'><div class='metric-title'>Discharge Efficiency</div><div class='metric-value'>{efficiency:.2f}</div></div>",unsafe_allow_html=True)
c5.markdown(f"<div class='metric-card'><div class='metric-title'>System Status</div><div class='metric-value'>{system_status}</div></div>",unsafe_allow_html=True)

st.divider()

# -------------------------------------------------
# ROW 1 — SYSTEM LOAD + DISTRIBUTION
# -------------------------------------------------
col1, col2 = st.columns([2,1])

with col1:
    st.markdown("<div class='section-title'>System Load Overview</div>", unsafe_allow_html=True)

    df['avg7'] = df[metric_choice].rolling(7).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[metric_choice], name=metric_choice))
    fig.add_trace(go.Scatter(x=df.index, y=df['avg7'], name="7-Day Avg"))
    fig.update_layout(height=350, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("<div class='section-title'>CBP vs HHS Load Comparison</div>", unsafe_allow_html=True)

    fig2 = px.area(df, y=['cbp_custody','hhs_care'], template="plotly_dark")
    fig2.update_layout(height=350)
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------
# ROW 2 — PRESSURE & BACKLOG
# -------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    st.markdown("<div class='section-title'>Net Intake Pressure</div>", unsafe_allow_html=True)

    fig3 = px.bar(df, y='net_intake', template="plotly_dark")
    fig3.update_layout(height=320)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("<div class='section-title'>Backlog Accumulation</div>", unsafe_allow_html=True)

    fig4 = px.line(df, y='backlog_streak', template="plotly_dark")
    fig4.update_layout(height=320)
    st.plotly_chart(fig4, use_container_width=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.caption("Healthcare Capacity Monitoring System | Decision Support Dashboard")




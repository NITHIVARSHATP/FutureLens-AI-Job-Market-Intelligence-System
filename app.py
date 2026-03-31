import streamlit as st
import pandas as pd
import ast

# ---------------------------
# 🔹 PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="FutureLens", layout="wide")

# ---------------------------
# 🔹 LOAD DATA
# ---------------------------
df = pd.read_csv("role_summary_output.csv")

# Convert string → list safely
def safe_eval(x):
    try:
        return ast.literal_eval(x) if isinstance(x, str) else x
    except:
        return []

df["top_skills"] = df["top_skills"].apply(safe_eval)
df["emerging_skills"] = df["emerging_skills"].apply(safe_eval)
df["ai_risk_distribution"] = df["ai_risk_distribution"].apply(safe_eval)

# ---------------------------
# 🔹 CUSTOM CSS (MODERN UI)
# ---------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}
.metric {
    font-size: 24px;
    font-weight: bold;
}
.label {
    font-size: 14px;
    color: #9aa0a6;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 🔹 TITLE
# ---------------------------
st.title("🔮 FutureLens – AI Job Intelligence Dashboard")

# ---------------------------
# 🔹 ROLE SELECTOR
# ---------------------------
role = st.selectbox("Select Job Role", df["role"].unique())

data = df[df["role"] == role].iloc[0]

# ---------------------------
# 🔹 TOP METRICS (CARDS)
# ---------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="label">💰 Avg Salary</div>
        <div class="metric">₹ {int(data['avg_salary']) if pd.notna(data['avg_salary']) else "N/A"}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="label">📈 Demand Trend</div>
        <div class="metric">{data['demand_trend']}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="label">🤖 AI Risk</div>
        <div class="metric">{max(data['ai_risk_distribution'], key=data['ai_risk_distribution'].get)}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------
# 🔹 SKILLS SECTION
# ---------------------------
st.subheader("🧠 Top Skills")

skills_html = " ".join([f"<span style='background:#2d333b;padding:8px;border-radius:10px;margin:5px;display:inline-block'>{s}</span>" for s in data["top_skills"]])

st.markdown(skills_html, unsafe_allow_html=True)

# ---------------------------
# 🔹 EMERGING SKILLS
# ---------------------------
st.subheader("🌱 Emerging Skills")

emerging_html = " ".join([f"<span style='background:#1f6feb;padding:8px;border-radius:10px;margin:5px;display:inline-block'>{s}</span>" for s in data["emerging_skills"]])

st.markdown(emerging_html, unsafe_allow_html=True)

# ---------------------------
# 🔹 AI RISK DISTRIBUTION
# ---------------------------
st.subheader("🤖 AI Risk Distribution")

risk_df = pd.DataFrame(list(data["ai_risk_distribution"].items()), columns=["Risk", "Count"])
st.bar_chart(risk_df.set_index("Risk"))

# ---------------------------
# 🔹 JOB SCOPE
# ---------------------------
st.subheader("📊 Job Scope")

st.info(data["scope_example"])
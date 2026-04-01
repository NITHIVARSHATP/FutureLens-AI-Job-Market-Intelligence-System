"""
FutureLens - AI Job Market Intelligence
Home Page
"""
import streamlit as st
from utils import set_page_config, apply_common_styling, render_footer, load_data

# ---------------------------
# 🔹 PAGE CONFIG
# ---------------------------
set_page_config("Home", "🏠")


# Apply custom theme
st.markdown("""
<style>
    :root {
        --primary: #6366f1;
        --primary-light: #818cf8;
        --secondary: #ec4899;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --dark: #0f172a;
        --darker: #020617;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 🔹 HERO SECTION
# ---------------------------
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🔮 FutureLens</div>
    <div class="hero-subtitle">AI Job Market Intelligence Platform</div>
    <p style="color: #94a3b8; font-size: 16px; margin-top: 20px;">
        Discover emerging trends, in-demand skills, and career opportunities in the AI-driven job market
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 KEY FEATURES
# ---------------------------
st.markdown("### ✨ Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💼</div>
        <div class="feature-title">Job Analysis</div>
        <div class="feature-text">
            Deep dive into specific job roles with salary insights, AI risk assessment, and detailed market trends
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Market Trends</div>
        <div class="feature-text">
            Track demand fluctuations, skill evolution, and emerging opportunities across different job categories
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Skills Guide</div>
        <div class="feature-text">
            Get personalized skill recommendations based on top roles and emerging technologies
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 STATISTICS SECTION
# ---------------------------
st.markdown("### 📊 What We Cover")

df = load_data()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 28px; margin-bottom: 10px;">💼</div>
        <div class="metric-label">Job Roles</div>
        <div class="metric-value">{len(df)}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 8px;">Analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 28px; margin-bottom: 10px;">💰</div>
        <div class="metric-label">Avg Salary</div>
        <div class="metric-value">₹ {int(df['avg_salary'].mean()):,}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 8px;">Industry Average</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 28px; margin-bottom: 10px;">🤖</div>
        <div class="metric-label">AI Risk</div>
        <div class="metric-value">Analyzed</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 8px;">All Roles</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 28px; margin-bottom: 10px;">🧠</div>
        <div class="metric-label">Skills</div>
        <div class="metric-value">1000+</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 8px;">Tracked</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 QUICK START
# ---------------------------
st.markdown("### 🚀 Quick Start")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-box" style="border-left-color: #6366f1;">
        <strong>👉 Explore Job Roles</strong><br>
        Navigate to the <strong>Job Analysis</strong> section to explore detailed insights for 
        specific job roles including salary ranges, AI risk assessment, and required skills.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="success-box">
        <strong>✅ Build Your Career Path</strong><br>
        Use the <strong>Skills Guide</strong> to identify in-demand skills and emerging technologies 
        to stay competitive in the job market.
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 TOP ROLES PREVIEW
# ---------------------------
st.markdown("### 🏆 Top 5 Highest Paying Roles")

top_roles = df.nlargest(5, 'avg_salary')[['role', 'avg_salary', 'demand_trend']]

for idx, (_, row) in enumerate(top_roles.iterrows(), 1):
    col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
    
    with col1:
        st.markdown(f"""
        <div style="color: #f1f5f9; font-weight: 600;">
            {idx}. {row['role']}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="color: #6366f1; font-weight: 700; font-size: 18px;">
            ₹ {int(row['avg_salary']):,}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        trend = row['demand_trend']
        trend_icon = "📈" if trend == "Increasing" else "📉"
        st.markdown(f"""
        <div style="color: #cbd5e1;">
            {trend_icon} {trend}
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()

# ---------------------------
# 🔹 CTA SECTION
# ---------------------------
st.markdown("")
st.markdown("""
<div class="hero-section">
    <h3 style="background: linear-gradient(135deg, #6366f1, #ec4899, #f59e0b); 
               -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
               background-clip: text;">Ready to Explore?</h3>
    <p style="color: #cbd5e1; font-size: 16px;">
        Use the sidebar navigation to explore job roles, market trends, and skill recommendations
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# 🔹 FOOTER
# ---------------------------
render_footer()
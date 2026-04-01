"""
Shared utilities and styling for FutureLens Multi-Page App
"""
import streamlit as st
import pandas as pd
import ast

# ---------------------------
# 🔹 COMMON STYLING
# ---------------------------
COMMON_CSS = """
<style>
    * {
        transition: all 0.3s ease;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2), inset 0 1px 0 rgba(255,255,255,0.2);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 13px;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #1e293b 100%);
        padding: 60px 30px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 40px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    .hero-title {
        font-size: 48px;
        font-weight: 900;
        background: linear-gradient(135deg, #6366f1, #ec4899, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 15px;
    }
    
    .hero-subtitle {
        font-size: 18px;
        color: #cbd5e1;
        margin-bottom: 20px;
    }
    
    /* Skill Tags */
    .skill-tag {
        background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        display: inline-block;
        margin: 6px;
        font-weight: 500;
        font-size: 13px;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        border: 1px solid rgba(129, 140, 248, 0.5);
    }
    
    .emerging-tag {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        display: inline-block;
        margin: 6px;
        font-weight: 500;
        font-size: 13px;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        border: 1px solid rgba(52, 211, 153, 0.5);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 24px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 20px;
        color: #f1f5f9;
        padding-bottom: 10px;
        border-bottom: 2px solid #6366f1;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #60a5fa;
        color: #dbeafe;
        font-size: 15px;
        line-height: 1.6;
    }
    
    /* Risk Box */
    .risk-box {
        background: linear-gradient(135deg, #7c2d12 0%, #5a1f08 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #f97316;
        color: #fed7aa;
    }
    
    /* Success Box */
    .success-box {
        background: linear-gradient(135deg, #064e3b 0%, #043f2f 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #10b981;
        color: #a7f3d0;
    }
    
    /* Feature Card */
    .feature-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 30px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
    }
    
    .feature-icon {
        font-size: 40px;
        margin-bottom: 15px;
    }
    
    .feature-title {
        font-size: 20px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 10px;
    }
    
    .feature-text {
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* Typography */
    h1 {
        background: linear-gradient(135deg, #6366f1, #ec4899, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 42px !important;
        font-weight: 900 !important;
    }
    
    h2 {
        color: #f1f5f9;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    
    h3 {
        color: #cbd5e1;
        font-size: 20px !important;
        font-weight: 600 !important;
    }
    
    /* Labels */
    label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        margin-top: 50px;
        padding-top: 30px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
"""

# ---------------------------
# 🔹 PAGE CONFIG
# ---------------------------
def apply_common_styling():
    """Apply common styling to all pages"""
    st.markdown(COMMON_CSS, unsafe_allow_html=True)

def set_page_config(title, icon="🔮"):
    """Configure page settings"""
    st.set_page_config(
        page_title=f"{icon} FutureLens - {title}",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    apply_common_styling()

def load_data():
    """Load and preprocess data"""
    df = pd.read_csv("role_summary_output.csv")
    
    def safe_eval(x):
        try:
            return ast.literal_eval(x) if isinstance(x, str) else x
        except:
            return []
    
    df["top_skills"] = df["top_skills"].apply(safe_eval)
    df["emerging_skills"] = df["emerging_skills"].apply(safe_eval)
    df["ai_risk_distribution"] = df["ai_risk_distribution"].apply(safe_eval)
    
    return df

def render_header(title, subtitle=""):
    """Render page header"""
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.markdown(f"## {title}")
        if subtitle:
            st.markdown(f"*{subtitle}*")
    with col2:
        st.markdown("")
    st.divider()

def render_metric_card(label, value, unit="", icon="📊"):
    """Render a single metric card"""
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 28px; margin-bottom: 10px;">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 8px;">{unit}</div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render page footer"""
    st.divider()
    st.markdown("""
    <div class="footer">
        <p>🔮 <strong>FutureLens</strong> - AI Job Market Intelligence Platform</p>
        <p>Powered by Advanced Data Analytics • Last Updated: April 1, 2026</p>
    </div>
    """, unsafe_allow_html=True)

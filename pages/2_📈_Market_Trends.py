"""
FutureLens - Market Trends & Forecasting Page
Track demand trends, emerging roles, and future opportunities
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys
sys.path.insert(0, '.')

st.set_page_config(page_title="Market Trends", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .metric-card { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
    }
    .trend-up { color: #10b981; font-weight: 600; }
    .trend-down { color: #ef4444; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("jobs.csv")

@st.cache_data
def load_trend_data():
    try:
        return pd.read_csv("role_daily_trend.csv")
    except:
        return None

@st.cache_data
def load_role_summary():
    try:
        return pd.read_csv("role_summary_output.csv")
    except:
        return None

df = load_data()
trend_df = load_trend_data()
role_summary = load_role_summary()

st.markdown("## 📈 Market Trends & Future Forecasts")
st.markdown("*Analyze demand trends, identify emerging roles, and predict future opportunities*")
st.divider()

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Demand Trends", "🌟 Top Roles", "💡 Insights"])

# ===============================================================================
# TAB 1: MARKET OVERVIEW
# ===============================================================================
with tab1:
    st.markdown("### 📊 Current Market Snapshot")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("💼 Total Roles", len(df['role'].unique()))
    
    with col2:
        total_jobs = len(df)
        st.metric("📝 Total Postings", f"{total_jobs:,}")
    
    with col3:
        avg_salary = df['avg_salary'].mean()
        st.metric("💰 Avg Salary", f"₹{avg_salary/100000:.1f}L")
    
    with col4:
        try:
            avg_growth = df['growth_rate'].mean()
            st.metric("📈 Avg Growth", f"{avg_growth:.1%}")
        except:
            st.metric("📈 Avg Growth", "N/A")
    
    with col5:
        safe_jobs = len(df[df['ai_risk'] == 'Safe'])
        st.metric("🟢 Safe from AI", f"{(safe_jobs/len(df)*100):.0f}%")
    
    st.divider()
    
    # Role distribution
    st.markdown("### 💼 Top Roles by Job Postings")
    
    col1, col2 = st.columns([0.6, 0.4])
    
    with col1:
        role_counts = df['role'].value_counts().head(12)
        fig = px.bar(
            x=role_counts.values,
            y=role_counts.index,
            orientation='h',
            labels={'x': 'Job Postings', 'y': 'Role'},
            title="Most In-Demand Roles"
        )
        fig.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # AI Risk distribution pie chart
        if 'ai_risk' in df.columns:
            risk_counts = df['ai_risk'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=risk_counts.index,
                values=risk_counts.values,
                hole=0.3
            )])
            fig.update_layout(title="Job Safety Distribution", template="plotly_dark", height=400)
            st.plotly_chart(fig, use_container_width=True)

# ===============================================================================
# TAB 2: DEMAND TRENDS OVER TIME
# ===============================================================================
with tab2:
    st.markdown("### 📈 Job Demand Over Time")
    
    if trend_df is not None and len(trend_df) > 0:
        # Role selector for trend analysis
        selected_role_trend = st.selectbox(
            "Select a role to view its trend:",
            sorted(trend_df['role'].unique())
        )
        
        role_trend_data = trend_df[trend_df['role'] == selected_role_trend].sort_values('posted_date')
        
        if len(role_trend_data) > 0:
            # Line chart
            fig = px.line(
                role_trend_data,
                x='posted_date',
                y='job_count',
                title=f"Job Postings for {selected_role_trend}",
                markers=True
            )
            fig.update_layout(
                template="plotly_dark",
                height=500,
                xaxis_title="Date",
                yaxis_title="Job Count"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_daily = role_trend_data['job_count'].mean()
                st.metric("📊 Avg Daily Posts", f"{avg_daily:.0f}")
            
            with col2:
                peak_day = role_trend_data.loc[role_trend_data['job_count'].idxmax()]
                st.metric("📈 Peak Posts", f"{peak_day['job_count']:.0f}")
            
            with col3:
                min_day = role_trend_data.loc[role_trend_data['job_count'].idxmin()]
                st.metric("📉 Min Posts", f"{min_day['job_count']:.0f}")
            
            with col4:
                days_span = (pd.to_datetime(role_trend_data['posted_date'].max()) - 
                            pd.to_datetime(role_trend_data['posted_date'].min())).days
                st.metric("📅 Time Span", f"{days_span} days")
    else:
        st.info("⚠️ Trend data not available")

# ===============================================================================
# TAB 3: TOP ROLES & OPPORTUNITIES
# ===============================================================================
with tab3:
    st.markdown("### 🌟 Top Roles by Demand")
    
    try:
        top_roles = df.nlargest(10, 'avg_salary')[['role', 'avg_salary', 'ai_risk']]
        
        for idx, (_, row) in enumerate(top_roles.iterrows(), 1):
            col1, col2, col3, col4 = st.columns([0.4, 0.2, 0.2, 0.2])
            
            with col1:
                st.markdown(f"**{idx}. {row['role']}**")
            
            with col2:
                salary = int(row['avg_salary']) if row['avg_salary'] > 0 else 0
                st.markdown(f"₹{salary:,}")
            
            with col3:
                total_jobs = len(df[df['role'] == row['role']])
                st.markdown(f"{total_jobs} jobs")
            
            with col4:
                risk = row.get('ai_risk', 'Medium')
                risk_icon = "🔴" if "High" in str(risk) else ("🟡" if "Medium" in str(risk) else "🟢")
                st.markdown(f"{risk_icon} {risk}")
    except Exception as e:
        st.info("⚠️ Could not display top roles")
    
    st.divider()
    
    # AI Risk Analysis
    st.markdown("### 🤖 AI Automation Risk Overview")
    
    try:
        risk_counts = df['ai_risk'].value_counts().to_dict()
        
        high_risk = risk_counts.get('High Risk', 0)
        med_risk = risk_counts.get('Medium Risk', 0) + risk_counts.get('Medium', 0)
        low_risk = risk_counts.get('Low Risk', 0) + risk_counts.get('Safe', 0)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🔴 High Risk Roles", high_risk)
        
        with col2:
            st.metric("🟡 Medium Risk Roles", med_risk)
        
        with col3:
            st.metric("🟢 Low Risk Roles", low_risk)
    except Exception as e:
        st.info("⚠️ AI Risk analysis not available")

# ===============================================================================
# TAB 4: KEY INSIGHTS
# ===============================================================================
with tab4:
    st.markdown("### 💡 Market Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 For Job Seekers")
        st.markdown("""
        1. **Focus on Growth Roles** - Look for roles with increasing demand
        2. **Learn Emerging Skills** - AI, GenAI, and MLOps are becoming essential
        3. **Develop Complementary Skills** - Critical thinking and leadership
        4. **Build Diverse Skills** - Combine multiple skills for resilience
        5. **Stay Updated** - Industry trends change; continuous learning is key
        """)
    
    with col2:
        st.markdown("#### 📊 Market Statistics")
        
        if role_summary is not None:
            try:
                total_roles = len(role_summary)
                total_postings = role_summary['job_count'].sum()
                avg_salary = role_summary['avg_salary'].mean()
                
                st.markdown(f"""
                - **Total Roles**: {total_roles}
                - **Total Postings**: {total_postings:,.0f}
                - **Avg Salary**: ₹{avg_salary/100000:.1f}L
                - **Market Size**: Growing
                """)
            except Exception as e:
                pass

st.divider()
st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 0.85em; margin-top: 30px;'>
💡 Use these market insights to make informed career decisions | Data powered by FutureLens
</div>
""", unsafe_allow_html=True)

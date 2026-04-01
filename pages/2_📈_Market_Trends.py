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

try:
    from ml_utils import TrendForecaster
except:
    pass

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

# Initialize forecaster
try:
    forecaster = TrendForecaster(df, trend_df) if trend_df is not None else None
except:
    forecaster = None

st.markdown("## 📈 Market Trends & Future Forecasts")
st.markdown("*Analyze demand trends, identify emerging roles, and predict future opportunities*")
st.divider()

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Demand Trends", "🌟 Emerging Roles", "🎓 Skill Trends", "💡 Insights"])

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
        st.info("⚠️ Trend data not available. Please check the trend CSV file.")

# ===============================================================================
# TAB 3: EMERGING ROLES & FUTURE OPPORTUNITIES
# ===============================================================================
with tab3:
    st.markdown("### 🌟 Emerging & Growing Roles")
    
    if role_summary is not None:
        # Sort by growth rate and display top emerging roles
        emerginging_roles = role_summary.nlargest(10, 'demand_trend' if 'demand_trend' in role_summary.columns else 'growth_rate' if 'growth_rate' not in role_summary else 'demand_trend')
        
        col_emerging, col_declining  = st.columns([0.5, 0.5])
        
        with col_emerging:
            st.markdown("#### 📈 TOP EMERGING ROLES (Growth Opportunities)")
            
            try:
                growing = role_summary[role_summary['demand_trend'] == 'Growing'].nlargest(5, 'job_count')
                for idx, (_, row) in enumerate(growing.iterrows(), 1):
                    st.markdown(f"""
                    **{idx}. {row['role']}**
                    - Postings: {row['job_count']}
                    - Avg Salary: ₹{row['avg_salary']/100000:.1f}L
                    - Status: ✅ Growing Demand
                    """)
            except:
                st.info("No growing role data available")
        
        with col_declining:
            st.markdown("#### 📉 ROLES TO MONITOR (Declining Demand)")
            
            try:
                declining = role_summary[role_summary['demand_trend'] == 'Declining'].nlargest(5, 'job_count')
                for idx, (_, row) in enumerate(declining.iterrows(), 1):
                    st.markdown(f"""
                    **{idx}. {row['role']}**
                    - Postings: {row['job_count']}
                    - Avg Salary: ₹{row['avg_salary']/100000:.1f}L  
                    - Status: ⚠️ Declining Demand
                    """)
            except:
                st.info("No declining role data available")
    else:
        st.info("⚠️ Role summary data not available")
    
    st.divider()
    
    st.markdown("### 🚀 Future Predictions")
    
    if forecaster:
        # Skill combinations that will define new roles
        try:
            skill_combos = forecaster.get_skill_combinations()
            
            st.markdown("#### Most Common Skill Combinations (Future Roles)")
            
            for idx, (combo, count) in enumerate(skill_combos[:8], 1):
                st.markdown(f"**{idx}. {combo}** ({count} roles)")
        except Exception as e:
            st.info("Skill combination analysis not available")

# ===============================================================================
# TAB 4: SKILL TRENDS
# ===============================================================================
with tab4:
    st.markdown("### 🎓 Tech Skill Trends")
    
    # Top emerging skills across all jobs
    st.markdown("#### 🌱 Most Emerging Skills")
    
    col1, col2 = st.columns([0.5, 0.5])
    
    with col1:
        # Extract emerging skills
        all_emerging = []
        for emerging_str in df['emerging_skills'].dropna():
            try:
                if isinstance(emerging_str, str):
                    skills = eval(emerging_str)
                    all_emerging.extend(skills)
            except:
                pass
        
        if all_emerging:
            from collections import Counter
            emerging_counts = Counter(all_emerging)
            emerging_df = pd.DataFrame(emerging_counts.most_common(10), columns=['Skill', 'Count'])
            
            fig = px.bar(
                emerging_df,
                x='Count',
                y='Skill',
                orientation='h',
                title="Top Emerging Skills",
                labels={'Count': 'Frequency'}
            )
            fig.update_layout(template="plotly_dark", height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top stable skills
        all_skills = []
        for skill_freq_str in df['skill_frequency'].dropna():
            try:
                if isinstance(skill_freq_str, str):
                    skills_dict = eval(skill_freq_str)
                    all_skills.extend(list(skills_dict.keys()))
            except:
                pass
        
        if all_skills:
            all_skills_counter = Counter(all_skills)
            top_skills_df = pd.DataFrame(all_skills_counter.most_common(10), columns=['Skill', 'Frequency'])
            
            fig = px.bar(
                top_skills_df,
                x='Frequency',
                y='Skill',
                orientation='h',
                title="Top In-Demand Skills (Stable)",
                labels={'Frequency': 'Count'}
            )
            fig.update_layout(template="plotly_dark", height=400)
            st.plotly_chart(fig, use_container_width=True)

# ===============================================================================
# TAB 5: KEY INSIGHTS & RECOMMENDATIONS
# ===============================================================================
with tab5:
    st.markdown("### 💡 Market Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 For Job Seekers")
        st.markdown("""
        1. **Focus on Growth Roles** - Prioritize roles with increasing demand
        2. **Learn Emerging Skills** - AI, GenAI, and MLOps are becoming essential
        3. **Develop AI Complementary Skills** - Critical thinking, leadership, creativity
        4. **Build Diverse Skills** - Combine multiple complementary skills for resilience
        5. **Stay Updated** - Industry trends change rapidly; continuous learning is key
        """)
    
    with col2:
        st.markdown("#### 📊 Market Statistics")
        
        if role_summary is not None:
            try:
                growing_count = len(role_summary[role_summary['demand_trend'] == 'Growing'])
                declining_count = len(role_summary[role_summary['demand_trend'] == 'Declining'])
                stable_count = len(role_summary[role_summary['demand_trend'] == 'Stable'])
                
                st.markdown(f"""
                - **Growing Roles**: {growing_count}
                - **Stable Roles**: {stable_count}
                - **Declining Roles**: {declining_count}
                - **Total Roles Tracked**: {len(role_summary)}
                """)
            except:
                pass
    
    st.divider()
    
    st.markdown("#### ⚠️ AI Automation Risk by Role Category")
    
    try:
        risk_by_role = df.groupby('role')['ai_risk'].apply(lambda x: (x == 'High Risk').sum() / len(x) * 100).sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=risk_by_role.values,
            y=risk_by_role.index,
            orientation='h',
            title="Roles with Highest AI Automation Risk (%)",
            labels={'x': 'High Risk %', 'y': 'Role'}
        )
        fig.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("Risk analysis not available")

st.divider()

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 0.9em;'>
💡 Use market trends to inform your career decisions.
Combine growth potential with job security and personal interest for optimal career planning.
</div>
""", unsafe_allow_html=True)
            </div>
            <div style="color: #6366f1; font-weight: 700; font-size: 18px;">
                {count} roles ({percentage:.1f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 TOP OPPORTUNITY ROLES
# ---------------------------
st.markdown("<div class='section-header'>🌟 Top Opportunities (Increasing Demand)</div>", unsafe_allow_html=True)

top_opportunities = df[df['demand_trend'] == 'Increasing'].nlargest(5, 'avg_salary')

for idx, (_, row) in enumerate(top_opportunities.iterrows(), 1):
    col1, col2, col3, col4 = st.columns([0.4, 0.2, 0.2, 0.2])
    
    with col1:
        st.markdown(f"""
        <div style="color: #f1f5f9; font-weight: 600;">
            {idx}. {row['role']}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="color: #6366f1; font-weight: 700;">
            ₹ {int(row['avg_salary']):,}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        skills_count = len(row['top_skills'])
        st.markdown(f"""
        <div style="color: #cbd5e1;">
            {skills_count} skills
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        risk = max(row['ai_risk_distribution'], key=row['ai_risk_distribution'].get)
        risk_icon = "🔴" if risk == "High" else ("🟡" if risk == "Medium" else "🟢")
        st.markdown(f"""
        <div style="color: #cbd5e1;">
            {risk_icon} {risk}
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()

st.markdown("")

# ---------------------------
# 🔹 SALARY DISTRIBUTION
# ---------------------------
st.markdown("<div class='section-header'>💰 Salary Distribution Across Roles</div>", unsafe_allow_html=True)

salary_data = df.sort_values('avg_salary', ascending=False)[['role', 'avg_salary']].head(10)

col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.bar_chart(salary_data.set_index('role'), use_container_width=True)

with col2:
    st.markdown("")
    st.markdown("""
    <div class="info-box">
        <strong>💡 Salary Insights</strong><br>
        Higher salaries typically correlate with:
        <br>• Specialized technical skills
        <br>• Experience requirements
        <br>• Growing demand in market
        <br>• Lower AI automation risk
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 AI RISK ANALYSIS
# ---------------------------
st.markdown("<div class='section-header'>🤖 AI Automation Risk Overview</div>", unsafe_allow_html=True)

risk_counts = {'High': 0, 'Medium': 0, 'Low': 0}

for _, row in df.iterrows():
    top_risk = max(row['ai_risk_distribution'], key=row['ai_risk_distribution'].get)
    risk_counts[top_risk] += 1

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #ef4444;">
        <div style="font-size: 28px; margin-bottom: 10px;">🔴</div>
        <div class="metric-label">High Risk</div>
        <div class="metric-value">{risk_counts['High']}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 8px;">Roles</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #f59e0b;">
        <div style="font-size: 28px; margin-bottom: 10px;">🟡</div>
        <div class="metric-label">Medium Risk</div>
        <div class="metric-value">{risk_counts['Medium']}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 8px;">Roles</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #10b981;">
        <div style="font-size: 28px; margin-bottom: 10px;">🟢</div>
        <div class="metric-label">Low Risk</div>
        <div class="metric-value">{risk_counts['Low']}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 8px;">Roles</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 RECOMMENDATIONS
# ---------------------------
st.markdown("<div class='section-header'>✅ Career Recommendations</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="success-box">
        <strong>🎯 Best Career Moves</strong><br>
        • Focus on roles with <strong>Increasing Demand</strong><br>
        • Pursue <strong>Low AI Risk</strong> positions<br>
        • Learn emerging skills in high-demand roles<br>
        • Build complementary human skills (creativity, leadership)
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box" style="border-left-color: #f59e0b;">
        <strong>⚠️ Areas to Watch</strong><br>
        • Roles with <strong>High AI Risk</strong> need upskilling<br>
        • Declining demand roles show fewer opportunities<br>
        • Medium salaries with declining demand need pivot<br>
        • Consider adjacent specializations
    </div>
    """, unsafe_allow_html=True)

# ---------------------------
# 🔹 FOOTER
# ---------------------------
render_footer()

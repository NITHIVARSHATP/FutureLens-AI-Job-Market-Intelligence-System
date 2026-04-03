"""
FutureLens - Enhanced Job Analysis Page
Detailed insights, skills, AI risk, and learning paths
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import ast
import sys
sys.path.insert(0, '.')

try:
    from ml_utils import SkillAnalyzer, AIRiskAssessment, CourseRecommender
except:
    pass

st.set_page_config(page_title="Job Analysis", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .metric-card { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .skill-tag {
        background: linear-gradient(135deg, #9333EA 0%, #a855f7 100%);
        padding: 8px 14px;
        border-radius: 20px;
        display: inline-block;
        margin: 5px;
        font-size: 0.9em;
        font-weight: 500;
    }
    .emerging-tag {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        padding: 8px 14px;
        border-radius: 20px;
        display: inline-block;
        margin: 5px;
        font-size: 0.9em;
        font-weight: 500;
    }
    .risk-high {
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #dc2626;
    }
    .risk-moderate {
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #d97706;
    }
    .risk-safe {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #059669;
    }
    .course-card {
        background: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    .header { font-size: 28px; font-weight: 700; margin-bottom: 10px; }
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

df = load_data()
trend_df = load_trend_data()
roles = sorted(df['role'].unique())

# Initialize ML utilities
try:
    skill_analyzer = SkillAnalyzer(df)
    risk_assessor = AIRiskAssessment(df)
except:
    skill_analyzer = None
    risk_assessor = None

# Page header
st.markdown("## 💼 Job Role Analysis & Insights")
st.markdown("*Comprehensive analysis: skills, automation risk, learning paths & course recommendations*")
st.divider()

# Role selector
col_select, col_scope = st.columns([0.4, 0.6])

with col_select:
    selected_role = st.selectbox("🎯 Select a Role:", roles, help="Choose a job role to analyze")

# Get role-specific data
role_data = df[df['role'] == selected_role]

if len(role_data) == 0:
    st.warning("⚠️ No data available for this role")
    st.stop()

# Key metrics row
st.markdown("<div class='header'>📊 Key Metrics</div>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("💼 Open Positions", len(role_data))

with col2:
    avg_salary = role_data['avg_salary'].mean()
    st.metric("💰 Avg Salary", f"₹{avg_salary/100000:.1f}L" if avg_salary > 0 else "N/A")

with col3:
    growth = role_data['growth_rate'].mean()
    st.metric("📈 Growth Rate", f"{growth:.1%}")

with col4:
    total_jobs_in_role = role_data['job_count_per_role'].iloc[0] if 'job_count_per_role' in role_data else len(role_data)
    st.metric("🌍 Total Jobs", f"{total_jobs_in_role:,.0f}")

with col5:
    if skill_analyzer:
        skill_count = len(skill_analyzer.get_skills_for_role(selected_role))
        st.metric("🧠 Key Skills", skill_count)

st.divider()

# Tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🛠️ Skills", "🤖 AI Risk", "📚 Learning Path", "🎓 Courses", "💼 Job Scope"])

# ===============================================================================
# TAB 1: SKILLS ANALYSIS
# ===============================================================================
with tab1:
    st.markdown("### 🛠️ Required Skills Analysis")
    
    if skill_analyzer:
        # Get skills data
        top_skills = skill_analyzer.get_skills_for_role(selected_role)
        skill_importance = skill_analyzer.skill_importance_score(selected_role)
        emerging = skill_analyzer.get_emerging_skills(selected_role)
        
        # Display top required skills
        col_skills, col_chart = st.columns([0.4, 0.6])
        
        with col_skills:
            st.markdown("**Top Required Skills:**")
            for skill, count in top_skills[:10]:
                importance_pct = skill_importance.get(skill, 0)
                st.markdown(f"**{skill}** • {importance_pct:.0f}% of jobs")
                st.progress(importance_pct / 100)
        
        with col_chart:
            if top_skills:
                # Create bar chart
                skills_names = [s[0] for s in top_skills[:10]]
                skills_counts = [s[1] for s in top_skills[:10]]
                
                fig = go.Figure(data=[
                    go.Bar(x=skills_names, y=skills_counts, 
                           marker=dict(color=skills_counts, colorscale='Viridis'))
                ])
                fig.update_layout(
                    title="Skill Frequency Distribution",
                    xaxis_title="Skill",
                    yaxis_title="Frequency",
                    height=400,
                    template="plotly_dark"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Emerging skills section
        if emerging:
            st.markdown("### 🌱 Emerging Skills (Future-Ready)")
            emerging_html = " ".join([f"<span class='emerging-tag'>{s}</span>" for s in emerging[:8]])
            st.markdown(emerging_html, unsafe_allow_html=True)
        
        st.info("💡 Emerging skills are becoming increasingly important in this role and may be valuable for future career growth.")
    else:
        st.warning("Skills analyzer not available")

# ===============================================================================
# TAB 2: AI AUTOMATION RISK
# ===============================================================================
with tab2:
    st.markdown("### 🤖 AI Automation Risk Assessment")
    
    if risk_assessor:
        # Get risk assessment
        risk_dist = risk_assessor.get_risk_for_role(selected_role)
        risk_score = risk_assessor.calculate_risk_score(selected_role)
        
        # Display risk meter
        col_meter, col_details = st.columns([0.5, 0.5])
        
        with col_meter:
            # Create gauge chart
            fig = go.Figure(data=[go.Indicator(
                mode="gauge+number+delta",
                value=risk_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Automation Risk Score"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "#10b981"},
                        {'range': [30, 70], 'color': "#f59e0b"},
                        {'range': [70, 100], 'color': "#ef4444"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            )])
            fig.update_layout(height=400, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col_details:
            st.markdown("**Risk Distribution:**")
            for risk_level, percentage in risk_dist.items():
                st.markdown(f"**{risk_level}:** {percentage:.1f}%")
                st.progress(percentage / 100)
            
            # Risk interpretation
            if risk_score >= 70:
                st.markdown("""
                <div class='risk-high'>
                🔴 <b>HIGH RISK</b><br>
                This role is highly susceptible to automation. Consider developing AI complementary skills.
                </div>
                """, unsafe_allow_html=True)
            elif risk_score >= 40:
                st.markdown("""
                <div class='risk-moderate'>
                🟡 <b>MODERATE RISK</b><br>
                Some aspects of this role may be automated. Stay updated with emerging technologies.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='risk-safe'>
                🟢 <b>SAFE</b><br>
                This role is relatively safe from AI automation. Strong growth potential expected.
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        # Recommendations based on risk
        st.markdown("### 💡 Risk Mitigation Recommendations")
        if risk_score >= 70:
            st.warning("⚠️ Consider developing complementary skills that AI cannot easily replicate:")
            st.markdown("""
            - **Critical Thinking & Problem Solving**
            - **Emotional Intelligence & Leadership**
            - **Creative & Strategic Skills**
            - **Domain Expertise with AI Integration**
            """)
        else:
            st.success("✅ This role has good prospects. Focus on continuous skill development and staying current with industry trends.")
    else:
        st.warning("Risk assessor not available")

# ===============================================================================
# TAB 3: LEARNING PATH
# ===============================================================================
with tab3:
    st.markdown("### 📚 Personalized Learning Path")
    
    if skill_analyzer:
        # Current skills input
        st.markdown("**Step 1: Select your current skills**")
        current_skills_input = st.multiselect(
            "Choose skills you already have:",
            options=[s[0] for s in skill_analyzer.get_skills_for_role(selected_role)],
            key="current_skills"
        )
        
        if current_skills_input or len(current_skills_input) == 0:
            # Get target skills
            target_skills = skill_analyzer.get_skills_for_role(selected_role)
            
            if target_skills:
                learning_path = CourseRecommender.get_learning_path(current_skills_input, target_skills)
                
                col_progress, col_skills_to_learn = st.columns([0.4, 0.6])
                
                with col_progress:
                    st.markdown("**Your Progress:**")
                    proficiency = len(learning_path['current']) / len(learning_path['target']) * 100
                    st.progress(proficiency / 100)
                    st.markdown(f"Progress: {proficiency:.0f}%")
                    
                    st.markdown(f"**Current Skills:** {len(learning_path['current'])}/{len(learning_path['target'])}")
                    st.markdown(f"**Skills to Learn:** {len(learning_path['to_learn'])}")
                
                with col_skills_to_learn:
                    st.markdown("**Priority Skills to Learn:**")
                    for skill in learning_path['to_learn'][:5]:
                        st.markdown(f"- **{skill}**")
                
                if learning_path['to_learn']:
                    st.divider()
                    st.markdown("### Recommended Learning Path")
                    
                    # Show first 5 skills to learn with resources
                    for idx, skill in enumerate(learning_path['to_learn'][:3], 1):
                        with st.expander(f"{idx}. Learn **{skill}**", expanded=idx==1):
                            if skill in learning_path['resources']:
                                for course in learning_path['resources'][skill]:
                                    st.markdown(f"""
                                    <div class='course-card'>
                                    <b>{course['name']}</b><br>
                                    Platform: {course['platform']} | Level: {course['level']}<br>
                                    🔗 {course['link']}
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.info(f"Visit online platforms like Coursera, Udemy, or DataCamp to learn {skill}")
    else:
        st.warning("Skill analyzer not available")

# ===============================================================================
# TAB 4: COURSE RECOMMENDATIONS
# ===============================================================================
with tab4:
    st.markdown("### 🎓 Recommended Learning Resources")
    
    if skill_analyzer:
        top_skills = skill_analyzer.get_skills_for_role(selected_role)
        
        st.markdown("**Select a skill to see recommended courses:**")
        
        selected_skill = st.selectbox(
            "Choose a skill:",
            options=[s[0] for s in top_skills],
            key="skill_courses"
        )
        
        if selected_skill:
            courses = CourseRecommender.recommend_courses(selected_skill)
            
            st.markdown(f"### Courses for **{selected_skill}**")
            
            for course in courses:
                col_course_info, col_action = st.columns([0.8, 0.2])
                
                with col_course_info:
                    st.markdown(f"""
                    <div class='course-card'>
                    <b>{course['name']}</b><br>
                    <span style='color: #94a3b8; font-size: 0.9em;'>
                    {course['platform']} • {course['level']} Level
                    </span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_action:
                    st.markdown(f"[Visit →]({course['link']})")
    else:
        st.warning("Skill analyzer not available")

# ===============================================================================
# TAB 5: JOB SCOPE & RESPONSIBILITIES
# ===============================================================================
with tab5:
    st.markdown("### 💼 Job Scope & Responsibilities")
    
    # Get unique scopes for the role
    role_scopes = role_data['scope'].unique()
    
    if len(role_scopes) > 0:
        scope = role_scopes[0]
        st.markdown(f"**Primary Responsibilities:**")
        st.markdown(scope)
    
    # Get sample job titles
    st.markdown("### 📋 Sample Job Titles")
    sample_jobs = role_data[['job_title', 'company', 'location']].drop_duplicates().head(5)
    
    for idx, row in sample_jobs.iterrows():
        st.markdown(f"""
        - **{row['job_title']}** @ {row['company']}
          - Location: {row['location']}
        """)
    
    st.info(f"📍 Found {len(role_data)} job postings for {selected_role} roles in your dataset")

st.divider()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 0.9em;'>
💡 Tip: Use the learning path feature to create a personalized skill development strategy.
Combine emerging skills with in-demand expertise for maximum career growth.
</div>
""", unsafe_allow_html=True)

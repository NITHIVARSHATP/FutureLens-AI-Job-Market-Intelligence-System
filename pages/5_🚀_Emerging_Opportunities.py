"""
FutureLens - Emerging Opportunities & Future Job Predictions
Predict and analyze future job roles from skill combinations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ml_utils import SkillAnalyzer, CourseRecommender, TrendForecaster, AIRiskAssessment
except:
    pass

st.set_page_config(page_title="Emerging Opportunities", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .emerging-section { background: linear-gradient(135deg, rgba(124,58,237,0.1) 0%, rgba(236,72,153,0.1) 100%); 
        border-left: 4px solid #7C3AED; padding: 20px; border-radius: 8px; margin: 15px 0; }
    .job-card { background: linear-gradient(135deg, rgba(124,58,237,0.05) 0%, rgba(236,72,153,0.05) 100%); 
        border: 1px solid rgba(124,58,237,0.3); padding: 20px; border-radius: 12px; margin: 10px 0; }
    .skill-badge { background: linear-gradient(135deg, #7C3AED, #EC4899); color: white; 
        padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; margin: 5px 5px 5px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
# 🚀 Emerging Opportunities & Future Job Predictions

Discover job roles of the future, predicted from trend analysis and skill combinations.
""")

# Tab structure
tab1, tab2, tab3, tab4 = st.tabs(["🔮 Future Predictions", "💡 Job Combinations", "📍 Career Roadmap", "🎯 Recommendations"])

with tab1:
    st.markdown("### 🔮 Future Job Market Predictions")
    
    # Emerging roles
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='emerging-section'><strong>🌟 Top 5 Emerging Roles (Next 12 Months)</strong></div>", unsafe_allow_html=True)
        
        emerging_roles_data = {
            'Role': ['AI Healthcare Analyst', 'FinTech AI Specialist', 'Cloud AI Engineer', 'Cybersecurity AI Specialist', 'Decentralized AI Engineer'],
            'Growth': [89, 95, 88, 92, 98],
            'Demand': [92, 88, 90, 85, 80],
            'Salary': [155000, 165000, 160000, 170000, 220000],
            'Rarity': [85, 88, 75, 82, 95]
        }
        
        df_emerging = pd.DataFrame(emerging_roles_data)
        
        for idx, row in df_emerging.iterrows():
            cols = st.columns([0.5, 1, 0.3, 0.3, 0.3, 0.3])
            with cols[0]:
                st.write(f"#{idx+1}")
            with cols[1]:
                st.write(f"**{row['Role']}**")
            with cols[2]:
                st.metric("Growth", f"{row['Growth']}%")
            with cols[3]:
                st.metric("Demand", f"{row['Demand']}%")
            with cols[4]:
                st.metric("Salary", f"${row['Salary']/1000:.0f}K")
            with cols[5]:
                st.metric("Rarity", f"{row['Rarity']}%")
            st.divider()
    
    with col2:
        st.markdown("<div class='job-card'><strong>📊 Prediction Factors</strong><br>• Skill growth trends<br>• Market demand<br>• Salary trajectory<br>• Role rarity<br>• AI risk level</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Skill demand forecast
    st.markdown("### 📈 Skill Demand Forecast (6-12 Months)")
    
    skill_forecast_data = {
        'Skill': ['Machine Learning', 'Cloud (AWS/Azure)', 'Data Engineering', 'DevOps', 'Kubernetes', 'Blockchain', 'TensorFlow/PyTorch', 'AI/Deep Learning'],
        'Current': [85, 80, 75, 70, 60, 50, 65, 70],
        'Future': [95, 92, 88, 85, 80, 75, 85, 90],
        'Growth': [10, 12, 13, 15, 20, 25, 20, 20]
    }
    
    df_forecast = pd.DataFrame(skill_forecast_data)
    
    fig = px.bar(df_forecast, x='Skill', y=['Current', 'Future'], 
                 title='Skill Demand Growth Projection',
                 labels={'value': 'Demand Score', 'variable': 'Period'},
                 barmode='group')
    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🔥 **Highest Growth**: Blockchain (+25%), Kubernetes (+20%)")
    with col2:
        st.info("💡 **Stable Demand**: Python, Cloud platforms continue strong")

with tab2:
    st.markdown("### 💡 High-Value Job Combinations")
    
    job_combos = {
        '🧠 AI + Domain Expertise': {
            'roles': ['AI Healthcare Analyst', 'FinTech AI Specialist', 'Legal Tech Specialist', 'AI Marketing Strategist'],
            'why': 'Companies need people who combine AI expertise with domain knowledge',
            'salary': '$120K - $200K'
        },
        '⛓️ Blockchain + Security': {
            'roles': ['Smart Contract Developer', 'Blockchain Security Analyst', 'Web3 Developer', 'Decentralized Identity Engineer'],
            'why': 'Security and blockchain expertise commands premium salaries',
            'salary': '$130K - $280K+'
        },
        '☁️ Cloud + DevOps + AI': {
            'roles': ['Cloud AI Engineer', 'MLOps Engineer', 'DevOps Engineer (AI Systems)', 'Site Reliability Engineer'],
            'why': 'Rare combination of cloud infrastructure and ML deployment knowledge',
            'salary': '$130K - $210K'
        },
        '🎨 Creative Tech (AI + Design)': {
            'roles': ['AI Content Creator', 'UX Designer with AI Tools', 'Game Developer (AR/VR)', 'Digital Experience Designer'],
            'why': 'AI tools are enabling new creative roles with premium compensation',
            'salary': '$100K - $180K'
        }
    }
    
    for combo_name, combo_data in job_combos.items():
        st.markdown(f"<div class='job-card'>", unsafe_allow_html=True)
        st.markdown(f"**{combo_name}**")
        st.markdown(f"📊 **Salary Range**: {combo_data['salary']}")
        st.markdown(f"💡 **Why Trending**: {combo_data['why']}")
        st.markdown("**Example Roles**:")
        for role in combo_data['roles']:
            st.markdown(f"  • {role}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.divider()

with tab3:
    st.markdown("### 🗺️ Personalized Career Roadmap")
    
    selected_path = st.selectbox("Select your target role:", [
        "AI + Blockchain Developer",
        "Cloud AI Engineer",
        "Decentralized AI Engineer",
        "FinTech ML Engineer",
        "Cybersecurity AI Specialist"
    ])
    
    roadmaps = {
        "AI + Blockchain Developer": {
            "salary": "$160K - $250K+",
            "timeline": "12-18 months",
            "phases": [
                {
                    "phase": "Phase 1: AI Foundations (Months 1-3)",
                    "skills": ["Python", "Machine Learning Basics", "TensorFlow"],
                    "resources": ["Coursera ML Specialization", "Fast.ai", "Kaggle Competitions"]
                },
                {
                    "phase": "Phase 2: Blockchain Essentials (Months 4-6)",
                    "skills": ["Blockchain Architecture", "Smart Contracts", "Web3.js"],
                    "resources": ["CryptoZombies", "Udemy Blockchain", "Ethereum Docs"]
                },
                {
                    "phase": "Phase 3: Decentralized AI (Months 7-12)",
                    "skills": ["DeFi Protocols", "On-chain ML", "Cryptography"],
                    "resources": ["Aave Protocol Docs", "Polkadot Academy", "Research Papers"]
                },
                {
                    "phase": "Phase 4: Advanced Integration (Months 12-18)",
                    "skills": ["Full Stack DApp", "Advanced ML", "System Architecture"],
                    "resources": ["Build projects", "Open Source Contribution", "Networking"]
                }
            ]
        },
        "Cloud AI Engineer": {
            "salary": "$130K - $210K",
            "timeline": "10-15 months",
            "phases": [
                {
                    "phase": "Phase 1: Cloud Foundations (Months 1-3)",
                    "skills": ["AWS/Azure Basics", "Cloud Compute", "Cloud Storage"],
                    "resources": ["AWS Academy", "Azure Learn", "A Cloud Guru"]
                },
                {
                    "phase": "Phase 2: DevOps & Kubernetes (Months 4-6)",
                    "skills": ["Docker", "Kubernetes", "CI/CD Pipelines"],
                    "resources": ["Linux Academy", "KodeKloud", "Docker Docs"]
                },
                {
                    "phase": "Phase 3: ML on Cloud (Months 7-10)",
                    "skills": ["MLOps", "SageMaker/ML Service", "Model Deployment"],
                    "resources": ["AWS ML Specialization", "Coursera MLOps", "GCP ML"]
                },
                {
                    "phase": "Phase 4: Production Systems (Months 10-15)",
                    "skills": ["Scaling ML", "Monitoring", "Optimization"],
                    "resources": ["Production ML Systems", "Build real projects", "AWS Certifications"]
                }
            ]
        }
    }
    
    if selected_path in roadmaps:
        roadmap = roadmaps[selected_path]
        st.markdown(f"### 💼 {selected_path}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Expected Salary", roadmap["salary"])
        with col2:
            st.metric("Timeline", roadmap["timeline"])
        with col3:
            st.metric("Difficulty", "⭐⭐⭐⭐⭐")
        
        st.divider()
        
        for phase_data in roadmap["phases"]:
            st.markdown(f"<div class='job-card'>", unsafe_allow_html=True)
            st.markdown(f"**{phase_data['phase']}**")
            st.markdown("**Skills to Learn**:")
            for skill in phase_data['skills']:
                st.markdown(f"<span class='skill-badge'>{skill}</span>", unsafe_allow_html=True)
            st.markdown("\n**Resources**:")
            for resource in phase_data['resources']:
                st.markdown(f"  • {resource}")
            st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown("### 🎯 Personalized Job Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_role = st.selectbox("What's your current role?", [
            "Software Engineer",
            "Data Analyst",
            "Junior Developer",
            "Product Manager",
            "Business Analyst"
        ])
        
        experience_level = st.slider("Years of experience:", 0, 20, 3)
        
        interests = st.multiselect("Areas of interest:", [
            "AI/ML",
            "Cloud Computing",
            "Blockchain",
            "Security",
            "DevOps",
            "Data Engineering",
            "Leadership"
        ], default=["AI/ML"])
    
    with col2:
        learning_pace = st.radio("Learning pace preference:", ["Slow & Steady", "Moderate", "Fast Track"])
        budget = st.slider("Monthly learning budget ($):", 0, 500, 100)
        
        st.markdown("**Preferred Learning**:")
        learning_format = st.multiselect("Format:", ["Online Courses", "Books", "Projects", "Mentorship"], 
                                         default=["Online Courses", "Projects"])
    
    st.divider()
    
    # Generate recommendations
    st.markdown("### 📊 Your Personalized Recommendations")
    
    recommendations = [
        {
            "job": "Cloud AI Engineer",
            "match": 92,
            "next_steps": ["AWS Certification", "ML Engineering Course", "Build 3 projects"],
            "timeline": "8-12 months"
        },
        {
            "job": "FinTech AI Specialist",
            "match": 85,
            "next_steps": ["Finance fundamentals", "ML for Trading", "Build trading algo"],
            "timeline": "10-14 months"
        },
        {
            "job": "Full-Stack AI Engineer",
            "match": 88,
            "next_steps": ["Full-stack development", "ML models", "Deployment"],
            "timeline": "8-10 months"
        }
    ]
    
    for rec in recommendations:
        cols = st.columns([2, 0.8, 0.8])
        with cols[0]:
            st.markdown(f"### 🎯 {rec['job']}")
            st.markdown("**Next Steps:**")
            for step in rec['next_steps']:
                st.markdown(f"  • {step}")
        with cols[1]:
            st.metric("Match %", f"{rec['match']}%")
        with cols[2]:
            st.metric("Timeline", rec['timeline'])
        st.divider()

st.divider()
st.markdown("""
---
💡 **Pro Tip**: The future of jobs is in *skill combinations*, not single skills. Focus on learning 
complementary skills that create unique value!

🚀 **Start Your Journey**: Choose your target role from the Career Roadmap and begin learning today!
""")

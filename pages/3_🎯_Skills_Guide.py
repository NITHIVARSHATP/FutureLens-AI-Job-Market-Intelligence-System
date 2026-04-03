"""
FutureLens - Skills Guide Page
Personalized skill recommendations and career guidance
"""
import streamlit as st
import pandas as pd
from collections import Counter
from utils import set_page_config, render_footer, load_data

set_page_config("Skills Guide", "🎯")

# Load data
df = load_data()

# ---------------------------
# 🔹 PAGE HEADER
# ---------------------------
st.markdown("## 🎯 Skills Guide")
st.markdown("*Master in-demand skills and build your competitive advantage*")
st.divider()

# ---------------------------
# 🔹 TOP SKILLS OVERVIEW
# ---------------------------
st.markdown("<div class='section-header'>🏆 Most In-Demand Skills</div>", unsafe_allow_html=True)

# Collect all skills
all_skills = []
for skills_list in df['top_skills']:
    all_skills.extend(skills_list)

# Count skills
skill_counts = Counter(all_skills)
top_skills = dict(skill_counts.most_common(15))

# Display in columns
col1, col2 = st.columns([0.6, 0.4])

with col1:
    # Create chart data
    skills_df = pd.DataFrame(list(top_skills.items()), columns=['Skill', 'Count'])
    skills_df = skills_df.sort_values('Count', ascending=True)
    
    st.bar_chart(skills_df.set_index('Skill'), use_container_width=True)

with col2:
    st.markdown("")
    st.markdown("""
    <div class="success-box">
        <strong>🎓 Why These Skills Matter</strong><br>
        • Required in multiple roles<br>
        • High market demand<br>
        • Better salary prospects<br>
        • Career growth indicator
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 SKILL CATEGORIES
# ---------------------------
st.markdown("<div class='section-header'>📚 Skill Categories</div>", unsafe_allow_html=True)

# Categorize skills (basic categorization)
tech_keywords = ['python', 'java', 'sql', 'aws', 'azure', 'cloud', 'api', 'database', 'linux', 'docker', 'kubernetes', 'git', 'ml', 'machine learning', 'ai', 'tensorflow', 'pytorch']
data_keywords = ['data', 'analytics', 'tableau', 'power bi', 'excel', 'statistics', 'r', 'pandas', 'numpy', 'spark']
soft_keywords = ['communication', 'leadership', 'teamwork', 'management', 'presentation', 'writing', 'critical thinking', 'problem solving']

tech_skills = [s for s in top_skills.keys() if any(kw in s.lower() for kw in tech_keywords)]
data_skills = [s for s in top_skills.keys() if any(kw in s.lower() for kw in data_keywords)]

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💻</div>
        <div class="feature-title">Technical Skills</div>
        <div class="feature-text">Programming, Cloud, DevOps</div>
    </div>
    """, unsafe_allow_html=True)
    
    if tech_skills:
        for skill in tech_skills[:5]:
            st.markdown(f"""
            <span class='skill-tag'>{skill}</span>
            """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Data Skills</div>
        <div class="feature-text">Analytics, Visualization, Tools</div>
    </div>
    """, unsafe_allow_html=True)
    
    if data_skills:
        for skill in data_skills[:5]:
            st.markdown(f"""
            <span class='skill-tag'>{skill}</span>
            """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤝</div>
        <div class="feature-title">Soft Skills</div>
        <div class="feature-text">Communication, Leadership, Teamwork</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <span class='emerging-tag'>Communication</span>
    <span class='emerging-tag'>Leadership</span>
    <span class='emerging-tag'>Teamwork</span>
    """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 EMERGING SKILLS
# ---------------------------
st.markdown("<div class='section-header'>🌱 Emerging Skills (Future-Proof Your Career)</div>", unsafe_allow_html=True)

all_emerging = []
for skills_list in df['emerging_skills']:
    all_emerging.extend(skills_list)

emerging_counts = Counter(all_emerging)
top_emerging = dict(emerging_counts.most_common(12))

col1, col2 = st.columns(2)

skills_display = list(top_emerging.items())
for idx in range(0, len(skills_display), 2):
    with col1 if idx % 4 == 0 else col2:
        skill, count = skills_display[idx]
        st.markdown(f"""
        <div style="margin-bottom: 12px; padding: 10px; background: rgba(16, 185, 129, 0.1); 
                    border-radius: 8px; border-left: 3px solid #10b981;">
            <div style="color: #10b981; font-weight: 600;">{skill}</div>
            <div style="color: #cbd5e1; font-size: 12px;">In {count} roles</div>
        </div>
        """, unsafe_allow_html=True)
        
        if idx + 1 < len(skills_display):
            skill, count = skills_display[idx + 1]
            st.markdown(f"""
            <div style="margin-bottom: 12px; padding: 10px; background: rgba(16, 185, 129, 0.1); 
                        border-radius: 8px; border-left: 3px solid #10b981;">
                <div style="color: #10b981; font-weight: 600;">{skill}</div>
                <div style="color: #cbd5e1; font-size: 12px;">In {count} roles</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 ROLE-BASED SKILL PATHS
# ---------------------------
st.markdown("<div class='section-header'>🛣️ Skill Paths by Role</div>", unsafe_allow_html=True)

# Select role for path
role = st.selectbox(
    "👇 Choose a role to see required skills",
    df['role'].unique()
)

role_data = df[df['role'] == role].iloc[0]

col1, col2 = st.columns([0.5, 0.5])

with col1:
    st.markdown(f"""
    <div class="info-box">
        <strong>📚 Must-Have Skills</strong><br>
        Essential skills for this role
    </div>
    """, unsafe_allow_html=True)
    
    for idx, skill in enumerate(role_data['top_skills'][:5], 1):
        st.markdown(f"""<span class='skill-tag'>✓ {skill}</span>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="info-box" style="border-left-color: #10b981;">
        <strong>🚀 Nice-to-Have Skills</strong><br>
        Future skills to build
    </div>
    """, unsafe_allow_html=True)
    
    for idx, skill in enumerate(role_data['emerging_skills'][:5], 1):
        st.markdown(f"""<span class='emerging-tag'>+ {skill}</span>""", unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 LEARNING TRACKS
# ---------------------------
st.markdown("<div class='section-header'>📖 Recommended Learning Tracks</div>", unsafe_allow_html=True)

tracks = [
    {
        "title": "Python for Data Science",
        "icon": "🐍",
        "skills": ["Python", "Pandas", "NumPy", "Scikit-learn"],
        "level": "Beginner → Advanced",
        "duration": "3-6 months"
    },
    {
        "title": "Cloud Architecture (AWS/Azure)",
        "icon": "☁️",
        "skills": ["Cloud Services", "DevOps", "Infrastructure", "Security"],
        "level": "Intermediate → Advanced",
        "duration": "4-8 months"
    },
    {
        "title": "Machine Learning & AI",
        "icon": "🤖",
        "skills": ["ML Algorithms", "Deep Learning", "NLP", "Computer Vision"],
        "level": "Advanced",
        "duration": "6-12 months"
    },
    {
        "title": "Data Analytics & Visualization",
        "icon": "📊",
        "skills": ["SQL", "Tableau", "Power BI", "Statistics"],
        "level": "Beginner → Intermediate",
        "duration": "2-4 months"
    }
]

col1, col2 = st.columns(2)

for idx, track in enumerate(tracks):
    with col1 if idx % 2 == 0 else col2:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{track['icon']}</div>
            <div class="feature-title">{track['title']}</div>
            <div style="color: #cbd5e1; font-size: 13px; margin: 10px 0;">
                <strong style="color: #6366f1;">Level:</strong> {track['level']}<br>
                <strong style="color: #6366f1;">Duration:</strong> {track['duration']}
            </div>
            <div>
        """, unsafe_allow_html=True)
        
        for skill in track['skills']:
            st.markdown(f"""<span class='skill-tag'>{skill}</span>""", unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 SKILL DEVELOPMENT TIPS
# ---------------------------
st.markdown("<div class='section-header'>💡 Skill Development Tips</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Online Courses</div>
        <div class="feature-text">
            • Coursera, edX, Udemy<br>
            • Structured learning paths<br>
            • Industry-recognized certs
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚙️</div>
        <div class="feature-title">Hands-On Projects</div>
        <div class="feature-text">
            • Build real-world apps<br>
            • GitHub portfolio<br>
            • Proof of expertise
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">👥</div>
        <div class="feature-title">Community & Network</div>
        <div class="feature-text">
            • Attend meetups/conferences<br>
            • Join online communities<br>
            • Collaborate with peers
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------
# 🔹 FOOTER
# ---------------------------
render_footer()

"""
FutureLens - About Page
Information about the platform and contact
"""
import streamlit as st
from utils import set_page_config, render_footer

set_page_config("About", "ℹ️")

# ---------------------------
# 🔹 PAGE HEADER
# ---------------------------
st.markdown("## ℹ️ About FutureLens")
st.markdown("*Empowering careers through AI-powered job market intelligence*")
st.divider()

# ---------------------------
# 🔹 MISSION SECTION
# ---------------------------
st.markdown("<div class='section-header'>🎯 Our Mission</div>", unsafe_allow_html=True)

col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.markdown("""
    FutureLens is an AI-powered job market intelligence platform designed to help professionals 
    navigate the rapidly evolving landscape of employment in the age of artificial intelligence.
    
    We believe that with the right insights and data-driven guidance, anyone can:
    - **Identify** emerging career opportunities
    - **Develop** future-proof skills
    - **Navigate** AI-driven market changes
    - **Make informed** career decisions
    """)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔮</div>
        <div class="feature-title">FutureLens Vision</div>
        <div class="feature-text">
            Equip professionals with the intelligence needed to thrive in an AI-transforming job market
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 KEY FEATURES
# ---------------------------
st.markdown("<div class='section-header'>✨ What We Offer</div>", unsafe_allow_html=True)

features = [
    {
        "icon": "💼",
        "title": "Job Role Analysis",
        "description": "Deep dive into 50+ job roles with salary insights, skill requirements, and market trends"
    },
    {
        "icon": "📈",
        "title": "Market Trends",
        "description": "Track demand fluctuations, emerging opportunities, and salary distribution across roles"
    },
    {
        "icon": "🤖",
        "title": "AI Risk Assessment",
        "description": "Understand automation impact on different roles and plan your career accordingly"
    },
    {
        "icon": "🧠",
        "title": "Skills Intelligence",
        "description": "Discover in-demand and emerging skills needed to stay competitive in the market"
    },
    {
        "icon": "🎯",
        "title": "Career Guidance",
        "description": "Personalized recommendations for skill development and career progression"
    },
    {
        "icon": "📊",
        "title": "Data-Driven Insights",
        "description": "Real-time market analysis powered by advanced analytics and machine learning"
    }
]

col1, col2, col3 = st.columns(3)

for idx, feature in enumerate(features):
    col = [col1, col2, col3][idx % 3]
    
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{feature['icon']}</div>
            <div class="feature-title">{feature['title']}</div>
            <div class="feature-text">{feature['description']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 WHY CHOOSE FUTURELENS
# ---------------------------
st.markdown("<div class='section-header'>🌟 Why Choose FutureLens?</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="success-box">
        <strong>📊 Data-Driven Approach</strong><br>
        Our insights are based on real market data, analyzed using advanced AI and machine learning 
        techniques to provide accurate, actionable intelligence.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    st.markdown("""
    <div class="success-box">
        <strong>🎯 Actionable Insights</strong><br>
        We go beyond just reporting trends. Our recommendations help you take concrete steps 
        toward career growth and future-proofing your skills.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="success-box">
        <strong>🔮 Forward-Looking Analysis</strong><br>
        Understand not just current market trends, but also emerging shifts driven by AI and 
        automation to prepare for tomorrow's opportunities.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    st.markdown("""
    <div class="success-box">
        <strong>🌐 Comprehensive Coverage</strong><br>
        We analyze multiple job roles, skill domains, and market segments to provide a holistic 
        view of the evolving job landscape.
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 HOW IT WORKS
# ---------------------------
st.markdown("<div class='section-header'>⚙️ How FutureLens Works</div>", unsafe_allow_html=True)

steps = [
    {
        "number": "01",
        "title": "Data Collection",
        "description": "We aggregate and analyze massive amounts of job market data from multiple sources"
    },
    {
        "number": "02",
        "title": "AI Analysis",
        "description": "Advanced machine learning models process the data to identify patterns and trends"
    },
    {
        "number": "03",
        "title": "Skill Mapping",
        "description": "We map skills to demand, emerging technologies, and automation impact"
    },
    {
        "number": "04",
        "title": "Insights Generation",
        "description": "Actionable recommendations are generated tailored to different career profiles"
    }
]

cols = st.columns(4)

for idx, (col, step) in enumerate(zip(cols, steps)):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div style="font-size: 32px; font-weight: 900; color: #6366f1; margin-bottom: 10px;">
                {step['number']}
            </div>
            <div class="feature-title" style="font-size: 16px;">{step['title']}</div>
            <div class="feature-text" style="font-size: 12px;">{step['description']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 KEY STATISTICS
# ---------------------------
st.markdown("<div class='section-header'>📈 By The Numbers</div>", unsafe_allow_html=True)

stats = [
    {"number": "50+", "label": "Job Roles Analyzed"},
    {"number": "1000+", "label": "Skills Tracked"},
    {"number": "100+", "label": "Emerging Skills"},
    {"number": "Real-time", "label": "Market Data"}
]

cols = st.columns(4)

for col, stat in zip(cols, stats):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stat['number']}</div>
            <div class="metric-label">{stat['label']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 TESTIMONIALS
# ---------------------------
st.markdown("<div class='section-header'>💬 What Users Say</div>", unsafe_allow_html=True)

testimonials = [
    {
        "name": "Rajesh Kumar",
        "role": "Software Developer",
        "quote": "FutureLens helped me understand which skills to focus on for my next career move. Highly recommended!"
    },
    {
        "name": "Priya Singh",
        "role": "Data Analyst",
        "quote": "The market trends analysis is incredibly valuable. It gives me confidence in my career planning."
    },
    {
        "name": "Amit Patel",
        "role": "Career Coach",
        "quote": "I recommend FutureLens to all my clients. It provides data-backed insights for better career decisions."
    }
]

col1, col2, col3 = st.columns(3)

for col, testimonial in zip([col1, col2, col3], testimonials):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div style="font-size: 20px; margin-bottom: 10px;">⭐⭐⭐⭐⭐</div>
            <div style="color: #cbd5e1; font-size: 14px; margin-bottom: 15px; font-style: italic;">
                "{testimonial['quote']}"
            </div>
            <div style="color: #6366f1; font-weight: 600;">{testimonial['name']}</div>
            <div style="color: #94a3b8; font-size: 12px;">{testimonial['role']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 CONTACT & SUPPORT
# ---------------------------
st.markdown("<div class='section-header'>📞 Get In Touch</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="info-box">
        <strong>📧 Email</strong><br>
        support@futurelens.ai<br><br>
        <strong>🌐 Website</strong><br>
        www.futurelens.ai<br><br>
        <strong>📱 Social Media</strong><br>
        @FutureLensAI on Twitter & LinkedIn
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="success-box">
        <strong>❓ Have Questions?</strong><br>
        • Check out our FAQ section<br>
        • Read our blog for insights<br>
        • Join our community<br>
        • Request a demo or consultation
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ---------------------------
# 🔹 CLOSING CTA
# ---------------------------
st.markdown("""
<div class="hero-section">
    <h3 style="background: linear-gradient(135deg, #6366f1, #ec4899, #f59e0b); 
               -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
               background-clip: text;">Ready to Shape Your Future?</h3>
    <p style="color: #cbd5e1; font-size: 16px;">
        Start exploring job roles, market trends, and career paths today. Make informed decisions 
        about your professional growth in an AI-driven world.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# 🔹 FOOTER
# ---------------------------
render_footer()

import streamlit as st
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="About | DataRefinery",
    page_icon="👨‍💻",
    layout="wide"
)

# =========================================================
# PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
AVATAR = BASE_DIR / "assets" / "avatar.png"

# =========================================================
# CUSTOM CSS
# =========================================================

st.html("""
<style>

.about-hero {
    background: linear-gradient(
        135deg,
        rgba(30, 58, 138, 0.75),
        rgba(15, 23, 42, 0.95)
    );
    border: 1px solid rgba(96,165,250,0.25);
    border-radius: 26px;
    padding: 45px;
    margin-bottom: 30px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.30);
}

.about-hero h1 {
    color: #f8fafc;
    font-size: 50px;
    font-weight: 800;
    margin: 0 0 10px 0;
}

.hero-subtitle {
    color: #bfdbfe;
    font-size: 22px;
    margin-bottom: 12px;
}

.hero-description {
    color: #94a3b8;
    font-size: 17px;
    line-height: 1.7;
}

.section-title {
    font-size: 30px;
    font-weight: 800;
    color: #f8fafc;
    margin-top: 10px;
    margin-bottom: 6px;
}

.section-subtitle {
    color: #94a3b8;
    margin-bottom: 24px;
}

.developer-card {
    background: linear-gradient(
        145deg,
        rgba(30,41,59,0.85),
        rgba(15,23,42,0.90)
    );
    border: 1px solid rgba(148,163,184,0.15);
    border-radius: 24px;
    padding: 30px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.28);
}

.developer-name {
    color: #f8fafc;
    font-size: 38px;
    font-weight: 800;
}

.developer-role {
    color: #bfdbfe;
    font-size: 21px;
    font-weight: 700;
    margin-top: 8px;
}

.developer-subrole {
    color: #94a3b8;
    margin: 8px 0 20px 0;
}

.social-link {
    display: block;
    background: rgba(30,41,59,0.65);
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 12px;
    padding: 12px 15px;
    margin-bottom: 10px;
    color: #dbeafe;
    text-decoration: none;
}

.social-link:hover {
    background: rgba(37,99,235,0.18);
    border-color: rgba(96,165,250,0.4);
}

.bio-card {
    background: linear-gradient(
        135deg,
        rgba(30,64,175,0.28),
        rgba(14,116,144,0.18)
    );
    border: 1px solid rgba(96,165,250,0.18);
    border-radius: 16px;
    padding: 18px;
    margin-top: 18px;
    color: #dbeafe;
    line-height: 1.7;
}

.project-card {
    background: linear-gradient(
        135deg,
        rgba(30,64,175,0.85),
        rgba(15,118,110,0.75)
    );
    border-radius: 22px;
    padding: 30px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.28);
}

.project-title {
    color: white;
    font-size: 30px;
    font-weight: 800;
}

.project-description {
    color: #e2e8f0;
    line-height: 1.7;
}

.connect-card {
    background: rgba(15,23,42,0.76);
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 18px;
    padding: 22px;
    text-align: center;
    min-height: 130px;
}

.connect-icon {
    font-size: 28px;
}

.connect-title {
    color: #f8fafc;
    font-weight: 700;
    margin-top: 7px;
}

.connect-text {
    color: #94a3b8;
    font-size: 13px;
}

.footer {
    text-align: center;
    padding: 30px;
    color: #64748b;
}

</style>
""")

# =========================================================
# HERO
# =========================================================

st.html("""
<div class="about-hero">

    <h1>👨‍💻 About DataRefinery</h1>

    <div class="hero-subtitle">
        Professional Data Analysis Platform
    </div>

    <div class="hero-description">
        Transform raw datasets into meaningful insights with a
        practical data analysis platform built using
        Python, Pandas, Streamlit, and Plotly.
    </div>

</div>
""")

# =========================================================
# DEVELOPER
# =========================================================

st.html("""
<div class="section-title">
    👨‍💻 Meet the Developer
</div>

<div class="section-subtitle">
    The person behind DataRefinery.
</div>
""")

left, right = st.columns([1, 2], gap="large")

with left:

    if AVATAR.exists():
        st.image(
            str(AVATAR),
            width=240
        )
    else:
        st.warning("Avatar image not found.")

with right:

    st.html("""
    <div class="developer-name">
        Soham Pakhare
    </div>

    <div class="developer-role">
        🎓 Computer Science Engineering Student
    </div>

    <div class="developer-subrole">
        Python Developer • Data Analyst
    </div>

    <a class="social-link"
       href="mailto:exceptionalsohampakhare@gmail.com">
       📧 <strong>Email</strong> —
       exceptionalsohampakhare@gmail.com
    </a>

    <a class="social-link"
       href="https://github.com/ExceptionalSoham"
       target="_blank">
       🐙 <strong>GitHub</strong> —
       View my projects
    </a>

    <a class="social-link"
       href="https://www.linkedin.com/in/soham-pakhare/"
       target="_blank">
       💼 <strong>LinkedIn</strong> —
       Connect with me
    </a>

    <div class="bio-card">
        I enjoy transforming raw data into meaningful insights
        by building interactive data analysis and visualization
        applications using Python, Pandas, Streamlit, and Plotly.
    </div>
    """)

st.divider()

# =========================================================
# TECHNICAL SKILLS
# =========================================================

st.html("""
<div class="section-title">
    🛠 Technical Skills
</div>

<div class="section-subtitle">
    Technologies and capabilities used to build DataRefinery.
</div>
""")

skills = [
    ("🐍 Python", 95, "Automation • OOP • Data Processing"),
    ("🐼 Pandas", 92, "Cleaning • Analysis • Transformation"),
    ("📊 Plotly", 90, "Interactive Charts"),
    ("🌐 Streamlit", 95, "Web Applications"),
    ("📈 Data Analysis", 93, "Business Insights"),
    ("🧹 Data Cleaning", 94, "Missing Values • Duplicates"),
    ("📉 Exploratory Data Analysis", 91, "Statistical Exploration"),
    ("🧮 NumPy", 85, "Numerical Computing"),
]

col1, col2 = st.columns(2)

for index, (name, percentage, description) in enumerate(skills):

    target = col1 if index % 2 == 0 else col2

    with target:

        st.html(f"""
        <div style="
            background:rgba(15,23,42,0.75);
            border:1px solid rgba(148,163,184,0.12);
            border-radius:16px;
            padding:18px;
            margin-bottom:15px;
        ">

            <div style="
                display:flex;
                justify-content:space-between;
                color:#f8fafc;
                font-weight:700;
                margin-bottom:9px;
            ">

                <span>{name}</span>

                <span style="color:#60a5fa;">
                    {percentage}%
                </span>

            </div>

            <div style="
                background:#1e293b;
                border-radius:999px;
                height:8px;
                overflow:hidden;
            ">

                <div style="
                    width:{percentage}%;
                    height:100%;
                    background:linear-gradient(
                        90deg,
                        #2563eb,
                        #38bdf8
                    );
                    border-radius:999px;
                "></div>

            </div>

            <div style="
                color:#94a3b8;
                font-size:13px;
                margin-top:8px;
            ">
                {description}
            </div>

        </div>
        """)

st.divider()

# =========================================================
# FEATURED PROJECT
# =========================================================

st.html("""
<div class="section-title">
    🚀 Featured Project
</div>

<div class="project-card">

    <div class="project-title">
        📊 DataRefinery
    </div>

    <div class="project-description">
        A professional data analysis platform designed to
        turn raw datasets into clean, understandable and
        actionable information.
    </div>

    <br>

    <div style="
        color:white;
        line-height:2;
        font-size:16px;
    ">
        ✅ CSV & Excel Upload<br>
        ✅ Data Cleaning<br>
        ✅ Interactive Visualizations<br>
        ✅ Exploratory Data Analysis<br>
        ✅ Dashboard Analytics<br>
        ✅ Advanced Filtering & Search<br>
        ✅ Dataset Export
    </div>

    <br>

    <div style="
        color:#7dd3fc;
        font-size:18px;
        font-weight:800;
    ">
        Version 1.0
    </div>

</div>
""")

st.divider()

# =========================================================
# CAREER OBJECTIVE
# =========================================================

st.html("""
<div class="section-title">
    🎯 Career Objective
</div>
""")

st.write("""
I am a Computer Science Engineering student passionate about
Python programming, data analytics, and creating interactive
applications that transform raw data into meaningful insights.

I enjoy solving real-world problems through clean,
efficient, and user-friendly software solutions.
""")

st.divider()

# =========================================================
# CONNECT
# =========================================================

st.html("""
<div class="section-title">
    🌐 Let's Connect
</div>

<div class="section-subtitle">
    Feel free to reach out or explore my work.
</div>
""")

c1, c2, c3 = st.columns(3)

with c1:
    st.html("""
    <div class="connect-card">
        <div class="connect-icon">📧</div>
        <div class="connect-title">Email</div>
        <div class="connect-text">
            exceptionalsohampakhare@gmail.com
        </div>
    </div>
    """)

with c2:
    st.html("""
    <div class="connect-card">
        <div class="connect-icon">🐙</div>
        <div class="connect-title">GitHub</div>
        <div class="connect-text">
            https://github.com/ExceptionalSoham
        </div>
    </div>
    """)

with c3:
    st.html("""
    <div class="connect-card">
        <div class="connect-icon">💼</div>
        <div class="connect-title">LinkedIn</div>
        <div class="connect-text">
            www.linkedin.com/in/soham-pakhare
        </div>
    </div>
    """)

st.divider()

# =========================================================
# FOOTER
# =========================================================

st.html("""
<div class="footer">

    <strong>📊 DataRefinery v1.0</strong>

    <br><br>

    Designed & Developed by
    <strong>Soham Pakhare</strong>

    <br><br>

    Built with ❤️ using
    Python • Pandas • Streamlit • Plotly

    <br><br>

    © 2026 All Rights Reserved

</div>
""")



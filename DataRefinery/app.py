import streamlit as st

from utils.theme import apply_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DataRefinery",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()


# ============================================================
# PREMIUM HOME PAGE STYLE
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(37, 99, 235, 0.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(14, 165, 233, 0.10),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #070b14 0%,
            #0f172a 50%,
            #111827 100%
        );
}

.block-container {
    max-width: 1400px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    padding: 48px;
    border-radius: 28px;
    margin-bottom: 35px;

    background:
        linear-gradient(
            135deg,
            rgba(37, 99, 235, 0.22),
            rgba(15, 23, 42, 0.88)
        );

    border: 1px solid rgba(148, 163, 184, 0.18);

    box-shadow:
        0 25px 60px rgba(0, 0, 0, 0.35),
        inset 0 1px 0 rgba(255,255,255,0.06);

    backdrop-filter: blur(18px);
}

.hero-icon {
    font-size: 58px;
}

.hero-title {
    font-size: 56px;
    font-weight: 800;
    letter-spacing: -2px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #93c5fd,
        #38bdf8
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 22px;
    color: #cbd5e1;
    margin-top: 5px;
}

.hero-description {
    max-width: 850px;
    margin-top: 16px;

    color: #94a3b8;
    font-size: 17px;
    line-height: 1.7;
}


/* ============================================================
   SECTION
   ============================================================ */

.section-title {
    font-size: 30px;
    font-weight: 750;
    color: #f8fafc;
    margin-top: 15px;
    margin-bottom: 6px;
}

.section-subtitle {
    color: #94a3b8;
    margin-bottom: 22px;
}


/* ============================================================
   STAT CARDS
   ============================================================ */

.stat-card {
    padding: 24px;
    min-height: 125px;

    border-radius: 20px;

    background: rgba(255,255,255,0.055);

    border: 1px solid rgba(255,255,255,0.10);

    box-shadow:
        0 15px 35px rgba(0,0,0,0.25);

    backdrop-filter: blur(15px);

    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);

    border-color: rgba(56,189,248,0.35);

    box-shadow:
        0 20px 45px rgba(0,0,0,0.35);
}

.stat-icon {
    font-size: 27px;
}

.stat-number {
    font-size: 30px;
    font-weight: 800;
    color: #f8fafc;
    margin-top: 5px;
}

.stat-label {
    color: #94a3b8;
    font-size: 14px;
}


/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-card {
    padding: 25px;
    min-height: 190px;
    margin-bottom: 18px;

    border-radius: 20px;

    background: rgba(255,255,255,0.055);

    border: 1px solid rgba(255,255,255,0.10);

    box-shadow:
        0 15px 35px rgba(0,0,0,0.22);

    backdrop-filter: blur(16px);

    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-6px);

    background: rgba(255,255,255,0.075);

    border-color: rgba(59,130,246,0.4);

    box-shadow:
        0 20px 45px rgba(0,0,0,0.35);
}

.feature-icon {
    font-size: 36px;
}

.feature-title {
    font-size: 21px;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 8px;
}

.feature-description {
    color: #94a3b8;
    line-height: 1.6;
    margin-top: 8px;
}


/* ============================================================
   WORKFLOW
   ============================================================ */

.workflow-card {
    padding: 22px 12px;
    min-height: 170px;

    text-align: center;

    border-radius: 18px;

    background: rgba(255,255,255,0.05);

    border: 1px solid rgba(255,255,255,0.10);

    backdrop-filter: blur(15px);

    transition: all 0.3s ease;
}

.workflow-card:hover {
    transform: translateY(-5px);

    border-color: rgba(56,189,248,0.35);
}

.workflow-number {
    width: 40px;
    height: 40px;

    margin: 0 auto;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 50%;

    background: linear-gradient(
        135deg,
        #2563eb,
        #06b6d4
    );

    color: white;
    font-weight: 800;
}

.workflow-icon {
    font-size: 32px;
    margin-top: 12px;
}

.workflow-title {
    color: #f8fafc;
    font-size: 17px;
    font-weight: 700;
    margin-top: 7px;
}

.workflow-text {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 5px;
}


/* ============================================================
   TECHNOLOGIES
   ============================================================ */

.tech-card {
    text-align: center;
    padding: 25px;

    border-radius: 18px;

    background: rgba(255,255,255,0.045);

    border: 1px solid rgba(255,255,255,0.09);

    transition: all 0.3s ease;
}

.tech-card:hover {
    transform: translateY(-4px);

    border-color: rgba(59,130,246,0.35);
}

.tech-icon {
    font-size: 35px;
}

.tech-name {
    color: #f8fafc;
    font-size: 18px;
    font-weight: 700;
    margin-top: 8px;
}


/* ============================================================
   CTA
   ============================================================ */

.cta {
    margin-top: 35px;
    padding: 42px;

    text-align: center;

    border-radius: 25px;

    background:
        linear-gradient(
            135deg,
            rgba(37,99,235,0.28),
            rgba(6,182,212,0.18)
        );

    border: 1px solid rgba(96,165,250,0.25);

    box-shadow:
        0 20px 50px rgba(0,0,0,0.3);
}

.cta-title {
    font-size: 30px;
    font-weight: 800;
    color: white;
}

.cta-text {
    color: #cbd5e1;
    margin-top: 8px;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
    padding-top: 35px;

    color: #64748b;
    font-size: 14px;
}

.footer-title {
    color: #cbd5e1;
    font-size: 18px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-icon">📊</div>
        <div class="hero-title">DataRefinery</div>
        <div class="hero-subtitle">
            Professional Data Analysis Web Application
        </div>
        <div class="hero-description">
            Transform raw datasets into meaningful insights with
            a powerful and intuitive data analysis platform built
            with Python, Pandas, Streamlit, and Plotly.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# QUICK STATS
# ============================================================

st.markdown(
    '<div class="section-title">📌 DataRefinery at a Glance</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Everything you need for practical dataset analysis.'
    '</div>',
    unsafe_allow_html=True
)

s1, s2, s3, s4 = st.columns(4)


with s1:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon">📄</div>
            <div class="stat-number">9</div>
            <div class="stat-label">Application Pages</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with s2:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-number">6+</div>
            <div class="stat-label">Interactive Charts</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with s3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon">🧹</div>
            <div class="stat-number">7+</div>
            <div class="stat-label">Cleaning Tools</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with s4:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon">💾</div>
            <div class="stat-number">CSV</div>
            <div class="stat-label">Export Format</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# FEATURES
# ============================================================

st.markdown(
    '<div class="section-title">'
    '✨ Powerful Data Analysis Features'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'A complete workflow from raw data to useful insights.'
    '</div>',
    unsafe_allow_html=True
)


features = [
    (
        "📂",
        "Upload Dataset",
        "Upload CSV and Excel datasets and preview your data instantly."
    ),
    (
        "🧹",
        "Data Cleaning",
        "Handle missing values, duplicates, and common data quality issues."
    ),
    (
        "📊",
        "Interactive Visualization",
        "Create histograms, bar charts, line charts, scatter plots, box plots and pie charts."
    ),
    (
        "🔍",
        "Filter & Search",
        "Search records, filter rows and explore specific parts of your dataset."
    ),
    (
        "📉",
        "Exploratory Data Analysis",
        "Understand statistics, relationships, distributions and patterns in your data."
    ),
    (
        "💾",
        "Export Data",
        "Download your cleaned dataset for further analysis or sharing."
    )
]


for row_start in range(0, 6, 3):

    cols = st.columns(3)

    for i, col in enumerate(cols):

        icon, title, description = features[row_start + i]

        with col:

            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-description">
                        {description}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


st.divider()


# ============================================================
# WORKFLOW
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📋 Simple Data Analysis Workflow'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Move from raw data to a clean and understandable dataset.'
    '</div>',
    unsafe_allow_html=True
)


workflow = [
    ("1", "📂", "Upload", "Import your dataset"),
    ("2", "🔎", "Explore", "Understand your data"),
    ("3", "🧹", "Clean", "Fix data quality"),
    ("4", "📊", "Visualize", "Create charts"),
    ("5", "📉", "Analyze", "Discover patterns"),
    ("6", "💾", "Export", "Download results")
]


workflow_cols = st.columns(6)


for col, item in zip(workflow_cols, workflow):

    number, icon, title, text = item

    with col:

        st.markdown(
            f"""
            <div class="workflow-card">
                <div class="workflow-number">{number}</div>
                <div class="workflow-icon">{icon}</div>
                <div class="workflow-title">{title}</div>
                <div class="workflow-text">{text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown("<br>", unsafe_allow_html=True)

st.divider()


# ============================================================
# TECHNOLOGIES
# ============================================================

st.markdown(
    '<div class="section-title">🛠 Built With</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Technologies powering the DataRefinery platform.'
    '</div>',
    unsafe_allow_html=True
)


technologies = [
    ("🐍", "Python"),
    ("🌐", "Streamlit"),
    ("🐼", "Pandas"),
    ("📊", "Plotly")
]


tech_cols = st.columns(4)


for col, (icon, name) in zip(tech_cols, technologies):

    with col:

        st.markdown(
            f"""
            <div class="tech-card">
                <div class="tech-icon">{icon}</div>
                <div class="tech-name">{name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# CTA
# ============================================================

st.markdown(
    """
    <div class="cta">
        <div class="cta-title">
            🚀 Ready to Analyze Your Data?
        </div>
        <div class="cta-text">
            Upload a dataset and start exploring your data with DataRefinery.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.success(
    "👈 Select a page from the sidebar to begin."
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <div class="footer-title">
            📊 DataRefinery v1.0
        </div>
        <br>
        Built with ❤️ using
        <br><br>
        Python • Streamlit • Pandas • Plotly
        <br><br>
        © 2026 All Rights Reserved
    </div>
    """,
    unsafe_allow_html=True
)

import streamlit as st


def apply_theme():

    st.html("""
    <style>

    /* =========================================================
       GLOBAL APP
    ========================================================= */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(37, 99, 235, 0.15),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 80%,
                rgba(14, 165, 233, 0.10),
                transparent 30%
            ),
            #080d1a;

        color: #f8fafc;
    }


    /* =========================================================
       MAIN CONTENT
    ========================================================= */

    .main .block-container {
        max-width: 1450px;

        padding-top: 1.5rem;
        padding-bottom: 4rem;

        padding-left: 2rem;
        padding-right: 2rem;
    }


    /* =========================================================
       SIDEBAR
    ========================================================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0b1120 0%,
                #0f172a 100%
            );

        border-right: 1px solid rgba(255,255,255,0.08);
    }


    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }


    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #cbd5e1;
    }


    /* =========================================================
       HEADINGS
    ========================================================= */

    h1 {
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        font-weight: 750 !important;
    }

    h3 {
        font-weight: 700 !important;
    }


    /* =========================================================
       METRIC CARDS
    ========================================================= */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(30,41,59,0.90),
                rgba(15,23,42,0.90)
            );

        border: 1px solid rgba(148,163,184,0.15);

        border-radius: 18px;

        padding: 20px;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.25);

        transition:
            transform 0.25s ease,
            border-color 0.25s ease;
    }


    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);

        border-color:
            rgba(59,130,246,0.45);
    }


    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }


    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 800;
    }


    /* =========================================================
       BUTTONS
    ========================================================= */

    .stButton > button {
        border-radius: 10px;

        border: 1px solid
            rgba(59,130,246,0.35);

        background:
            rgba(30,41,59,0.8);

        color: white;

        transition: all 0.25s ease;
    }


    .stButton > button:hover {
        border-color:
            rgba(59,130,246,0.8);

        background:
            rgba(37,99,235,0.25);

        transform: translateY(-2px);
    }


    /* =========================================================
       DATAFRAME
    ========================================================= */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;

        overflow: hidden;

        border:
            1px solid rgba(148,163,184,0.12);
    }


    /* =========================================================
       FILE UPLOADER
    ========================================================= */

    section[data-testid="stFileUploaderDropzone"] {
        background:
            rgba(15,23,42,0.65);

        border:
            1px dashed
            rgba(96,165,250,0.35);

        border-radius: 16px;
    }


    /* =========================================================
       ALERTS
    ========================================================= */

    div[data-testid="stAlert"] {
        border-radius: 14px;

        border: 1px solid
            rgba(255,255,255,0.08);
    }


    /* =========================================================
       DIVIDER
    ========================================================= */

    hr {
        border: none;

        border-top:
            1px solid
            rgba(148,163,184,0.12);

        margin: 2rem 0;
    }


    /* =========================================================
       SCROLLBAR
    ========================================================= */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #080d1a;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;

        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }


    /* =========================================================
       SIDEBAR NAVIGATION
    ========================================================= */

    [data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }


    [data-testid="stSidebarNav"] li {
        margin: 4px 8px;
    }


    [data-testid="stSidebarNav"] a {
        border-radius: 10px;

        transition:
            background 0.2s ease,
            transform 0.2s ease;
    }


    [data-testid="stSidebarNav"] a:hover {
        background:
            rgba(59,130,246,0.12);

        transform: translateX(3px);
    }

    /* =========================================================
       HIDE APP FROM SIDEBAR
    ========================================================= */

    [data-testid="stSidebarNav"] ul li:first-child {
        display: none !important;
    }


    /* =========================================================
       NAVIGATION / PAGE TRANSITION POLISH
    ========================================================= */

    html,
    body {
        scroll-behavior: auto !important;
    }


    .main {
        scroll-margin-top: 0 !important;
    }


    </style>
    """)



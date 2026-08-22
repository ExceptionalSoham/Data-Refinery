# DataRefinery

Professional data analysis web app built with Streamlit, Pandas, and Plotly.

## Folder structure

```
DataRefinery/
├── app.py                     # Home page (entry point)
├── requirements.txt
├── utils/
│   └── theme.py                # Shared dark theme (apply_theme)
├── pages/                      # Streamlit auto-discovers these as sidebar pages
│   ├── 1_Upload.py
│   ├── 2_Dataset_Overview.py
│   ├── 3_Data_Cleaning.py
│   ├── 4_Data_Visualization.py
│   ├── 5_Data_Filter_Search.py
│   ├── 6_Exploratory_Data_Analysis.py
│   ├── 7_Dashboard.py
│   ├── 8_Export_Data.py
│   └── 9_About.py
└── assets/
    └── avatar.png               # Used by the About page
```

This is the standard Streamlit **multipage app** layout: `app.py` is the
entry point, and every script inside `pages/` automatically becomes a page
in the sidebar (Streamlit sorts them using the leading number).

## Run locally

```bash
cd DataRefinery
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this whole `DataRefinery/` folder to a GitHub repo (keep the
   structure above — `app.py` at the repo root, `pages/`, `utils/`,
   `assets/` alongside it).
2. Go to https://share.streamlit.io → **New app**.
3. Point it at your repo, branch, and set **Main file path** to `app.py`.
4. Deploy.

## Notes on fixes made while packaging

- Moved every numbered page into `pages/` (required for Streamlit's
  automatic multipage navigation — they were flat files before).
- Put `theme.py` inside `utils/` (with an `utils/__init__.py`) so the
  `from utils.theme import apply_theme` import used by every page resolves
  correctly.
- Put `avatar.png` inside `assets/`, matching the path the About page
  already expects: `Path(__file__).resolve().parent.parent / "assets" / "avatar.png"`.
- Dropped the stray `theme_cpython-313.pyc` (a compiled bytecode cache
  file) — it's not needed and Python regenerates `__pycache__` on its own.
- Verified every `.py` file compiles cleanly (`python -m py_compile`).

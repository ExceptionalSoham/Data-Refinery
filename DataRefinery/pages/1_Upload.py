import streamlit as st
import pandas as pd

from utils.theme import apply_theme


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Upload Dataset | DataRefinery",
    page_icon="📂",
    layout="wide"
)

apply_theme()


# ==========================
# SESSION STATE
# ==========================

if "df" not in st.session_state:
    st.session_state.df = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None


# ==========================
# HEADER
# ==========================

st.title("📂 Upload Dataset")

st.subheader(
    "Import your dataset and start analyzing"
)

st.markdown(
    "Upload a **CSV or Excel** dataset to begin your "
    "data analysis workflow."
)

st.divider()


# ==========================
# UPLOAD SECTION
# ==========================

uploaded_file = st.file_uploader(
    "Choose your dataset",
    type=["csv", "xlsx", "xls"],
    help="Supported formats: CSV, XLSX and XLS"
)


# ==========================
# READ DATASET
# ==========================

if uploaded_file is not None:

    try:

        file_name = uploaded_file.name

        # --------------------------
        # Read CSV
        # --------------------------

        if file_name.lower().endswith(".csv"):

            try:

                df = pd.read_csv(
                    uploaded_file
                )

            except UnicodeDecodeError:

                uploaded_file.seek(0)

                df = pd.read_csv(
                    uploaded_file,
                    encoding="latin1"
                )

        # --------------------------
        # Read Excel
        # --------------------------

        else:

            df = pd.read_excel(
                uploaded_file
            )

        # --------------------------
        # Save Dataset
        # --------------------------

        st.session_state.df = df
        st.session_state.file_name = file_name

        st.success(
            f"✅ Dataset uploaded successfully: **{file_name}**"
        )

        st.divider()

        # ==========================
        # DATASET INFORMATION
        # ==========================

        st.subheader(
            "📊 Dataset Information"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Rows",
                f"{df.shape[0]:,}"
            )

        with col2:
            st.metric(
                "Columns",
                f"{df.shape[1]:,}"
            )

        with col3:
            st.metric(
                "Missing Values",
                f"{int(df.isna().sum().sum()):,}"
            )

        with col4:
            st.metric(
                "Duplicate Rows",
                f"{int(df.duplicated().sum()):,}"
            )

        st.divider()

        # ==========================
        # DATASET PREVIEW
        # ==========================

        st.subheader(
            "👀 Dataset Preview"
        )

        st.dataframe(
            df.head(10),
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ==========================
        # COLUMN INFORMATION
        # ==========================

        st.subheader(
            "📋 Column Information"
        )

        column_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isna().sum().values,
            "Unique Values": [
                df[column].nunique()
                for column in df.columns
            ]
        })

        st.dataframe(
            column_info,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ==========================
        # COLUMN CATEGORIES
        # ==========================

        st.subheader(
            "🔎 Column Categories"
        )

        # Numeric columns
        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        # Initially find text/category columns
        categorical_columns = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        # Detect date-like columns
        date_columns = []

        for column in categorical_columns.copy():

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            if converted.notna().mean() >= 0.80:

                date_columns.append(
                    column
                )

                categorical_columns.remove(
                    column
                )

        # ==========================
        # CATEGORY CARDS
        # ==========================

        c1, c2, c3 = st.columns(3)

        with c1:

            st.info(
                f"""
                **🔢 Numeric Columns**

                {len(numeric_columns)}

                {", ".join(numeric_columns[:5])
                if numeric_columns
                else "None"}
                """
            )

        with c2:

            st.success(
                f"""
                **🔤 Categorical Columns**

                {len(categorical_columns)}

                {", ".join(categorical_columns[:5])
                if categorical_columns
                else "None"}
                """
            )

        with c3:

            st.warning(
                f"""
                **📅 Date Columns**

                {len(date_columns)}

                {", ".join(date_columns[:5])
                if date_columns
                else "None"}
                """
            )

        st.divider()

        # ==========================
        # READY MESSAGE
        # ==========================

        st.success(
            "🚀 Your dataset is ready! "
            "Use the sidebar to continue with "
            "Dataset Overview, Data Cleaning, "
            "Visualization, EDA, Dashboard or Export."
        )

    except Exception as e:

        st.error(
            f"❌ Unable to read the dataset: {e}"
        )


# ==========================
# NO DATASET
# ==========================

else:

    st.info(
        "👆 Upload a CSV or Excel file to begin."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            ### 📄 CSV

            Upload `.csv` files for analysis.
            """
        )

    with col2:

        st.markdown(
            """
            ### 📊 Excel

            Upload `.xlsx` or `.xls` files.
            """
        )

    with col3:

        st.markdown(
            """
            ### 🚀 Analyze

            Explore, clean, visualize and
            export your data.
            """
        )






import streamlit as st
import pandas as pd

from utils.theme import apply_theme


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Dataset Overview | DataRefinery",
    page_icon="📊",
    layout="wide"
)

apply_theme()


# =========================================================
# CHECK DATASET
# =========================================================

if "df" not in st.session_state or st.session_state.df is None:

    st.warning(
        "⚠️ Please upload a dataset from the Upload page first."
    )

    st.stop()


df = st.session_state.df


# =========================================================
# HEADER
# =========================================================

st.title("📊 Dataset Overview")

st.caption(
    "Understand the structure, quality and characteristics "
    "of your uploaded dataset."
)

st.info(
    "This page summarizes your dataset's size, data types, "
    "missing values, duplicates, statistics and overall health."
)

st.divider()


# =========================================================
# BASIC INFORMATION
# =========================================================

rows, columns = df.shape

missing_values = int(
    df.isnull().sum().sum()
)

duplicate_rows = int(
    df.duplicated().sum()
)


# =========================================================
# COLUMN CATEGORIES
# =========================================================

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

categorical_columns = df.select_dtypes(
    include=["object", "category"]
).columns.tolist()

date_columns = []

for column in categorical_columns.copy():

    converted = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    if converted.notna().mean() >= 0.80:

        date_columns.append(column)

        categorical_columns.remove(column)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📌 Dataset Summary")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "📄 Rows",
        f"{rows:,}"
    )

with c2:
    st.metric(
        "📋 Columns",
        f"{columns:,}"
    )

with c3:
    st.metric(
        "❗ Missing Values",
        f"{missing_values:,}"
    )

with c4:
    st.metric(
        "🔁 Duplicate Rows",
        f"{duplicate_rows:,}"
    )

with c5:
    st.metric(
        "🔢 Numeric Columns",
        f"{len(numeric_columns):,}"
    )


st.divider()


# =========================================================
# DATASET HEALTH
# =========================================================

st.subheader("🩺 Dataset Health")


if rows > 0:

    missing_percentage = (
        missing_values / (rows * columns)
    ) * 100

else:

    missing_percentage = 0


duplicate_percentage = (
    duplicate_rows / rows * 100
) if rows > 0 else 0


# Health score
health_score = 100

health_score -= min(
    missing_percentage * 2,
    40
)

health_score -= min(
    duplicate_percentage * 2,
    30
)

health_score = max(
    0,
    min(100, health_score)
)

health_score = round(
    health_score
)


health_col1, health_col2 = st.columns(
    [1, 2]
)


with health_col1:

    st.metric(
        "Dataset Health Score",
        f"{health_score}/100"
    )


with health_col2:

    st.progress(
        health_score / 100
    )

    if health_score >= 90:

        st.success(
            "✅ Excellent dataset quality."
        )

    elif health_score >= 70:

        st.info(
            "ℹ️ Good dataset quality with some issues to review."
        )

    elif health_score >= 50:

        st.warning(
            "⚠️ Dataset needs some cleaning."
        )

    else:

        st.error(
            "❌ Dataset requires significant cleaning."
        )


st.caption(
    f"Missing data: {missing_percentage:.2f}% "
    f"• Duplicate rows: {duplicate_percentage:.2f}%"
)


st.divider()


# =========================================================
# COLUMN CATEGORIES
# =========================================================

st.subheader("🔎 Column Categories")

cat1, cat2, cat3 = st.columns(3)


with cat1:

    st.info(
        f"""
        **🔢 Numeric Columns**

        {len(numeric_columns)}

        {", ".join(numeric_columns[:5])
        if numeric_columns
        else "None"}
        """
    )


with cat2:

    st.success(
        f"""
        **🔤 Categorical Columns**

        {len(categorical_columns)}

        {", ".join(categorical_columns[:5])
        if categorical_columns
        else "None"}
        """
    )


with cat3:

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


# =========================================================
# COLUMN DETAILS
# =========================================================

st.subheader("📋 Column Details")


column_info = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": df.isnull().sum().values,
    "Missing %": [
        round(
            (df[column].isnull().sum() / rows) * 100,
            2
        ) if rows > 0 else 0
        for column in df.columns
    ],
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


# =========================================================
# DATASET PREVIEW
# =========================================================

st.subheader("👀 Dataset Preview")


max_preview = min(
    100,
    max(5, len(df))
)

default_preview = min(
    10,
    max_preview
)


rows_to_show = st.slider(
    "Rows to display",
    min_value=5,
    max_value=max_preview,
    value=default_preview,
    step=5
)


st.dataframe(
    df.head(rows_to_show),
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# DESCRIPTIVE STATISTICS
# =========================================================

st.subheader("📈 Descriptive Statistics")


try:

    statistics = df.describe(
        include="all"
    ).transpose()

    st.dataframe(
        statistics,
        use_container_width=True
    )

except Exception:

    st.info(
        "Descriptive statistics could not be calculated "
        "for all columns."
    )


st.divider()


# =========================================================
# DATA TYPES SUMMARY
# =========================================================

st.subheader("📑 Data Types Summary")


dtype_count = (
    df.dtypes
    .astype(str)
    .value_counts()
    .rename_axis("Data Type")
    .reset_index(name="Count")
)


st.dataframe(
    dtype_count,
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# MEMORY USAGE
# =========================================================

memory_kb = (
    df.memory_usage(deep=True).sum()
    / 1024
)

memory_mb = memory_kb / 1024


m1, m2 = st.columns(2)


with m1:

    st.metric(
        "💾 Memory Usage",
        f"{memory_kb:,.2f} KB"
    )


with m2:

    st.metric(
        "💾 Memory Usage",
        f"{memory_mb:,.2f} MB"
    )


st.divider()


# =========================================================
# FINAL STATUS
# =========================================================

if missing_values == 0 and duplicate_rows == 0:

    st.success(
        "✅ Your dataset is clean with no missing values "
        "or duplicate rows."
    )

elif missing_values > 0 and duplicate_rows == 0:

    st.warning(
        f"⚠️ Your dataset contains {missing_values:,} "
        "missing values. Consider visiting Data Cleaning."
    )

elif missing_values == 0 and duplicate_rows > 0:

    st.warning(
        f"⚠️ Your dataset contains {duplicate_rows:,} "
        "duplicate rows. Consider visiting Data Cleaning."
    )

else:

    st.warning(
        f"⚠️ Your dataset contains {missing_values:,} "
        f"missing values and {duplicate_rows:,} duplicate rows."
    )

    

import streamlit as st
import pandas as pd
import plotly.express as px


from utils.theme import apply_theme


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Dashboard | DataRefinery",
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


df = st.session_state.df.copy()


# =========================================================
# HEADER
# =========================================================

st.title("📊 DataRefinery Dashboard")

st.caption(
    "A centralized view of your dataset, key metrics, "
    "performance indicators and analytical insights."
)

st.info(
    "This dashboard summarizes the current dataset after any "
    "cleaning or analysis operations."
)

st.divider()


# =========================================================
# DATA PREPARATION
# =========================================================

rows = len(df)
columns = len(df.columns)

missing = int(
    df.isnull().sum().sum()
)

duplicates = int(
    df.duplicated().sum()
)

numeric_columns = (
    df.select_dtypes(include="number")
    .columns
    .tolist()
)

categorical_columns = (
    df.select_dtypes(
        include=["object", "category"]
    )
    .columns
    .tolist()
)

date_columns = []

for column in categorical_columns.copy():

    converted = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    if converted.notna().mean() >= 0.80:

        date_columns.append(column)

        categorical_columns.remove(column)


memory_mb = (
    df.memory_usage(deep=True).sum()
    / 1024
    / 1024
)


if rows > 0 and columns > 0:

    completeness = (
        1
        - missing / (rows * columns)
    ) * 100

else:

    completeness = 100


# =========================================================
# MAIN KPI CARDS
# =========================================================

st.subheader("📌 Key Performance Indicators")

k1, k2, k3, k4, k5 = st.columns(5)


with k1:

    st.metric(
        "📄 Total Rows",
        f"{rows:,}"
    )


with k2:

    st.metric(
        "📋 Total Columns",
        f"{columns:,}"
    )


with k3:

    st.metric(
        "🔢 Numeric Columns",
        f"{len(numeric_columns):,}"
    )


with k4:

    st.metric(
        "❗ Missing Values",
        f"{missing:,}"
    )


with k5:

    st.metric(
        "🔁 Duplicate Rows",
        f"{duplicates:,}"
    )


st.divider()


# =========================================================
# DATASET HEALTH
# =========================================================

st.subheader("🩺 Dataset Health")

h1, h2, h3, h4 = st.columns(4)


with h1:

    st.metric(
        "✅ Completeness",
        f"{completeness:.2f}%"
    )


with h2:

    st.metric(
        "🔤 Categorical Columns",
        f"{len(categorical_columns):,}"
    )


with h3:

    st.metric(
        "📅 Date Columns",
        f"{len(date_columns):,}"
    )


with h4:

    st.metric(
        "💾 Memory Usage",
        f"{memory_mb:.2f} MB"
    )


if missing == 0 and duplicates == 0:

    st.success(
        "✅ Excellent dataset health — no missing values "
        "or duplicate rows were detected."
    )

elif completeness >= 95:

    st.info(
        "ℹ️ Dataset quality is high, with only minor "
        "data-quality issues."
    )

elif completeness >= 80:

    st.warning(
        "⚠️ Dataset contains data-quality issues that "
        "should be reviewed."
    )

else:

    st.error(
        "❌ Dataset requires significant cleaning."
    )


st.divider()


# =========================================================
# NUMERIC OVERVIEW
# =========================================================

st.subheader("📈 Numeric Overview")


if numeric_columns:

    selected_numeric = st.selectbox(
        "Select Numeric Metric",
        numeric_columns,
        key="dashboard_numeric"
    )

    numeric_series = (
        df[selected_numeric]
        .dropna()
    )

    if not numeric_series.empty:

        n1, n2, n3, n4, n5 = st.columns(5)


        with n1:

            st.metric(
                "Average",
                f"{numeric_series.mean():,.2f}"
            )


        with n2:

            st.metric(
                "Median",
                f"{numeric_series.median():,.2f}"
            )


        with n3:

            st.metric(
                "Minimum",
                f"{numeric_series.min():,.2f}"
            )


        with n4:

            st.metric(
                "Maximum",
                f"{numeric_series.max():,.2f}"
            )


        with n5:

            st.metric(
                "Std Dev",
                f"{numeric_series.std():,.2f}"
            )

else:

    st.info(
        "No numeric columns are available."
    )


st.divider()


# =========================================================
# MAIN VISUALIZATIONS
# =========================================================

st.subheader("📊 Data Visualization")


chart_left, chart_right = st.columns(2)


# =========================================================
# CATEGORY PERFORMANCE
# =========================================================

with chart_left:

    if categorical_columns and numeric_columns:

        dashboard_category = st.selectbox(
            "Category",
            categorical_columns,
            key="dashboard_category"
        )

        dashboard_value = st.selectbox(
            "Measure",
            numeric_columns,
            key="dashboard_value"
        )

        category_summary = (
            df.groupby(
                dashboard_category,
                dropna=False
            )[dashboard_value]
            .sum()
            .reset_index()
            .sort_values(
                dashboard_value,
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            category_summary,
            x=dashboard_category,
            y=dashboard_value,
            title=f"{dashboard_value} by {dashboard_category}"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Category performance requires categorical "
            "and numeric columns."
        )


# =========================================================
# DISTRIBUTION
# =========================================================

with chart_right:

    if numeric_columns:

        distribution_column = st.selectbox(
            "Distribution Column",
            numeric_columns,
            key="dashboard_distribution"
        )

        fig = px.histogram(
            df,
            x=distribution_column,
            nbins=30,
            title=f"Distribution of {distribution_column}"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No numeric columns available."
        )


st.divider()


# =========================================================
# SECOND CHART ROW
# =========================================================

chart_left, chart_right = st.columns(2)


# =========================================================
# BOX PLOT
# =========================================================

with chart_left:

    if numeric_columns:

        box_column = st.selectbox(
            "Box Plot Column",
            numeric_columns,
            key="dashboard_box"
        )

        fig = px.box(
            df,
            y=box_column,
            points="outliers",
            title=f"Box Plot of {box_column}"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# CATEGORY DISTRIBUTION
# =========================================================

with chart_right:

    if categorical_columns:

        pie_column = st.selectbox(
            "Category Distribution",
            categorical_columns,
            key="dashboard_pie"
        )

        pie_data = (
            df[pie_column]
            .value_counts()
            .head(10)
            .reset_index()
        )

        pie_data.columns = [
            pie_column,
            "Count"
        ]

        fig = px.pie(
            pie_data,
            names=pie_column,
            values="Count",
            hole=0.45,
            title=f"Distribution of {pie_column}"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No categorical columns available."
        )


st.divider()


# =========================================================
# CORRELATION OVERVIEW
# =========================================================

st.subheader("🔥 Correlation Overview")


if len(numeric_columns) >= 2:

    correlation = df[
        numeric_columns
    ].corr()

    fig = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        title="Numeric Column Correlation"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "At least two numeric columns are required "
        "for correlation analysis."
    )


st.divider()


# =========================================================
# TOP CATEGORY INSIGHTS
# =========================================================

st.subheader("🏆 Top Category Insights")


if categorical_columns and numeric_columns:

    insight_category = st.selectbox(
        "Category",
        categorical_columns,
        key="dashboard_insight_category"
    )

    insight_value = st.selectbox(
        "Measure",
        numeric_columns,
        key="dashboard_insight_value"
    )

    top_categories = (
        df.groupby(
            insight_category,
            dropna=False
        )[insight_value]
        .sum()
        .reset_index()
        .sort_values(
            insight_value,
            ascending=False
        )
        .head(10)
    )

    top_categories.columns = [
        insight_category,
        insight_value
    ]

    st.dataframe(
        top_categories,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Category insights require categorical and "
        "numeric columns."
    )


st.divider()


# =========================================================
# DATASET PROFILE
# =========================================================

st.subheader("📋 Dataset Profile")


profile = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": (
        df.isnull()
        .sum()
        .values
    ),
    "Unique Values": [
        df[column].nunique()
        for column in df.columns
    ]
})


st.dataframe(
    profile,
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# RECENT / CURRENT DATA PREVIEW
# =========================================================

st.subheader("👀 Dataset Preview")


preview_rows = min(
    25,
    max(5, len(df))
)


rows_to_show = st.slider(
    "Rows to display",
    min_value=5,
    max_value=preview_rows,
    value=min(10, preview_rows),
    step=5,
    key="dashboard_preview"
)


st.dataframe(
    df.head(rows_to_show),
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# FINAL DASHBOARD STATUS
# =========================================================

st.subheader("💡 Dashboard Summary")


if missing == 0 and duplicates == 0:

    st.success(
        f"✅ The current dataset contains {rows:,} rows "
        f"and {columns:,} columns and is ready for analysis."
    )

else:

    st.warning(
        f"⚠️ The current dataset contains {missing:,} missing "
        f"values and {duplicates:,} duplicate rows. "
        "Review Data Cleaning before final reporting."
    )








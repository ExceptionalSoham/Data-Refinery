import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Exploratory Data Analysis | DataRefinery",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# OPTIONAL THEME
# ============================================================

try:
    from utils.theme import apply_theme
    apply_theme()
except Exception:
    pass


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def detect_date_columns(dataframe):
    """
    Detect real datetime columns plus object/string columns
    that can reasonably be converted to dates.
    """
    detected = []

    for column in dataframe.columns:

        if pd.api.types.is_datetime64_any_dtype(dataframe[column]):
            detected.append(column)
            continue

        # Try conversion only for columns that look date-related
        name = str(column).lower()

        if any(word in name for word in ["date", "time", "year"]):
            converted = pd.to_datetime(
                dataframe[column],
                errors="coerce"
            )

            valid_ratio = converted.notna().mean()

            if valid_ratio >= 0.70:
                detected.append(column)

    return detected


def format_number(value):
    """Format numeric values safely."""
    if pd.isna(value):
        return "N/A"

    return f"{value:,.2f}"


def calculate_iqr_outliers(series):
    """Return IQR bounds and outlier mask."""
    clean = pd.to_numeric(series, errors="coerce").dropna()

    if clean.empty:
        return np.nan, np.nan, pd.Series(dtype=bool)

    q1 = clean.quantile(0.25)
    q3 = clean.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    mask = (series < lower_bound) | (series > upper_bound)

    return lower_bound, upper_bound, mask


# ============================================================
# DATASET CHECK
# ============================================================

if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠️ Please upload a dataset first.")
    st.stop()


df = st.session_state.df.copy()


# ============================================================
# COLUMN TYPES
# ============================================================

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

categorical_columns = df.select_dtypes(
    include=["object", "category", "string"]
).columns.tolist()

date_columns = detect_date_columns(df)


# ============================================================
# HEADER
# ============================================================

st.title("📈 Exploratory Data Analysis")

st.caption(
    "Explore distributions, relationships, statistics, outliers, "
    "grouped summaries and patterns within your dataset."
)

st.info(
    "Use the sections below to understand your data before making "
    "decisions or creating final visualizations."
)


# ============================================================
# DATASET SUMMARY
# ============================================================

st.divider()

st.header("📊 Dataset Summary")

summary_col1, summary_col2, summary_col3, summary_col4, summary_col5 = (
    st.columns(5)
)

with summary_col1:
    st.metric(
        "Rows",
        f"{df.shape[0]:,}"
    )

with summary_col2:
    st.metric(
        "Columns",
        f"{df.shape[1]:,}"
    )

with summary_col3:
    st.metric(
        "Numeric",
        len(numeric_columns)
    )

with summary_col4:
    st.metric(
        "Categorical",
        len(categorical_columns)
    )

with summary_col5:
    st.metric(
        "Date",
        len(date_columns)
    )


# ============================================================
# DATASET QUALITY
# ============================================================

st.header("🩺 Dataset Quality")

missing_values = int(df.isna().sum().sum())
duplicate_rows = int(df.duplicated().sum())

memory_mb = (
    df.memory_usage(deep=True).sum() / (1024 ** 2)
)

quality_col1, quality_col2, quality_col3 = st.columns(3)

with quality_col1:
    st.metric(
        "Missing Values",
        f"{missing_values:,}"
    )

with quality_col2:
    st.metric(
        "Duplicate Rows",
        f"{duplicate_rows:,}"
    )

with quality_col3:
    st.metric(
        "Memory Usage",
        f"{memory_mb:.2f} MB"
    )

if missing_values == 0 and duplicate_rows == 0:
    st.success(
        "✅ Dataset quality looks good. No missing values "
        "or duplicate rows were detected."
    )

elif missing_values > 0 and duplicate_rows == 0:
    st.warning(
        "⚠️ Missing values were detected, but there are "
        "no duplicate rows."
    )

elif missing_values == 0 and duplicate_rows > 0:
    st.warning(
        "⚠️ Duplicate rows were detected, but there are "
        "no missing values."
    )

else:
    st.error(
        "❌ Missing values and duplicate rows were detected."
    )


# ============================================================
# STATISTICAL ANALYSIS
# ============================================================

st.divider()

st.header("📈 Statistical Analysis")

if numeric_columns:

    selected_stat_column = st.selectbox(
        "Select Numeric Column",
        numeric_columns,
        key="eda_stats_column"
    )

    selected_series = pd.to_numeric(
        df[selected_stat_column],
        errors="coerce"
    ).dropna()

    if not selected_series.empty:

        stat1, stat2, stat3, stat4 = st.columns(4)
        stat5, stat6, stat7, stat8 = st.columns(4)

        with stat1:
            st.metric(
                "Mean",
                format_number(selected_series.mean())
            )

        with stat2:
            st.metric(
                "Median",
                format_number(selected_series.median())
            )

        with stat3:
            st.metric(
                "Minimum",
                format_number(selected_series.min())
            )

        with stat4:
            st.metric(
                "Maximum",
                format_number(selected_series.max())
            )

        with stat5:
            st.metric(
                "Standard Deviation",
                format_number(selected_series.std())
            )

        with stat6:
            st.metric(
                "Variance",
                format_number(selected_series.var())
            )

        with stat7:
            mode_values = selected_series.mode()

            mode_value = (
                mode_values.iloc[0]
                if not mode_values.empty
                else np.nan
            )

            st.metric(
                "Mode",
                format_number(mode_value)
            )

        with stat8:
            st.metric(
                "Unique Values",
                f"{selected_series.nunique():,}"
            )

        skewness = selected_series.skew()
        kurtosis = selected_series.kurt()

        st.caption(
            f"Skewness: {skewness:.3f}  |  "
            f"Kurtosis: {kurtosis:.3f}"
        )

    else:
        st.warning(
            "No valid numeric values are available for this column."
        )

else:
    st.info("No numeric columns were found.")


# ============================================================
# DISTRIBUTION ANALYSIS
# ============================================================

st.divider()

st.header("📊 Distribution Analysis")

if numeric_columns:

    distribution_col = st.selectbox(
        "Choose Numeric Column",
        numeric_columns,
        key="eda_distribution_column"
    )

    bin_count = st.slider(
        "Number of Histogram Bins",
        min_value=5,
        max_value=100,
        value=30,
        key="eda_hist_bins"
    )

    fig_distribution = px.histogram(
        df,
        x=distribution_col,
        nbins=bin_count,
        title=f"Distribution of {distribution_col}"
    )

    fig_distribution.update_layout(
        xaxis_title=distribution_col,
        yaxis_title="Count"
    )

    st.plotly_chart(
        fig_distribution,
        use_container_width=True,
        key="eda_distribution_chart"
    )

else:
    st.info("No numeric columns available for distribution analysis.")


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

st.divider()

st.header("🔥 Correlation Analysis")

if len(numeric_columns) >= 2:

    correlation_matrix = df[numeric_columns].corr()

    st.dataframe(
        correlation_matrix.round(4),
        use_container_width=True
    )

    fig_correlation = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        title="Correlation Heatmap",
        aspect="auto"
    )

    st.plotly_chart(
        fig_correlation,
        use_container_width=True,
        key="eda_correlation_heatmap"
    )

    # Find strongest relationships
    correlation_pairs = []

    for i in range(len(numeric_columns)):
        for j in range(i + 1, len(numeric_columns)):

            col1 = numeric_columns[i]
            col2 = numeric_columns[j]

            value = correlation_matrix.loc[col1, col2]

            if not pd.isna(value):

                correlation_pairs.append(
                    {
                        "Column 1": col1,
                        "Column 2": col2,
                        "Correlation": value
                    }
                )

    strongest_df = pd.DataFrame(correlation_pairs)

    if not strongest_df.empty:

        strongest_df["Absolute Correlation"] = (
            strongest_df["Correlation"].abs()
        )

        strongest_df = strongest_df.sort_values(
            "Absolute Correlation",
            ascending=False
        ).head(10)

        strongest_df = strongest_df[
            [
                "Column 1",
                "Column 2",
                "Correlation"
            ]
        ]

        st.subheader("📌 Strongest Correlations")

        st.dataframe(
            strongest_df.round(4),
            use_container_width=True,
            hide_index=True
        )

else:
    st.info(
        "At least two numeric columns are required for correlation analysis."
    )


# ============================================================
# OUTLIER DETECTION
# ============================================================

st.divider()

st.header("🚨 Outlier Detection")

if numeric_columns:

    outlier_column = st.selectbox(
        "Select Numeric Column",
        numeric_columns,
        key="eda_outlier_column"
    )

    lower_bound, upper_bound, outlier_mask = calculate_iqr_outliers(
        df[outlier_column]
    )

    outlier_count = int(outlier_mask.sum())

    out_col1, out_col2, out_col3 = st.columns(3)

    with out_col1:
        st.metric(
            "Lower Bound",
            format_number(lower_bound)
        )

    with out_col2:
        st.metric(
            "Upper Bound",
            format_number(upper_bound)
        )

    with out_col3:
        st.metric(
            "Outliers Found",
            f"{outlier_count:,}"
        )

    fig_outlier = px.box(
        df,
        y=outlier_column,
        title=f"Box Plot of {outlier_column}"
    )

    st.plotly_chart(
        fig_outlier,
        use_container_width=True,
        key="eda_outlier_boxplot"
    )

    if outlier_count > 0:

        detected_outliers = df.loc[
            outlier_mask
        ]

        st.subheader("🔎 Detected Outliers")

        st.dataframe(
            detected_outliers.head(100),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Showing up to 100 of {outlier_count:,} detected outlier rows."
        )

        if st.button(
            "🗑️ Remove Detected Outliers",
            key="eda_remove_outliers"
        ):

            cleaned_df = df.loc[
                ~outlier_mask
            ].copy()

            st.session_state.df = cleaned_df

            st.success(
                f"✅ Removed {outlier_count:,} outlier rows."
            )

            st.rerun()

    else:
        st.success(
            "✅ No outliers were detected using the IQR method."
        )

else:
    st.info("No numeric columns available for outlier detection.")


# ============================================================
# GROUPBY ANALYSIS
# ============================================================

st.divider()

st.header("📊 GroupBy Analysis")

if categorical_columns and numeric_columns:

    group_column = st.selectbox(
        "Group By",
        categorical_columns,
        key="eda_group_column"
    )

    value_column = st.selectbox(
        "Value Column",
        numeric_columns,
        key="eda_group_value"
    )

    aggregation = st.selectbox(
        "Aggregation",
        [
            "Mean",
            "Sum",
            "Median",
            "Minimum",
            "Maximum",
            "Count"
        ],
        key="eda_group_aggregation"
    )

    aggregation_map = {
        "Mean": "mean",
        "Sum": "sum",
        "Median": "median",
        "Minimum": "min",
        "Maximum": "max",
        "Count": "count"
    }

    agg_func = aggregation_map[aggregation]

    grouped = (
        df.groupby(group_column)[value_column]
        .agg(agg_func)
        .reset_index()
    )

    grouped.columns = [
        group_column,
        value_column
    ]

    grouped = grouped.sort_values(
        value_column,
        ascending=False
    )

    st.dataframe(
        grouped,
        use_container_width=True,
        hide_index=True
    )

    fig_groupby = px.bar(
        grouped.head(20),
        x=group_column,
        y=value_column,
        title=(
            f"{aggregation} of {value_column} "
            f"by {group_column}"
        )
    )

    st.plotly_chart(
        fig_groupby,
        use_container_width=True,
        key="eda_groupby_chart"
    )

else:
    st.info(
        "GroupBy analysis requires at least one categorical "
        "and one numeric column."
    )


# ============================================================
# PIVOT TABLE
# ============================================================

st.divider()

st.header("📋 Pivot Table")

if len(categorical_columns) >= 2 and numeric_columns:

    pivot_row = st.selectbox(
        "Rows",
        categorical_columns,
        key="eda_pivot_rows"
    )

    pivot_column_options = [
        col for col in categorical_columns
        if col != pivot_row
    ]

    pivot_column = st.selectbox(
        "Columns",
        pivot_column_options,
        key="eda_pivot_columns"
    )

    pivot_value = st.selectbox(
        "Values",
        numeric_columns,
        key="eda_pivot_values"
    )

    pivot_aggregation = st.selectbox(
        "Aggregation",
        [
            "sum",
            "mean",
            "median",
            "min",
            "max",
            "count"
        ],
        key="eda_pivot_aggregation"
    )

    pivot_table = pd.pivot_table(
        df,
        index=pivot_row,
        columns=pivot_column,
        values=pivot_value,
        aggfunc=pivot_aggregation,
        fill_value=0
    )

    st.dataframe(
        pivot_table,
        use_container_width=True
    )

    # Limit displayed heatmap size for performance
    heatmap_table = pivot_table.copy()

    if heatmap_table.shape[0] > 30:
        heatmap_table = heatmap_table.head(30)

    if heatmap_table.shape[1] > 20:
        heatmap_table = heatmap_table.iloc[:, :20]

    fig_pivot = px.imshow(
        heatmap_table,
        text_auto=".2f",
        title="Pivot Table Heatmap",
        aspect="auto"
    )

    st.plotly_chart(
        fig_pivot,
        use_container_width=True,
        key="eda_pivot_heatmap"
    )

else:
    st.info(
        "Pivot tables require at least two categorical "
        "columns and one numeric column."
    )


# ============================================================
# AUTOMATIC DATASET INSIGHTS
# ============================================================

st.divider()

st.header("💡 Automatic Dataset Insights")

st.subheader("📋 Dataset Quality")

st.write(
    f"Dataset contains **{df.shape[0]:,} rows** "
    f"and **{df.shape[1]:,} columns**."
)

if missing_values == 0:
    st.success("✅ No missing values found.")
else:
    st.warning(
        f"⚠️ {missing_values:,} missing values found."
    )

if duplicate_rows == 0:
    st.success("✅ No duplicate rows found.")
else:
    st.warning(
        f"⚠️ {duplicate_rows:,} duplicate rows found."
    )


# ============================================================
# NUMERIC INSIGHTS
# ============================================================

if numeric_columns:

    st.subheader("📊 Numeric Insights")

    insight_numeric_column = st.selectbox(
        "Select Numeric Column",
        numeric_columns,
        key="eda_numeric_insight"
    )

    insight_series = pd.to_numeric(
        df[insight_numeric_column],
        errors="coerce"
    ).dropna()

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    with insight_col1:
        st.metric(
            "Average",
            format_number(insight_series.mean())
        )

    with insight_col2:
        st.metric(
            "Highest",
            format_number(insight_series.max())
        )

    with insight_col3:
        st.metric(
            "Lowest",
            format_number(insight_series.min())
        )


# ============================================================
# CATEGORICAL INSIGHTS
# ============================================================

if categorical_columns:

    st.subheader("🏷️ Categorical Insights")

    insight_category = st.selectbox(
        "Select Categorical Column",
        categorical_columns,
        key="eda_category_insight"
    )

    top_categories = (
        df[insight_category]
        .value_counts(dropna=False)
        .head(10)
        .reset_index()
    )

    top_categories.columns = [
        insight_category,
        "Count"
    ]

    st.dataframe(
        top_categories,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MISSING VALUE REPORT
# ============================================================

st.subheader("📌 Missing Value Report")

missing_report = pd.DataFrame(
    {
        "Column": df.columns,
        "Missing Values": df.isna().sum().values,
        "Percentage": (
            df.isna().mean().values * 100
        )
    }
)

missing_report["Percentage"] = (
    missing_report["Percentage"].round(2)
)

st.dataframe(
    missing_report,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# COLUMN PROFILER
# ============================================================

st.divider()

st.header("🔎 Column Profiler")

profile_column = st.selectbox(
    "Select a Column",
    df.columns.tolist(),
    key="eda_profile_column"
)

profile_series = df[profile_column]

profile_type = str(profile_series.dtype)
profile_missing = int(profile_series.isna().sum())
profile_unique = int(profile_series.nunique(dropna=True))
profile_memory = (
    profile_series.memory_usage(deep=True) / 1024
)

profile_col1, profile_col2, profile_col3, profile_col4 = st.columns(4)

with profile_col1:
    st.metric(
        "Data Type",
        profile_type
    )

with profile_col2:
    st.metric(
        "Missing Values",
        f"{profile_missing:,}"
    )

with profile_col3:
    st.metric(
        "Unique Values",
        f"{profile_unique:,}"
    )

with profile_col4:
    st.metric(
        "Memory",
        f"{profile_memory:.2f} KB"
    )


# ============================================================
# COLUMN NUMERIC ANALYSIS
# ============================================================

if pd.api.types.is_numeric_dtype(profile_series):

    st.subheader("📈 Numeric Analysis")

    numeric_profile = pd.to_numeric(
        profile_series,
        errors="coerce"
    ).dropna()

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.metric(
            "Mean",
            format_number(numeric_profile.mean())
        )

    with p2:
        st.metric(
            "Median",
            format_number(numeric_profile.median())
        )

    with p3:
        st.metric(
            "Minimum",
            format_number(numeric_profile.min())
        )

    with p4:
        st.metric(
            "Maximum",
            format_number(numeric_profile.max())
        )

    fig_profile_distribution = px.histogram(
        df,
        x=profile_column,
        nbins=30,
        title=f"Distribution of {profile_column}"
    )

    st.plotly_chart(
        fig_profile_distribution,
        use_container_width=True,
        key="eda_profile_distribution"
    )

    fig_profile_box = px.box(
        df,
        y=profile_column,
        title=f"Box Plot of {profile_column}"
    )

    st.plotly_chart(
        fig_profile_box,
        use_container_width=True,
        key="eda_profile_boxplot"
    )


# ============================================================
# COLUMN CATEGORICAL ANALYSIS
# ============================================================

elif (
    pd.api.types.is_object_dtype(profile_series)
    or pd.api.types.is_categorical_dtype(profile_series)
):

    st.subheader("🏷️ Categorical Analysis")

    profile_counts = (
        profile_series
        .value_counts(dropna=False)
        .head(20)
        .reset_index()
    )

    profile_counts.columns = [
        profile_column,
        "Count"
    ]

    st.dataframe(
        profile_counts,
        use_container_width=True,
        hide_index=True
    )

    fig_profile_category = px.bar(
        profile_counts,
        x=profile_column,
        y="Count",
        title=f"Distribution of {profile_column}"
    )

    st.plotly_chart(
        fig_profile_category,
        use_container_width=True,
        key="eda_profile_category"
    )


# ============================================================
# DATE ANALYSIS
# ============================================================

if date_columns:

    st.divider()

    st.header("📅 Date Analysis")

    selected_date_column = st.selectbox(
        "Select Date Column",
        date_columns,
        key="eda_date_column"
    )

    converted_dates = pd.to_datetime(
        df[selected_date_column],
        errors="coerce"
    )

    valid_dates = converted_dates.dropna()

    if not valid_dates.empty:

        date_col1, date_col2, date_col3 = st.columns(3)

        with date_col1:
            st.metric(
                "Earliest Date",
                valid_dates.min().strftime("%Y-%m-%d")
            )

        with date_col2:
            st.metric(
                "Latest Date",
                valid_dates.max().strftime("%Y-%m-%d")
            )

        with date_col3:
            st.metric(
                "Unique Dates",
                f"{valid_dates.nunique():,}"
            )

        date_counts = (
            valid_dates
            .dt.to_period("M")
            .value_counts()
            .sort_index()
            .reset_index()
        )

        date_counts.columns = [
            "Month",
            "Count"
        ]

        date_counts["Month"] = (
            date_counts["Month"]
            .astype(str)
        )

        fig_date = px.line(
            date_counts,
            x="Month",
            y="Count",
            markers=True,
            title=f"Records Over Time — {selected_date_column}"
        )

        st.plotly_chart(
            fig_date,
            use_container_width=True,
            key="eda_date_chart"
        )


# ============================================================
# FINAL STATUS
# ============================================================

st.divider()

st.success(
    "✅ Exploratory Data Analysis completed. "
    "Use Data Visualization, Dashboard, or Export Data "
    "to continue."
)



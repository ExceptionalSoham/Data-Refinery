import streamlit as st
import pandas as pd


from utils.theme import apply_theme


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Filter & Search | DataRefinery",
    page_icon="🔍",
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

st.title("🔍 Data Filter & Search")

st.caption(
    "Search, filter and sort your dataset to find the records you need."
)

st.info(
    "Use one or more filters together. The results update automatically."
)

st.divider()


# =========================================================
# ORIGINAL DATASET SUMMARY
# =========================================================

st.subheader("📊 Original Dataset")

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "📄 Rows",
        f"{df.shape[0]:,}"
    )

with c2:

    st.metric(
        "📋 Columns",
        f"{df.shape[1]:,}"
    )

with c3:

    st.metric(
        "🔎 Searchable Records",
        f"{df.shape[0]:,}"
    )


st.divider()


# =========================================================
# FILTERED DATAFRAME
# =========================================================

filtered_df = df.copy()


# =========================================================
# TEXT SEARCH
# =========================================================

st.subheader("🔎 Global Search")

search_text = st.text_input(
    "Search across all columns",
    placeholder="Enter a name, city, product, order ID, etc."
)


if search_text:

    filtered_df = filtered_df[
        filtered_df
        .astype(str)
        .apply(
            lambda column:
            column.str.contains(
                search_text,
                case=False,
                na=False,
                regex=False
            )
        )
        .any(axis=1)
    ]


st.divider()


# =========================================================
# COLUMN FILTER
# =========================================================

st.subheader("📂 Category Filter")

categorical_columns = (
    filtered_df
    .select_dtypes(
        include=["object", "category"]
    )
    .columns
    .tolist()
)


if categorical_columns:

    selected_column = st.selectbox(
        "Select categorical column",
        ["None"] + categorical_columns,
        key="category_filter"
    )

    if selected_column != "None":

        available_values = (
            filtered_df[selected_column]
            .dropna()
            .unique()
            .tolist()
        )

        available_values = sorted(
            available_values,
            key=lambda value: str(value)
        )

        selected_values = st.multiselect(
            "Select values",
            available_values,
            key="category_values"
        )

        if selected_values:

            filtered_df = filtered_df[
                filtered_df[selected_column]
                .isin(selected_values)
            ]


else:

    st.info(
        "No categorical columns are available for category filtering."
    )


st.divider()


# =========================================================
# NUMERIC RANGE FILTER
# =========================================================

st.subheader("🔢 Numeric Range Filter")

numeric_columns = (
    filtered_df
    .select_dtypes(include="number")
    .columns
    .tolist()
)


if numeric_columns:

    numeric_column = st.selectbox(
        "Select numeric column",
        ["None"] + numeric_columns,
        key="numeric_filter"
    )

    if numeric_column != "None":

        numeric_series = (
            filtered_df[numeric_column]
            .dropna()
        )

        if not numeric_series.empty:

            min_value = float(
                numeric_series.min()
            )

            max_value = float(
                numeric_series.max()
            )

            if min_value < max_value:

                selected_range = st.slider(
                    "Select value range",
                    min_value=min_value,
                    max_value=max_value,
                    value=(
                        min_value,
                        max_value
                    ),
                    key="numeric_range"
                )

                filtered_df = filtered_df[
                    (
                        filtered_df[numeric_column]
                        >= selected_range[0]
                    )
                    &
                    (
                        filtered_df[numeric_column]
                        <= selected_range[1]
                    )
                ]

            else:

                st.info(
                    f"All values in `{numeric_column}` are the same."
                )


else:

    st.info(
        "No numeric columns are available for numeric filtering."
    )


st.divider()


# =========================================================
# DATE FILTER
# =========================================================

st.subheader("📅 Date Filter")

date_candidates = []

for column in filtered_df.columns:

    if pd.api.types.is_datetime64_any_dtype(
        filtered_df[column]
    ):

        date_candidates.append(column)

    elif filtered_df[column].dtype == "object":

        converted = pd.to_datetime(
            filtered_df[column],
            errors="coerce"
        )

        if converted.notna().mean() >= 0.80:

            date_candidates.append(column)


if date_candidates:

    date_column = st.selectbox(
        "Select date column",
        ["None"] + date_candidates,
        key="date_filter"
    )

    if date_column != "None":

        date_series = pd.to_datetime(
            filtered_df[date_column],
            errors="coerce"
        )

        valid_dates = date_series.dropna()

        if not valid_dates.empty:

            minimum_date = valid_dates.min().date()
            maximum_date = valid_dates.max().date()

            date_range = st.date_input(
                "Select date range",
                value=(
                    minimum_date,
                    maximum_date
                ),
                min_value=minimum_date,
                max_value=maximum_date,
                key="date_range"
            )

            if isinstance(
                date_range,
                tuple
            ) and len(date_range) == 2:

                start_date, end_date = date_range

                filtered_df = filtered_df[
                    (
                        date_series.dt.date
                        >= start_date
                    )
                    &
                    (
                        date_series.dt.date
                        <= end_date
                    )
                ]

else:

    st.info(
        "No date columns detected in the current dataset."
    )


st.divider()


# =========================================================
# SORTING
# =========================================================

st.subheader("↕️ Sort Results")

sort_column = st.selectbox(
    "Sort by column",
    ["None"] + filtered_df.columns.tolist(),
    key="sort_column"
)


if sort_column != "None":

    sort_order = st.radio(
        "Sort order",
        ["Ascending", "Descending"],
        horizontal=True,
        key="sort_order"
    )

    filtered_df = filtered_df.sort_values(
        by=sort_column,
        ascending=(sort_order == "Ascending")
    )


st.divider()


# =========================================================
# RESULTS SUMMARY
# =========================================================

st.subheader("📊 Filter Results")

result_count = len(filtered_df)
original_count = len(df)

if original_count > 0:

    percentage = (
        result_count / original_count
    ) * 100

else:

    percentage = 0


r1, r2, r3 = st.columns(3)


with r1:

    st.metric(
        "Rows Found",
        f"{result_count:,}"
    )


with r2:

    st.metric(
        "Rows Removed",
        f"{original_count - result_count:,}"
    )


with r3:

    st.metric(
        "Match Rate",
        f"{percentage:.2f}%"
    )


# =========================================================
# RESULT STATUS
# =========================================================

if result_count == 0:

    st.warning(
        "⚠️ No records match the current filters."
    )

elif result_count == original_count:

    st.info(
        "ℹ️ All records match the current filters."
    )

else:

    st.success(
        f"✅ {result_count:,} records match your filters."
    )


st.divider()


# =========================================================
# FILTERED DATA PREVIEW
# =========================================================

st.subheader("👀 Filtered Dataset")

preview_rows = min(
    100,
    max(1, len(filtered_df))
)


if len(filtered_df) > 0:

    rows_to_show = st.slider(
        "Rows to display",
        min_value=1,
        max_value=preview_rows,
        value=min(10, preview_rows),
        key="filtered_preview"
    )

    st.dataframe(
        filtered_df.head(rows_to_show),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No data to display."
    )


st.divider()


# =========================================================
# DOWNLOAD
# =========================================================

st.subheader("💾 Export Filtered Results")


if not filtered_df.empty:

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered CSV",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

else:

    st.info(
        "There are no filtered records available for download."
    )


# =========================================================
# SAVE FILTERED DATASET
# =========================================================

st.session_state.filtered_df = filtered_df.copy()






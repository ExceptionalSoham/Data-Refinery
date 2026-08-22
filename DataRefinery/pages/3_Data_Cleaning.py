import streamlit as st
import pandas as pd

from utils.theme import apply_theme


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Data Cleaning | DataRefinery",
    page_icon="🧹",
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

st.title("🧹 Data Cleaning")

st.caption(
    "Prepare your dataset by identifying and fixing common "
    "data quality issues."
)

st.info(
    "Use the tools below to handle missing values, duplicate rows, "
    "column names, and data types."
)

st.divider()


# =========================================================
# CURRENT DATASET SUMMARY
# =========================================================

st.subheader("📊 Current Dataset")

rows_before = len(df)
columns_before = len(df.columns)
missing_before = int(df.isnull().sum().sum())
duplicates_before = int(df.duplicated().sum())


c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "📄 Rows",
        f"{rows_before:,}"
    )

with c2:
    st.metric(
        "📋 Columns",
        f"{columns_before:,}"
    )

with c3:
    st.metric(
        "❗ Missing Values",
        f"{missing_before:,}"
    )

with c4:
    st.metric(
        "🔁 Duplicate Rows",
        f"{duplicates_before:,}"
    )


st.divider()


# =========================================================
# DATASET HEALTH
# =========================================================

st.subheader("🩺 Cleaning Status")

if missing_before == 0 and duplicates_before == 0:

    st.success(
        "✅ Your dataset currently has no missing values or duplicate rows."
    )

elif missing_before > 0 and duplicates_before == 0:

    st.warning(
        f"⚠️ {missing_before:,} missing values need attention."
    )

elif missing_before == 0 and duplicates_before > 0:

    st.warning(
        f"⚠️ {duplicates_before:,} duplicate rows need attention."
    )

else:

    st.error(
        f"❌ The dataset contains {missing_before:,} missing values "
        f"and {duplicates_before:,} duplicate rows."
    )


st.divider()


# =========================================================
# MISSING VALUES BY COLUMN
# =========================================================

st.subheader("🔎 Missing Values by Column")

missing_df = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values
})

missing_df["Missing %"] = (
    missing_df["Missing Values"]
    / len(df)
    * 100
).round(2)

missing_df = missing_df.sort_values(
    by="Missing Values",
    ascending=False
)


st.dataframe(
    missing_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# MISSING VALUE HANDLING
# =========================================================

st.subheader("🛠 Missing Value Handling")

cleaning_option = st.selectbox(
    "Select a cleaning method",
    [
        "Do Nothing",
        "Remove Rows with Missing Values",
        "Fill Numeric Columns with Mean",
        "Fill Numeric Columns with Median",
        "Fill Numeric Columns with 0",
        "Fill Categorical Columns with Mode",
        "Fill Categorical Columns with 'Unknown'"
    ]
)


if st.button(
    "🧹 Apply Missing Value Cleaning",
    type="primary"
):

    before_rows = len(df)
    before_missing = int(
        df.isnull().sum().sum()
    )

    if cleaning_option == "Remove Rows with Missing Values":

        df = df.dropna()

    elif cleaning_option == "Fill Numeric Columns with Mean":

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_cols) > 0:

            df[numeric_cols] = (
                df[numeric_cols]
                .fillna(
                    df[numeric_cols].mean()
                )
            )

    elif cleaning_option == "Fill Numeric Columns with Median":

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_cols) > 0:

            df[numeric_cols] = (
                df[numeric_cols]
                .fillna(
                    df[numeric_cols].median()
                )
            )

    elif cleaning_option == "Fill Numeric Columns with 0":

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_cols) > 0:

            df[numeric_cols] = (
                df[numeric_cols]
                .fillna(0)
            )

    elif cleaning_option == "Fill Categorical Columns with Mode":

        categorical_cols = df.select_dtypes(
            include=["object", "category"]
        ).columns

        for column in categorical_cols:

            mode = df[column].mode()

            if not mode.empty:

                df[column] = df[column].fillna(
                    mode.iloc[0]
                )

    elif cleaning_option == "Fill Categorical Columns with 'Unknown'":

        categorical_cols = df.select_dtypes(
            include=["object", "category"]
        ).columns

        for column in categorical_cols:

            df[column] = df[column].fillna(
                "Unknown"
            )

    after_rows = len(df)

    after_missing = int(
        df.isnull().sum().sum()
    )

    st.session_state.df = df

    rows_removed = before_rows - after_rows
    missing_fixed = before_missing - after_missing

    st.success(
        f"✅ Cleaning completed. "
        f"Rows removed: {rows_removed:,} | "
        f"Missing values resolved: {missing_fixed:,}"
    )

    st.rerun()


st.divider()


# =========================================================
# DUPLICATE ROWS
# =========================================================

st.subheader("🔁 Duplicate Rows")

duplicate_count = int(
    df.duplicated().sum()
)

if duplicate_count > 0:

    st.warning(
        f"⚠️ {duplicate_count:,} duplicate rows detected."
    )

    if st.button(
        "🗑️ Remove Duplicate Rows",
        type="primary"
    ):

        before = len(df)

        df = df.drop_duplicates()

        after = len(df)

        removed = before - after

        st.session_state.df = df

        st.success(
            f"✅ {removed:,} duplicate rows removed."
        )

        st.rerun()

else:

    st.success(
        "✅ No duplicate rows found."
    )


st.divider()


# =========================================================
# COLUMN OPERATIONS
# =========================================================

st.header("🛠️ Column Operations")


# =========================================================
# RENAME COLUMN
# =========================================================

st.subheader("✏️ Rename Column")

rename_col1, rename_col2 = st.columns(2)

with rename_col1:

    old_name = st.selectbox(
        "Select column",
        df.columns,
        key="rename_old"
    )

with rename_col2:

    new_name = st.text_input(
        "New column name",
        key="rename_new"
    )


if st.button("✏️ Rename Column"):

    new_name = new_name.strip()

    if not new_name:

        st.warning(
            "Please enter a new column name."
        )

    elif new_name in df.columns:

        st.warning(
            "That column name already exists."
        )

    else:

        df = df.rename(
            columns={
                old_name: new_name
            }
        )

        st.session_state.df = df

        st.success(
            f"✅ '{old_name}' renamed to '{new_name}'."
        )

        st.rerun()


st.divider()


# =========================================================
# DELETE COLUMNS
# =========================================================

st.subheader("🗑️ Delete Columns")

columns_to_delete = st.multiselect(
    "Select columns to delete",
    df.columns
)


if st.button("🗑️ Delete Selected Columns"):

    if not columns_to_delete:

        st.warning(
            "Please select at least one column."
        )

    elif len(columns_to_delete) == len(df.columns):

        st.error(
            "You cannot delete every column in the dataset."
        )

    else:

        df = df.drop(
            columns=columns_to_delete
        )

        st.session_state.df = df

        st.success(
            "✅ Selected columns deleted."
        )

        st.rerun()


st.divider()


# =========================================================
# CHANGE DATA TYPE
# =========================================================

st.subheader("🔄 Change Data Type")

dtype_col1, dtype_col2 = st.columns(2)

with dtype_col1:

    selected_column = st.selectbox(
        "Select column",
        df.columns,
        key="dtype_column"
    )

with dtype_col2:

    new_dtype = st.selectbox(
        "Convert to",
        [
            "Integer",
            "Float",
            "String",
            "Datetime"
        ]
    )


if st.button("🔄 Convert Data Type"):

    try:

        if new_dtype == "Integer":

            converted = pd.to_numeric(
                df[selected_column],
                errors="coerce"
            )

            df[selected_column] = (
                converted.astype("Int64")
            )

        elif new_dtype == "Float":

            df[selected_column] = pd.to_numeric(
                df[selected_column],
                errors="coerce"
            )

        elif new_dtype == "String":

            df[selected_column] = (
                df[selected_column]
                .astype("string")
            )

        elif new_dtype == "Datetime":

            df[selected_column] = pd.to_datetime(
                df[selected_column],
                errors="coerce"
            )

        st.session_state.df = df

        st.success(
            f"✅ '{selected_column}' converted to {new_dtype}."
        )

        st.rerun()

    except Exception as e:

        st.error(
            f"❌ Data type conversion failed: {e}"
        )


st.divider()


# =========================================================
# FINAL CLEANED DATASET SUMMARY
# =========================================================

st.subheader("📊 Cleaned Dataset Summary")

final_rows = len(df)
final_columns = len(df.columns)
final_missing = int(
    df.isnull().sum().sum()
)
final_duplicates = int(
    df.duplicated().sum()
)


f1, f2, f3, f4 = st.columns(4)

with f1:
    st.metric(
        "Rows",
        f"{final_rows:,}"
    )

with f2:
    st.metric(
        "Columns",
        f"{final_columns:,}"
    )

with f3:
    st.metric(
        "Missing Values",
        f"{final_missing:,}"
    )

with f4:
    st.metric(
        "Duplicate Rows",
        f"{final_duplicates:,}"
    )


st.divider()


# =========================================================
# CLEANED DATASET PREVIEW
# =========================================================

st.subheader("👀 Cleaned Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# FINAL MESSAGE
# =========================================================

if final_missing == 0 and final_duplicates == 0:

    st.success(
        "🎉 Your dataset is clean and ready for analysis."
    )

else:

    st.info(
        "ℹ️ Some data-quality issues remain. "
        "Use the cleaning tools above before moving to "
        "Visualization or EDA."
    )







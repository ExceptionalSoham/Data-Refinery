import streamlit as st
import pandas as pd
from io import BytesIO

from utils.theme import apply_theme


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Export Data | DataRefinery",
    page_icon="💾",
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

st.title("💾 Export Data")

st.caption(
    "Download your current dataset or filtered results "
    "in convenient file formats."
)

st.info(
    "Choose an export format below. The exported data reflects "
    "the current dataset stored in DataRefinery."
)

st.divider()


# =========================================================
# DATASET INFORMATION
# =========================================================

st.subheader("📊 Current Dataset")

rows = len(df)
columns = len(df.columns)
missing = int(df.isnull().sum().sum())
duplicates = int(df.duplicated().sum())

memory_mb = (
    df.memory_usage(deep=True).sum()
    / 1024
    / 1024
)

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
        f"{missing:,}"
    )

with c4:
    st.metric(
        "🔁 Duplicate Rows",
        f"{duplicates:,}"
    )

with c5:
    st.metric(
        "💾 Memory",
        f"{memory_mb:.2f} MB"
    )


st.divider()


# =========================================================
# EXPORT FILENAME
# =========================================================

st.subheader("📝 Export Settings")

base_filename = st.text_input(
    "Enter filename",
    value="datarefinery_dataset",
    help="Do not include the file extension."
)

base_filename = base_filename.strip()

if not base_filename:

    base_filename = "datarefinery_dataset"


st.divider()


# =========================================================
# DATASET PREVIEW
# =========================================================

st.subheader("👀 Export Preview")

preview_rows = min(
    10,
    max(1, rows)
)

st.dataframe(
    df.head(preview_rows),
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# CSV EXPORT
# =========================================================

st.subheader("📄 CSV Export")

csv_data = df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Current Dataset as CSV",
    data=csv_data,
    file_name=f"{base_filename}.csv",
    mime="text/csv",
    use_container_width=True
)


st.success(
    "✅ CSV export is ready."
)


st.divider()


# =========================================================
# EXCEL EXPORT
# =========================================================

st.subheader("📊 Excel Export")


try:

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Data"
        )

    excel_buffer.seek(0)

    st.download_button(
        label="⬇️ Download Current Dataset as Excel",
        data=excel_buffer.getvalue(),
        file_name=f"{base_filename}.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True
    )

    st.success(
        "✅ Excel export is ready."
    )

except Exception as e:

    st.error(
        f"❌ Unable to create Excel file: {e}"
    )


st.divider()


# =========================================================
# FILTERED DATA EXPORT
# =========================================================

st.subheader("🔍 Filtered Dataset Export")


if (
    "filtered_df" in st.session_state
    and st.session_state.filtered_df is not None
):

    filtered_df = st.session_state.filtered_df.copy()

    filtered_rows = len(filtered_df)

    st.metric(
        "Filtered Rows",
        f"{filtered_rows:,}"
    )

    if filtered_rows > 0:

        st.dataframe(
            filtered_df.head(10),
            use_container_width=True,
            hide_index=True
        )

        filtered_csv = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Filtered Results",
            data=filtered_csv,
            file_name=f"{base_filename}_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.success(
            "✅ Filtered dataset is ready for download."
        )

    else:

        st.info(
            "ℹ️ The current filter contains no records."
        )

else:

    st.info(
        "ℹ️ No filtered dataset is currently available. "
        "Use the Data Filter & Search page first."
    )


st.divider()


# =========================================================
# EXPORT SUMMARY
# =========================================================

st.subheader("📋 Export Summary")

summary = pd.DataFrame({
    "Item": [
        "Rows",
        "Columns",
        "Missing Values",
        "Duplicate Rows",
        "Memory Usage"
    ],
    "Value": [
        f"{rows:,}",
        f"{columns:,}",
        f"{missing:,}",
        f"{duplicates:,}",
        f"{memory_mb:.2f} MB"
    ]
})


st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# FINAL STATUS
# =========================================================

if missing == 0 and duplicates == 0:

    st.success(
        "🚀 Your dataset is clean and ready for export."
    )

else:

    st.warning(
        "⚠️ Your dataset still contains data-quality issues. "
        "Review Data Cleaning before final export."
    )




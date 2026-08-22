import streamlit as st
import pandas as pd
import plotly.express as px


from utils.theme import apply_theme


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Data Visualization | DataRefinery",
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

st.title("📊 Data Visualization")

st.caption(
    "Explore patterns, trends, distributions and relationships "
    "through interactive charts."
)

st.info(
    "Choose a chart type below and select the columns you want "
    "to visualize."
)

st.divider()


# =========================================================
# COLUMN GROUPS
# =========================================================

numeric_columns = (
    df.select_dtypes(include="number")
    .columns
    .tolist()
)

categorical_columns = (
    df.select_dtypes(include=["object", "category"])
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


all_columns = df.columns.tolist()


# =========================================================
# CHART SELECTOR
# =========================================================

st.subheader("🎨 Choose Visualization")

chart = st.selectbox(
    "Chart Type",
    [
        "Histogram",
        "Bar Chart",
        "Line Chart",
        "Area Chart",
        "Scatter Plot",
        "Box Plot",
        "Violin Plot",
        "Pie Chart",
        "Donut Chart",
        "Treemap",
        "Sunburst Chart",
        "Bubble Chart",
        "Correlation Heatmap"
    ]
)


st.divider()


# =========================================================
# HELPER
# =========================================================

def show_chart(fig):

    fig.update_layout(
        template="plotly_dark",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True
        }
    )


# =========================================================
# HISTOGRAM
# =========================================================

if chart == "Histogram":

    if not numeric_columns:

        st.warning(
            "⚠️ No numeric columns are available for a histogram."
        )

    else:

        column = st.selectbox(
            "Numeric Column",
            numeric_columns
        )

        bins = st.slider(
            "Number of bins",
            min_value=5,
            max_value=100,
            value=30
        )

        fig = px.histogram(
            df,
            x=column,
            nbins=bins,
            title=f"Distribution of {column}"
        )

        show_chart(fig)


# =========================================================
# BAR CHART
# =========================================================

elif chart == "Bar Chart":

    if not categorical_columns or not numeric_columns:

        st.warning(
            "⚠️ Bar Chart requires at least one categorical "
            "and one numeric column."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:
            category = st.selectbox(
                "Category",
                categorical_columns,
                key="bar_category"
            )

        with col2:
            value = st.selectbox(
                "Numeric Value",
                numeric_columns,
                key="bar_value"
            )

        aggregation = st.selectbox(
            "Aggregation",
            ["Sum", "Average", "Count", "Minimum", "Maximum"]
        )

        if aggregation == "Sum":

            chart_df = (
                df.groupby(category, dropna=False)[value]
                .sum()
                .reset_index()
            )

        elif aggregation == "Average":

            chart_df = (
                df.groupby(category, dropna=False)[value]
                .mean()
                .reset_index()
            )

        elif aggregation == "Count":

            chart_df = (
                df.groupby(category, dropna=False)[value]
                .count()
                .reset_index()
            )

        elif aggregation == "Minimum":

            chart_df = (
                df.groupby(category, dropna=False)[value]
                .min()
                .reset_index()
            )

        else:

            chart_df = (
                df.groupby(category, dropna=False)[value]
                .max()
                .reset_index()
            )

        chart_df = chart_df.sort_values(
            by=value,
            ascending=False
        ).head(30)

        fig = px.bar(
            chart_df,
            x=category,
            y=value,
            title=f"{aggregation} of {value} by {category}"
        )

        show_chart(fig)


# =========================================================
# LINE CHART
# =========================================================

elif chart == "Line Chart":

    if not numeric_columns:

        st.warning(
            "⚠️ At least one numeric column is required."
        )

    elif not date_columns and not categorical_columns:

        st.warning(
            "⚠️ A date or categorical column is required for the X axis."
        )

    else:

        x_options = date_columns + categorical_columns

        col1, col2 = st.columns(2)

        with col1:

            x = st.selectbox(
                "X Axis",
                x_options,
                key="line_x"
            )

        with col2:

            y = st.selectbox(
                "Y Axis",
                numeric_columns,
                key="line_y"
            )

        sort_data = st.checkbox(
            "Sort X axis",
            value=True
        )

        line_df = df[[x, y]].dropna()

        if sort_data:
            line_df = line_df.sort_values(x)

        fig = px.line(
            line_df,
            x=x,
            y=y,
            markers=True,
            title=f"{y} over {x}"
        )

        show_chart(fig)


# =========================================================
# AREA CHART
# =========================================================

elif chart == "Area Chart":

    if not numeric_columns:

        st.warning(
            "⚠️ At least one numeric column is required."
        )

    else:

        x_options = date_columns + categorical_columns

        if not x_options:

            st.warning(
                "⚠️ A categorical or date column is required."
            )

        else:

            col1, col2 = st.columns(2)

            with col1:

                x = st.selectbox(
                    "X Axis",
                    x_options,
                    key="area_x"
                )

            with col2:

                y = st.selectbox(
                    "Y Axis",
                    numeric_columns,
                    key="area_y"
                )

            area_df = df[[x, y]].dropna()

            fig = px.area(
                area_df,
                x=x,
                y=y,
                title=f"{y} over {x}"
            )

            show_chart(fig)


# =========================================================
# SCATTER PLOT
# =========================================================

elif chart == "Scatter Plot":

    if len(numeric_columns) < 2:

        st.warning(
            "⚠️ At least two numeric columns are required."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            x = st.selectbox(
                "X Axis",
                numeric_columns,
                key="scatter_x"
            )

        with col2:

            y_options = [
                column
                for column in numeric_columns
                if column != x
            ]

            y = st.selectbox(
                "Y Axis",
                y_options,
                key="scatter_y"
            )

        color_options = (
            ["None"] +
            categorical_columns
        )

        color = st.selectbox(
            "Color",
            color_options,
            key="scatter_color"
        )

        if color == "None":

            fig = px.scatter(
                df,
                x=x,
                y=y,
                title=f"{y} vs {x}"
            )

        else:

            fig = px.scatter(
                df,
                x=x,
                y=y,
                color=color,
                title=f"{y} vs {x}"
            )

        show_chart(fig)


# =========================================================
# BOX PLOT
# =========================================================

elif chart == "Box Plot":

    if not numeric_columns:

        st.warning(
            "⚠️ No numeric columns are available."
        )

    else:

        numeric_column = st.selectbox(
            "Numeric Column",
            numeric_columns,
            key="box_column"
        )

        category_options = (
            ["None"] +
            categorical_columns
        )

        category = st.selectbox(
            "Group By",
            category_options,
            key="box_category"
        )

        if category == "None":

            fig = px.box(
                df,
                y=numeric_column,
                title=f"Box Plot of {numeric_column}"
            )

        else:

            fig = px.box(
                df,
                x=category,
                y=numeric_column,
                title=f"{numeric_column} by {category}"
            )

        show_chart(fig)


# =========================================================
# VIOLIN PLOT
# =========================================================

elif chart == "Violin Plot":

    if not numeric_columns:

        st.warning(
            "⚠️ No numeric columns are available."
        )

    else:

        numeric_column = st.selectbox(
            "Numeric Column",
            numeric_columns,
            key="violin_column"
        )

        category_options = (
            ["None"] +
            categorical_columns
        )

        category = st.selectbox(
            "Group By",
            category_options,
            key="violin_category"
        )

        if category == "None":

            fig = px.violin(
                df,
                y=numeric_column,
                box=True,
                title=f"Violin Plot of {numeric_column}"
            )

        else:

            fig = px.violin(
                df,
                x=category,
                y=numeric_column,
                box=True,
                title=f"{numeric_column} by {category}"
            )

        show_chart(fig)


# =========================================================
# PIE CHART
# =========================================================

elif chart == "Pie Chart":

    if not categorical_columns:

        st.warning(
            "⚠️ No categorical columns are available."
        )

    else:

        category = st.selectbox(
            "Category",
            categorical_columns,
            key="pie_category"
        )

        counts = (
            df[category]
            .value_counts()
            .head(15)
            .reset_index()
        )

        counts.columns = [
            category,
            "Count"
        ]

        fig = px.pie(
            counts,
            names=category,
            values="Count",
            title=f"Distribution of {category}"
        )

        show_chart(fig)


# =========================================================
# DONUT CHART
# =========================================================

elif chart == "Donut Chart":

    if not categorical_columns:

        st.warning(
            "⚠️ No categorical columns are available."
        )

    else:

        category = st.selectbox(
            "Category",
            categorical_columns,
            key="donut_category"
        )

        counts = (
            df[category]
            .value_counts()
            .head(15)
            .reset_index()
        )

        counts.columns = [
            category,
            "Count"
        ]

        fig = px.pie(
            counts,
            names=category,
            values="Count",
            hole=0.55,
            title=f"Distribution of {category}"
        )

        show_chart(fig)


# =========================================================
# TREEMAP
# =========================================================

elif chart == "Treemap":

    if not categorical_columns or not numeric_columns:

        st.warning(
            "⚠️ Treemap requires at least one categorical "
            "and one numeric column."
        )

    else:

        category = st.selectbox(
            "Category",
            categorical_columns,
            key="treemap_category"
        )

        value = st.selectbox(
            "Numeric Value",
            numeric_columns,
            key="treemap_value"
        )

        treemap_df = (
            df.groupby(category, dropna=False)[value]
            .sum()
            .reset_index()
        )

        fig = px.treemap(
            treemap_df,
            path=[category],
            values=value,
            title=f"{value} by {category}"
        )

        show_chart(fig)


# =========================================================
# SUNBURST
# =========================================================

elif chart == "Sunburst Chart":

    if len(categorical_columns) < 2:

        st.warning(
            "⚠️ Sunburst Chart requires at least two "
            "categorical columns."
        )

    elif not numeric_columns:

        st.warning(
            "⚠️ At least one numeric column is required."
        )

    else:

        level1 = st.selectbox(
            "Level 1",
            categorical_columns,
            key="sun_level1"
        )

        remaining = [
            column
            for column in categorical_columns
            if column != level1
        ]

        level2 = st.selectbox(
            "Level 2",
            remaining,
            key="sun_level2"
        )

        value = st.selectbox(
            "Numeric Value",
            numeric_columns,
            key="sun_value"
        )

        sunburst_df = (
            df.groupby(
                [level1, level2],
                dropna=False
            )[value]
            .sum()
            .reset_index()
        )

        fig = px.sunburst(
            sunburst_df,
            path=[level1, level2],
            values=value,
            title=f"{value} by {level1} → {level2}"
        )

        show_chart(fig)


# =========================================================
# BUBBLE CHART
# =========================================================

elif chart == "Bubble Chart":

    if len(numeric_columns) < 3:

        st.warning(
            "⚠️ Bubble Chart requires at least three "
            "numeric columns."
        )

    else:

        x = st.selectbox(
            "X Axis",
            numeric_columns,
            key="bubble_x"
        )

        y_options = [
            column
            for column in numeric_columns
            if column != x
        ]

        y = st.selectbox(
            "Y Axis",
            y_options,
            key="bubble_y"
        )

        size_options = [
            column
            for column in numeric_columns
            if column not in [x, y]
        ]

        if not size_options:

            size_options = numeric_columns

        size = st.selectbox(
            "Bubble Size",
            size_options,
            key="bubble_size"
        )

        color_options = (
            ["None"] +
            categorical_columns
        )

        color = st.selectbox(
            "Color",
            color_options,
            key="bubble_color"
        )

        if color == "None":

            fig = px.scatter(
                df,
                x=x,
                y=y,
                size=size,
                title=f"Bubble Chart: {y} vs {x}"
            )

        else:

            fig = px.scatter(
                df,
                x=x,
                y=y,
                size=size,
                color=color,
                title=f"Bubble Chart: {y} vs {x}"
            )

        show_chart(fig)


# =========================================================
# CORRELATION HEATMAP
# =========================================================

elif chart == "Correlation Heatmap":

    if len(numeric_columns) < 2:

        st.warning(
            "⚠️ At least two numeric columns are required."
        )

    else:

        corr = df[numeric_columns].corr()

        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            title="Numeric Column Correlation"
        )

        show_chart(fig)


# =========================================================
# CHART INFORMATION
# =========================================================

st.divider()

st.subheader("💡 Visualization Tips")

st.markdown("""
**Histogram** → Understand the distribution of a numeric column.

**Bar Chart** → Compare a numeric value across categories.

**Line / Area Chart** → Explore trends over time or ordered categories.

**Scatter Plot** → Examine relationships between two numeric columns.

**Box / Violin Plot** → Understand spread and potential outliers.

**Pie / Donut Chart** → View category proportions.

**Treemap / Sunburst** → Explore hierarchical category relationships.

**Correlation Heatmap** → Identify relationships between numeric columns.
""")


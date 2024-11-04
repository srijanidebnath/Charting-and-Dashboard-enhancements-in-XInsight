import pandas as pd
import streamlit as st
import altair as alt
import json
import plotly.express as px

# Load the geojson file for India census choropleth map
with open("states_india.geojson", "r", encoding="utf-8") as f:
    india_states = json.load(f)

# Ensure the "id" is assigned correctly to the GeoJSON features
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]

# Set Streamlit app configuration
st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")
st.header("Xinsight Demo")
st.subheader("Upload your Data!")
uploaded_file = st.file_uploader("Upload a file", type=['csv', 'xlsx', 'xls'])

# Load the data if a file is uploaded
df = None
if uploaded_file:
    if uploaded_file.type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.type == 'text/csv':
        df = pd.read_csv(uploaded_file)

    # Remove columns with complete NaN values
    df = df.dropna(axis=1, how='all')
    state_columns = {"state", "state_name", "state or union territory"}
    population_columns = {"population", "total_population", "density", "area"}

    # Determine if the data matches census data structure
    geo_col = next((col for col in df.columns if col.lower() in state_columns), None)
    is_census_data = geo_col is not None

    # Function to classify columns as numeric or categorical
    def identify_column_types(df):
        numeric_columns = []
        categorical_columns = []
        for column in df.columns:
            try:
                df[column].astype(float)
                numeric_columns.append(column)
            except ValueError:
                categorical_columns.append(column)
        return numeric_columns, categorical_columns

    # Identify column types based on convertibility to float
    numeric_columns, categorical_columns = identify_column_types(df)

    # Display dataset checkbox
    if st.sidebar.checkbox("Display Dataset"):
        st.write(df)

    if st.sidebar.checkbox("Display Charts"):
        st.header("Visualization")

        # Select X and Y axes
        x_axis = st.selectbox("Select X axis", options=df.columns, key="x_axis")
        y_axis = st.selectbox("Select Y axis", options=df.columns, key="y_axis")

        # Check if selected columns are compatible with chosen charts
        display_bar = st.sidebar.checkbox("Display Bar Chart")
        display_pie = st.sidebar.checkbox("Display Pie Chart")
        display_scatter = st.sidebar.checkbox("Display Scatter Plot")
        display_map = st.sidebar.checkbox("Display Choropleth Map")

        # Filter section based on X and Y axis selection
        apply_filters = st.sidebar.checkbox("Apply Filters")
        if apply_filters and display_map:
            st.warning("Column filters cannot be applied for the Choropleth map.")
            st.warning("Please deselect the choropleth map option otherwise column filters cannot be applied in the visualizations.")
            apply_filters = False

        # Initialize filtered dataset as empty if filters are applied with no selections
        filtered_df = pd.DataFrame()

        if apply_filters:
            filters = {}
            range_filters = {}
            for i, column in enumerate([x_axis, y_axis]):
                if column in numeric_columns:
                    minimum = df[column].min()
                    maximum = df[column].max()
                    
                    if not pd.isnull(minimum) and not pd.isnull(maximum):
                        range_filters[column] = st.slider(
                            f"Range for {column}",
                            min_value=float(minimum),
                            max_value=float(maximum),
                            value=(float(minimum), float(maximum)),
                            key=f"range_{i}"
                        )
                elif column in categorical_columns:
                    unique_values = df[column].dropna().unique().tolist()
                    unique_values.insert(0, "All")
                    selected_value = st.multiselect(f'Select {column}', unique_values, key=f"filter_{i}", default=["All"])

                    # Implement "All" functionality
                    if "All" in selected_value:
                        selected_value = unique_values[1:]  # Select all options if "All" is chosen

                    filters[column] = selected_value

            # Apply filters to the data only if a filter option is selected
            if any(filters.values()) or any(range_filters.values()):
                filtered_df = df.copy()
                for column, selected_value in filters.items():
                    if selected_value:
                        filtered_df = filtered_df[filtered_df[column].isin(selected_value)]
                for column, range_values in range_filters.items():
                    filtered_df = filtered_df[filtered_df[column].between(*range_values)]
        else:
            filtered_df = df

        # Display charts based on selected types and column compatibility
        color_options = ["Blue", "Green", "Red", "Purple", "Orange"]

        # Display Bar Chart
        # Display Bar Chart
        if display_bar and not filtered_df.empty:
    # Allow the bar chart to take a categorical column on either the x or y axis
            if (x_axis in categorical_columns and y_axis in numeric_columns) or (y_axis in categorical_columns and x_axis in numeric_columns):
                bar_chart_title = st.text_input("Enter Bar Chart Title", key="bar_title")
                bar_color = st.selectbox("Select Bar Chart Color", options=color_options, key="bar_color")
        
        # Dynamically set the axis encoding based on which axis is categorical
                if x_axis in categorical_columns and y_axis in numeric_columns:
                    bar_chart = alt.Chart(filtered_df).mark_bar(color=bar_color.lower()).encode(
                    x=alt.X(f"{x_axis}", type="nominal"),
                    y=alt.Y(f"{y_axis}", type="quantitative")
            )
                elif y_axis in categorical_columns and x_axis in numeric_columns:
                    bar_chart = alt.Chart(filtered_df).mark_bar(color=bar_color.lower()).encode(
                    x=alt.X(f"{x_axis}", type="quantitative"),
                    y=alt.Y(f"{y_axis}", type="nominal")
            )
        
                bar_chart = bar_chart.properties(title=bar_chart_title)
                st.markdown(f"### **{bar_chart_title}**", unsafe_allow_html=True)
                st.altair_chart(bar_chart)
            else:
                st.warning("For a bar chart, select one categorical column and one numeric column.")

        # Display Pie Chart
        if display_pie and not filtered_df.empty:
            if (x_axis in categorical_columns and y_axis in numeric_columns) or (y_axis in categorical_columns and x_axis in numeric_columns):
                pie_chart_title = st.text_input("Enter Pie Chart Title", key="pie_title")
                pie_chart = alt.Chart(filtered_df).mark_arc().encode(
                    theta=f"{y_axis}:Q" if y_axis in numeric_columns else f"{x_axis}:Q",
                    color=f"{x_axis}:N" if x_axis in categorical_columns else f"{y_axis}:N"
                ).properties(title=pie_chart_title, width=500, height=500)
                st.markdown(f"### **{pie_chart_title}**", unsafe_allow_html=True)
                st.altair_chart(pie_chart)
            else:
                st.warning("For a pie chart, select one numeric column and one categorical column.")

        # Display Scatter Plot
        if display_scatter and not filtered_df.empty:
            if x_axis in numeric_columns and y_axis in numeric_columns:
                scatter_chart_title = st.text_input("Enter Scatter Plot Title", key="scatter_title")
                scatter_color = st.selectbox("Select Scatter Plot Color", options=color_options, key="scatter_color")
                scatter_plot = alt.Chart(filtered_df).mark_point(color=scatter_color.lower()).encode(
                    x=alt.X(f"{x_axis}"),
                    y=alt.Y(f"{y_axis}")
                ).properties(title=scatter_chart_title, width=700, height=500)
                st.markdown(f"### **{scatter_chart_title}**", unsafe_allow_html=True)
                st.altair_chart(scatter_plot)
            else:
                st.warning("Both selected columns must be numeric for a scatter plot.")

        # Display Choropleth Map
        if display_map and not filtered_df.empty:
            if is_census_data and ((x_axis.lower() in state_columns) != (y_axis.lower() in state_columns)):
                map_chart_title = st.text_input("Enter Choropleth Map Title", key="map_title")
                state_id_map = {feature["properties"]["st_nm"]: feature["id"] for feature in india_states["features"]}
                geo_axis = x_axis if x_axis.lower() in state_columns else y_axis
                filtered_df["id"] = filtered_df[geo_axis].apply(lambda x: state_id_map.get(x))

                if "id" in filtered_df.columns and not filtered_df["id"].isna().all():
                    fig = px.choropleth(
                        filtered_df,
                        geojson=india_states,
                        featureidkey="properties.state_code",
                        locations="id",
                        color=y_axis if y_axis != geo_axis else x_axis,
                        hover_name=geo_axis,
                        hover_data=[y_axis if y_axis != geo_axis else x_axis],
                        color_continuous_scale=px.colors.diverging.BrBG,
                        title=map_chart_title
                    )
                    fig.update_geos(fitbounds="locations", visible=False)
                    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
                    st.markdown(f"### **{map_chart_title}**", unsafe_allow_html=True)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("The map data could not be aligned with the state column data. Check for state name mismatches.")
            else:
                st.warning("To create a choropleth map, make sure the dataset includes a state column and appropriate geographical data and give the state column for either of the axes. ")

        # Display the filtered dataset if filters are applied
        if apply_filters and not filtered_df.empty:
            st.header("Filtered Dataset")
            st.write(filtered_df)


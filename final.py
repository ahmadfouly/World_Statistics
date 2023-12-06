# Import packages
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st




# Function to load data
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    
    
    return df

# Load the data
world_data = load_data("CountriesData.csv")


# Streamlit app layout

st.markdown("""
# World Data Explorer

Welcome to the World Data Explorer, a Streamlit application designed to provide interactive visualizations of global data. This app allows users to explore various metrics and trends across different countries.

1. **Select Countries:** Choose one or more countries from the multi-select option in the sidebar.
2. **Choose Metrics:** Select the metrics you are interested in exploring.
3. **Set Time Range:** Use the slider to define the time range for your data.
4. **Pick a Chart Type:** Choose how you want to visualize the data—via line graphs, scatterplots, or boxplots.

Dive into the World Data Explorer and unlock insights from global data trends!
""", unsafe_allow_html=True)


# Sidebar for user inputs
with st.sidebar:
    # Multi-select for selecting countries
    selected_countries = st.multiselect("Select Countries", world_data['Entity'].unique())

    # Multi-select for selecting metrics
    metrics = [col for col in world_data.columns if world_data[col].dtype != 'object' and col != 'Year']
    selected_metrics = st.multiselect("Select Metrics", metrics)

    # Time range slider
    years = sorted(world_data['Year'].unique())
    min_year, max_year = min(years), max(years)
    selected_years = st.slider("Select Time Range", min_year, max_year, (min_year, max_year), 1)
    
    # Select box for choosing chart type
    chart_type = st.selectbox("Select Chart Type", ["Line Graph", "Scatterplot", "Boxplot"])

    if chart_type == "Scatterplot":
        second_metric = st.selectbox("Select Second Metric for Scatterplot", metrics)


# Main panel
# Filter data based on selected countries and time range
filtered_data = world_data[(world_data['Entity'].isin(selected_countries)) & (world_data['Year'].between(*selected_years))]


# Function to create chart for each metric
def create_chart(metric, chart_type, second_metric=None):
    if chart_type == "Line Graph":
        chart = alt.Chart(filtered_data).mark_line(point=True).encode(
            x='Year:N',
            y=alt.Y(f'{metric}:Q', axis=alt.Axis(title=metric)),
            color='Entity:N',
            tooltip=['Entity', 'Year', metric]
        )
    elif chart_type == "Scatterplot":
        chart = alt.Chart(filtered_data).mark_circle().encode(
            x=alt.X(f'{metric}:Q', axis=alt.Axis(title=metric)),
            y=alt.Y(f'{second_metric}:Q', axis=alt.Axis(title=second_metric)),
            color='Entity:N',
            tooltip=['Entity', metric, second_metric]
        )
    elif chart_type == "Boxplot":
        chart = alt.Chart(filtered_data).mark_boxplot().encode(
            x='Entity:N',
            y=alt.Y(f'{metric}:Q', axis=alt.Axis(title=metric)),
            color='Entity:N'
        )
    return chart.interactive()

# Render chart for each selected metric
for metric in selected_metrics:
    # Set a dynamic title for each chart
    st.markdown(f"<h2 style='color: green;'>{metric}</h2>", unsafe_allow_html=True)
    
    st.altair_chart(create_chart(metric, chart_type, second_metric if chart_type == "Scatterplot" else None), use_container_width=True)

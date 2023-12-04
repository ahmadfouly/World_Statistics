# Import packages
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import pydeck as pdk

# Function to load data
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    return df

# Load the data
world_data = load_data("CountriesDataImputed.csv")

# Streamlit app layout
st.markdown("<h1 style='color: blue; font-size: 40px;'>World Data Explorer</h1>", unsafe_allow_html=True)

# Sidebar for user inputs
with st.sidebar:
    # Multi-select for selecting countries
    selected_countries = st.multiselect("Select Countries", world_data['Entity'].unique())

    # Multi-select for selecting metrics
    metrics = [col for col in world_data.columns if world_data[col].dtype != 'object' and col != 'Year']
    selected_metrics = st.multiselect("Select Metrics", metrics)

    # Time range slider

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
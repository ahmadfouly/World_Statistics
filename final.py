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
st.title("Interactive Country Statistics Visualization")

# Sidebar for user inputs
with st.sidebar:
    # Multi-select for selecting countries
    selected_countries = st.multiselect("Select Countries", world_data['Entity'].unique())

    # Multi-select for selecting metrics
    metrics = [col for col in world_data.columns if world_data[col].dtype != 'object' and col != 'Year']
    selected_metrics = st.multiselect("Select Metrics", metrics)

    # Time range slider
    years = world_data['Year'].unique()
    min_year, max_year = min(years), max(years)
    selected_years = st.slider("Select Time Range", min_year, max_year, (min_year, max_year), 1)

# Main panel
# Filter data based on selected countries and time range
filtered_data = world_data[(world_data['Entity'].isin(selected_countries)) & (world_data['Year'].between(*selected_years))]

# Function to create chart for each metric
def create_chart(metric):
    chart = alt.Chart(filtered_data).mark_line(point=True).encode(
        x='Year:N',
        y=alt.Y(f'{metric}:Q', axis=alt.Axis(title=metric)),
        color='Entity:N',
        tooltip=['Entity', 'Year', metric]
    ).interactive()
    return chart


# Render chart for each selected metric
for metric in selected_metrics:
    # Set a dynamic title for each chart
    st.title(f"{metric}")
    
    st.altair_chart(create_chart(metric), use_container_width=True)

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

Explore various metrics and trends across different countries.

To begin, open the sidebar by clicking on the '>' icon at the top-left corner.

1. **Select Countries:** Choose one or more countries from the multi-select option in the sidebar.
2. **Choose Metrics:** Select the metrics you are interested in exploring.
3. **Set Time Range:** Use the slider to define the time range for your data.
4. **Pick a Chart Type:** Choose how you want to visualize the data.

Dive into the World Data Explorer and unlock insights from global data trends!
""", unsafe_allow_html=True)

def reset_selections():
    # Resetting each widget's value in the session state
    st.session_state['selected_countries'] = []
    st.session_state['selected_metrics'] = []
    st.session_state['selected_years'] = [min_year, max_year]
    st.session_state['chart_type'] = "Line Graph"
if 'selected_countries' not in st.session_state:
    st.session_state['selected_countries'] = []
if 'selected_metrics' not in st.session_state:
    st.session_state['selected_metrics'] = []

selected_countries = st.multiselect("Select Countries", world_data['Entity'].unique(), default=st.session_state['selected_countries'])
selected_metrics = st.multiselect("Select Metrics", [all_metrics_option] + metrics, default=st.session_state['selected_metrics'])

if st.sidebar.button('Reset'):
    reset_selections()


# Sidebar for user inputs
with st.sidebar:
    # Multi-select for selecting countries
    selected_countries = st.multiselect("Select Countries", world_data['Entity'].unique())

    # Multi-select for selecting metrics
    metrics = [col for col in world_data.columns if world_data[col].dtype != 'object' and col != 'Year']
    all_metrics_option = "All Metrics"
    selected_metrics = st.multiselect("Select Metrics", [all_metrics_option] + metrics)
    
    # Check if 'All Metrics' is selected
    if all_metrics_option in selected_metrics:
        # If other metrics are also selected, remove them
        if len(selected_metrics) > 1:
            selected_metrics = [all_metrics_option]
        # Set selected metrics to all metrics
        selected_metrics = metrics

    # Time range slider
    years = sorted(world_data['Year'].unique())
    min_year, max_year = min(years), max(years)
    selected_years = st.slider("Select Time Range", min_year, max_year, (min_year, max_year), 1)
    
    # Select box for choosing chart type
    chart_type = st.selectbox("Select Chart Type", ["Line Graph", "Scatterplot", "Boxplot", "Histogram", "Heatmap", "Pie Chart"])

    # Additional options based on chart type
    second_metric = None
    if chart_type == "Scatterplot":
        second_metric = st.selectbox("Select Second Metric for Scatterplot", metrics)


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
    elif chart_type == "Histogram":
        chart = alt.Chart(filtered_data).mark_bar().encode(
            x=alt.X(f'{metric}:Q', bin=True),
            y='count()',
            color='Entity:N'
        )
    elif chart_type == "Heatmap":
        chart = alt.Chart(filtered_data).mark_rect().encode(
            x='Year:O',
            y='Entity:N',
            color=alt.Color(f'{metric}:Q')
        )
    elif chart_type == "Pie Chart":
        chart = alt.Chart(filtered_data).mark_arc().encode(
            theta=alt.Theta(f'{metric}:Q'),
            color='Entity:N'
        )
    return chart.interactive()

# Render chart for each selected metric
for metric in selected_metrics:
    # Set a dynamic title for each chart
    st.markdown(f"<h2 style='color: green;'>{metric}</h2>", unsafe_allow_html=True)
    
    st.altair_chart(create_chart(metric, chart_type, second_metric if chart_type in ["Scatterplot", "Heatmap"] else None), use_container_width=True)
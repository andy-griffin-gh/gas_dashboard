import streamlit as st
import pandas as pd
import requests
import io
import altair as alt

# Caching the data loading function
@st.cache_data
def load_data_from_google_drive(file_id):
    """Function to download and cache CSV file from Google Drive."""
    download_url = f'https://drive.google.com/uc?id={file_id}&export=download'
    response = requests.get(download_url)
    response.raise_for_status()  # Ensure the request was successful
    
    if '<html' in response.text.lower():
        raise ValueError("The downloaded content is not a CSV file. Please check the file link and permissions.")
    
    # Load CSV data
    return pd.read_csv(io.StringIO(response.text))

# Load the dataset from Google Drive with caching
file_id = '1xofhXxREtpx2dX41eBqtUWGlRDKIPL8U'
data = load_data_from_google_drive(file_id)

# Convert date columns to datetime format
data['FirstProdDate'] = pd.to_datetime(data['FirstProdDate'], errors='coerce')
data['CompletionDate'] = pd.to_datetime(data['CompletionDate'], errors='coerce')

# Sidebar filter for selecting an ENVRegion with an "All Regions" option
st.sidebar.header("Filter by Region")
regions = ["All Regions"] + sorted(data['ENVRegion'].unique())
selected_region = st.sidebar.selectbox("Select Region:", options=regions)

# Apply filter based on the selected region
if selected_region != "All Regions":
    filtered_data = data[data['ENVRegion'] == selected_region]
else:
    filtered_data = data

st.title("Oil & Gas Production Analysis Dashboard")

# Histogram of the target variable
st.subheader("Histogram of 36-Month Gas Production")
st.histogram = alt.Chart(filtered_data).mark_bar().encode(
    alt.X('First36MonthGas_MCF', bin=alt.Bin(maxbins=30), title='36-Month Gas Production (MCF)'),
    y='count()'
).properties(width=700, height=400)
st.altair_chart(st.histogram, use_container_width=True)

# Scatter Plots
numerical_vars = ['TVD_FT', 'PerfInterval_FT', 'ProppantIntensity_LBSPerFT', 'FluidIntensity_BBLPerFT', 'First6MonthGas_MCF']
st.subheader("Scatter Plots Against 36-Month Gas Production")

for var in numerical_vars:
    scatter_chart = alt.Chart(filtered_data).mark_circle(size=60).encode(
        x=alt.X(var, title=var),
        y=alt.Y('First36MonthGas_MCF', title='36-Month Gas Production (MCF)'),
        tooltip=[var, 'First36MonthGas_MCF']
    ).interactive()
    st.altair_chart(scatter_chart, use_container_width=True)

st.write("Dashboard by ADTA 5410 Project Team")
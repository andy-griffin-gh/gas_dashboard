import streamlit as st
import pandas as pd
import requests
import io
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

def load_data_from_google_drive(file_id):
    """Function to download CSV file from Google Drive."""
    download_url = f'https://drive.google.com/uc?id={file_id}&export=download'
    response = requests.get(download_url)
    response.raise_for_status()  # Ensure the request was successful

    # Print the first 500 characters of the response to confirm the content
    print("Downloaded content preview:")
    print(response.text[:500])

    # Check if the response contains HTML
    if '<html' in response.text.lower():
        raise ValueError("The downloaded content is not a CSV file. Please check the file link and permissions.")

    # Load CSV data
    return pd.read_csv(io.StringIO(response.text))

# Load the dataset from Google Drive
file_id = '1xofhXxREtpx2dX41eBqtUWGlRDKIPL8U'
data = load_data_from_google_drive(file_id)

# Convert date columns to datetime format
data['FirstProdDate'] = pd.to_datetime(data['FirstProdDate'], errors='coerce')
data['CompletionDate'] = pd.to_datetime(data['CompletionDate'], errors='coerce')

# Sidebar filter for selecting an ENVRegion
st.sidebar.header("Filters")
selected_region = st.sidebar.selectbox(
    "Select Region:",
    options=["All"] + sorted(data['ENVRegion'].unique())
)

# Filter data based on the selected region
if selected_region != "All":
    filtered_data = data[data['ENVRegion'] == selected_region]
else:
    filtered_data = data

st.title("Oil & Gas Production Analysis Dashboard")

# Visualization 1: Proppant Intensity vs. 36-Month Gas Production
st.subheader("Proppant Intensity vs. 36-Month Gas Production")
scatter_data = filtered_data[['ProppantIntensity_LBSPerFT', 'First36MonthGas_MCF']].dropna()
scatter_chart = alt.Chart(scatter_data).mark_circle(size=60).encode(
    x=alt.X('ProppantIntensity_LBSPerFT', title='Proppant Intensity (LBS/FT)'),
    y=alt.Y('First36MonthGas_MCF', title='36-Month Gas Production (MCF)'),
    tooltip=['ProppantIntensity_LBSPerFT', 'First36MonthGas_MCF']
).interactive()
st.altair_chart(scatter_chart, use_container_width=True)

# Visualization 2: Box Plot of ENVInterval vs. 36-Month Gas Production
st.subheader("36-Month Gas Production by Interval")
box_data = filtered_data[['ENVInterval', 'First36MonthGas_MCF']].dropna()
box_chart = alt.Chart(box_data).mark_boxplot().encode(
    x='ENVInterval',
    y='First36MonthGas_MCF',
    tooltip=['ENVInterval', 'First36MonthGas_MCF']
).properties(width=700, height=400)
st.altair_chart(box_chart, use_container_width=True)

# Visualization 3: Correlation Heatmap
st.subheader("Correlation Heatmap of Features")
corr_columns = [
    'First36MonthGas_MCF', 'PerfInterval_FT', 'ProppantIntensity_LBSPerFT', 
    'FluidIntensity_BBLPerFT', 'First6MonthGas_MCF', 'First12MonthGas_MCF'
]
corr_data = filtered_data[corr_columns].dropna()

# Generate the heatmap
plt.figure(figsize=(10, 8))
correlation_matrix = corr_data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
st.pyplot(plt.gcf())

st.write("Dashboard by ADTA 5410 Project Team")

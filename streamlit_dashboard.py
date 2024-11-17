import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Load the dataset
file_path = r'C:\Users\acgri\Box\ADTA 5410\ProjectData\data_outliers_cleaned.csv'
data = pd.read_csv(file_path)

# Step 2: Convert date columns to datetime format
data['FirstProdDate'] = pd.to_datetime(data['FirstProdDate'], errors='coerce')
data['CompletionDate'] = pd.to_datetime(data['CompletionDate'], errors='coerce')

# Step 3: Sidebar filter for selecting an ENVRegion
st.sidebar.header("Filters")
selected_region = st.sidebar.selectbox(
    "Select Region:",
    options=["All"] + sorted(data['ENVRegion'].unique())
)

# Step 4: Filter data based on the selected region
if selected_region != "All":
    filtered_data = data[data['ENVRegion'] == selected_region]
else:
    filtered_data = data

st.title("Oil & Gas Production Analysis Dashboard")

# Step 5: Scatter Plot: Proppant Intensity vs. 36-Month Gas Production
st.subheader("Proppant Intensity vs. 36-Month Gas Production")
scatter_data = filtered_data[['ProppantIntensity_LBSPerFT', 'First36MonthGas_MCF']].dropna()

scatter_chart = alt.Chart(scatter_data).mark_circle(size=60).encode(
    x=alt.X('ProppantIntensity_LBSPerFT', title='Proppant Intensity (LBS/FT)'),
    y=alt.Y('First36MonthGas_MCF', title='36-Month Gas Production (MCF)'),
    tooltip=['ProppantIntensity_LBSPerFT', 'First36MonthGas_MCF']
).interactive()

st.altair_chart(scatter_chart, use_container_width=True)

# Step 6: Box Plot: ENVInterval vs. 36-Month Gas Production
st.subheader("36-Month Gas Production by Interval")
box_data = filtered_data[['ENVInterval', 'First36MonthGas_MCF']].dropna()

box_chart = alt.Chart(box_data).mark_boxplot().encode(
    x='ENVInterval',
    y='First36MonthGas_MCF',
    tooltip=['ENVInterval', 'First36MonthGas_MCF']
).properties(width=700, height=400)

st.altair_chart(box_chart, use_container_width=True)

# Step 7: Correlation Heatmap
st.subheader("Correlation Heatmap of Features")
corr_columns = [
    'First36MonthGas_MCF', 'PerfInterval_FT', 'ProppantIntensity_LBSPerFT', 
    'FluidIntensity_BBLPerFT', 'First6MonthGas_MCF', 'First12MonthGas_MCF'
]
corr_data = filtered_data[corr_columns].dropna()

plt.figure(figsize=(10, 8))
correlation_matrix = corr_data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
st.pyplot(plt.gcf())

st.write("Dashboard by ADTA 5410 Project Team")

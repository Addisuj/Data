import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff

# Page Configuration
st.set_page_config(page_title="EDA Dashboard", layout="wide")

# Title
st.title("Exploratory Data Analysis Dashboard for benin")

# Sidebar File Uploader
with st.sidebar:
    upload_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
    if upload_file is None:
        st.warning("Please upload a file to proceed.")
        st.stop()

# Load Data
@st.cache_data
def load_data(upload_file):
    if upload_file.name.endswith('.csv'):
        data = pd.read_csv(upload_file)
    else:
        data = pd.read_excel(upload_file)
    return data

df = load_data(upload_file)

# Display Data
st.write("## Data Preview")
st.dataframe(df.head(), use_container_width=True)

# Summary Statistics
st.write("## Summary Statistics")
st.dataframe(df.describe(), use_container_width=True)

# Data Quality Check: Missing Values
st.write("## Missing Values")
missing_values = df.isnull().sum()
st.bar_chart(missing_values)

# Time Series Analysis
st.write("## Time Series Analysis")
df['Timestamp'] = pd.to_datetime(df['Timestamp'])  # Convert to datetime

with st.expander("Time Series of Solar Radiation and Temperature"):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='Timestamp', y='GHI', label='GHI', ax=ax)
    sns.lineplot(data=df, x='Timestamp', y='DNI', label='DNI', ax=ax)
    sns.lineplot(data=df, x='Timestamp', y='DHI', label='DHI', ax=ax)
    sns.lineplot(data=df, x='Timestamp', y='Tamb', label='Ambient Temperature', ax=ax)
    ax.set_title("Solar Radiation and Ambient Temperature over Time")
    st.pyplot(fig)

# Correlation Analysis
st.write("## Correlation Matrix")
correlation_matrix = df.corr()
st.write(
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1),
    use_container_width=True
)

# Wind Analysis
st.write("## Wind Analysis")
with st.expander("Wind Speed and Gust Analysis"):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='Timestamp', y='WS', label='Wind Speed', ax=ax)
    sns.lineplot(data=df, x='Timestamp', y='WSgust', label='Wind Gust Speed', ax=ax)
    ax.set_title("Wind Speed and Gust Speed over Time")
    st.pyplot(fig)

# Temperature Analysis
with st.expander("Module Temperature Analysis"):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='Timestamp', y='Tamb', label='Ambient Temperature', ax=ax)
    sns.lineplot(data=df, x='TModA', y='Timestamp', label='Module A Temperature', ax=ax)
    sns.lineplot(data=df, x='TModB', y='Timestamp', label='Module B Temperature', ax=ax)
    ax.set_title("Module and Ambient Temperature over Time")
    st.pyplot(fig)

# Histograms
st.write("## Histograms")
variables_to_plot = ['GHI', 'DNI', 'DHI', 'WS', 'Tamb', 'TModA', 'TModB']

for var in variables_to_plot:
    with st.expander(f"{var} Histogram"):
        fig, ax = plt.subplots()
        sns.histplot(data=df, x=var, kde=True, ax=ax)
        ax.set_title(f'{var} Histogram')
        st.pyplot(fig)

# Box Plots
st.write("## Box Plots")
for var in variables_to_plot:
    with st.expander(f"{var} Box Plot"):
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x=var, ax=ax)
        ax.set_title(f'{var} Box Plot')
        st.pyplot(fig)

# Scatter Plots
st.write("## Scatter Plots")
with st.expander("Scatter Plots for Interesting Variables"):
    fig = px.scatter(df, x='GHI', y='Tamb', color='Timestamp', title='GHI vs Tamb')
    st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(df, x='WS', y='WSgust', color='Timestamp', title='Wind Speed vs Gust Speed')
    st.plotly_chart(fig, use_container_width=True)

# Data Cleaning
st.write("## Data Cleaning")
# Handle missing numeric values with mean
df.fillna(df.mean(), inplace=True)

# Remove rows with negative values in specific columns
columns_to_check = ['GHI', 'DNI', 'DHI']
df = df[df[columns_to_check] >= 0]

# Drop 'Comments' if entirely null
if df['Comments'].isnull().all():
    df.drop(columns=['Comments'], inplace=True)

st.success("Data Cleaning Complete")



# Pie chart
@st.cache_data
def pie_plot():
    fig = px.pie(df, names="Account")
    st.plotly_chart(fig, use_container_width=True)

with col3:
    pie_plot()


# Bar chart
@st.cache_data
def bar_plot():
    fig = px.bar(sales_data, x="month", y="sales", color="Scenario", title="Monthly Budget vs Forecast 2023")
    st.plotly_chart(fig, use_container_width=True)  


with col1:
    bar_plot()
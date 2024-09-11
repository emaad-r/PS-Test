import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Custom color palette
color_p = ["#1984c5", "#63bff0", "#a7d5ed", "#de6e56", "#e14b31", "#c23728"]

# Streamlit app configuration
st.set_page_config(layout="wide")
st.title("Experiment Results Analysis")

# Step 1: Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_uploader_1")

# Ensure that the file uploader component is visible before processing the file
if uploaded_file is not None:
    try:
        # Step 1: Debug - Show the raw content of the file to verify reading
        st.write("Raw file content:")
        raw_content = uploaded_file.getvalue().decode("utf-8")
        st.text(raw_content)  # Display raw content for further inspection

        # Step 2: Read the CSV file and display columns
        data = pd.read_csv(uploaded_file, sep=',', encoding='utf-8')  # Adjust separator and encoding if necessary
        st.success("File successfully loaded!")

        # Display the column names
        st.write("Column Names in the Data:")
        st.write(data.columns.tolist())

        # Display the first few rows of the data for inspection
        st.write("Here are the first few rows of your data:")
        st.dataframe(data.head())  # First few rows for quick check

        # Step 3: Data Cleaning - Check for missing or null values
        st.write("Check for missing values in the data:")
        missing_data = data.isna().sum()
        st.write(missing_data)  # Show how many missing values are present in each column

        # Step 4: Filter columns that are relevant and ensure correct data types
        filtered_data = data[['dimension', 'angle', 'wm', 'key_resp.corr', 'vivid_response', 'strategy_response', 'key_resp.rt']]

        # Ensure correct data types for the relevant columns
        filtered_data['dimension'] = filtered_data['dimension'].astype(str)  # Ensure dimension is treated as string
        filtered_data['wm'] = filtered_data['wm'].astype(bool)  # Ensure wm is treated as boolean
        filtered_data['strategy_response'] = pd.to_numeric(filtered_data['strategy_response'], errors='coerce')  # Convert strategy_response to numeric
        
        # Step 5: Handle missing or invalid data (replace or drop as needed)
        filtered_data = filtered_data.dropna(subset=['vivid_response', 'strategy_response'])  # Drop rows where vivid_response or strategy_response is missing

        st.write("Filtered data with relevant columns:")
        st.dataframe(filtered_data.head())

        # Debugging: Show unique values in strategy_response and wm to ensure correctness
        st.write("Unique values in 'strategy_response':", filtered_data['strategy_response'].unique())
        st.write("Unique values in 'wm':", filtered_data['wm'].unique())

        # Step 6: Visualizations

        # 6.1: Correctness based on conditions
        st.write("Correctness by Dimension, Angle, and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.barplot(x="angle", y="key_resp.corr", hue="dimension", data=filtered_data, palette=color_p)
        plt.title("Correctness by Angle and Dimension")
        st.pyplot(plt)

        # 6.2: Response time as a function of conditions
        st.write("Response Time by Dimension, Angle, and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.barplot(x="angle", y="key_resp.rt", hue="dimension", data=filtered_data, palette=color_p)
        plt.title("Response Time by Angle and Dimension")
        st.pyplot(plt)

        # 6.3: Vividness and strategy response by condition
        st.write("Vividness Response by Dimension and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x="dimension", y="vivid_response", hue="wm", data=filtered_data, palette=color_p)
        plt.title("Vividness Response by Dimension and WM Condition")
        st.pyplot(plt)

        # 6.4: Strategy response by condition
        st.write("Strategy Response by Dimension and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.barplot(x="dimension", y="strategy_response", hue="wm", data=filtered_data, palette=color_p)
        plt.title("Strategy Response by Dimension and WM Condition")
        st.pyplot(plt)

    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.write("Please upload a CSV file to get started.")

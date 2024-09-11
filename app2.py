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
        # Debugging: Show raw content of the file
        st.write("Raw file content:")
        st.write(uploaded_file.getvalue())

        # Read the CSV file with explicit delimiter and encoding
        data = pd.read_csv(uploaded_file, sep=',', encoding='utf-8')  # Adjust encoding or delimiter as needed

        st.success("File successfully loaded!")

        # Show the column names to help debug missing columns
        st.write("Column Names in the Data:")
        st.write(list(data.columns))

        # Display the first few rows of the data
        st.write("Here are the first few rows of your data:")
        st.dataframe(data.head())

        # Filter columns that are relevant
        filtered_data = data[['dimension', 'angle', 'wm', 'key_resp.corr', 'vivid_response', 'strategy_response', 'key_resp.rt']]

        # Ensure correct data types
        filtered_data['dimension'] = filtered_data['dimension'].astype(str)
        filtered_data['wm'] = filtered_data['wm'].astype(bool)
        filtered_data['strategy_response'] = filtered_data['strategy_response'].astype(str)

        # Handle missing vivid_response and strategy_response data
        filtered_data = filtered_data.dropna(subset=['vivid_response', 'strategy_response'])

        st.write("Filtered data with relevant columns:")
        st.dataframe(filtered_data.head())

        # Debugging: Check for 2D and wm=False data
        st.write("Check for 2D and WM=False Data:")
        st.write(filtered_data[(filtered_data['dimension'] == '2D') & (filtered_data['wm'] == False)])

        # Debugging: Print unique values in 'dimension' and 'wm' to ensure they're being processed correctly
        st.write("Unique values in 'dimension':", filtered_data['dimension'].unique())
        st.write("Unique values in 'wm':", filtered_data['wm'].unique())

        # Debugging: Print unique values in 'strategy_response' to ensure it's being processed correctly
        st.write("Unique values in 'strategy_response':", filtered_data['strategy_response'].unique())

        # Step 4: Visualizations

        # 4.1: Correctness based on conditions
        st.write("Correctness by Dimension, Angle, and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.barplot(x="angle", y="key_resp.corr", hue="dimension", data=filtered_data, palette=color_p)
        plt.title("Correctness by Angle and Dimension")
        st.pyplot(plt)

        # 4.2: Response time as a function of conditions
        st.write("Response Time by Dimension, Angle, and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.barplot(x="angle", y="key_resp.rt", hue="dimension", data=filtered_data, palette=color_p)
        plt.title("Response Time by Angle and Dimension")
        st.pyplot(plt)

        # 4.3: Vividness and strategy response by condition

        # Fixing the boxplot to ensure correct handling of data
        st.write("Vividness Response by Dimension and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x="dimension", y="vivid_response", hue="wm", data=filtered_data, palette=color_p)
        plt.title("Vividness Response by Dimension and WM Condition")
        st.pyplot(plt)

        # 4.4: Strategy response by condition
        st.write("Strategy Response by Dimension and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.barplot(x="dimension", y="strategy_response", hue="wm", data=filtered_data, palette=color_p)
        plt.title("Strategy Response by Dimension and WM Condition")
        st.pyplot(plt)

    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.write("Please upload a CSV file to get started.")

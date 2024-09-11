import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the App
st.title("Experiment Results Analysis")

# Step 1: Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_uploader_1")

if uploaded_file is not None:
    try:
        # Step 2: Read the CSV file
        data = pd.read_csv(uploaded_file)
        st.success("File successfully loaded!")
        
        # Display the dataframe
        st.write("Here are the first few rows of your data:")
        st.dataframe(data.head())

        # Filter columns that are relevant
        filtered_data = data[['dimension', 'angle', 'wm', 'key_resp.corr', 'vivid_response', 'strategy_response', 'key_resp.rt']]
        
        st.write("Filtered data with relevant columns:")
        st.dataframe(filtered_data.head())

        # Step 3: Summary Statistics
        st.write("Summary statistics of the filtered data:")
        st.write(filtered_data.describe())

        # Step 4: Visualizations

        # 4.1: Correctness based on conditions (including WM)
        st.write("Correctness by Dimension, Angle, and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.barplot(x="angle", y="key_resp.corr", hue="wm", data=filtered_data, ci=None)
        plt.title("Correctness by Angle, WM Condition, and Dimension")
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # 4.2: Response time as a function of conditions (including WM)
        st.write("Response Time by Dimension, Angle, and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.barplot(x="angle", y="key_resp.rt", hue="wm", data=filtered_data, ci=None)
        plt.title("Response Time by Angle, WM Condition, and Dimension")
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # 4.3: Vividness and strategy response by condition (including WM)
        st.write("Vividness Response by Dimension and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x="dimension", y="vivid_response", hue="wm", data=filtered_data)
        plt.title("Vividness Response by Dimension and WM Condition")
        st.pyplot(plt)
        
        st.write("Strategy Response by Dimension and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x="dimension", y="strategy_response", hue="wm", data=filtered_data)
        plt.title("Strategy Response by Dimension and WM Condition")
        st.pyplot(plt)

    except Exception as e:
        st.error(f"Error loading file: {e}")

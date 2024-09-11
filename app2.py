import streamlit as st
import pandas as pd
import numpy as np
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
        # Read the CSV file
        data = pd.read_csv(uploaded_file)
        st.success("File successfully loaded!")

        # Display the first few rows of the data
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
        st.write("Vividness Response by Dimension and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x="dimension", y="vivid_response", hue="wm", data=filtered_data, palette=color_p)
        plt.title("Vividness Response by Dimension and WM Condition")
        st.pyplot(plt)

        st.write("Strategy Response by Dimension and WM Condition")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x="dimension", y="strategy_response", hue="wm", data=filtered_data, palette=color_p)
        plt.title("Strategy Response by Dimension and WM Condition")
        st.pyplot(plt)

        # Additional visualizations based on your previous setup
        # Angular effect on correctness
        st.write("Angular Effect on Correctness within Conditions")
        angular_effect = filtered_data.groupby(['dimension', 'angle'])['key_resp.corr'].mean().reset_index()
        plt.figure(figsize=(10, 6))
        sns.barplot(x='angle', y='key_resp.corr', hue='dimension', data=angular_effect, palette=color_p)
        plt.title("Correctness by Angle and Dimension")
        st.pyplot(plt)

        # Angular effect on response time
        st.write("Angular Effect on Response Time within Conditions")
        angular_rt = filtered_data.groupby(['dimension', 'angle'])['key_resp.rt'].mean().reset_index()
        plt.figure(figsize=(10, 6))
        sns.barplot(x='angle', y='key_resp.rt', hue='dimension', data=angular_rt, palette=color_p)
        plt.title("Response Time by Angle and Dimension")
        st.pyplot(plt)

    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.write("Please upload a CSV file to get started.")

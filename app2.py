import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Custom color palette
color_p = ["#1984c5", "#63bff0", "#a7d5ed", "#de6e56", "#e14b31", "#c23728"]

# Title of the App
st.title("Experiment Results Analysis with Data Cleaning and Inspection")

# Step 1: Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_uploader_1")

if uploaded_file is not None:
    try:
        # Step 2: Read the CSV file
        data = pd.read_csv(uploaded_file)
        st.success("File successfully loaded!")

        # Display the raw dataframe for the user
        st.write("Here are the first few rows of your raw data:")
        st.dataframe(data.head())

        # Step 3: Data Cleaning
        st.subheader("Cleaning Data")

        # Drop columns that are completely empty
        data = data.dropna(how='all', axis=1)

        # Convert 'vivid_response' and 'strategy_response' columns to numerical, replacing 'None' with NaN
        data['vivid_response'] = pd.to_numeric(data['vivid_response'], errors='coerce')
        data['strategy_response'] = pd.to_numeric(data['strategy_response'], errors='coerce')

        # Ensure 'wm' is boolean
        data['wm'] = data['wm'].astype('boolean')

        # Handle missing values: Drop rows with missing values in the critical columns
        critical_columns = ['dimension', 'angle', 'wm', 'key_resp.corr', 'vivid_response', 'strategy_response', 'key_resp.rt']
        cleaned_data = data.dropna(subset=critical_columns)

        # Check if the cleaned data still has valid entries
        st.write("Data after cleaning (dropped rows with missing values in critical columns):")
        st.dataframe(cleaned_data.head())

        st.write("Summary of the cleaned data:")
        st.write(cleaned_data.describe())

        # Ensure that there are no missing values in the critical columns
        st.write("Missing values after cleaning:")
        st.write(cleaned_data.isnull().sum())

        # Step 4: Visualizations

        # Filter relevant columns
        filtered_data = cleaned_data[['dimension', 'angle', 'wm', 'key_resp.corr', 'vivid_response', 'strategy_response', 'key_resp.rt']]

        st.write("Filtered data with relevant columns:")
        st.dataframe(filtered_data.head())

        # Summary statistics
        st.write("Summary statistics of the filtered data:")
        st.write(filtered_data.describe())

        # 4.1: Correctness based on Dimension, Angle, and WM
        st.write("Correctness by Dimension, Angle, and WM Condition")
        if not filtered_data.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(x="angle", y="key_resp.corr", hue="dimension", data=filtered_data, palette=color_p)
            plt.title("Correctness by Angle and Dimension")
            st.pyplot(plt)
        else:
            st.warning("Filtered data is empty, cannot plot correctness.")

        # 4.2: Response Time as a function of Dimension, Angle, and WM
        st.write("Response Time by Dimension, Angle, and WM Condition")
        if not filtered_data.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(x="angle", y="key_resp.rt", hue="dimension", data=filtered_data, palette=color_p)
            plt.title("Response Time by Angle and Dimension")
            st.pyplot(plt)
        else:
            st.warning("Filtered data is empty, cannot plot response time.")

        # 4.3: Vividness and Strategy Response
        st.write("Vividness Response by Dimension and WM Condition")
        if not filtered_data.empty:
            plt.figure(figsize=(10, 6))
            sns.boxplot(x="dimension", y="vivid_response", hue="wm", data=filtered_data, palette=color_p, boxprops=dict(alpha=0.7))
            plt.title("Vividness Response by Dimension and WM Condition")
            st.pyplot(plt)
        else:
            st.warning("Filtered data is empty, cannot plot vividness response.")

        st.write("Strategy Response by Dimension and WM Condition")
        if not filtered_data.empty:
            plt.figure(figsize=(10, 6))
            sns.boxplot(x="dimension", y="strategy_response", hue="wm", data=filtered_data, palette=color_p, boxprops=dict(alpha=0.7))
            plt.title("Strategy Response by Dimension and WM Condition")
            st.pyplot(plt)
        else:
            st.warning("Filtered data is empty, cannot plot strategy response.")

    except Exception as e:
        st.error(f"Error processing the file: {e}")

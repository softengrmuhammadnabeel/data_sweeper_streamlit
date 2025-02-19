import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up the page layout configuration
st.set_page_config(page_title="Data Sweeper By MD Nabeel", layout="wide")

# Custom Styling implementation for better UI 
st.markdown("""
    <style>
        .stApp { background-color: black; color: white; }
        h1, h2, h3, h4, h5, h6, p, label { color: white !important; }
        .stButton > button { 
            width: 100%; 
            color: white; 
            background-color: black; 
            border-radius: 10px;
            font-weight: bold;
            border:2px solid white;
        }
        .stDownloadButton > button { 
            width: 50%; 
            color: white; 
            background-color: black; 
            border-radius: 10px;
            font-weight: bold;
            border:2px solid white;
        }
        .uploaded-file { font-weight: bold; color: #2E8B57; }
        .download-file { font-weight: bold; color: black; background-color:white }
        .section-header { font-size: 22px; font-weight: bold; color: #1E90FF; }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1 style='text-align: center; color: white;'>📊 Data Sweeper By MD Nabeel</h1>", unsafe_allow_html=True)
st.write("### **Upload and clean your data effortlessly!**")

# File Uploader
st.markdown("<h3 class='section-header'>📂 Upload CSV or Excel Files</h3>", unsafe_allow_html=True)
uploaded_files = st.file_uploader("", type=["csv", "xlsx", "xls"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()

        # Read file based on type
        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension in [".xlsx", ".xls"]:
            df = pd.read_excel(file, engine="openpyxl")
        else:
            st.error(f"❌ Unsupported file type: {file_extension}")
            continue

        # File Details Section
        st.markdown(f"<p class='uploaded-file'>📁 File Name: {file.name} | 📏 Size: {file.size / 1024:.2f} KB</p>", unsafe_allow_html=True)
        
        # Display Preview
        st.markdown("<h3 class='section-header'>👀 Data Preview</h3>", unsafe_allow_html=True)
        st.dataframe(df.head())

        # Data Cleaning Section
        st.markdown("<h3 class='section-header'>🛠️ Data Cleaning</h3>", unsafe_allow_html=True)
        if st.checkbox(f"Enable cleaning for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Remove Duplicates ({file.name})"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")

            with col2:
                if st.button(f"🔄 Fill Missing Values ({file.name})"):
                    num_cols = df.select_dtypes(include=['number']).columns
                    df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
                    st.success("✅ Missing values filled!")

        # Column Selection
        st.markdown("<h3 class='section-header'>📌 Select Columns</h3>", unsafe_allow_html=True)
        columns = st.multiselect(f"Choose columns from {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.markdown("<h3 class='section-header'>📊 Data Visualization</h3>", unsafe_allow_html=True)
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion Section
        st.markdown("<h3 class='section-header'>🔄 Convert & Download</h3>", unsafe_allow_html=True)
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"📥 Convert {file.name}"):
            buffer = BytesIO()
            file_name = file.name.replace(file_extension, f".{conversion_type.lower()}")

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Download {file_name}",
                data=buffer.getvalue(),
                file_name=file_name,
                mime=mime_type
            )

st.success("✅ All files processed successfully!")

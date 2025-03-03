import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up the app with a wide layout
st.set_page_config(page_title="Data Sweeper", layout="wide")


# Show styled title and description
st.markdown('<h1 class="title">Data Sweeper</h1>', unsafe_allow_html=True)
st.markdown('<p class="info-text">Upload CSV or Excel files, clean them, and convert them!</p>', unsafe_allow_html=True)

# File upload box
uploaded_files = st.file_uploader("Drop your files here", type=["csv", "xlsx"], accept_multiple_files=True)

# Process uploaded files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Load file based on extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Sorry, {file_ext} files are not supported!")
            continue

        # Show file info
        st.markdown(f'<p class="info-text">File: <b>{file.name}</b></p>', unsafe_allow_html=True)
        st.markdown(f'<p class="info-text">Size: <b>{round(file.size / 1024, 1)} KB</b></p>', unsafe_allow_html=True)

        st.markdown('<p class="info-text">Here is the first 5 rows:</p>', unsafe_allow_html=True)
        st.dataframe(df.head())

        # Data cleaning section
        st.subheader("Clean Your Data")
        if st.checkbox(f"Clean {file.name}"):
            if st.button("Remove Duplicates"):
                df.drop_duplicates(inplace=True)
                st.markdown('<p class="info-text">Duplicates are gone!</p>', unsafe_allow_html=True)
            if st.button("Fill Missing Numbers"):
                df.fillna(df.mean(numeric_only=True), inplace=True)
                st.markdown('<p class="info-text">Missing numbers filled!</p>', unsafe_allow_html=True)

        # Column selection
        st.subheader("Pick Columns")
        chosen_columns = st.multiselect("Choose columns", df.columns, default=df.columns)
        df = df[chosen_columns]

        # File conversion section
        st.subheader("Convert File")
        convert_to = st.radio("Convert to:", ["CSV", "Excel"], key=file.name)
        
        if st.button("Convert Now"):
            buffer = BytesIO()
            if convert_to == "CSV":
                df.to_csv(buffer, index=False)
                new_name = file.name.replace(file_ext, ".csv")
                file_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                new_name = file.name.replace(file_ext, ".xlsx")
                file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)  # Reset buffer to start for download

            st.download_button(
                label=f"Download as {convert_to}",
                data=buffer,
                file_name=new_name,
                mime=file_type
            )

    st.success("All files are ready!")

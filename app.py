import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Load secrets from the secrets.toml file
spreadsheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]

# Set up Google Sheets API credentials
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = {
    "type": st.secrets["connections"]["gsheets"]["type"],
    "project_id": st.secrets["connections"]["gsheets"]["project_id"],
    "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
    "private_key": st.secrets["connections"]["gsheets"]["private_key"],
    "client_email": st.secrets["connections"]["gsheets"]["client_email"],
    "client_id": st.secrets["connections"]["gsheets"]["client_id"],
    "auth_uri": st.secrets["connections"]["gsheets"]["auth_uri"],
    "token_uri": st.secrets["connections"]["gsheets"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"]
}

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client = gspread.authorize(creds)

# Access the spreadsheet
sheet = client.open_by_url(spreadsheet_url).sheet1

# Load data as a pandas DataFrame
def load_data():
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df

# Function to write a new row to Google Sheets
def add_row_to_google_sheet(new_row):
    sheet.append_row(new_row)

# Streamlit multipage setup
st.set_page_config(page_title="Google Sheets Data App", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["View Data", "Edit Data"])

# Page 1: View Data
if page == "View Data":
    st.title("View Data from Google Sheets")
    data_df = load_data()
    
    # Display data in a table
    st.dataframe(data_df)

# Page 2: Edit Data (everyone can now edit data)
elif page == "Edit Data":
    st.title("Edit Data in Google Sheets")
    
    # Display data in a table
    data_df = load_data()
    st.dataframe(data_df)
    
    st.subheader("Add a new row")
    with st.form("add_row_form"):
        # Assume there are 3 columns in your Google Sheet (update as needed)
        col1 = st.text_input("Column 1")
        col2 = st.text_input("Column 2")
        col3 = st.text_input("Column 3")
        
        submitted = st.form_submit_button("Add Row")
        if submitted:
            if col1 and col2 and col3:  # Ensure all fields are filled
                new_row = [col1, col2, col3]
                add_row_to_google_sheet(new_row)
                st.success("Row added successfully!")
                st.experimental_rerun()  # Refresh to see the new data
            else:
                st.error("Please fill in all fields before submitting.")

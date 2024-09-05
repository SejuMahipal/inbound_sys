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

# Helper to create a visually appealing card layout
def display_card_layout(df):
    for index, row in df.iterrows():
        with st.container():
            st.markdown(f"### 🔑 Keyword: {row['キーワード']}")
            st.markdown(f"**Phone Number**: `{row['電話番号']}`")
            st.markdown(f"**SMS**: `{row['SMS']}`")
            
            # Display synonyms
            st.markdown("**Synonyms:**")
            synonyms = [row['類似語1'], row['類似語2'], row['類似語3'], row['類似語4']]
            synonyms = [syn for syn in synonyms if syn]  # Remove empty values
            st.write(", ".join(synonyms))
            
            # Daytime and Nighttime details
            st.markdown("**Daytime Transfer Method & Response:**")
            st.write(f"Method: `{row['昼の転送方法']}`")
            st.write(f"Response: {row['昼の返答']}")
            st.write(f"Time: {row['昼の開始時間']} - {row['昼の終了時間']}")
            
            with st.expander("Nighttime Settings"):
                st.markdown("**Nighttime Transfer Method & Response:**")
                st.write(f"Method: `{row['夜の転送方法']}`")
                st.write(f"Response: {row['夜の返答']}")
                st.write(f"Time: {row['夜の開始時間']} - {row['夜の終了時間']}")
            
            st.markdown("---")  # Add a separator between each card

# Page 1: View Data
st.title("📊 View Data from Google Sheets")

data_df = load_data()

if not data_df.empty:
    display_card_layout(data_df)
else:
    st.write("No data available to display.")

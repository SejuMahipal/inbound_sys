import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

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

# Helper to configure Ag-Grid options
def configure_grid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)  # Enable pagination
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=False)
    gb.configure_column("電話番号", type=["numericColumn"], headerCheckboxSelection=True)
    gb.configure_side_bar()  # Enable a sidebar for filter & column management
    grid_options = gb.build()
    
    return grid_options

# Page 1: View Data
st.title("📊 Interactive Data from Google Sheets")

data_df = load_data()

if not data_df.empty:
    # Generate Ag-Grid table with interactive features
    grid_options = configure_grid(data_df)
    
    st.subheader("Interactive Table View")
    
    response = AgGrid(
        data_df,
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        theme="material",  # Theme options: 'streamlit', 'light', 'dark', 'blue', 'material'
        update_mode='SELECTION_CHANGED',
        height=400,
        fit_columns_on_grid_load=True
    )
    
    st.write("You selected:")
    st.write(response['selected_rows'])  # Display selected rows
else:
    st.write("No data available to display.")

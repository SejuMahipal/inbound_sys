import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Expected column order
EXPECTED_COLUMNS = [
    'キーワード', '類似語1', '類似語2', '類似語3', '類似語4', 
    '電話番号', 'SMS', 'E-MAIL', '昼の転送方法', '昼の返答', 
    '昼の開始時間', '昼の終了時間', '夜の転送方法', 
    '夜の返答', '夜の開始時間', '夜の終了時間'
]

# Google Sheets API setup
spreadsheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]

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

# Function to load data from Google Sheets
def load_data():
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df

# Function to display the Keyword List
def display_keyword_list(data_df):
    keyword_df = data_df[['キーワード', '類似語1', '類似語2', '類似語3', '類似語4']]
    st.subheader("📋 キーワードリスト")
    st.table(keyword_df)

# Function to display the Action List
def display_action_list(data_df):
    action_df = data_df[['キーワード', '電話番号', 'SMS', 'E-MAIL', '昼の転送方法', '昼の返答', 
                         '昼の開始時間', '昼の終了時間', '夜の転送方法', '夜の返答', 
                         '夜の開始時間', '夜の終了時間']]
    st.subheader("📋 アクションリスト")
    st.table(action_df)

# Streamlit multipage setup
st.set_page_config(page_title="Google Sheets Data App", layout="wide")

# Top navigation buttons for switching between pages, aligned to the right
st.title("Google Sheets Data App")

# Create three columns for alignment, where the last two will contain the buttons
col1, col2, col3 = st.columns([6, 1, 1])

# Default to "View Data" if session state isn't set
if "page" not in st.session_state:
    st.session_state.page = "View Data"

with col2:
    if st.button("View Data"):
        st.session_state.page = "View Data"

with col3:
    if st.button("Upload Data"):
        st.session_state.page = "Upload Data"

# Handle page switching
page = st.session_state.page

# Page 1: View Data
if page == "View Data":
    st.title("📊 View Data from Google Sheets")
    
    # Load the data each time the View Data page is accessed
    data_df = load_data()

    if not data_df.empty:
        # Button layout for Keyword List and Action List
        st.markdown("""
        <style>
        .big-button {
            display: inline-block;
            width: 45%;
            padding: 20px;
            margin: 10px;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            color: white;
            background-color: #4CAF50;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("Keyword List"):
                st.session_state.view = "Keyword List"
        with col2:
            if st.button("Action List"):
                st.session_state.view = "Action List"

        # Initialize session state for view if not already set
        if "view" not in st.session_state:
            st.session_state.view = "Keyword List"

        # Display the chosen list
        if st.session_state.view == "Keyword List":
            display_keyword_list(data_df)
        elif st.session_state.view == "Action List":
            display_action_list(data_df)
    else:
        st.write("No data available to display.")

# Page 2: Upload Data
elif page == "Upload Data":
    st.title("📤 Upload Excel to Update Google Sheets")

    # File uploader
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

    if uploaded_file:
        try:
            # Read the uploaded Excel file using openpyxl engine
            df = pd.read_excel(uploaded_file, engine="openpyxl")

            # Display the uploaded file's content
            st.write("### Uploaded Data Preview:")
            st.table(df)

            # Check if the column names match the expected columns
            if list(df.columns) == EXPECTED_COLUMNS:
                st.success("The columns match the expected order.")

                # Overwrite the Google Sheet with the new data
                if st.button("Update Google Sheets"):
                    overwrite_google_sheet(df)
                    st.success("Google Sheets has been successfully updated!")
            else:
                st.error(f"The columns in the uploaded file do not match the expected columns. Please ensure the following order: {', '.join(EXPECTED_COLUMNS)}")
        except Exception as e:
            st.error(f"Error processing the file: {e}")





# #################################################################

# import streamlit as st
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import pandas as pd

# # Load secrets from the secrets.toml file
# spreadsheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]

# # Set up Google Sheets API credentials
# SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds_dict = {
#     "type": st.secrets["connections"]["gsheets"]["type"],
#     "project_id": st.secrets["connections"]["gsheets"]["project_id"],
#     "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
#     "private_key": st.secrets["connections"]["gsheets"]["private_key"],
#     "client_email": st.secrets["connections"]["gsheets"]["client_email"],
#     "client_id": st.secrets["connections"]["gsheets"]["client_id"],
#     "auth_uri": st.secrets["connections"]["gsheets"]["auth_uri"],
#     "token_uri": st.secrets["connections"]["gsheets"]["token_uri"],
#     "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
#     "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"]
# }

# creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
# client = gspread.authorize(creds)

# # Access the spreadsheet
# sheet = client.open_by_url(spreadsheet_url).sheet1

# # Load data as a pandas DataFrame
# def load_data():
#     data = sheet.get_all_records()
#     df = pd.DataFrame(data)
#     return df

# # Function to write a new row to Google Sheets
# def add_row_to_google_sheet(new_row):
#     sheet.append_row(new_row)

# # Streamlit multipage setup
# st.set_page_config(page_title="Google Sheets Data App", layout="wide")

# # Sidebar for navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["View Data", "Edit Data"])

# # Helper to create a user-friendly display for time columns
# def format_time_period(df):
#     df['昼の時間'] = df['昼の開始時間'] + " - " + df['昼の終了時間']
#     df['夜の時間'] = df['夜の開始時間'] + " - " + df['夜の終了時間']
#     return df[['キーワード', '類似語1', '類似語2', '類似語3', '類似語4', '電話番号', 'SMS', '昼の転送方法', '昼の返答', '昼の時間', '夜の転送方法', '夜の返答', '夜の時間']]

# # Page 1: View Data
# if page == "View Data":
#     st.title("📊 View Data from Google Sheets")
    
#     data_df = load_data()

#     if not data_df.empty:
#         st.subheader("Keyword Information")
#         # Show only specific columns to make it easier to view
#         formatted_df = format_time_period(data_df)

#         st.write("### 🗂️ Keywords and Contact Info")
#         st.dataframe(formatted_df, width=1200)

#         with st.expander("🔍 View Detailed Information"):
#             st.write(data_df)  # Display full data in expandable section
#     else:
#         st.write("No data available to display.")

# # Page 2: Edit Data (everyone can now edit data)
# elif page == "Edit Data":
#     st.title("📝 Edit Data in Google Sheets")
    
#     # Display data in a table
#     data_df = load_data()
#     if not data_df.empty:
#         st.subheader("Current Data")
#         st.dataframe(format_time_period(data_df), width=1200)

#     st.subheader("Add a New Entry")
#     with st.form("add_row_form"):
#         # Adjust input fields to match your sheet columns
#         col1 = st.text_input("キーワード (Keyword)")
#         col2 = st.text_input("類似語1 (Synonym 1)")
#         col3 = st.text_input("類似語2 (Synonym 2)")
#         col4 = st.text_input("類似語3 (Synonym 3)")
#         col5 = st.text_input("類似語4 (Synonym 4)")
#         phone_number = st.text_input("電話番号 (Phone Number)")
#         sms_number = st.text_input("SMS")
#         email = st.text_input("E-MAIL")
#         day_transfer = st.text_input("昼の転送方法 (Day Transfer Method)")
#         day_response = st.text_area("昼の返答 (Day Response)")
#         day_start = st.time_input("昼の開始時間 (Day Start Time)", value=pd.to_datetime("09:00").time())
#         day_end = st.time_input("昼の終了時間 (Day End Time)", value=pd.to_datetime("18:00").time())
#         night_transfer = st.text_input("夜の転送方法 (Night Transfer Method)")
#         night_response = st.text_area("夜の返答 (Night Response)")
#         night_start = st.time_input("夜の開始時間 (Night Start Time)", value=pd.to_datetime("18:01").time())
#         night_end = st.time_input("夜の終了時間 (Night End Time)", value=pd.to_datetime("22:00").time())
        
#         submitted = st.form_submit_button("Add Row")
#         if submitted:
#             if col1 and phone_number:  # Ensure necessary fields are filled
#                 new_row = [col1, col2, col3, col4, col5, phone_number, sms_number, email, day_transfer, day_response, day_start.strftime("%H:%M"), day_end.strftime("%H:%M"), night_transfer, night_response, night_start.strftime("%H:%M"), night_end.strftime("%H:%M")]
#                 add_row_to_google_sheet(new_row)
#                 st.success("New entry added successfully!")
#                 st.experimental_rerun()
#             else:
#                 st.error("Please fill in all required fields (Keyword and Phone Number).")

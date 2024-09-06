import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Expected columns for Keyword and Action lists
KEYWORD_COLUMNS = ['キーワード', '類似語1', '類似語2', '類似語3', '類似語4']
ACTION_COLUMNS = [
    'キーワード', '電話番号', 'SMS', 'E-MAIL', '昼の転送方法', '昼の返答', 
    '昼の開始時間', '昼の終了時間', '夜の転送方法', '夜の返答', 
    '夜の開始時間', '夜の終了時間'
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
    # Filter for only the Keyword List columns
    keyword_df = data_df[['キーワード', '類似語1', '類似語2', '類似語3', '類似語4']]
    st.subheader("📋 キーワードリスト")
    st.table(keyword_df)

# Function to display the Action List
def display_action_list(data_df):
    # Filter for only the Action List columns
    action_df = data_df[['キーワード', '電話番号', 'SMS', 'E-MAIL', '昼の転送方法', '昼の返答', 
                         '昼の開始時間', '昼の終了時間', '夜の転送方法', '夜の返答', 
                         '夜の開始時間', '夜の終了時間']]
    st.subheader("📋 アクションリスト")
    st.table(action_df)

# Streamlit multipage setup
st.set_page_config(page_title="Google Sheets Data App", layout="wide")

# Top section title
st.title("Google Sheets Data App")

# Load the data from Google Sheets
data_df = load_data()

# Use custom markdown to create horizontal buttons
st.markdown("""
    <style>
    .button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .button-container div {
        margin: 0 10px;
    }
    .custom-button {
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        font-size: 18px;
        text-align: center;
        border-radius: 5px;
        width: 300px;
        display: inline-block;
        cursor: pointer;
    }
    .custom-button:hover {
        background-color: #0056b3;
    }
    </style>
    <div class="button-container">
        <div>
            <button class="custom-button" id="keyword_button">Keyword List</button>
        </div>
        <div>
            <button class="custom-button" id="action_button">Action List</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Handle user click using JavaScript for buttons
clicked = st.session_state.get("clicked", None)

# JavaScript to detect clicks on buttons and update Streamlit state
st.markdown("""
    <script>
    const keywordButton = document.getElementById("keyword_button");
    const actionButton = document.getElementById("action_button");
    
    keywordButton.addEventListener("click", function() {
        window.parent.postMessage('{"clicked": "Keyword"}', "*");
    });
    
    actionButton.addEventListener("click", function() {
        window.parent.postMessage('{"clicked": "Action"}', "*");
    });
    </script>
    """, unsafe_allow_html=True)

# Capture postMessage event
st.markdown("""
    <script>
    window.addEventListener('message', (event) => {
        if (event.data && event.data.clicked) {
            if (event.data.clicked === "Keyword") {
                window.parent.streamlitFrontend.postMessage('setState', {
                    clicked: 'Keyword'
                });
                window.location.reload();
            } else if (event.data.clicked === "Action") {
                window.parent.streamlitFrontend.postMessage('setState', {
                    clicked: 'Action'
                });
                window.location.reload();
            }
        }
    });
    </script>
    """, unsafe_allow_html=True)

# Handle button clicks by checking the `clicked` session state
if clicked == "Keyword" or clicked is None:
    display_keyword_list(data_df)
elif clicked == "Action":
    display_action_list(data_df)




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

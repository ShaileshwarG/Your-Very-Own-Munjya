import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Munjya_Bot_Logs_For_Core1").sheet1

# --- Google Sheets Logger ---
def log_to_google_sheets(query, response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, query, response])

# --- Load Anaplan Functions Data ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/ShaileshwarG/Your-Very-Own-Munjya/main/anaplan_functions.csv"
    return pd.read_csv(url)

data = load_data()

# --- Streamlit App UI ---
st.set_page_config(page_title="Your Very Own Munjya 🤖", page_icon="🤖")
st.title("Ask Munjya About Anaplan Functions")

user_input = st.text_input("🔍 Enter your Anaplan function or question:")

if st.button("Ask Munjya"):
    if user_input:
        # Search for exact match
        match = data[data['Function'].str.lower() == user_input.strip().lower()]

        if not match.empty:
            row = match.iloc[0]
            response = f"""
### 🔍 Function: `{row['Function']}`  
📘 **Description**: {row['Function Description']}  
📌 **Syntax**: `{row['Syntax Example']}`  
🔗 [Read more on Anapedia]({row['Anapedia Link']})
            """
        else:
            response = "❌ Function not found. Please check the spelling or try a different keyword."

        # Show result
        st.markdown(response, unsafe_allow_html=True)

        # ✅ Log to Google Sheet
        log_to_google_sheets(user_input, response)

        # Save in session for download
        if "logs" not in st.session_state:
            st.session_state.logs = []
        st.session_state.logs.append((datetime.now(), user_input, response))

# --- Downloadable Log Button ---
if "logs" in st.session_state and st.session_state.logs:
    df_log = pd.DataFrame(st.session_state.logs, columns=["Timestamp", "User Query", "Bot Response"])
    csv = df_log.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Your Session Log", csv, "your_munjya_log.csv", "text/csv")

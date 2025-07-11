import streamlit as st
import pandas as pd
import datetime
import json
import gspread
from google.oauth2.service_account import Credentials

# ----------------------------- GOOGLE SHEETS SETUP -----------------------------
# Load Google credentials from Streamlit secrets
creds_dict = json.loads(st.secrets["GOOGLE_SHEET_CREDENTIALS"])

# Setup scopes and authenticate
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(credentials)

# Open the sheet
sheet = client.open_by_key("1ugdIE1ygUn8pW-6Dpf_eISuAAowzHIde2GeAddVQtEU").sheet1

# ----------------------------- STREAMLIT APP -----------------------------
st.set_page_config(page_title="Your Very Own Munjya", layout="wide")
st.title("🤖 Your Very Own Munjya")
st.markdown("Ask anything related to Anaplan, supply chain logic, or Core 1 solutions.")

# Session state for storing conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# User input
query = st.text_input("💬 Ask Munjya:", placeholder="Type your question here and press Enter...")

# Simple response simulation (to be replaced with actual LLM or logic)
def mock_munjya_response(q):
    return f"🤖 This is a mock response for: '{q}'"

# Save to log and display conversation
if query:
    response = mock_munjya_response(query)
    st.session_state.conversation.append((query, response))

    # Log to Google Sheet
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = st.secrets.get("USER_EMAIL", "anonymous")  # Optional field
    sheet.append_row([timestamp, user, query, response])

# Display conversation
if st.session_state.conversation:
    st.subheader("🗂️ Chat Log")
    for q, r in st.session_state.conversation:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Munjya:** {r}")

# Allow session log download
if st.session_state.conversation:
    df = pd.DataFrame(st.session_state.conversation, columns=["User", "Munjya"])
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Your Session Log", csv, "your_munjya_log.csv", "text/csv")

# Footer
st.markdown("---")
st.caption("Maintained by Core_1 | Logs are saved securely in Google Sheets.")

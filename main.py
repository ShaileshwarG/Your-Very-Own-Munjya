import streamlit as st
import datetime
import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import APIError
from query_core_1 import query_core_1  # Core_1 head logic

# 🔐 Google Sheets Auth
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info({
    "type": st.secrets["type"],
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": st.secrets["auth_uri"],
    "token_uri": st.secrets["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["client_x509_cert_url"],
    "universe_domain": st.secrets["universe_domain"]
}, scopes=SCOPE)

client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1ugdIE1ygUn8pW-6Dpf_eISuAAowzHIde2GeAddVQtEU").sheet1

# 🤖 UI Setup
st.set_page_config(page_title="Your Anaplan/SupplyChain Buddy - The personal Munjya", page_icon="🧠")
st.title("🧠 Your Anaplan/SupplyChain Buddy - The personal Munjya")

# 🧠 Query Input
query = st.text_input("Ask your question (Anaplan, Supply Chain, Formulas, Planning...)")
submit = st.button("Ask Munjya")

# 🧠 Fallback Setup
from openai import OpenAI
openai_client = OpenAI(api_key=st.secrets.get("openai_api_key", ""))

def query_with_fallback(user_query):
    response = query_core_1(user_query, top_k=3)
    source = "Core_1"

    if not response or response.strip() == "":
        source = "GPT fallback"
        with st.spinner("No direct match found in Core_1. Trying fallback model..."):
            try:
                completion = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a Master Anaplanner and Supply Chain expert. Respond concisely and precisely."},
                        {"role": "user", "content": user_query}
                    ]
                )
                response = completion.choices[0].message.content.strip()
            except Exception as e:
                response = (
                    "🧠 I'm still learning, and this part isn't in my Core_1 memory yet. "
                    "Thank you for the question — I’ll learn this soon!"
                )
                source = "Core_1 only (fallback failed)"

    return response, source

# 🚀 Main Logic
if submit and query:
    try:
        with st.spinner("Munjya is thinking..."):
            answer, source = query_with_fallback(query)

        st.markdown(f"### Munjya says:\n\n{answer}")
        
        # ✅ Log to sheet
        sheet.append_row([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            query,
            answer,
            source
        ])
        st.success(f"📝 Logged successfully via `{source}`")

    except APIError:
        st.error("⚠️ Issue writing to Google Sheet. Check sharing permissions and API status.")
    except Exception as e:
        st.error("❌ Unexpected error occurred.")
        st.exception(e)

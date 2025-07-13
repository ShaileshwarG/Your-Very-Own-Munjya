import streamlit as st
import datetime
import gspread
from google.oauth2.service_account import Credentials
from query_core_1 import query_core_1  # 🧠 Your logic head
from gspread.exceptions import APIError

# -------------------- Auth Setup -------------------- #
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

# -------------------- Streamlit UI -------------------- #
st.set_page_config(page_title="Munjya Bot", page_icon="🤖")
st.title("🤖 Munjya Bot - Powered by Core_1")

query = st.text_input("Enter your Anaplan or Supply Chain query:")
submit = st.button("Ask Munjya")

# -------------------- Core + Fallback -------------------- #
def query_with_fallback(user_query):
    response = query_core_1(user_query)  # Try Core_1
    source = "Core_1"

    if not response or response.strip() == "":
        source = "GPT fallback"
        with st.spinner("No direct match found in Core_1. Trying fallback model..."):
            import openai
            openai.api_key = st.secrets.get("openai_api_key", "")
            if openai.api_key:
                fallback = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a Master Anaplanner and Supply Chain expert. Respond concisely."},
                        {"role": "user", "content": user_query}
                    ]
                )
                response = fallback.choices[0].message.content.strip()
            else:
                response = "Fallback failed: OpenAI key not configured."

    return response, source

# -------------------- Action -------------------- #
if submit and query:
    try:
        with st.spinner("Thinking like Core_1..."):
            answer, source = query_with_fallback(query)

        st.markdown(f"**Munjya says:**\n\n{answer}")
        sheet.append_row([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            query,
            answer,
            source
        ])
        st.success(f"Logged to sheet via {source}")

    except APIError as e:
        st.error("⚠️ Error logging to sheet. Check Google credentials or sheet sharing.")
        st.exception(e)
    except Exception as e:
        st.error("❌ Unexpected error occurred.")
        st.exception(e)

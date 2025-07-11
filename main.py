import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

# ------------------ GOOGLE SHEETS AUTH ------------------ #
SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_info({
    "type": st.secrets["type"],
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"].replace("\\n", "\n"),
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": st.secrets["auth_uri"],
    "token_uri": st.secrets["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["client_x509_cert_url"],
    "universe_domain": st.secrets["universe_domain"]
}, scopes=SCOPE)

client = gspread.authorize(creds)
sheet = client.open_by_key("1ugdIE1ygUn8pW-6Dpf_eISuAAowzHIde2GeAddVQtEU").sheet1

# ------------------ QUERY PROCESSING ENGINE ------------------ #
def query_core_1(user_query: str):
    query = user_query.lower().strip()

    if "wos" in query and "5 week" in query:
        return "Use 5-week rolling average WoS with quarter reset. Reference SYS Time Week module for QuarterID and build dynamic mapping for first/last week."

    elif "constraint supply plan" in query:
        return ("Apply W1 for first week only, W2-W3 logic for initial non-zero shipment weeks. "
                "From the first zero shipment week, switch to W4+ logic using Supply Plan."
                " Dynamically identify first zero after non-zero using running count or booleans.")

    elif "constraint demand plan" in query:
        return ("Base Constraint Demand Plan on the active Constraint Supply Plan. Ensure proper logic to avoid double counting."
                " Use LOOKUPs and TIMESUM with appropriate filtering modules. Validate against Excel behavior.")

    elif "assign account to territory" in query:
        return ("Use SYS Account, SYS Territory modules. Store assignment in TAR01. Reference user stories from Level 3 Sales Planning."
                " Ensure RANK and ISFIRSTOCCURRENCE are used for scoring and assignment.")

    elif "designate sales rep" in query:
        return ("Use REP01, TAR01, and Assignment mapping logic. Build scoring mechanism based on capacity, performance, territory compatibility."
                " Design user-facing process using UX worksheet guidance.")

    elif "isfirstoccurrence" in query:
        return "ISFIRSTOCCURRENCE(Boolean, List) returns TRUE for the first TRUE occurrence in a list context. Useful in filtering, ranking."

    elif "rank" in query:
        return "Use RANK to order values, optionally by group. Handle ties using MIN/MAX/SEQUENTIAL. Avoid circular references in complex rank chains."

    elif "circular reference" in query:
        return "Avoid daisy chaining logic. Separate modules by function and use clear calculation paths. Prefer LOOKUP and TIMESUM over SELECT."

    elif "performance" in query and "anaplan" in query:
        return "Limit line item count, avoid dense multi-dim modules, use subsets, turn off summary when not needed. Use ALM for controlled deployments."

    return None

# ------------------ STREAMLIT UI ------------------ #
st.set_page_config(page_title="Your Very Own Munjya", page_icon="🤖")
st.title("🤖 Your Very Own Munjya")

user_input = st.text_input("Ask me anything about Anaplan logic, supply chain, or Core_1 knowledge:")

if user_input:
    core_response = query_core_1(user_input)

    if core_response:
        st.success(f"🧠 Core_1 Response:\n\n{core_response}")
    else:
        st.info("🤖 This question is being escalated to Core_1’s fallback AI. (Mocked response below)")
        st.markdown("*‘I’m searching deeper...’*")
        st.warning("🚧 This part is under development. You’ll soon get detailed fallback responses here.")

    # Append log to sheet
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user_input, core_response or "Fallback Triggered"])

# ------------------ SESSION DOWNLOAD ------------------ #
log_data = pd.DataFrame(sheet.get_all_records())
csv = log_data.to_csv(index=False)
st.download_button("📥 Download Your Session Log", csv, "your_munjya_log.csv", "text/csv")

import streamlit as st
import pandas as pd
from datetime import datetime

# Title and header
st.set_page_config(page_title="Munjya Anaplan Bot", layout="centered")
st.title("🤖 Munjya Anaplan Bot (v1.1)")
st.markdown("Ask me anything about Anaplan functions, modeling logic, and best practices. I’ll retrieve and format a trusted answer.")

# Load function data (CSV)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/shaileshwaranaplan/munjya-anaplan-bot/main/anaplan_functions.csv"
    return pd.read_csv(url)

data = load_data()

# User input
query = st.text_input("🔍 Your question:")

# Logging interactions
if "logs" not in st.session_state:
    st.session_state.logs = []

def log_interaction(query, response):
    st.session_state.logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "response": response
    })

# Response logic
def retrieve_answer(q):
    q = q.lower().strip()
    matches = data[data["Function Description"].str.lower().str.contains(q, na=False) | 
                   data["Function"].str.lower().str.contains(q, na=False)]

    if not matches.empty:
        row = matches.iloc[0]
        response = f"""### ✅ {row['Function']}
**Syntax:** `{row['Syntax Example']}`  
**Description:** {row['Function Description']}  
[🔗 Anapedia Link]({row['Anapedia link for the that functions']})
"""
        return response
    else:
        return "❌ I couldn't find a matching Anaplan function or description. Try rephrasing your question."

# Show result
if query:
    result = retrieve_answer(query)
    log_interaction(query, result)
    st.markdown(result, unsafe_allow_html=True)

# Log download
st.markdown("---")
st.subheader("📥 Export Your Session Log")
if st.button("Download Log as CSV"):
    df = pd.DataFrame(st.session_state.logs)
    filename = f"munjya_bot_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    st.success("✅ Log file generated. Use 'Download' from your browser to save it.")

st.markdown("---")
st.caption("Munjya Anaplan Bot v1.1 | Powered by Core_1 memory packet | All responses are logged for review.")

import os

import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.title("Access Request Triage (g07)")
st.caption("Routing proposals only. Nothing is granted and every result requires human review.")
api_url = os.getenv("API_URL", "http://localhost:8000")
with st.form("request"):
    subject = st.text_input("Subject", "New account for a contractor")
    text = st.text_area(
        "Request", "Please create an account for a contractor who starts on Monday."
    )
    submitted = st.form_submit_button("Analyze")
if submitted:
    try:
        response = httpx.post(
            api_url + "/api/analyze",
            json={"subject": subject, "text": text},
            timeout=75,
            trust_env=False,
        )
        response.raise_for_status()
        record = response.json()
        analysis = record["analysis"]
        st.warning("Requires human review: this is a proposal and no action was taken.")
        col1, col2 = st.columns(2)
        col1.metric("Category", analysis["category"])
        col2.metric("Priority", analysis["priority"])
        st.markdown(f"**Summary:** {analysis['summary']}")
        st.markdown(f"**Proposed next action:** {analysis['next_action']}")
        st.caption(
            f"Record {record['id']} · provider {record['provider']} · "
            f"requires_review={record['requires_review']}"
        )
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 422:
            st.error("Invalid input: subject 3 to 100 characters, request 10 to 4000 characters.")
        else:
            st.error(
                f"API returned {exc.response.status_code}: the model is unavailable or its "
                "output was rejected. Nothing was saved."
            )
    except httpx.RequestError:
        st.error("API is unreachable. Check API_URL and the backend process.")

st.subheader("Recent validated results")
try:
    history = httpx.get(api_url + "/api/history", timeout=10, trust_env=False).json()
    st.dataframe([{"id": item["id"], **item["analysis"]} for item in history])
except (httpx.HTTPError, ValueError, KeyError, TypeError):
    st.info("History unavailable.")

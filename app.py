import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

def fetch_response(endpoint, payload=None, method="GET"):
    """Handles API requests with a timeout."""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=payload, timeout=20)
        else:  # POST
            response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

st.title("E-Commerce Customer Service Agent")

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["Order Tracking", "Return Request", "Agent Chat", "Voice Input"])

if menu == "Order Tracking":
    st.header("Track Your Order")
    order_id = st.text_input("Enter Order ID:")
    if st.button("Track Order"):
        result = fetch_response(f"/tracking/orders/{order_id}")
        st.json(result)

elif menu == "Return Request":
    st.header("Submit a Return Request")
    order_id = st.text_input("Enter Order ID:")
    reason = st.text_area("Reason for Return:")
    if st.button("Submit Request"):
        payload = {"order_id": order_id, "reason": reason}
        result = fetch_response("/returns/return-request/", payload, method="POST")
        st.json(result)

elif menu == "Agent Chat":
    st.header("Chat with Customer Service Agent")
    user_input = st.text_input("Enter your query:")
    if st.button("Send"):
        result = fetch_response("/agent/customer-service/", {"user_input": user_input}, method="POST")
        st.write(f"**Agent:** {result.get('response', 'Error processing request')}")

elif menu == "Voice Input":
    st.header("Voice to Text")
    if st.button("Start Listening"):
        result = fetch_response("/voice/voice-to-text/")
        st.write(f"You said: {result.get('transcription', 'Error processing voice input')}")

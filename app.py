import streamlit as st
import requests
import json
from dotenv import dotenv_values
import google-generativeai as genai

# Load environment variables from .env file
config = dotenv_values(".env")

# Extract the API key from the loaded configuration
openai_api_key = config.get("API_KEY")

app_url = "http://localhost:8000"
endpoint = "/generate"
model_url = f"{app_url}{endpoint}"

# Set the hardcoded API key
api_key = "gemini-pro"

import streamlit as st
st.set_page_config(layout="wide")

with open("test/test_inputs.json", "r") as f:
    default_input = json.load(f)

default_input = default_input["apple"]

st.title("email marketing campaign generator")

# Remove the sidebar section

col1, col2 = st.columns(2)

with col1:
    # Input fields remain the same

inputs = {
    "email_inputs": {
         "business_information": {
            "business_name": business_name,
            "business_type": business_type,
            "campaign_goal": campaign_goal,
            "audience_demographics": audience_demographics
        },
        "content_guidelines": {
            "content_type": content_type,
            "key_message": key_message
        },
        "email_structure": {
            "call_to_action": call_to_action
        },
        "product_service_information": {
            "product_service_details": product_service_details,
            "features_and_benefits": features_and_benefits
        },
        "tone_and_voice": {
            "tone_and_voice_from_website": website_url,
            "communication_tone": communication_tone,
            "brand_voice": brand_voice
        },
        "storyline_progression": {
            "email_sequence_narrative": email_sequence_narrative
        },
        "pain_points_and_solutions": {
            "pain_points_addressed": pain_points_addressed,
            "solutions_presented": solutions_presented
        }
    },
    "api_key": api_key  # Using the hardcoded API key instead of user input
}

with col2:
    st.write("## output")
    st.divider()

if "output" not in st.session_state:
    st.session_state.output = None

if st.button("generate emails"):
    with col2:
        with st.spinner("generating emails..."):
            response = requests.post(model_url, json=inputs)
            if response.ok:
                emails = response.json()
                st.session_state.output = emails
            else:
                with col2:
                    st.write("error generating emails", response.status_code, response.text)

with col2:
    if st.session_state.output:
        headers = ["email 1: introduction",
            "email 2: building on pain point",
            "email 3: solution presentation",
            "email 4: benefits and social proof",
            "email 5: call to action and conclusion"
        ]

        for index, (email_id, email_data) in enumerate(st.session_state.output.items()):
            st.subheader(headers[index])
            st.write("**subject:**", email_data["subject"])
            st.write(email_data["greeting"])
            st.write(email_data["body"])
            st.write(email_data["signature"])
            st.divider()

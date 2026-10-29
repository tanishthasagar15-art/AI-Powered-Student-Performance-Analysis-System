from google import genai
import streamlit as st

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

st.title("Gemini Model Availability Test")

if st.button("Check Available Models"):
    try:
        models = client.models.list()

        st.write("Models supporting text generation:")

        found = False

        for model in models:
            methods = getattr(
                model,
                "supported_actions",
                []
            ) or []

            if "generateContent" in methods:
                st.write(model.name)
                found = True

        if not found:
            st.info(
                "No matching models were listed. "
                "Check the available models in Google AI Studio."
            )

    except Exception as e:
        st.error(f"Unable to list models: {e}")
import streamlit as st
import google.generativeai as genai

# Layout setup
c1, c2 = st.columns([30, 50])
c2.title("PredictGuard: Predicting the disease based on symptoms")
c1.image("logo-removebg-preview.png")

# Configure Gemini
genai.configure(api_key="AIzaSyBriPGfcEJ30_U3zevWuyYe2BvL8Mcb2TQ")

def create_gen_model():
    return genai.GenerativeModel('models/gemini-1.5-pro')

def main():
    query = st.chat_input("Enter the Symptoms:")

    if query:
        model = create_gen_model()

        # Prompt for 2-3 possible conditions based on symptom severity
        prediction_prompt = (
            f"I have the following symptoms: {query}. "
            "Please suggest 2 to 3 possible diseases or conditions that match these symptoms, "
            "ranked by likelihood. If symptoms are mild (e.g., vomiting, headache, sneezing), prefer non-serious conditions "
            "like acidity, common cold, etc. Only mention serious diseases if strongly indicated. "
            "Respond in bullet points. Keep each condition's name concise (just the name)."

        )

        response = model.generate_content(prediction_prompt)
        predicted_conditions = response.text.strip()

        st.subheader("Possible Conditions:")
        st.markdown(predicted_conditions)

        # Prompt for treatments for the listed conditions
        solution_prompt = (
            f"Based on the conditions listed here:\n{predicted_conditions}\n"
            "Please provide brief, common treatments or medications for each one. "
            "Use bullet points with the condition name followed by treatment. Keep it simple and avoid technical jargon. and at last add a line which tells about always consult a professional"
        )

        response2 = model.generate_content(solution_prompt)
        st.subheader("Suggested Treatments / Medications:")
        st.markdown(response2.text.strip())

if __name__ == "__main__":
    main()

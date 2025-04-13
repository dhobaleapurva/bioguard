import streamlit as st
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key="AIzaSyDpB0TSK6uGGj4EppytQ0YaTOZFMHg134I")


# Function to get emergency financial assistance information from Gemini
def get_financial_assistance_info(hospital_name, location):
    model = genai.GenerativeModel('models/gemini-1.5-pro')

    # Modified query to focus on legitimate financial assistance options
    query = (
        f"Create a list of NGOs and financial assistance options for patients at {hospital_name} in {location}, let the contact number be for demonstration purpose only and each ngo's contact number starting should be in different digit. but do not mention in response anywhere that it for demo. "
        f"Include 5 reputable NGOs that help with medical expenses, their contact numbers (fictional ), "
        f"their focus areas, and application process. "
        f"Format as a markdown table .")

    # Generation config to make response more predictable
    generation_config = {
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 1024,
    }

    # Get AI-generated content
    response = model.generate_content(query, generation_config=generation_config)
    return response.text


# Main Emergency Financial Assistance function
def emergency_financial_services_main():
    c1, c2 = st.columns([30, 50])
    c2.title("FundGuard: Emergency Financial Assistance")
    c1.image("logo-removebg-preview.png")

    st.write("Find financial assistance for medical expenses")

    # Input fields
    hospital_name = st.text_input("Enter the name of the hospital:")
    location = st.text_input("Enter your current location (city/area):")


    if st.button("Find Financial Assistance"):
        if hospital_name and location:
            with st.spinner("Searching for financial assistance options..."):
                # Get financial assistance information from the Gemini model
                assistance_info = get_financial_assistance_info(hospital_name, location)

                # Display the recommendations
                st.subheader("Financial Assistance Options:")
                st.markdown(assistance_info)
        else:
            st.warning("Please enter both the hospital name and your location.")

    # Chat input for more specific questions
    user_question = st.chat_input("Ask a specific question about financial assistance:")

    if user_question:
        with st.spinner("Processing your question..."):
            model = genai.GenerativeModel('models/gemini-1.5-pro')
            response = model.generate_content(
                f"The user is asking about financial assistance for medical treatment at {hospital_name if 'hospital_name' in locals() else 'a hospital'}. Their question is: {user_question}. Provide helpful information focused on legitimate financial assistance options only.")
            st.write("Response:")
            st.write(response.text)


if __name__ == "__main__":
    emergency_financial_services_main()

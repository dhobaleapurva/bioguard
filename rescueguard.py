import streamlit as st
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key="AIzaSyDpB0TSK6uGGj4EppytQ0YaTOZFMHg134I")  # Replace with your API key


# Function to get emergency information from Gemini
def get_emergency_info(keyword, location):
    model = genai.GenerativeModel('models/gemini-1.5-pro')

    # Formulate a query that's more likely to produce structured data
    query = (f"Create a demonstration emergency information table for {keyword} emergency in {location}. "
             f"Include 5 major hospitals, their contact numbers (each hospital contact number should be totally. all hospital contact numbers should not start with same number and it is for demo purposes), "
             f"approximate locations, and typical travel times from {location}. "
             f"Format as a markdown table and do not include appropriate disclaimers that this is for demonstration purposes only.")

    # Generation config to make response more predictable
    generation_config = {
        "temperature": 0.2,  # Lower temperature for more consistent output
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 1024,
    }

    # Get AI-generated content
    response = model.generate_content(query, generation_config=generation_config)
    return response.text


# Main Emergency Services function
def emergency_services_main():
    c1, c2 = st.columns([30, 50])
    c2.title("RescueGuard: Emergency Contacts & Locations")
    c1.image("logo-removebg-preview.png")

    st.write("Please provide the details of your emergency below.")

    # Input fields
    keyword = st.text_input("Enter the type of emergency (e.g., accident, pregnancy, etc.):")
    location = st.text_input("Enter your current location (e.g., address or coordinates):")



    if st.button("Get Emergency Help"):
        if keyword and location:
            with st.spinner("Fetching emergency information..."):
                # Get emergency information from the Gemini model
                emergency_info = get_emergency_info(keyword, location)

                # Display the recommendations
                st.subheader("Emergency Help Information:")
                st.markdown(emergency_info)  # Using st.markdown to properly render the table
        else:
            st.warning("Please enter both the type of emergency and your location.")

    # Add additional information section
    with st.expander("Emergency Services Information"):
        st.write("""
        - **Ambulance Services:** 108 or 102
        - **Police:** 100
        - **Fire Department:** 101
        - **National Emergency Number:** 112
        - **Women Helpline:** 1091

        Download emergency services apps like:
        - 108 Ambulance Service
        - Red Cross First Aid
        - Practo
        """)


if __name__ == "__main__":
    emergency_services_main()

import streamlit as st
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key="AIzaSyDpB0TSK6uGGj4EppytQ0YaTOZFMHg134I")  # Replace with your API key

# Function to get detailed hospital emergency information
def get_emergency_info(keyword, location):
    model = genai.GenerativeModel('models/gemini-1.5-pro')

    query = (
        f"Create a detailed markdown table listing 5 major hospitals for a {keyword} emergency in {location}. "
        f"For each hospital, include the following columns:\n"
        f"- *Name of the Hospital*\n"
        f"- *Location / Address*\n"
        f"- *Accessibility (public transport, parking, etc.)*\n"
        f"- *Contact Information (phone, email, website)*\n"
        f"- *Type of Hospital (e.g., government, private, multi-specialty, etc.)*\n"
        f"- *Available Departments / Specialties*\n"
        f"- *Hospital Hours / Visiting Hours*\n"
        f"- *Appointment Process (online booking, walk-in, phone appointments)*\n"
        f"Ensure diversity in contact numbers and realistic-sounding data for demo purposes. "
        f"Output only the markdown table without any disclaimers."
    )

    generation_config = {
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 2048,
    }

    response = model.generate_content(query, generation_config=generation_config)
    return response.text

# Main Emergency Services function
def emergency_services_main():
    c1, c2 = st.columns([30, 50])
    c2.title("RescueGuard: Emergency Contacts & Locations")
    c1.image("logo-removebg-preview.png")

    st.write("Please provide the details of your emergency below.")

    keyword = st.text_input("Enter the type of emergency (e.g., accident, pregnancy, etc.):")
    location = st.text_input("Enter your current location (e.g., address or coordinates):")

    if st.button("Get Emergency Help"):
        if keyword and location:
            with st.spinner("Fetching emergency information..."):
                emergency_info = get_emergency_info(keyword, location)
                st.subheader("Emergency Help Information:")
                st.markdown(emergency_info)
        else:
            st.warning("Please enter both the type of emergency and your location.")

    with st.expander("Emergency Services Information"):
        st.write("""
        - *Ambulance Services:* 108 or 102
        - *Police:* 100
        - *Fire Department:* 101
        - *National Emergency Number:* 112
        - *Women Helpline:* 1091

        Recommended apps:
        - 108 Ambulance Service
        - Red Cross First Aid
        - Practo
        """)

if __name__ == "__main__":

    emergency_services_main()

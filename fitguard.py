import streamlit as st
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key="AIzaSyDpB0TSK6uGGj4EppytQ0YaTOZFMHg134I")


# Function to calculate BMI
def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return bmi


# Function to suggest a basic plan based on BMI
def suggest_plan(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"


# Function to interact with the Gemini model for detailed recommendations
def get_gemini_recommendation(bmi_status, health_condition, weight, height, age, gender, activity_level):
    model = genai.GenerativeModel('models/gemini-1.5-pro')

    # Improved prompt to get better formatted responses
    query = f"""
    Based on the following health details, please provide a well-structured fitness and nutrition plan:

    - BMI Status: {bmi_status} (calculated from height: {height}m, weight: {weight}kg)
    - Health Conditions: {health_condition if health_condition else "None specified"}
    - Age: {age} years
    - Gender: {gender}
    - Activity Level: {activity_level}

    Please format your response with clear headings and sections:
    1. Summary of health assessment
    2. Nutrition Plan (with specific meal suggestions)
    3. Fitness Plan (with specific exercise routines)
    4. Special considerations for the health conditions mentioned
    5. Weekly progress tracking recommendations

    Use markdown formatting for better readability. Include appropriate emoji where relevant.
    """

    # Generation config for better structured output
    generation_config = {
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 1024,
    }

    # Get AI-generated content
    response = model.generate_content(query, generation_config=generation_config)
    return response.text


# Main FitGuard function
def fitguard_main():
    c1, c2 = st.columns([30, 50])
    c2.title("FitGuard: Calculates BMI & Suggests Fitness Plan")
    c1.image("logo-removebg-preview.png")

    # Store session state
    if "bmi" not in st.session_state:
        st.session_state.bmi = None
        st.session_state.bmi_status = None
        st.session_state.plan = None
        st.session_state.tab_index = 0

    # Create tabs for a better user experience
    tab1, tab2 = st.tabs(["Input Your Details", "View Results"])

    with tab1:
        # Add more comprehensive input fields
        col1, col2 = st.columns(2)

        with col1:
            height = st.number_input("Height (in meters):", min_value=0.5, max_value=2.5, value=1.7, step=0.01)
            weight = st.number_input("Weight (in kilograms):", min_value=10.0, max_value=200.0, value=70.0, step=0.1)
            age = st.number_input("Age:", min_value=18, max_value=100, value=30, step=1)

        with col2:
            gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
            activity_level = st.select_slider(
                "Activity Level:",
                options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
                value="Moderately Active"
            )
            health_condition = st.text_area("Health Conditions (if any):", height=100)

        # Add disclaimer
      
        generate_button = st.button("Calculate BMI & Generate Plan", type="primary")

    # Process when button is clicked
    if generate_button:
        if height > 0 and weight > 0:
            bmi = calculate_bmi(weight, height)
            bmi_status = suggest_plan(bmi)

            with st.spinner("Generating your personalized fitness plan..."):
                gemini_recommendation = get_gemini_recommendation(
                    bmi_status, health_condition, weight, height, age, gender, activity_level
                )

            # Store in session state
            st.session_state.bmi = bmi
            st.session_state.bmi_status = bmi_status
            st.session_state.plan = gemini_recommendation
            st.session_state.tab_index = 1  # Set to results tab

            # Rerun to switch tabs
            st.rerun()

    # Display results in the second tab
    with tab2:
        if st.session_state.bmi is not None:
            # Create BMI display with color coding
            bmi_col1, bmi_col2 = st.columns([1, 2])

            with bmi_col1:
                st.metric("Your BMI", f"{st.session_state.bmi:.1f}")

                # Color-coded BMI status
                status_color = {
                    "Underweight": "orange",
                    "Normal weight": "green",
                    "Overweight": "orange",
                    "Obese": "red"
                }

                st.markdown(
                    f"<h3 style='color: {status_color.get(st.session_state.bmi_status, 'blue')};'>{st.session_state.bmi_status}</h3>",
                    unsafe_allow_html=True)

            with bmi_col2:
                st.markdown("""
                **BMI Categories:**
                - Underweight: < 18.5
                - Normal weight: 18.5–24.9
                - Overweight: 25–29.9
                - Obese: ≥ 30
                """)

            # Show the generated plan
            st.markdown("## Your Personalized Plan")
            st.markdown(st.session_state.plan)

            # Add a download button for the plan
            st.download_button(
                label="Download Your Plan",
                data=f"""# Your FitGuard Personalized Plan

## BMI Result: {st.session_state.bmi:.1f} ({st.session_state.bmi_status})

{st.session_state.plan}

*Generated by FitGuard*
                """,
                file_name="my_fitness_plan.md",
                mime="text/markdown"
            )
        else:
            st.info("Please enter your details and generate a plan in the 'Input Your Details' tab.")


# Ensure the correct tab is selected based on session state
if __name__ == "__main__":
    fitguard_main()

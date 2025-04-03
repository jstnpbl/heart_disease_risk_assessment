import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Set up the favicon and page title
st.set_page_config(
    page_title="Heart Disease Risk Assessment",  # Title of the tab
    page_icon="C:/Users/johnr/Thesis System/Heart Disease Risk System/icon.jpg",  # Path to your favicon file
)

# Load the dataset (adjust path as needed)
heart_disease_data = pd.read_csv("heart_disease_health_indicators_BRFSS2015.csv")


# Function to calculate QRISK3-based heart disease risk
def calculate_qrisk3(age, sex, smoking, diabetes, blood_pressure, cholesterol, bmi, atrial_fibrillation,
                     rheumatoid_arthritis, physical_activity, diet_quality, alcohol_consumption, family_history,
                     mental_health, sleep_duration, chronic_kidney_disease, migraine_history):
    base_risk = age * 0.15
    risk_factors = {
        "Sex (Male)": 1.2 if sex == "Male" else 1.0,
        "Smoking": 1.3 if smoking else 1.0,
        "Diabetes": 1.4 if diabetes else 1.0,
        # Modified only these three lines to handle empty values
        "High Blood Pressure": 1.2 if blood_pressure is not None and blood_pressure > 140 else 1.0,
        "High Cholesterol": 1.2 if cholesterol is not None and cholesterol > 5.0 else 1.0,
        "High BMI": 1.2 if bmi is not None and bmi > 30 else 1.0,
        # Rest remains unchanged as it already handles unspecified values correctly
        "Atrial Fibrillation": 1.3 if atrial_fibrillation else 1.0,
        "Rheumatoid Arthritis": 1.1 if rheumatoid_arthritis else 1.0,
        "Sedentary Lifestyle": 1.3 if physical_activity == "Sedentary" else (
            1.1 if physical_activity == "Moderate" else 1.0),
        "Unhealthy Diet": 1.3 if diet_quality == "Unhealthy" else (1.1 if diet_quality == "Balanced" else 1.0),
        "Frequent Alcohol Consumption": 1.2 if alcohol_consumption == "Frequent" else 1.0,
        "Family History": 1.4 if family_history else 1.0,
        "Mental Health Issues": 1.2 if mental_health else 1.0,
        "Short Sleep Duration": 1.3 if sleep_duration == "Less than 6 hours" else 1.0,
        "Chronic Kidney Disease": 1.3 if chronic_kidney_disease else 1.0,
        "Migraine History": 1.1 if migraine_history else 1.0
    }

    for factor, multiplier in risk_factors.items():
        base_risk *= multiplier

    risk_percentage = min(base_risk, 100)
    return round(risk_percentage, 2), risk_factors
# Function to generate personalized recommendations
def get_recommendations(risk_factors):
    recommendations = {}

    # Generate recommendations based on risk factors
    if risk_factors["Smoking"] > 1.0:
        recommendations["Smoking"] = {
            "title": "🚬 Quit Smoking",
            "tips": [
                "Set a specific quit date within the next 2 weeks",
                "Speak to your doctor about nicotine replacement therapies",
                "Join a support group or seek counseling",
                "Download a quit-smoking app to track progress",
                "Avoid triggers and replace smoking with healthier habits"
            ],
            "impact": "Quitting smoking can reduce your risk by up to 30% within 1 year"
        }

    if risk_factors["High Blood Pressure"] > 1.0:
        recommendations["Blood Pressure"] = {
            "title": "📈  Blood Pressure",
            "tips": [
                "Reduce sodium intake to less than 2,300mg per day",
                "Exercise regularly - aim for 150 minutes per week",
                "Practice stress reduction techniques like meditation",
                "Monitor your blood pressure at home regularly",
                "Take prescribed medications as directed"
            ],
            "impact": "Reducing blood pressure to normal levels can decrease risk by up to 25%"
        }

    if risk_factors["High Cholesterol"] > 1.0:
        recommendations["Cholesterol"] = {
            "title": "🩸 Improve Cholesterol Levels",
            "tips": [
                "Increase soluble fiber intake (oats, beans, fruits)",
                "Limit saturated fat and eliminate trans fat",
                "Include omega-3 rich foods like fish twice weekly",
                "Consider plant stanols/sterols in your diet",
                "Maintain a consistent exercise regimen"
            ],
            "impact": "Optimal cholesterol management can reduce risk by 20-35%"
        }

    if risk_factors["High BMI"] > 1.0:
        recommendations["Weight"] = {
            "title": "⚖️ Achieve Healthy Weight",
            "tips": [
                "Aim for gradual weight loss of 1-2 pounds per week",
                "Focus on portion control rather than strict dieting",
                "Include strength training to maintain muscle mass",
                "Track food intake with a journal or app",
                "Set realistic goals based on BMI targets"
            ],
            "impact": "A 5-10% weight reduction can lower heart disease risk by up to 20%"
        }

    if risk_factors["Sedentary Lifestyle"] > 1.0:
        recommendations["Exercise"] = {
            "title": "🏃‍♂️ Increase Physical Activity",
            "tips": [
                "Start with 10-minute walks and gradually increase duration",
                "Aim for 150 minutes of moderate or 75 minutes of vigorous activity weekly",
                "Include strength training 2-3 times per week",
                "Find activities you enjoy to maintain consistency",
                "Break up sitting time with short movement breaks"
            ],
            "impact": "Regular exercise can reduce heart disease risk by 30-40%"
        }

    if risk_factors["Unhealthy Diet"] > 1.0:
        recommendations["Diet"] = {
            "title": "🥕 Improve Diet Quality",
            "tips": [
                "Follow a Mediterranean or DASH eating pattern",
                "Increase fruits and vegetables to 5+ servings daily",
                "Choose whole grains over refined carbohydrates",
                "Limit processed foods and added sugars",
                "Prepare more meals at home"
            ],
            "impact": "A heart-healthy diet can lower risk by 25-30%"
        }

    if risk_factors["Frequent Alcohol Consumption"] > 1.0:
        recommendations["Alcohol"] = {
            "title": "🍺 Moderate Alcohol Consumption",
            "tips": [
                "Limit to 1 drink daily for women, 2 for men",
                "Have alcohol-free days each week",
                "Choose beverages with lower alcohol content",
                "Drink water between alcoholic beverages",
                "Avoid binge drinking completely"
            ],
            "impact": "Proper alcohol moderation can reduce cardiovascular risk by 15-20%"
        }

    if risk_factors["Short Sleep Duration"] > 1.0:
        recommendations["Sleep"] = {
            "title": "💤 Improve Sleep Quality",
            "tips": [
                "Maintain consistent sleep and wake times",
                "Create a relaxing bedtime routine",
                "Keep bedroom cool, dark, and quiet",
                "Limit screen time 1-2 hours before bed",
                "Aim for 7-9 hours of quality sleep each night"
            ],
            "impact": "Proper sleep can reduce heart disease risk by 10-15%"
        }

    # Return at least 3 recommendations if possible
    if len(recommendations) < 3:
        # Add general recommendations to ensure at least 3
        if "Diet" not in recommendations:
            recommendations["Diet"] = {
                "title": "🥦 Heart-Healthy Diet",
                "tips": [
                    "Increase consumption of fruits, vegetables, and whole grains",
                    "Choose lean proteins and limit red meat",
                    "Include fish rich in omega-3 fatty acids twice weekly",
                    "Minimize sodium, sugar, and processed foods",
                    "Consider the DASH or Mediterranean eating pattern"
                ],
                "impact": "A heart-healthy diet can improve overall cardiovascular health"
            }

        if "Exercise" not in recommendations:
            recommendations["Exercise"] = {
                "title": "🏃‍♂️ Regular Physical Activity",
                "tips": [
                    "Aim for at least 150 minutes of moderate activity weekly",
                    "Include both aerobic exercise and strength training",
                    "Find physical activities you enjoy to maintain consistency",
                    "Start slowly and gradually increase intensity",
                    "Break up sitting time with short movement breaks"
                ],
                "impact": "Regular exercise improves heart function and overall health"
            }

        if "Preventive Care" not in recommendations:
            recommendations["Preventive Care"] = {
                "title": "👨‍⚕️ Regular Medical Check-ups",
                "tips": [
                    "Schedule annual physical examinations",
                    "Monitor blood pressure, cholesterol, and blood sugar regularly",
                    "Discuss appropriate screening tests with your doctor",
                    "Follow through with recommended vaccinations",
                    "Maintain open communication with your healthcare provider"
                ],
                "impact": "Regular preventive care enables early intervention"
            }

    return recommendations

# Streamlit UI
st.title("❤️ LIFELINE")
st.markdown("### **Estimate your 10-year risk of heart disease**")
st.write("Welcome to Lifeline! Use this tool to check your cardiovascular health and get actionable insights.")

# Sidebar Section
st.sidebar.image(
    "C:/Users/johnr/Thesis System/Heart Disease Risk System/system_logo.jpg",  # Replace with the actual file name
    use_container_width=True,  # Updated parameter for proper resizing
    caption="**Assess. Act. Achieve a healthier future.**"  # Optional caption
)

# Mission Statement
st.sidebar.markdown("""
    <h3 style="color:#ff4b4b; text-align:center;">Our Mission</h3>
    <p style="text-align:center; color:#333; font-size:15px;">
        "To shift the focus from reaction to prevention in the fight against heart disease. By providing accurate and easy-to-understand risk assessments, we aim to motivate individuals to adopt healthier habits and proactively manage their heart health."
    </p>        
""", unsafe_allow_html=True)

# Philippine Emergency Numbers
st.sidebar.markdown("""
    <h3 style="color:#ff4b4b; text-align:center;">In Case of Emergency</h3>
    <p style="text-align:center; font-size:15px; color:#333;">
        ☎️ <strong>Department of Health (DOH):</strong> <a href="tel:+63286517800" style="color:#ff4b4b;">+63 2 8651 7800</a><br>
        ☎️ <strong>Philippine Red Cross:</strong> <a href="tel:+63287902300" style="color:#ff4b4b;">+63 2 8790 2300</a> or <a href="tel:143" style="color:#ff4b4b;">143</a>
    </p>
""", unsafe_allow_html=True)

# Social Media Links
st.sidebar.markdown("""
    <h3 style="color:#ff4b4b; text-align:center;">Follow Us</h3>
    <p style="text-align:center; font-size:18px;">
        <a href="https://twitter.com" target="_blank" style="text-decoration:none;">
            <img src="https://s2.googleusercontent.com/s2/favicons?sz=64&domain_url=https://twitter.com" width="20"/> X (Twitter)
        </a><br>
        <a href="https://facebook.com" target="_blank" style="text-decoration:none;">
            <img src="https://s2.googleusercontent.com/s2/favicons?sz=64&domain_url=https://facebook.com" width="20"/> Facebook
        </a><br>
        <a href="https://instagram.com" target="_blank" style="text-decoration:none;">
            <img src="https://s2.googleusercontent.com/s2/favicons?sz=64&domain_url=https://instagram.com" width="20"/> Instagram
        </a>
    </p>
""", unsafe_allow_html=True)

# Disclaimer Section
st.sidebar.markdown("""
    <hr style="border:1px solid #ff4b4b; margin-top:20px; margin-bottom:20px;">
    <p style="text-align:center; font-size:13px; color:#555;">
        <strong>Disclaimer:</strong> This tool provides an estimate of your risk and should not be considered a substitute for professional medical advice. Always consult with a qualified healthcare provider for diagnosis and treatment.
    </p>
""", unsafe_allow_html=True)

# Tabbed Interface
tabs = st.tabs(
    [
        "Risk Assessment",
        "Prevention & Recommendations",
        "About the Model",
        "Heart Health Insights",
    ]
)

# Tab 1: Risk Assessment
with tabs[0]:
    st.subheader("🧑‍🦰 Personal Information")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        age = st.slider("Age", 25, 84, 50, help="How many years since you were born?")
    with col2:
        sex = st.radio("Sex", ["Male", "Female"], help="Biological sex assigned at birth", horizontal=True)

    st.subheader("🩺 Clinical Measurements")
    col3, col4 = st.columns(2, gap="large")
    with col3:
        st.markdown("*Enter a value between 80-200 mmHg*")
        blood_pressure = st.number_input(
            "Blood Pressure (mmHg)", min_value=80, max_value=200, value=None, help="Your systolic blood pressure value"
        )
    with col4:
        st.markdown("*Enter a value between 2.0-10.0 mmol/L*")
        cholesterol = st.number_input(
            "Cholesterol Level (mmol/L)", min_value=2.0, max_value=10.0, value=None,
            help="Total cholesterol level in blood"
        )

    col5, col6 = st.columns(2, gap="large")
    with col5:
        st.markdown("*Enter a value between 15.0-50.0*")
        bmi = st.number_input(
            "Body Mass Index (BMI)",
            min_value=15.0,
            max_value=50.0,
            value=None,
            help="A measure of body fat based on height and weight",
        )
    with col6:
        smoking = st.checkbox("Are you a smoker?", help="Have you ever smoked or currently smoke?")

    st.subheader("💊 Medical History")
    col7, col8 = st.columns(2, gap="large")
    with col7:
        diabetes = st.checkbox("Do you have diabetes?", help="Have you been diagnosed with diabetes?")
        atrial_fibrillation = st.checkbox("Do you have atrial fibrillation?",
                                          help="An irregular heart rhythm condition")
    with col8:
        rheumatoid_arthritis = st.checkbox(
            "Do you have rheumatoid arthritis?", help="A chronic inflammatory disorder affecting joints"
        )
        chronic_kidney_disease = st.checkbox(
            "Do you have chronic kidney disease?", help="Chronic kidney disease can affect heart health."
        )

    st.subheader("🏋️ Lifestyle Factors")
    col9, col10 = st.columns(2, gap="large")
    with col9:
        physical_activity = st.selectbox(
            "Physical Activity Level",
            ["Not Specified", "Sedentary", "Moderate", "Active"],
            help="How often do you engage in physical activity?",
        )
        diet_quality = st.selectbox(
            "Diet Quality",
            ["Not Specified", "Unhealthy", "Balanced", "Healthy"],
            help="How would you describe your diet?",
        )
    with col10:
        alcohol_consumption = st.selectbox(
            "Alcohol Consumption",
            ["Not Specified", "Never", "Occasionally", "Frequent"],
            help="How often do you consume alcohol?",
        )
        sleep_duration = st.selectbox(
            "Average Sleep Duration",
            ["Not Specified", "Less than 6 hours", "6-8 hours", "More than 8 hours"],
            help="Sleep duration can impact heart health.",
        )
        st.info(
            "Note: Fields marked as optional or 'Not Specified' will use default values in the risk calculation. For more accurate results, fill in as many fields as possible."
        )

    st.subheader("🔬 Additional Risk Factors")
    col11, col12 = st.columns(2, gap="large")
    with col11:
        family_history = st.checkbox(
            "Do you have a family history of heart disease?",
            help="Has a close family member been diagnosed with heart disease?",
        )
        mental_health = st.checkbox(
            "Do you have a history of mental health conditions?", help="Such as anxiety or depression."
        )
    with col12:
        migraine_history = st.checkbox(
            "Have you had migraines?", help="Migraine history may be linked to cardiovascular risk."
        )

    # Add spacing before the button
    st.write("")
    st.write("")

    # Center the button using columns
    left_col, center_col, right_col = st.columns([1, 2, 1])
    with center_col:
        calculate_button = st.button(
            "Calculate Risk",  # Removed emojis for professionalism
            type="primary",
            use_container_width=True,
            key="calculate_button",
        )

    # Custom CSS for Button Styling (Unchanged Logic)
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 12px;
            padding: 12px 20px;
            font-weight: bold;
            font-size: 16px;
            transition: all 0.3s ease-in-out;
        }
        div[data-testid="stButton"] button:hover {
            background-color: #e63939;
            transform: scale(1.05);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if calculate_button:
        risk, risk_factors = calculate_qrisk3(age, sex, smoking, diabetes, blood_pressure, cholesterol, bmi,
                                              atrial_fibrillation, rheumatoid_arthritis, physical_activity,
                                              diet_quality,
                                              alcohol_consumption, family_history, mental_health,
                                              sleep_duration, chronic_kidney_disease, migraine_history)
        st.markdown(f"## Your estimated 10-year risk: **{risk}%**")

        # Save the results to session state for use in other tabs
        st.session_state.risk = risk
        st.session_state.risk_factors = risk_factors
        st.session_state.has_results = True

        # Gauge Chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk,
            title={"text": "Heart Disease Risk"},
            gauge={"axis": {"range": [0, 100]},
                   "bar": {"color": "pink"},
                   "steps": [
                       {"range": [0, 20], "color": "green"},
                       {"range": [20, 40], "color": "yellow"},
                       {"range": [40, 60], "color": "orange"},
                       {"range": [60, 80], "color": "red"},
                       {"range": [80, 100], "color": "blue"}
                   ]}
        ))
        st.plotly_chart(fig)

        st.markdown("""
                ### Understanding Your Risk Score

                This gauge visualization represents your 10-year cardiovascular risk score, which estimates the probability of developing cardiovascular disease (CVD) within the next decade. The colors indicate different risk levels:

                - 🟢 **Green (0-20%)**: Very Low Risk - Excellent cardiovascular health
                - 🟡 **Yellow (20-40%)**: Low-Moderate Risk - Some room for improvement
                - 🟠 **Orange (40-60%)**: Moderate Risk - Active attention needed
                - 🔴 **Red (60-80%)**: High Risk - Immediate action recommended
                - 🔵 **Blue (80-100%)**: Very High Risk - Urgent medical attention required

                *Source: Based on risk categorization guidelines from the American College of Cardiology/American Heart Association.*
                """)

        # Risk breakdown chart
        st.markdown("### Risk Contribution Breakdown")
        factor_names = list(risk_factors.keys())
        factor_values = list(risk_factors.values())

        # Sort factors by their values in descending order
        sorted_indices = np.argsort(factor_values)[::-1]
        sorted_names = [factor_names[i] for i in sorted_indices]
        sorted_values = [factor_values[i] for i in sorted_indices]

        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(sorted_names, sorted_values, color='skyblue')

        # Add values at the end of each bar
        for i, bar in enumerate(bars):
            ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                    f'{sorted_values[i]:.1f}x',
                    va='center', fontsize=8)

        ax.set_xlabel("Risk Multiplier")
        ax.set_title("How Each Factor Contributes to Your Risk Score")
        plt.tight_layout()
        st.pyplot(fig)

        # Add risk factors explanation here
        st.markdown("""
                ### Understanding Your Risk Factors

                The chart above shows how different factors contribute to your overall cardiovascular risk. Each bar represents a risk multiplier, where:
                - 1.0x = Neutral impact
                - ->1.0x = Increases risk
                - The longer the bar, the stronger the impact

                #### Key Points About Cardiovascular Risk:

                1. **Modifiable vs. Non-Modifiable Factors**
                   - 🔄 **Modifiable**: Blood pressure, cholesterol, smoking, physical activity, diet, and weight
                   - ⚓ **Non-Modifiable**: Age, sex, and family history

                2. **Risk Factor Interactions**
                   Multiple risk factors can compound each other, creating a higher overall risk than any single factor alone.

                3. **Prevention Strategies**
                   Research shows that up to 80% of premature heart disease and stroke can be prevented through lifestyle changes.

                #### Clinical Perspective

                According to the World Health Organization and recent clinical studies:
                - Cardiovascular disease remains the leading cause of death globally
                - Early risk assessment and intervention can significantly improve outcomes
                - Regular monitoring of risk factors is essential for prevention

                *Sources: World Health Organization (WHO), American Heart Association (AHA), European Society of Cardiology (ESC)*

                #### Next Steps
                - 📋 Save or print your risk assessment
                - 👨‍⚕️ Discuss results with your healthcare provider
                - 📅 Schedule regular check-ups
                - 📝 Create an action plan for modifiable risk factors

                ---
                **Disclaimer**: This risk assessment tool provides estimates based on general population data and should not replace professional medical advice. Always consult with healthcare providers for personal medical decisions.
                """)

with tabs[1]:
    st.markdown("### Prevention & Personalized Recommendations")

    if 'has_results' not in st.session_state or not st.session_state.has_results:
        st.info("Please complete the Risk Assessment tab first to get personalized recommendations.")
    else:
        risk = st.session_state.risk
        risk_factors = st.session_state.risk_factors

        # Risk category
        if risk < 20:
            risk_category = "Very Low"
            category_color = "green"
            category_description = "Your cardiovascular health appears to be in excellent condition. Your current lifestyle and health factors indicate a very low risk of developing cardiovascular disease in the next 10 years."
        elif risk < 40:
            risk_category = "Low-Moderate"
            category_color = "yellow"
            category_description = "While your risk is still relatively low, there may be some areas for improvement. Consider making minor lifestyle adjustments to further reduce your risk of cardiovascular disease."
        elif risk < 60:
            risk_category = "Moderate"
            category_color = "orange"
            category_description = "You have a moderate risk of developing cardiovascular disease. It's recommended to review your lifestyle habits and consult with a healthcare provider about potential preventive measures."
        elif risk < 80:
            risk_category = "High"
            category_color = "red"
            category_description = "Your risk factors indicate a high likelihood of cardiovascular disease. It's strongly advised to consult with a healthcare provider and make significant lifestyle changes to reduce your risk."
        else:
            risk_category = "Very High"
            category_color = "blue"
            category_description = "You are in the highest risk category for cardiovascular disease. Immediate consultation with a healthcare provider is essential. A comprehensive health management plan should be developed to address your risk factors."

        # Display risk category (note this should NOT be inside the else block)
        st.markdown(
            f"### Your Risk Category: <span style='color:{category_color};font-weight:bold'>{risk_category} Risk ({risk}%)</span>",
            unsafe_allow_html=True)
        st.markdown(category_description)

        # Get personalized recommendations
        recommendations = get_recommendations(risk_factors)

        # Display recommendations
        st.markdown("## Your Personalized Action Plan")
        st.markdown("Based on your risk factors, here are specific recommendations to improve your heart health:")

        # Create tabs for each recommendation
        rec_tabs = st.tabs(list(recommendations.keys()))

        for i, (key, rec) in enumerate(recommendations.items()):
            with rec_tabs[i]:
                st.markdown(f"### {rec['title']}")
                st.markdown(f"**Potential Impact**: {rec['impact']}")
                st.markdown("#### 🎯 Action Steps:")
                for j, tip in enumerate(rec['tips'], 1):
                    st.markdown(f"{j}. {tip}")

        # Overall recommendations
        st.markdown("---")
        st.markdown("### General Recommendations for Heart Health")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📋 Regular Monitoring")
            st.markdown("""
            - Check blood pressure at least once a year
            - Have cholesterol tested every 4-6 years
            - Regular diabetes screening
            - Annual physical examination
            """)

            st.markdown("#### 🧠 Mental Well-being")
            st.markdown("""
            - Practice stress management techniques
            - Seek support for mental health concerns
            - Maintain social connections
            - Get adequate sleep
            """)

        with col2:
            st.markdown("#### 🥗 Heart-Healthy Lifestyle")
            st.markdown("""
            - Balanced diet rich in fruits, vegetables, and whole grains
            - Regular physical activity (150+ minutes per week)
            - Maintain healthy weight
            - Avoid tobacco and excessive alcohol
            """)

            st.markdown("#### ⚕️ Medical Considerations")
            st.markdown("""
            - Take medications as prescribed
            - Discuss aspirin therapy with your doctor if appropriate
            - Know your family history
            - Understand symptoms of heart disease and when to seek help
            """)

        # Doctor discussion guide
        st.markdown("---")
        st.markdown("### 🏥 Discussion Guide for Your Next Doctor Visit")
        st.markdown("""
        Print this section or take notes to help guide your conversation with your healthcare provider:
        
        1. My calculated 10-year cardiovascular risk is **{}%** ({}risk)
        2. My most significant risk factors are:
            {}
        3. Questions to ask my doctor:
            - Would I benefit from medication to lower my risk?
            - How often should I have my blood pressure/cholesterol checked?
            - What lifestyle changes would be most beneficial for my specific situation?
            - Are there any specialized tests I should consider?
            - How does my family history affect my risk?
        """.format(
            risk,
            risk_category.lower() + " ",
            "\n            ".join([f"- {factor}" for factor, value in sorted(risk_factors.items(), key=lambda x: x[1], reverse=True)[:3] if value > 1.0])
        ))

        # Download options
        st.markdown("---")

        # Create a downloadable PDF (simulated with markdown)
        recommendations_text = "\n".join([f"- {rec['title']}: {rec['impact']}" for rec in recommendations.values()])
        report_md = f"""
        # Heart Health Report
        
        ## Risk Assessment
        - 10-Year Risk: {risk}% ({risk_category})
        - Top Risk Factors: {', '.join([factor for factor, value in sorted(risk_factors.items(), key=lambda x: x[1], reverse=True)[:3] if value > 1.0])}
        
        ## Recommendations
        {recommendations_text}
        
        Generated on {pd.Timestamp.now().strftime('%Y-%m-%d')}
        """

        st.download_button(
            label="Download Your Heart Health Report",
            data=report_md,
            file_name="heart_health_report.md",
            mime="text/markdown"
        )

with tabs[2]:
    st.markdown("### About the Model")

    # Introduction to the model
    st.markdown("""
    This application utilizes the QRISK3 risk prediction model, a clinically validated tool designed to estimate an individual’s 10-year risk of cardiovascular disease. Built using the Cox proportional hazards regression algorithm, QRISK3 was developed by researchers at the University of Nottingham and has been externally validated across multiple populations, ensuring its accuracy and reliability in assessing heart disease risk.
    """)

    # Add tabs within this tab for organized information
    model_tabs = st.tabs(["How It Works", "References"])

    with model_tabs[0]:
        st.markdown("""
         ## The QRISK3 Model
         The QRISK3 model uses the Cox proportional hazards regression algorithm to estimate your 10-year risk of developing cardiovascular disease, considering various health and lifestyle factors

         ### 📊 Development & Validation
         * 📑 Built using data from over 10.5 million patients in the UK
         * 🏥 Includes 693,000 recorded cardiovascular events
         * ✅ Clinically validated across diverse populations

         ### How Your Risk is Calculated
         **1️⃣ Collecting Personal Health Data**  
         Includes key risk factors such as age, blood pressure, cholesterol levels, and medical history.

         **2️⃣ Applying Statistical Weights**  
         Uses population-based risk models to assess the impact of each factor.

         **3️⃣ Calculating Your Risk**  
         Provides a percentage estimate of your likelihood of experiencing a cardiovascular event within 10 years.
         """)

        # Add the visualization here, inside the "How It Works" tab
        def create_risk_factors_tree():
            fig = go.Figure()

            # Define the center point and radius
            center_x, center_y = 0.5, 0.5
            radius = 0.35

            # Define main categories and their factors
            categories = {
                'Demographic\nFactors': ['Age', 'Sex'],
                'Clinical\nMeasurements': ['Blood Pressure', 'Cholesterol Ratio', 'BMI'],
                'Pre-existing\nConditions': ['Diabetes', 'Atrial Fibrillation', 'Kidney Disease'],
                'Other Medical\nConditions': ['Rheumatoid Arthritis', 'Mental Illness', 'Migraine'],
                'Lifestyle &\nHistory': ['Smoking', 'Family History', 'Medications']
            }

            # Calculate positions for main categories
            import math
            n_categories = len(categories)
            angles = [2 * math.pi * i / n_categories - math.pi / 2 for i in range(n_categories)]

            # Add central node
            fig.add_trace(go.Scatter(
                x=[center_x],
                y=[center_y],
                mode='markers+text',
                text=['QRISK3\nFactors'],
                textposition='middle center',
                textfont=dict(color='#000000'),
                marker=dict(size=60, color='#2E86C1'),  # Original size
                name='Central'
            ))

            # Add categories and their factors
            colors = ['#3498DB', '#E74C3C', '#2ECC71', '#F1C40F', '#9B59B6']

            for i, (category, factors) in enumerate(categories.items()):
                # Calculate category position
                cat_x = center_x + radius * math.cos(angles[i])
                cat_y = center_y + radius * math.sin(angles[i])

                # Add category node
                fig.add_trace(go.Scatter(
                    x=[cat_x],
                    y=[cat_y],
                    mode='markers+text',
                    text=[category],
                    textposition='middle center',
                    textfont=dict(color='#000000'),
                    marker=dict(size=45, color=colors[i]),  # Original size
                    name=category
                ))

                # Add line from center to category
                fig.add_trace(go.Scatter(
                    x=[center_x, cat_x],
                    y=[center_y, cat_y],
                    mode='lines',
                    line=dict(color=colors[i], width=2),
                    showlegend=False
                ))

            # Update layout
            fig.update_layout(
                showlegend=False,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
                plot_bgcolor='white',
                title=dict(
                    text='QRISK3 Risk Factor Categories',
                    x=0.5,
                    y=0.95,
                    xanchor='center',
                    yanchor='top',
                    font=dict(size=24, color='#000000')  # Original size
                ),
                height=450,  # Only changed the overall height
                margin=dict(l=20, r=20, t=80, b=20)
            )

            return fig

    # Display the content with the visualization
    st.markdown("#### Factors Considered in QRISK3")
    st.plotly_chart(create_risk_factors_tree(), use_container_width=True)

    # Create two columns for factors
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            **Demographic Factors:**
            - Age
            - Sex

            **Clinical Measurements:**
            - Systolic blood pressure
            - Total cholesterol to HDL ratio
            - Body Mass Index (BMI)

            **Pre-existing Conditions:**
            - Diabetes
            - Atrial fibrillation
            - Chronic kidney disease
            """)

    with col2:
        st.markdown("""
            **Other Medical Conditions:**
            - Rheumatoid arthritis
            - Severe mental illness
            - Migraine 

            **Medications:**
            - Corticosteroid use

            **Family History:**
            - Angina or heart attack in a 1st degree relative < 60

            **Lifestyle:**
            - Smoking status
            """)

    st.markdown("#### ⚠️ Limitations of the Model")
    st.markdown("""
                While QRISK3 is a powerful predictive tool, it's important to understand its limitations:

                - **Age Range**: Validated for adults aged 25-84
                - **Prediction Window**: Focuses on 10-year risk, not lifetime risk
                - **Limited Lifestyle Factors**: Does not include detailed information about diet, exercise, or stress levels
                - **Individual Variations**: Cannot account for all unique genetic and environmental factors
                - **Not a Diagnostic Tool**: Predicts risk but does not diagnose current heart disease

                Always consult with healthcare professionals for personalized medical advice and interpretation of your results.
                """)

with model_tabs[1]:
    st.markdown("#### References and Further Reading")

    # Original QRISK3 Publication
    st.markdown("""
    **Original QRISK3 Publication:**  
    Hippisley-Cox J, Coupland C, Brindle P. Development and validation of QRISK3 risk prediction algorithms to estimate future risk of cardiovascular disease: prospective cohort study. *BMJ* 2017;357:j2099.
    """)

    # Additional Resources List
    st.markdown("""
    **Additional Resources:**
    
    1. [Official QRISK3 Website](https://qrisk.org/three/)  
    2. [British Cardiovascular Society Guidelines](https://www.britishcardiovascularsociety.org/)  
    3. [American Heart Association Risk Assessment Guidelines](https://www.heart.org/en/health-topics/consumer-healthcare/what-is-cardiovascular-disease/coronary-artery-disease/coronary-artery-disease-risk-assessment)  
    4. [European Society of Cardiology Risk Assessment Tools](https://www.escardio.org/Education/Practice-Tools/CVD-prevention-toolbox/SCORE-Risk-Charts)  
    """)

    # More Related References Section
    st.markdown("""
    **Related Research and Guidelines:**
    
    - **NICE Cardiovascular Disease Prevention Guidelines**:  
      Recommendations by the National Institute for Health and Care Excellence (NICE) for assessing and reducing cardiovascular risk.  
      [Read the Guidelines](https://www.nice.org.uk/guidance/cg181)

    - **World Health Organization (WHO) Global Health Estimates**:  
      Provides global statistics and insights on cardiovascular disease prevalence and mortality rates.  
      [WHO Website](https://www.who.int/news-room/fact-sheets/detail/cardiovascular-diseases-(cvds))

    - **Framingham Heart Study**:  
      A ground-breaking longitudinal study providing key insights into cardiovascular risk factors.  
      [Explore the Study](https://www.framinghamheartstudy.org/)

    - **CDC - Heart Disease Facts**:  
      Statistics and detailed information on cardiovascular disease in the U.S. from the Centers for Disease Control and Prevention.  
      [Visit CDC Website](https://www.cdc.gov/heartdisease/facts.htm)
    """)

    # Add a divider for separation before dataset details
    st.divider()

    # Dataset Reference Section
    st.subheader("Dataset Reference")

    # Dataset Description
    st.markdown("""
    This heart disease risk assessment system is built on data from the **Behavioral Risk Factor 
    Surveillance System (BRFSS) 2015**, a comprehensive health survey conducted by the CDC. 
    This nationally representative dataset provides insights into various health indicators 
    and heart disease status across diverse populations in the United States.
    """)

    # Dataset Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Sample Size",
            value=f"{heart_disease_data.shape[0]:,}",
            help="Number of individual health records analyzed"
        )
    with col2:
        st.metric(
            label="Features",
            value=f"{heart_disease_data.shape[1]}",
            help="Health indicators and demographic factors assessed"
        )
    with col3:
        st.metric(
            label="Year",
            value="2015",
            help="Year the BRFSS survey data was collected"
        )

    # Expandable Sections for Dataset Details
    with st.expander("Dataset Features"):
        features = list(heart_disease_data.columns)
        num_cols = 3
        feature_cols = st.columns(num_cols)
        for i, feature in enumerate(features):
            formatted_feature = " ".join(word.capitalize() for word in feature.split('_'))
            feature_cols[i % num_cols].markdown(f"• {formatted_feature}")

    with st.expander("Data Quality Information"):
        st.markdown("""
        - **Completeness**: The dataset underwent thorough cleaning to handle missing values
        - **Validation**: Data quality checks were performed to ensure consistency
        - **Preprocessing**: Features were normalized and encoded for optimal model performance
        - **Balancing**: Class imbalance was addressed to ensure equitable predictions
        """)

        # Visual separator
        st.markdown("---")

with tabs[3]:
    st.markdown("### Heart Health Insights")

    # Create subtabs for different insights
    insight_tabs = st.tabs(["Heart Disease Facts", "Risk Trends & Analysis"])

    with insight_tabs[0]:
        st.markdown("## Key Facts About Heart Disease")

        # Statistics section
        st.markdown("### Global Statistics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 17.9 Million")
            st.markdown("Annual deaths worldwide from cardiovascular disease")

        with col2:
            st.markdown("#### #1 Cause")
            st.markdown("Leading cause of death globally")

        with col3:
            st.markdown("#### 80%")
            st.markdown("Of premature heart disease is preventable")

        # Risk factors visualization
        st.markdown("### Major Risk Factors")

        risk_data = {
            'Factor': ['Smoking', 'High Blood Pressure', 'Diabetes', 'Obesity', 'Physical Inactivity', 'Poor Diet'],
            'Relative Risk': [2.5, 2.0, 1.8, 1.6, 1.5, 1.7]

        }

        df_risk = pd.DataFrame(risk_data)

        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(df_risk['Factor'], df_risk['Relative Risk'], color='#ff9999')

        for i, bar in enumerate(bars):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{df_risk["Relative Risk"][i]}x',
                    ha='center', fontsize=9)

        ax.set_ylabel('Relative Risk Increase')
        ax.set_title('Impact of Major Risk Factors on Heart Disease')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

        # Add the detailed explanation below the visualization
        st.markdown("## Key Risk Factors and Their Impact")

        # Create two columns
        col1, col2 = st.columns(2)

        # Content for the first column (Factors 1-3)
        with col1:
            st.markdown("""
            ### 1. Smoking 
            Smoking is one of the most dangerous lifestyle habits, significantly increasing the risk of heart disease. It damages blood vessels, raises blood pressure, and contributes to plaque buildup in arteries, leading to conditions like heart attacks and strokes.

            ### 2. High Blood Pressure 
            Often referred to as the "silent killer," high blood pressure (hypertension) forces the heart to work harder, leading to artery damage and a greater risk of heart disease. Managing blood pressure through lifestyle changes and medication can drastically lower risk.

            ### 3. Diabetes
            Diabetes, especially when uncontrolled, damages blood vessels and nerves that control the heart. High blood sugar levels contribute to inflammation and atherosclerosis (artery narrowing), increasing the likelihood of heart complications.
            """)

        # Content for the second column (Factors 4-6)
        with col2:
            st.markdown("""
            ### 4. Obesity 
            Excess weight puts additional strain on the heart, raises cholesterol levels, and increases the likelihood of hypertension and diabetes. A healthy diet and regular exercise can significantly lower the risks associated with obesity.

            ### 5. Physical Inactivity 
            A sedentary lifestyle weakens the cardiovascular system, leading to poor circulation, higher cholesterol levels, and weight gain. Regular exercise strengthens the heart, improves circulation, and helps maintain overall heart health.

            ### 6. Poor Diet
            Diets high in processed foods, sugar, and unhealthy fats contribute to obesity, high cholesterol, and inflammation—all of which are major contributors to heart disease. Opting for whole foods, lean proteins, and heart-healthy fats can significantly reduce risk.
            """)

        # Heart disease types
        st.markdown("### Types of Heart Disease")

        types_data = {
            'Type': ['Coronary Artery Disease', 'Heart Failure', 'Arrhythmias', 'Valve Disease', 'Congenital Heart Disease'],
            'Prevalence': [42, 23, 15, 12, 8]
        }

        df_types = pd.DataFrame(types_data)

        fig = plt.figure(figsize=(10, 6))
        plt.pie(df_types['Prevalence'], labels=df_types['Type'], autopct='%1.1f%%',
                startangle=90, shadow=True, explode=[0.1, 0, 0, 0, 0],
                colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
        plt.axis('equal')
        plt.title('Distribution of Heart Disease Types')
        plt.tight_layout()
        st.pyplot(fig)

        # Symptoms and warning signs
        st.markdown("### Warning Signs")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Common Warning Signs")
            st.markdown("""
            - Chest pain or discomfort
            - Shortness of breath
            - Pain or discomfort in arms, back, neck, jaw or stomach
            - Breaking out in a cold sweat
            - Nausea or lightheadedness
            """)

            st.warning("**Know the signs of a heart attack and seek immediate medical attention if you experience these symptoms.**")

        with col2:
            st.markdown("#### Signs in Women vs. Men")
            st.markdown("""
            **Women may experience:**
            - Back or jaw pain
            - Nausea and vomiting
            - Shortness of breath without chest pain
            - Unusual fatigue
            
            **Men more commonly report:**
            - Crushing chest pain
            - Pain radiating to left arm
            - Breaking out in cold sweat
            """)

    with insight_tabs[1]:
        st.markdown("## Risk Trends & Analysis")

        # Age vs. Risk chart
        st.markdown("### Heart Disease Risk by Age")

        age_data = {
            'Age': [30, 40, 50, 60, 70, 80],
            'Men': [3, 8, 15, 25, 35, 42],
            'Women': [1.5, 4, 8, 15, 25, 35]
        }

        df_age = pd.DataFrame(age_data)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df_age['Age'], df_age['Men'], marker='o', linewidth=2, label='Men')
        ax.plot(df_age['Age'], df_age['Women'], marker='o', linewidth=2, label='Women')
        ax.set_xlabel('Age')
        ax.set_ylabel('Risk Percentage (%)')
        ax.set_title('10-Year Heart Disease Risk by Age and Sex')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)

        # Add Key Observations and Analysis below the chart
        st.markdown("""
            ## Key Observations
            📌 **Heart disease risk increases with age** – Both men and women see a steady rise in heart disease risk as they grow older.

            📌 **Men have a higher risk than women at every age** – The gap is evident, with men's risk being consistently higher than women's. This aligns with medical research, which suggests that estrogen provides some cardiovascular protection for women before menopause, but the risk catches up after menopause.

            📌 **Exponential growth in risk after 50** – The risk increases gradually at younger ages but accelerates significantly after 50, especially for men. This suggests that age-related factors like high blood pressure, cholesterol buildup, and lifestyle habits play a major role.
            """)

        # Create two columns for the remaining information
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
                ## Why is Male Risk Higher?
                * **Hormonal differences** – Testosterone is linked to higher cholesterol and blood pressure levels.

                * **Lifestyle factors** – Historically, men have higher smoking rates and more exposure to certain risk factors.

                * **Genetic predisposition** – Some heart disease-related genes have been found to affect men more.
                """)

        with col2:
            st.markdown("""
                ## What This Means for Prevention
                Regardless of sex, heart disease prevention should start early:

                ✔️ **Regular check-ups** – Monitor cholesterol, blood pressure, and blood sugar.

                ✔️ **Healthy diet** – Prioritize whole foods, fiber, and healthy fats.

                ✔️ **Exercise regularly** – At least 150 minutes of moderate activity weekly.

                ✔️ **Manage stress & sleep** – Chronic stress and poor sleep are underestimated risk factors.

                ✔️ **Quit smoking & limit alcohol** – Both significantly impact heart health.
                """)


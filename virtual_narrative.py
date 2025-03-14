import streamlit as st
import base64  # For base64 encoding
import plotly.graph_objects as go  # For the gauge chart
import re  # For extracting numeric scores
from fpdf import FPDF  # For generating PDF reports
import os  # For file path handling

# ✅ Set page configuration to wide mode (MUST be the first Streamlit command)
st.set_page_config(page_title="The Virtual Narrative", page_icon="🌐", layout="wide")

# Hide Default Streamlit Elements
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ✅ Function to Extract Numeric Scores from Responses
def extract_score(response):
    """
    Extract numeric score from the selected response.
    Args:
        response (str): The response string containing a score in parentheses.
    Returns:
        int: The extracted score or 1 if no match is found.
    """
    match = re.search(r"\((\d+)\)", response)  # Look for a number inside parentheses
    return int(match.group(1)) if match else 1  # Default to 1 if no match

# ✅ Function to Create Gauge Chart
def create_gauge_chart(score):
    """
    Create a gauge chart for the data maturity score.
    Args:
        score (float): The data maturity score (between 1 and 5).
    Returns:
        plotly.graph_objects.Figure: The gauge chart figure.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        title={'text': "Your Data Maturity Score", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 5]},
            'bar': {'color': "orange"},
            'steps': [
                {'range': [0, 1.5], 'color': "red"},
                {'range': [1.5, 2.5], 'color': "orange"},
                {'range': [2.5, 3.5], 'color': "yellow"},
                {'range': [3.5, 4.5], 'color': "green"},
                {'range': [4.5, 5], 'color': "blue"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(width=500, height=300)
    return fig

# ✅ Initialize Session State Variables (Only Once)
session_defaults = {
    "start_assessment": False,
    "data_privacy_accepted": False,
    "user_info_complete": False,
    "dynamic_weights_set": False,  # Track if dynamic weights are set
    "data_governance_complete": False,
    "data_quality_complete": False,
    "metadata_management_complete": False,
    "data_integration_complete": False,
    "data_analytics_complete": False,
    "data_security_complete": False,
    "all_sections_completed": False,
    "weights": {  # Default weights (will be updated dynamically)
        "Data Governance": 0.20,
        "Data Quality": 0.20,
        "Metadata Management": 0.15,
        "Data Integration": 0.15,
        "Data Analytics & AI": 0.15,
        "Data Security & Privacy": 0.15
    },
    "gov_q1_response": " (1)", "gov_q2_response": " (1)", "gov_q3_response": " (1)",
    "dq1_response": " (1)", "dq2_response": " (1)", "dq3_response": " (1)",
    "mm1_response": " (1)", "mm2_response": " (1)", "mm3_response": " (1)",
    "di1_response": " (1)", "di2_response": " (1)", "di3_response": " (1)",
    "ai1_response": " (1)", "ai2_response": " (1)", "ai3_response": " (1)",
    "sp1_response": " (1)", "sp2_response": " (1)", "sp3_response": " (1)",
    "current_question": 1  # Track the current question in a section
}

# Initialize session state variables if they don't exist
for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ✅ Open the image file and encode it as base64
with open("logo.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# ✅ Add centered content using markdown (with background color)
st.markdown(
    f"""
    <style>
    .top-page {{
        background-color: #1e2a47;  /* Set background color */
        padding: 50px;
        text-align: center;
        color: white;  /* Changed text color to white for better contrast */
        position: relative;
    }}
    .top-page h1 {{
        font-size: 36px;
    }}
    .top-page p {{
        font-size: 18px;
    }}
    .center-button {{
        display: flex;
        justify-content: center;
        margin-top: 20px;  /* Add some space above the button */
    }}
    .stButton button {{
        background-color: #FFA500;  /* Orange background */
        color: white;  /* White text */
        font-size: 20px;
        padding: 15px 30px;
        border-radius: 5px;
        cursor: pointer;
        border: none;
    }}
    .stButton button:hover {{
        background-color: #ff8c00;  /* Darker orange on hover */
    }}
    .next-button button {{
        background-color: #0047AB;  /* Dark blue background */
        color: white;  /* White text */
        font-size: 20px;
        padding: 15px 30px;
        border-radius: 5px;
        cursor: pointer;
        border: none;
    }}
    .next-button button:hover {{
        background-color: #003366;  /* Darker blue on hover */
    }}
    </style>
    <div class="top-page">
        <img src="data:image/png;base64,{encoded_image}" width="250" style="display:block; margin-left:auto; margin-right:auto;">
        <h1>Welcome to The Virtual Narrative</h1>
        <p>Complete this Data Maturity Assessment to understand your organization's data maturity level.<br>
        Grab a cup of coffee ☕, pull up a chair, and let's dive into the world of data management!</p>
        <p>⏳ Takes 7+ minutes</p>
        <div class="center-button">
            <!-- Streamlit button will be injected here -->
        </div>
    </div>
    """, unsafe_allow_html=True
)

# ✅ Add the Streamlit button inside the centered div
st.markdown('<div class="center-button">', unsafe_allow_html=True)
if st.button("Let's do this!", key="start_button"):
    st.session_state.start_assessment = True
    st.session_state.data_privacy_accepted = False  # Set this flag to False when starting
    st.success("Great! Let's begin your Data Maturity Assessment, but first a word on Data Privacy and protection.")
st.markdown('</div>', unsafe_allow_html=True)

# ✅ Data Privacy & Protection Page (Page 2)
if st.session_state.start_assessment and not st.session_state.data_privacy_accepted:
    st.write("## Data Privacy & Protection")
    st.markdown("""
        We take your Data Privacy seriously. 
        The data you share with us will be treated as though it were our own. We will use this information 
        solely to provide you with a bespoke report with actionable insights into your current state of 
        Data Maturity, alongside suggestions on how you can improve. Over time, we will compile research 
        findings for industries and regions, but these will be completely anonymized. 
        <a href="#privacy-policy" style="color: orange; text-decoration: underline;" onclick="togglePrivacyPolicy()">Read our full Privacy Policy below</a>.
    """, unsafe_allow_html=True)

    # Add a placeholder for the privacy policy section
    st.markdown("<a name='privacy-policy'></a>", unsafe_allow_html=True)

    # Use st.expander to hide the privacy policy by default
    with st.expander("📜 Privacy Policy", expanded=False):
        try:
            # Get the absolute path to the file
            file_path = os.path.join(os.path.dirname(__file__), "privacy_policy.txt")
            with open(file_path, "r") as file:
                privacy_policy_content = file.read()
            st.markdown(privacy_policy_content, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("Privacy Policy file not found. Please ensure 'privacy_policy.txt' is in the correct directory.")

    # Add JavaScript to toggle the expander when the link is clicked
    st.markdown("""
        <script>
        function togglePrivacyPolicy() {
            const expander = document.querySelector('.stExpander');
            if (expander) {
                const button = expander.querySelector('button');
                if (button) {
                    button.click(); // Simulate a click on the expander button
                }
            }
        }
        </script>
    """, unsafe_allow_html=True)

    if st.button("Continue"):
        st.session_state.data_privacy_accepted = True  # Proceed to next section when the button is clicked
        st.success("Alright, Lets get started! 😎 Just a couple of quick details so we can personalize your experience.")

# ✅ User Information Collection Page (Page 3)
if st.session_state.data_privacy_accepted and not st.session_state.user_info_complete:
    st.write("### 📝 Let's get started by knowing you!")
    
    # Use temporary variables to store user inputs
    first_name = st.text_input("Enter your First Name:", key="user_first_name_input")
    last_name = st.text_input("Enter your Last Name:", key="user_last_name_input")
    email = st.text_input("Enter your Email Address:", key="user_email_input")
    org_name = st.text_input("Enter your Organization Name:", key="user_org_name_input")
    business_unit = st.text_input("Which Business Unit do you work in?", key="user_business_unit_input")

    if st.button("Start Assessment"):
        if not first_name or not last_name or not email:
            st.error("⚠️ Please fill in all required fields!")
        else:
            # Store user information in session state (using separate keys)
            st.session_state.user_first_name = first_name
            st.session_state.user_last_name = last_name
            st.session_state.user_email = email
            st.session_state.user_org_name = org_name
            st.session_state.user_business_unit = business_unit

            st.session_state.user_info_complete = True
            st.success(f"Thanks, {first_name}! Nice to meet you!. Let's make this assessment even more personalized 🔥. How important are each of these data practices to your organization? 🤔")

# ✅ Dynamic Weighting Section
if st.session_state.user_info_complete and not st.session_state.dynamic_weights_set:
    st.write("## ⚖️ Weighting Your Priorities")
    st.write("On a scale of 0-5 (ascending priority), relative to the others, how do you prioritize the following **six pillars of data maturity** to your organization: **1) Governance, 2) Quality, 3) Metadata, 4) Integration, 5) Analytics, and 6) Security?**")
    st.write("**0 = Not Important | 5 = Extremely Important**")

    # Define the questions and their options
    questions = [
        {
            "question": "1️⃣ How important is it for your organization to have clear <span style='text-decoration: underline dotted;'>data governance</span> policies, including ownership and accountability?",
            "options": ["Not Important (1)", "Slightly Important (2)", "Moderately Important (3)", "Very Important (4)", "Extremely Important (5)"]
        },
        {
            "question": "2️⃣ How critical is <span style='text-decoration: underline dotted;'>data quality</span>—ensuring accuracy and completeness—for your organization's decision-making?",
            "options": ["Not Critical (1)", "Slightly Critical (2)", "Moderately Critical (3)", "Very Critical (4)", "Extremely Critical (5)"]
        },
        {
            "question": "3️⃣ How important is <span style='text-decoration: underline dotted;'>metadata management</span>, such as maintaining a centralized metadata repository, for your organization?",
            "options": ["Not Important (1)", "Slightly Important (2)", "Moderately Important (3)", "Very Important (4)", "Extremely Important (5)"]
        },
        {
            "question": "4️⃣ How important is <span style='text-decoration: underline dotted;'>data integration</span>, ensuring seamless connectivity across different systems, for your organization?",
            "options": ["Not Important (1)", "Slightly Important (2)", "Moderately Important (3)", "Very Important (4)", "Extremely Important (5)"]
        },
        {
            "question": "5️⃣ How important is leveraging <span style='text-decoration: underline dotted;'>data analytics and AI</span> for decision-making in your organization?",
            "options": ["Not Important (1)", "Slightly Important (2)", "Moderately Important (3)", "Very Important (4)", "Extremely Important (5)"]
        },
        {
            "question": "6️⃣ How important is <span style='text-decoration: underline dotted;'>data security</span>, including compliance with regulations, for your organization?",
            "options": ["Not Important (1)", "Slightly Important (2)", "Moderately Important (3)", "Very Important (4)", "Extremely Important (5)"]
        }
    ]

    # Track the current question
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0

    # Display the current question
    current_question = questions[st.session_state.current_question_index]
    st.write(f"### {current_question['question']}", unsafe_allow_html=True)  # Enable HTML rendering
    response = st.radio("Select your response:", current_question["options"], key=f"q{st.session_state.current_question_index}")

    # Add buttons for navigation
    button_container = st.container()  # Use a container for buttons

    with button_container:
        # Next button (only show if not on the last question)
        if st.session_state.current_question_index < len(questions) - 1:
            if st.button("Next ➡️", key=f"next_{st.session_state.current_question_index}", help="Move to the next question"):
                # Save the response
                st.session_state[f"q{st.session_state.current_question_index}_response"] = response
                st.session_state.current_question_index += 1
                st.rerun()  # Force a rerun to update the question
        else:
            if st.button("Submit", key="submit_dynamic_weighting", help="Submit your responses"):
                # Save the response
                st.session_state[f"q{st.session_state.current_question_index}_response"] = response

                # Extract scores from responses
                scores = []
                for i in range(len(questions)):
                    response = st.session_state.get(f"q{i}_response", " (1)")
                    score = extract_score(response)
                    scores.append(score)

                # Calculate total score
                total_score = sum(scores)

                # Assign weights
                st.session_state.weights = {
                    "Data Governance": scores[0] / total_score,
                    "Data Quality": scores[1] / total_score,
                    "Metadata Management": scores[2] / total_score,
                    "Data Integration": scores[3] / total_score,
                    "Data Analytics & AI": scores[4] / total_score,
                    "Data Security & Privacy": scores[5] / total_score
                }

                st.session_state.dynamic_weights_set = True
                st.success(f"Awesome work, {st.session_state.user_first_name}! – Weights set!✅ You’ve made it to the Data Governance section 🔐. Lets see how well your organization is managing data ownership and accountability")

# ✅ Track Completion Progress
total_sections = 6  # Total number of assessment sections
def calculate_progress():
    completed = sum([
        st.session_state.data_governance_complete,
        st.session_state.data_quality_complete,
        st.session_state.metadata_management_complete,
        st.session_state.data_integration_complete,
        st.session_state.data_analytics_complete,
        st.session_state.data_security_complete
    ])
    return int((completed / total_sections) * 100)

# Show progress bar only after the assessment has started
if st.session_state.start_assessment:
    progress = calculate_progress()
    st.progress(progress)  # Show progress bar
    st.write(f"🟢 **Progress: {progress}% Complete**")

# 🏛️ **SECTION 1: DATA GOVERNANCE**
if st.session_state.dynamic_weights_set and not st.session_state.data_governance_complete:
    st.write("## 🏛️ Section 1: Data Governance")
    st.write(f"This section assesses how well data governance is established in your organization.")

    if st.session_state.current_question == 1:
        gov_q1 = st.radio("1️⃣ **Does your organization have a formal Data Governance policy?**",
                          ["No governance exists (1)",
                           "Some informal rules, but not enforced (2)",
                           "Formal governance in place, but not consistently followed (3)",
                           "Governance is standardized and monitored (4)",
                           "Governance is automated, AI-driven, and continuously optimized (5)"], key="gov_q1")
        
        button_container = st.container()
        with button_container:
            if st.button("Next ➡️", key="gov_q1_next", help="Move to the next question"):
                st.session_state.gov_q1_response = gov_q1
                st.session_state.current_question = 2
                st.rerun()

    elif st.session_state.current_question == 2:
        gov_q2 = st.radio("2️⃣ **Are roles and responsibilities clearly defined? (e.g., Data Stewards, Chief Data Officer)?**",
                          ["No defined roles (1)",
                           "Some responsibilities exist but unclear (2)",
                           "Defined roles exist, but accountability is weak (3)",
                           "Roles are well-defined and monitored (4)",
                           "Governance roles are optimized and continuously improved (5)"], key="gov_q2")
        
        button_container = st.container()
        with button_container:
            if st.button("Next ➡️", key="gov_q2_next", help="Move to the next question"):
                st.session_state.gov_q2_response = gov_q2
                st.session_state.current_question = 3
                st.rerun()

    elif st.session_state.current_question == 3:
        gov_q3 = st.radio("3️⃣ **How frequently is your Data Governance policy reviewed and updated?**",
                          ["Never (1)",
                           "Ad-hoc updates with no schedule (2)",
                           "Reviewed every few years (3)",
                           "Reviewed annually (4)",
                           "Continuously improved with data-driven feedback (5)"], key="gov_q3")
        
        button_container = st.container()
        with button_container:
            if st.button("Submit Governance Responses", key="gov_q3_submit", help="Submit your responses"):
                st.session_state.gov_q3_response = gov_q3
                st.session_state.data_governance_complete = True
                st.session_state.current_question = 1  # Reset for the next section
                st.success(f"Awesome work, {st.session_state.user_first_name}! – On to Data Quality! 📊 How do you ensure that your data is accurate, complete and consistent?")

# 📊 **SECTION 2: DATA QUALITY**
if st.session_state.data_governance_complete and not st.session_state.data_quality_complete:
    st.write("## 📊 Section 2: Data Quality")
    st.write(f"This section evaluates how well your organization maintains accurate, complete, and reliable data.**")

    if st.session_state.current_question == 1:
        dq1 = st.radio("1️⃣ **How does your organization ensure data accuracy?**",
                       ["No process for accuracy (1)",
                        "Basic manual checks (2)",
                        "Defined validation rules (3)",
                        "Automated quality checks (4)",
                        "AI-powered real-time monitoring (5)"], key="dq1")
        
        button_container = st.container()
        with button_container:
            if st.button("Next ➡️", key="dq1_next", help="Move to the next question"):
                st.session_state.dq1_response = dq1
                st.session_state.current_question = 2
                st.rerun()

    elif st.session_state.current_question == 2:
        dq2 = st.radio("2️⃣ **How is data completeness ensured in your organization?**",
                       ["No strategy in place (1)",
                        "Manual data entry reviews (2)",
                        "Automated missing value checks (3)",
                        "Proactive data validation (4)",
                        "Machine learning-driven data integrity (5)"], key="dq2")
        
        button_container = st.container()
        with button_container:
            if st.button("Next ➡️", key="dq2_next", help="Move to the next question"):
                st.session_state.dq2_response = dq2
                st.session_state.current_question = 3
                st.rerun()

    elif st.session_state.current_question == 3:
        dq3 = st.radio("3️⃣ **How consistently is data updated and synchronized across systems?**",
                       ["No updates, data silos exist (1)",
                        "Periodic manual updates (2)",
                        "Automated scheduled updates (3)",
                        "Real-time data sync (4)",
                        "Self-healing, AI-driven consistency (5)"], key="dq3")
        
        button_container = st.container()
        with button_container:
            if st.button("Submit Data Quality Responses", key="dq3_submit", help="Submit your responses"):
                st.session_state.dq3_response = dq3
                st.session_state.data_quality_complete = True
                st.session_state.current_question = 1  # Reset for the next section
                st.success(f"You’re on fire 🔥 {st.session_state.user_first_name}! Now let’s take a look at how your metadata is being managed and if it’s in a centralized place. 📚")

# 🏷 **SECTION 3: METADATA MANAGEMENT**
if st.session_state.data_quality_complete and not st.session_state.metadata_management_complete:
    st.write("## 🏷 Section 3: Metadata Management")
    st.write(f"This section evaluates how well your organization manages metadata, including data definitions, lineage, and classification.")

    if st.session_state.current_question == 1:
        mm1 = st.radio("1️⃣ **Does your organization maintain a centralized metadata repository?**",
                       ["No metadata repository exists (1)",
                        "Some metadata exists in scattered documentation (2)",
                        "A structured metadata catalog is available (3)",
                        "A centralized metadata repository is maintained (4)",
                        "Fully automated metadata management with AI-driven lineage tracking (5)"], key="mm1")
        
        button_container = st.container()
        with button_container:
            if st.button("Next ➡️", key="mm1_next", help="Move to the next question"):
                st.session_state.mm1_response = mm1
                st.session_state.current_question = 2
                st.rerun()

    elif st.session_state.current_question == 2:
        mm2 = st.radio("2️⃣ **How well-defined and standardized are your data definitions?**",
                       ["No definitions exist (1)",
                        "Ad-hoc definitions in some areas (2)",
                        "Standardized definitions exist but not enforced (3)",
                        "Organization-wide metadata standards are enforced (4)",
                        "AI-driven metadata governance ensures full compliance (5)"], key="mm2")
        
        button_container = st.container()
        with button_container:
            if st.button("Next ➡️", key="mm2_next", help="Move to the next question"):
                st.session_state.mm2_response = mm2
                st.session_state.current_question = 3
                st.rerun()

    elif st.session_state.current_question == 3:
        mm3 = st.radio("3️⃣ **How is data lineage tracked in your organization?**",
                       ["No lineage tracking (1)",
                        "Basic manual lineage documentation (2)",
                        "Automated lineage tracking for some systems (3)",
                        "Comprehensive automated lineage tracking (4)",
                        "AI-driven lineage tracking with real-time anomaly detection (5)"], key="mm3")
        
        button_container = st.container()
        with button_container:
            if st.button("Submit Metadata Management Responses", key="mm3_submit", help="Submit your responses"):
                st.session_state.mm3_response = mm3
                st.session_state.metadata_management_complete = True
                st.session_state.current_question = 1  # Reset for the next section
                st.success(f"That was easy, right? Great job {st.session_state.user_first_name}! Moving on to Data Integration 🔗! Is your data flowing seamlessly across systems?")

# 🔗 **SECTION 4: DATA INTEGRATION**
if st.session_state.metadata_management_complete and not st.session_state.data_integration_complete:
    st.write("## 🔗 Section 4: Data Integration")
    st.write(f"This section evaluates how well data is integrated across your organization, ensuring seamless interoperability.")

    if st.session_state.current_question == 1:
        di1 = st.radio("1️⃣ **How does your organization handle data integration between different systems?**",
                       ["No integration exists (1)",
                        "Manual data transfers (2)",
                        "Basic ETL processes in place (3)",
                        "Automated API-based data flows (4)",
                        "Real-time AI-driven integration across platforms (5)"], key="di1")
        
        button_container = st.container()
        with button_container:
            if st.button("Next ➡️", key="di1_next", help="Move to the next question"):
                st.session_state.di1_response = di1
                st.session_state.current_question = 2
                st.rerun()

    elif st.session_state.current_question == 2:
        di2 = st.radio("2️⃣ **How frequently does your organization update and synchronize data across different platforms?**",
                       ["Never (1)",
                        "Occasionally with manual intervention (2)",
                        "Automated updates on a scheduled basis (3)",
                        "Near real-time synchronization (4)",
                        "AI-driven, self-healing data synchronization (5)"], key="di2")
        
        button_container = st.container()
        with button_container:
            if st.button("Next ➡️", key="di2_next", help="Move to the next question"):
                st.session_state.di2_response = di2
                st.session_state.current_question = 3
                st.rerun()

    elif st.session_state.current_question == 3:
        di3 = st.radio("3️⃣ **Does your organization utilize cloud-based data integration platforms?**",
                       ["No cloud integration (1)",
                        "Limited use of cloud data storage (2)",
                        "Some cloud integration but no automation (3)",
                        "Fully automated cloud-based integration (4)",
                        "AI-optimized multi-cloud integration (5)"], key="di3")
        
        button_container = st.container()
        with button_container:
            if st.button("Submit Data Integration Responses", key="di3_submit", help="Submit your responses"):
                st.session_state.di3_response = di3
                st.session_state.data_integration_complete = True
                st.session_state.current_question = 1  # Reset for the next section
                st.success(f"Awesome work, {st.session_state.user_first_name}! You're almost halfway there! 🤖 Time to explore how well you're using analytics and AI to make decisions.")

# 📊 **SECTION 5: DATA ANALYTICS & AI**
if st.session_state.data_integration_complete and not st.session_state.data_analytics_complete:
    st.write("## 📊 Section 5: Data Analytics & AI")
    st.write(f"This section assesses your organization's ability to leverage data analytics and AI for decision-making.")

    if st.session_state.current_question == 1:
        ai1 = st.radio("1️⃣ **What is the level of adoption of business intelligence and reporting in your organization?**",
                       ["No formal reporting (1)",
                        "Basic manual reports with spreadsheets (2)",
                        "Automated dashboards with static reports (3)",
                        "Interactive BI tools with real-time data (4)",
                        "AI-driven predictive analytics and self-service BI (5)"], key="ai1")
        
        button_container = st.container()
        with button_container:
            if st.button("Next ➡️", key="ai1_next", help="Move to the next question"):
                st.session_state.ai1_response = ai1
                st.session_state.current_question = 2
                st.rerun()

    elif st.session_state.current_question == 2:
        ai2 = st.radio("2️⃣ **How is machine learning used in your organization?**",
                       ["Not used at all (1)",
                        "Basic experiments without production deployment (2)",
                        "Some predictive models used in decision-making (3)",
                        "Machine learning models are embedded in core processes (4)",
                        "AI-driven automation and decision intelligence across the business (5)"], key="ai2")
        
        button_container = st.container()
        with button_container:
            if st.button("Next ➡️", key="ai2_next", help="Move to the next question"):
                st.session_state.ai2_response = ai2
                st.session_state.current_question = 3
                st.rerun()

    elif st.session_state.current_question == 3:
        ai3 = st.radio("3️⃣ **How well is AI governance and ethics considered in your organization?**",
                       ["No AI governance in place (1)",
                        "Basic awareness but no formal guidelines (2)",
                        "AI policies exist but are inconsistently followed (3)",
                        "AI governance is well-defined and monitored (4)",
                        "AI ethics, bias detection, and compliance are actively managed (5)"], key="ai3")
        
        button_container = st.container()
        with button_container:
            if st.button("Submit Data Analytics & AI Responses", key="ai3_submit", help="Submit your responses"):
                st.session_state.ai3_response = ai3
                st.session_state.data_analytics_complete = True
                st.session_state.current_question = 1  # Reset for the next section
                st.success(f"You’re on fire 🔥 {st.session_state.user_first_name}! Just a few more steps! 🔒 How secure is your data? Let’s make sure everything is locked down.")

# 🔒 **SECTION 6: DATA SECURITY & PRIVACY**
if st.session_state.data_analytics_complete and not st.session_state.data_security_complete:
    st.write("## 🔒 Section 6: Data Security & Privacy")
    st.write(f"This section evaluates how well your organization ensures data security, privacy, and compliance with regulations.")

    if st.session_state.current_question == 1:
        sp1 = st.radio("1️⃣ **How is access to sensitive data controlled in your organization?**",
                       ["No access control (1)",
                        "Basic password protection (2)",
                        "Role-based access control (RBAC) in place (3)",
                        "Multi-factor authentication and encryption (4)",
                        "Zero-trust security model with continuous monitoring (5)"], key="sp1")
        
        button_container = st.container()
        with button_container:
            if st.button("Next ➡️", key="sp1_next", help="Move to the next question"):
                st.session_state.sp1_response = sp1
                st.session_state.current_question = 2
                st.rerun()

    elif st.session_state.current_question == 2:
        sp2 = st.radio("2️⃣ **Does your organization comply with data protection regulations (e.g., GDPR, HIPAA, Kenya Data Protection Act)?**",
                       ["No compliance efforts (1)",
                        "Minimal awareness, but no formal compliance (2)",
                        "Compliance policies exist but are inconsistently followed (3)",
                        "Fully compliant with regular audits (4)",
                        "Continuous compliance monitoring and automated reporting (5)"], key="sp2")
        
        button_container = st.container()
        with button_container:
            if st.button("Next ➡️", key="sp2_next", help="Move to the next question"):
                st.session_state.sp2_response = sp2
                st.session_state.current_question = 3
                st.rerun()

    elif st.session_state.current_question == 3:
        sp3 = st.radio("3️⃣ **How well does your organization handle data encryption and secure storage?**",
                       ["No encryption (1)",
                        "Basic encryption for some data (2)",
                        "Encryption used for sensitive data (3)",
                        "Industry-standard encryption applied across systems (4)",
                        "End-to-end encryption with automated security updates (5)"], key="sp3")
        
        button_container = st.container()
        with button_container:
            if st.button("Submit Data Security & Privacy Responses", key="sp3_submit", help="Submit your responses"):
                st.session_state.sp3_response = sp3
                st.session_state.data_security_complete = True
                st.session_state.current_question = 1  # Reset for the next section
                st.session_state.all_sections_completed = True  # Mark all sections as completed
                st.success(f"🎉 Congratulations, {st.session_state.user_first_name}! You've completed the assessment! Here’s how your data maturity looks:")

# ✅ Function to Generate AI-Driven Insights
def generate_ai_insights(scores):
    """Generate AI-driven insights based on the user's responses."""
    insights = []

    # Data Governance Insights
    if scores["Data Governance"] <= 2:
        insights.append("🔴 **Data Governance**: Your organization lacks formal governance policies. Consider establishing a data governance framework with clear roles and responsibilities.")
    elif scores["Data Governance"] <= 3.5:
        insights.append("🟡 **Data Governance**: Your governance policies are in place but need better enforcement. Focus on consistent monitoring and accountability.")
    else:
        insights.append("🟢 **Data Governance**: Your governance policies are well-established. Continue optimizing with automation and AI-driven insights.")

    # Data Quality Insights
    if scores["Data Quality"] <= 2:
        insights.append("🔴 **Data Quality**: Data accuracy and completeness are major concerns. Implement automated validation and monitoring processes.")
    elif scores["Data Quality"] <= 3.5:
        insights.append("🟡 **Data Quality**: Your data quality processes are improving but need more automation. Consider AI-powered real-time monitoring.")
    else:
        insights.append("🟢 **Data Quality**: Your data quality is excellent. Focus on maintaining consistency and exploring advanced analytics.")

    # Metadata Management Insights
    if scores["Metadata Management"] <= 2:
        insights.append("🔴 **Metadata Management**: Metadata is poorly managed. Establish a centralized metadata repository and enforce standardized definitions.")
    elif scores["Metadata Management"] <= 3.5:
        insights.append("🟡 **Metadata Management**: Metadata management is improving but lacks automation. Consider AI-driven lineage tracking.")
    else:
        insights.append("🟢 **Metadata Management**: Metadata is well-managed. Continue leveraging AI for real-time anomaly detection.")

    # Data Integration Insights
    if scores["Data Integration"] <= 2:
        insights.append("🔴 **Data Integration**: Data integration is manual and inconsistent. Invest in automated API-based data flows.")
    elif scores["Data Integration"] <= 3.5:
        insights.append("🟡 **Data Integration**: Integration processes are improving but need more automation. Consider real-time synchronization.")
    else:
        insights.append("🟢 **Data Integration**: Data integration is seamless. Explore AI-driven multi-cloud integration.")

    # Data Analytics & AI Insights
    if scores["Data Analytics & AI"] <= 2:
        insights.append("🔴 **Data Analytics & AI**: Analytics adoption is low. Start with basic reporting and explore predictive analytics.")
    elif scores["Data Analytics & AI"] <= 3.5:
        insights.append("🟡 **Data Analytics & AI**: Analytics adoption is growing. Focus on embedding machine learning models into core processes.")
    else:
        insights.append("🟢 **Data Analytics & AI**: Analytics adoption is excellent. Continue leveraging AI for decision intelligence.")

    # Data Security & Privacy Insights
    if scores["Data Security & Privacy"] <= 2:
        insights.append("🔴 **Data Security & Privacy**: Security measures are weak. Implement role-based access control and encryption.")
    elif scores["Data Security & Privacy"] <= 3.5:
        insights.append("🟡 **Data Security & Privacy**: Security measures are improving but need better enforcement. Consider continuous compliance monitoring.")
    else:
        insights.append("🟢 **Data Security & Privacy**: Security measures are robust. Focus on AI-driven anomaly detection and zero-trust models.")

    return insights

# ✅ Define Analytics Capabilities for Each Maturity Stage
analytics_capabilities = {
    "Initial/Ad Hoc": {
        "capabilities": [
            "Descriptive Analytics: Reporting and summarizing past data.",
            "Manual Reporting: Periodic reporting using basic tools like Excel.",
            "Limited Automation: Minimal automation in data collection and reporting."
        ],
        "example": "Tracking monthly sales with basic Excel sheets."
    },
    "Developing": {
        "capabilities": [
            "Basic Diagnostic Analytics: Understanding why certain outcomes occurred.",
            "Standardized Reports: Some standardization in reporting.",
            "Some Automation: Introduction of basic analytics tools and dashboards."
        ],
        "example": "Dashboards showing sales performance against targets."
    },
    "Defined": {
        "capabilities": [
            "Predictive Analytics: Forecasting future outcomes using statistical techniques.",
            "Automated Reporting: Self-service dashboards and automated insights.",
            "Data-Driven Decision-Making: Reports and analysis directly influence decisions."
        ],
        "example": "Predicting customer churn using historical data."
    },
    "Managed": {
        "capabilities": [
            "Prescriptive Analytics: Recommending actions based on predictive models.",
            "Advanced Reporting: Real-time dashboards and actionable insights.",
            "Integrated Analytics: Analytics tools embedded in business processes."
        ],
        "example": "Dynamic product recommendations based on customer behavior."
    },
    "Optimized": {
        "capabilities": [
            "Cognitive/AI Analytics: AI-driven insights and self-learning systems.",
            "Real-Time Decision-Making: Autonomous systems adjust to new data.",
            "Integrated AI: AI and machine learning integrated into core business functions."
        ],
        "example": "Real-time pricing adjustments based on market conditions."
    }
}

# ✅ Define Dynamic Recommendations for Each Maturity Stage
dynamic_recommendations = {
    "Initial/Ad Hoc": {
        "recommendations": [
            "Establish a formal data governance framework to define roles and responsibilities.",
            "Implement basic data quality checks to ensure accuracy and completeness.",
            "Start using simple reporting tools (e.g., Excel, Google Sheets) to track key metrics."
        ],
        "next_steps": [
            "Move towards basic diagnostic analytics by introducing business intelligence tools (e.g., Tableau, Power BI).",
            "Standardize reporting processes to reduce manual effort."
        ]
    },
    "Developing": {
        "recommendations": [
            "Standardize data definitions and metadata management to improve consistency.",
            "Automate data collection and reporting processes to reduce manual effort.",
            "Introduce basic diagnostic analytics to understand trends and patterns."
        ],
        "next_steps": [
            "Adopt predictive analytics to forecast future outcomes.",
            "Invest in self-service dashboards to empower business users."
        ]
    },
    "Defined": {
        "recommendations": [
            "Expand predictive analytics capabilities to forecast key business outcomes.",
            "Integrate analytics tools into business processes for real-time decision-making.",
            "Train staff on data-driven decision-making to maximize the value of analytics."
        ],
        "next_steps": [
            "Explore prescriptive analytics to recommend actionable insights.",
            "Integrate real-time data streams for continuous monitoring."
        ]
    },
    "Managed": {
        "recommendations": [
            "Leverage prescriptive analytics to recommend optimal actions.",
            "Integrate advanced analytics tools into core business functions.",
            "Focus on real-time data processing and decision-making."
        ],
        "next_steps": [
            "Adopt AI-driven analytics for cognitive insights and self-learning systems.",
            "Explore autonomous decision-making capabilities."
        ]
    },
    "Optimized": {
        "recommendations": [
            "Continuously refine AI and machine learning models for better accuracy.",
            "Expand autonomous decision-making capabilities across the organization.",
            "Foster a culture of innovation to explore new analytics use cases."
        ],
        "next_steps": [
            "Stay ahead of industry trends by adopting emerging technologies.",
            "Focus on scaling AI-driven insights across all business units."
        ]
    }
}

def generate_pdf_report(maturity_level, weighted_avg_score, recommendation, weighted_scores, insights, current_capabilities, recommendations, roadmap):
    pdf = FPDF()
    pdf.add_page()

    # Add all variants of the DejaVuSans font
    font_path = r"C:\Users\dkeya\Documents\projects\virtual_narrative\DejaVuSans.ttf\ttf\DejaVuSans.ttf"
    pdf.add_font("DejaVuSans", "", font_path, uni=True)  # Regular
    pdf.add_font("DejaVuSans", "B", font_path, uni=True)  # Bold
    pdf.add_font("DejaVuSans", "I", font_path, uni=True)  # Italic
    pdf.add_font("DejaVuSans", "BI", font_path, uni=True)  # Bold-Italic

    # Set the default font to regular
    pdf.set_font("DejaVuSans", size=12)

    try:
        # Attempt to open the logo file
        logo_path = r"C:\Users\dkeya\Documents\projects\virtual_narrative\logo_1.png"
        with open(logo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        
        # Save the base64 image to a temporary file
        temp_logo_path = "temp_logo_1.png"
        with open(temp_logo_path, "wb") as temp_file:
            temp_file.write(base64.b64decode(encoded_image))
        
        # Add the logo to the PDF
        pdf.image(temp_logo_path, x=50, w=100)  # Center the logo and set width to 100
        pdf.ln(20)  # Add some space after the logo
    except FileNotFoundError:
        st.error("Logo file 'logo_1.png' not found. Please ensure the file is in the correct directory.")
        return  # Exit the function if the logo file is missing

    # Add title
    pdf.set_font("DejaVuSans", "B", 16)  # Bold and larger font for the title
    pdf.cell(200, 10, txt="The Virtual Narrative: Data Maturity Assessment Report", ln=True, align="C")
    pdf.ln(10)  # Add some space after the title

    # Add the introduction paragraph
    pdf.set_font("DejaVuSans", size=12)  # Regular font for content
    intro_text = """
    In today’s rapidly evolving digital world, data is not just an asset; it's the backbone of decision-making, strategy, and innovation. Understanding the maturity of your data practices is key to unlocking its full potential. The concept of Data Maturity reflects how well an organization manages, integrates, analyzes, and secures its data. It’s a journey that takes an organization from basic, reactive data handling to a sophisticated, proactive approach where data is seamlessly integrated into decision-making processes.

    The journey through data maturity is often divided into five stages:
    - Initial/Ad Hoc: Where data processes are disjointed and unpredictable.
    - Developing: Where basic processes are established but still lack consistency.
    - Defined: Where standard processes are in place, and data is beginning to drive decisions.
    - Managed: Where data management is more structured, automated, and fully integrated into business processes.
    - Optimized: Where data is fully embedded in decision-making, and advanced analytics and AI continuously improve business outcomes.

    Each stage reflects an organization's growing ability to leverage data to gain insights, optimize operations, and drive innovation. In this assessment, we’ll evaluate where your organization stands on this maturity journey and provide actionable insights to help you advance.

    Now, let’s see where your organization’s data maturity currently stands with the Data Maturity Score, as visualized below in the gauge chart.
    """
    pdf.multi_cell(200, 10, txt=intro_text.replace("’", "'"), align="L")
    pdf.ln(10)  # Add some space after the introduction

    # Add maturity level and score
    pdf.set_font("DejaVuSans", "B", 14)  # Bold for section titles
    pdf.cell(200, 10, txt="Maturity Level and Score", ln=True)
    pdf.set_font("DejaVuSans", size=12)  # Regular font for content
    pdf.cell(200, 10, txt=f"Your organization's data maturity level is: {maturity_level.replace('🔴', 'Initial/Ad Hoc').replace('🟠', 'Developing').replace('🟡', 'Defined').replace('🟢', 'Managed').replace('🔵', 'Optimized')}", ln=True)
    pdf.cell(200, 10, txt=f"Weighted Average Maturity Score: {weighted_avg_score:.2f}/5", ln=True)
    pdf.cell(200, 10, txt=f"Recommendation: {recommendation}", ln=True)
    pdf.ln(10)  # Add some space after the section

    # Add weighted scores breakdown
    pdf.set_font("DejaVuSans", "B", 14)  # Bold for section titles
    pdf.cell(200, 10, txt="Breakdown by Category (Weighted Scores)", ln=True)
    pdf.set_font("DejaVuSans", size=12)  # Regular font for content
    for category, score in weighted_scores.items():
        pdf.cell(200, 10, txt=f"{category}: {score:.2f}/5", ln=True)
    pdf.ln(10)  # Add some space after the section

    # Add AI-driven insights
    pdf.set_font("DejaVuSans", "B", 14)  # Bold for section titles
    pdf.cell(200, 10, txt="AI-Driven Insights", ln=True)
    pdf.set_font("DejaVuSans", size=12)  # Regular font for content
    for insight in insights:
        pdf.multi_cell(200, 10, txt=f"- {insight.replace('🔴', 'Initial/Ad Hoc').replace('🟠', 'Developing').replace('🟡', 'Defined').replace('🟢', 'Managed').replace('🔵', 'Optimized')}", align="L")
    pdf.ln(10)  # Add some space after the section

    # Add current analytics capabilities with dynamic color
    pdf.set_font("DejaVuSans", "B", 14)  # Bold for section titles
    if maturity_level == "🔴 Initial/Ad Hoc":
        pdf.set_text_color(255, 0, 0)  # Red for Initial/Ad Hoc
    elif maturity_level == "🟠 Developing":
        pdf.set_text_color(255, 165, 0)  # Orange for Developing
    elif maturity_level == "🟡 Defined":
        pdf.set_text_color(255, 255, 0)  # Yellow for Defined
    elif maturity_level == "🟢 Managed":
        pdf.set_text_color(0, 128, 0)  # Green for Managed
    elif maturity_level == "🔵 Optimized":
        pdf.set_text_color(0, 0, 255)  # Blue for Optimized
    pdf.cell(200, 10, txt="Current Analytics Capabilities", ln=True)
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.set_font("DejaVuSans", size=12)  # Regular font for content
    for capability in current_capabilities["capabilities"]:
        # Split the capability into type and description
        capability_type, capability_desc = capability.split(":", 1)
        pdf.set_font("DejaVuSans", "B", 12)  # Bold for capability type
        pdf.cell(200, 10, txt=f"- {capability_type}:", ln=True)
        pdf.set_font("DejaVuSans", size=12)  # Regular font for description
        pdf.multi_cell(200, 10, txt=f"  {capability_desc.strip()}", align="L")
    pdf.cell(200, 10, txt=f"Example: {current_capabilities['example']}", ln=True)
    pdf.ln(10)  # Add some space after the section

    # Add dynamic recommendations
    pdf.set_font("DejaVuSans", "B", 14)  # Bold for section titles
    pdf.cell(200, 10, txt="Recommendations for Improvement", ln=True)
    pdf.set_font("DejaVuSans", size=12)  # Regular font for content
    for rec in recommendations["recommendations"]:
        pdf.multi_cell(200, 10, txt=f"- {rec}", align="L")
    pdf.set_font("DejaVuSans", "B", 12)  # Bold for subheadings
    pdf.cell(200, 10, txt="Next Steps:", ln=True)
    pdf.set_font("DejaVuSans", size=12)  # Regular font for content
    for step in recommendations["next_steps"]:
        pdf.multi_cell(200, 10, txt=f"- {step}", align="L")
    pdf.ln(10)  # Add some space after the section

    # Add roadmap
    pdf.set_font("DejaVuSans", "B", 14)  # Bold for section titles
    pdf.cell(200, 10, txt="Roadmap to Higher Maturity Levels", ln=True)
    pdf.set_font("DejaVuSans", size=12)  # Regular font for content
    for stage, details in roadmap.items():
        pdf.set_font("DejaVuSans", "B", 12)  # Bold for subheadings
        pdf.cell(200, 10, txt=f"{stage}:", ln=True)
        pdf.set_font("DejaVuSans", size=12)  # Regular font for content
        for capability in details["capabilities"]:
            # Split the capability into type and description
            capability_type, capability_desc = capability.split(":", 1)
            pdf.set_font("DejaVuSans", "B", 12)  # Bold for capability type
            pdf.cell(200, 10, txt=f"- {capability_type}:", ln=True)
            pdf.set_font("DejaVuSans", size=12)  # Regular font for description
            pdf.multi_cell(200, 10, txt=f"  {capability_desc.strip()}", align="L")
        pdf.cell(200, 10, txt=f"Example: {details['example']}", ln=True)
    pdf.ln(10)  # Add some space after the section

    # Add a concluding note
    pdf.set_font("DejaVuSans", "I", 12)  # Italic for the concluding note
    pdf.cell(200, 10, txt="Thank you for using The Virtual Narrative: Data Maturity Assessment Tool!", ln=True, align="C")
    pdf.ln(10)  # Add some space after the note

    # Add a creative call to action
    pdf.set_font("DejaVuSans", "B", 14)  # Bold for the call to action
    pdf.set_text_color(0, 0, 255)  # Blue for emphasis
    pdf.cell(200, 10, txt="Need a Helping Hand Across the Chasm to Data Maturity?", ln=True, align="C")
    pdf.set_font("DejaVuSans", size=12)  # Regular font for content
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.cell(200, 10, txt="Embarking on the journey to data maturity can be challenging, but you don't have to do it alone.", ln=True, align="C")
    pdf.cell(200, 10, txt="Reach out to us for expert guidance and support:", ln=True, align="C")
    pdf.set_font("DejaVuSans", "B", 12)  # Bold for contact details
    pdf.cell(200, 10, txt="Virtual Analytics", ln=True, align="C")
    pdf.cell(200, 10, txt="www.virtualanalytics.co.ke | info@virtualanalytics.co.ke", ln=True, align="C")
    pdf.set_font("DejaVuSans", size=12)  # Regular font for content
    pdf.cell(200, 10, txt="Let us help you unlock the full potential of your data!", ln=True, align="C")

    # Save the PDF
    pdf.output("data_maturity_report.pdf")

# ✅ Display Data Maturity Score after all sections are completed
if st.session_state.all_sections_completed:
    # Add the title above the gauge chart
    st.write("## The Virtual Narrative: Data Maturity Assessment Report")
    
    # Add the introduction paragraph with icons
    st.write("""
    In today’s rapidly evolving digital world, data is not just an asset; it's the backbone of decision-making, strategy, and innovation. Understanding the maturity of your data practices is key to unlocking its full potential. The concept of **Data Maturity** reflects how well an organization manages, integrates, analyzes, and secures its data. It’s a journey that takes an organization from basic, reactive data handling to a sophisticated, proactive approach where data is seamlessly integrated into decision-making processes.

    The journey through data maturity is often divided into five stages:

    - **🔴 Initial/Ad Hoc**: Where data processes are disjointed and unpredictable.
    - **🟠 Developing**: Where basic processes are established but still lack consistency.
    - **🟡 Defined**: Where standard processes are in place, and data is beginning to drive decisions.
    - **🟢 Managed**: Where data management is more structured, automated, and fully integrated into business processes.
    - **🔵 Optimized**: Where data is fully embedded in decision-making, and advanced analytics and AI continuously improve business outcomes.

    Each stage reflects an organization's growing ability to leverage data to gain insights, optimize operations, and drive innovation. In this assessment, we’ll evaluate where your organization stands on this maturity journey and provide actionable insights to help you advance.

    Now, let’s see where your organization’s data maturity currently stands with the **Data Maturity Score**, as visualized below in the gauge chart.
    """)
    
    # Calculate the weighted average maturity score
    weighted_scores = {
        "Data Governance": extract_score(st.session_state.get("gov_q1_response", " (1)")) * st.session_state.weights["Data Governance"],
        "Data Quality": extract_score(st.session_state.get("dq1_response", " (1)")) * st.session_state.weights["Data Quality"],
        "Metadata Management": extract_score(st.session_state.get("mm1_response", " (1)")) * st.session_state.weights["Metadata Management"],
        "Data Integration": extract_score(st.session_state.get("di1_response", " (1)")) * st.session_state.weights["Data Integration"],
        "Data Analytics & AI": extract_score(st.session_state.get("ai1_response", " (1)")) * st.session_state.weights["Data Analytics & AI"],
        "Data Security & Privacy": extract_score(st.session_state.get("sp1_response", " (1)")) * st.session_state.weights["Data Security & Privacy"]
    }

    # Calculate the weighted average maturity score (between 1 and 5)
    weighted_avg_score = sum(weighted_scores.values())

    # Create and display the gauge chart with a unique key
    st.plotly_chart(create_gauge_chart(weighted_avg_score), key="gauge_chart_final")

    # Determine Maturity Level & Recommendations
    if weighted_avg_score <= 1.5:
        maturity_level = "🔴 Initial/Ad Hoc"
        recommendation = "You are at the beginning point for Data Management. Start by defining data governance policies and improving data quality."
    elif weighted_avg_score <= 2.5:
        maturity_level = "🟠 Developing"
        recommendation = "You have basic policies but lack consistency. Focus on standardizing processes and improving data integration."
    elif weighted_avg_score <= 3.5:
        maturity_level = "🟡 Defined"
        recommendation = "You have structured processes, but there is room for more automation and real-time analytics."
    elif weighted_avg_score <= 4.5:
        maturity_level = "🟢 Managed"
        recommendation = "Your organization has well-established data governance. Continue refining automation and advanced analytics adoption."
    else:
        maturity_level = "🔵 Optimized"
        recommendation = "Your organization is at the highest level of data maturity! Continue leveraging AI-driven insights for optimization."

    # Display the score and recommendation
    st.write(f"### 🎯 Your Organization's Maturity Level: {maturity_level}")
    st.write(f"📊 **Weighted Average Maturity Score:** {weighted_avg_score:.2f}/5")
    st.write(f"💡 **Recommendation:** {recommendation}")

    # Display Individual Scores Breakdown
    st.write("### 📌 Breakdown by Category (Weighted Scores)")
    for category, score in weighted_scores.items():
        st.write(f"✅ **{category}**: {score:.2f}/5")

    # Generate and display AI-driven insights
    st.write("### 🤖 AI-Driven Insights")
    insights = generate_ai_insights({
        "Data Governance": extract_score(st.session_state.get("gov_q1_response", " (1)")),
        "Data Quality": extract_score(st.session_state.get("dq1_response", " (1)")),
        "Metadata Management": extract_score(st.session_state.get("mm1_response", " (1)")),
        "Data Integration": extract_score(st.session_state.get("di1_response", " (1)")),
        "Data Analytics & AI": extract_score(st.session_state.get("ai1_response", " (1)")),
        "Data Security & Privacy": extract_score(st.session_state.get("sp1_response", " (1)"))
    })
    for insight in insights:
        st.write(insight)

    # Display Analytics Capabilities for Current Maturity Level
    st.write("### 📈 Analytics Capabilities at Your Maturity Level")
    current_capabilities = analytics_capabilities.get(maturity_level.replace("🔴", "").replace("🟠", "").replace("🟡", "").replace("🟢", "").replace("🔵", "").strip())
    if current_capabilities:
        st.write(f"#### Current Capabilities:")
        for capability in current_capabilities["capabilities"]:
            st.write(f"- {capability}")
        st.write(f"**Example:** {current_capabilities['example']}")
    else:
        st.write("No analytics capabilities found for this maturity level.")

    # Display Dynamic Recommendations
    st.write("### 🛠️ Recommendations for Improvement")
    recommendations = dynamic_recommendations.get(maturity_level.replace("🔴", "").replace("🟠", "").replace("🟡", "").replace("🟢", "").replace("🔵", "").strip())
    if recommendations:
        st.write(f"#### Recommendations:")
        for rec in recommendations["recommendations"]:
            st.write(f"- {rec}")
        st.write(f"#### Next Steps:")
        for step in recommendations["next_steps"]:
            st.write(f"- {step}")
    else:
        st.write("No recommendations found for this maturity level.")

    # Display Roadmap for Higher Maturity Levels
    st.write("### 🛣️ Roadmap to Higher Maturity Levels")
    st.write("Here’s what you can achieve by progressing to higher stages of data maturity:")
    for stage, details in analytics_capabilities.items():
        if stage != maturity_level.replace("🔴", "").replace("🟠", "").replace("🟡", "").replace("🟢", "").replace("🔵", "").strip():
            st.write(f"#### {stage}")
            for capability in details["capabilities"]:
                st.write(f"- {capability}")
            st.write(f"**Example:** {details['example']}")

    # Add a button to download the PDF report
    if st.button("Download PDF Report"):
        generate_pdf_report(
            maturity_level,
            weighted_avg_score,
            recommendation,
            weighted_scores,
            insights,
            current_capabilities,
            recommendations,
            {k: v for k, v in analytics_capabilities.items() if k != maturity_level.replace("🔴", "").replace("🟠", "").replace("🟡", "").replace("🟢", "").replace("🔵", "").strip()}
        )
        st.success("✅ PDF report generated! Click below to download.")
        with open("data_maturity_report.pdf", "rb") as file:
            st.download_button(
                label="Download Report",
                data=file,
                file_name="data_maturity_report.pdf",
                mime="application/pdf"
            )

    st.success("🎉 Congratulations on completing The Virtual Narrative: Data Maturity Assessment!")
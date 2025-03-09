import streamlit as st
import base64  # For base64 encoding
import plotly.graph_objects as go  # For the gauge chart
import re  # For extracting numeric scores

# ✅ Function to Extract Numeric Scores from Responses
def extract_score(response):
    """Extract numeric score from the selected response."""
    match = re.search(r"\((\d+)\)", response)  # Look for a number inside parentheses
    return int(match.group(1)) if match else 1  # Default to 1 if no match

# ✅ Function to Create Gauge Chart
def create_gauge_chart(score):
    """Create a gauge chart for the data maturity score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        title={'text': "Your Data Maturity Score", 'font': {'size': 24}},
        gauge={'axis': {'range': [None, 5]},
               'bar': {'color': "orange"},
               'steps': [
                   {'range': [0, 1.5], 'color': "red"},
                   {'range': [1.5, 2.5], 'color': "orange"},
                   {'range': [2.5, 3.5], 'color': "yellow"},
                   {'range': [3.5, 4.5], 'color': "green"},
                   {'range': [4.5, 5], 'color': "blue"}],
               'threshold': {
                   'line': {'color': "black", 'width': 4},
                   'thickness': 0.75,
                   'value': score}
        }
    ))
    fig.update_layout(width=500, height=300)
    return fig

# ✅ Set page configuration to wide mode (MUST be the first Streamlit command)
st.set_page_config(page_title="The Virtual Narrative", page_icon="🌀", layout="wide")

# ✅ Initialize Session State Variables (Only Once)
session_defaults = {
    "start_assessment": False,
    "data_privacy_accepted": False,
    "user_info_complete": False,  # Track if user info is completed
    "data_governance_complete": False,
    "data_quality_complete": False,
    "metadata_management_complete": False,
    "data_integration_complete": False,
    "data_analytics_complete": False,
    "data_security_complete": False,
    "all_sections_completed": False,
    "gov_q1_response": " (1)", "gov_q2_response": " (1)", "gov_q3_response": " (1)",
    "dq1_response": " (1)", "dq2_response": " (1)", "dq3_response": " (1)",
    "mm1_response": " (1)", "mm2_response": " (1)", "mm3_response": " (1)",
    "di1_response": " (1)", "di2_response": " (1)", "di3_response": " (1)",
    "ai1_response": " (1)", "ai2_response": " (1)", "ai3_response": " (1)",
    "sp1_response": " (1)", "sp2_response": " (1)", "sp3_response": " (1)",
    "current_question": 1  # Track the current question in a section
}
for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ✅ Open the image file and encode it as base64
with open("logo.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# ✅ Add background color and center the content using markdown
st.markdown(
    f"""
    <style>
    .top-page {{
        background-color: #1e2a47;  /* Set background color similar to the original image */
        padding: 50px;
        text-align: center;
        color: white;
        position: relative;
    }}
    .top-page h1 {{
        font-size: 36px;
    }}
    .top-page p {{
        font-size: 18px;
    }}
    .start-button {{
        position: absolute;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        background-color: #FFA500;
        color: white;
        font-size: 20px;
        padding: 15px 30px;
        border-radius: 5px;
        cursor: pointer;
        border: none;
    }}
    .start-button:hover {{
        background-color: #ff8c00;
    }}
    </style>
    <div class="top-page">
        <img src="data:image/png;base64,{encoded_image}" width="250" style="display:block; margin-left:auto; margin-right:auto;">
        <h1>Welcome to The Virtual Narrative</h1>
        <p>Complete this Data Maturity Assessment to understand your organization's data maturity level.<br>
        Grab a coffee ☕ or a beer 🍺, pull up a chair, and let's dive into the world of data management!</p>
        <p>⏳ Takes 7+ minutes</p>
        <button class="start-button" onclick="window.location.reload();">Let's do this!</button>
    </div>
    """, unsafe_allow_html=True
)

# ✅ Handle button click for starting the assessment and navigating to the next page
if st.button("Let's do this!"):
    st.session_state.start_assessment = True
    st.session_state.data_privacy_accepted = False  # Set this flag to False when starting
    st.success("Great! Let's begin your Data Maturity Assessment.")

# ✅ Data Privacy & Protection Page (Page 2)
if st.session_state.start_assessment and not st.session_state.data_privacy_accepted:
    st.write("## Data Privacy & Protection")
    st.write("""
        Before we begin - a word on Data Privacy and Protection. We take your Data Privacy seriously. The data you share with us will be treated as though it were our own. 
        We will use this information solely to provide you with a bespoke report with actionable insights into your current state of Data Maturity, alongside suggestions on how you can improve.
        Over time, we will compile research findings for industries and regions, but these will be completely anonymized.
    """)
    if st.button("Continue"):
        st.session_state.data_privacy_accepted = True  # Proceed to next section when the button is clicked

# ✅ User Information Collection Page (Page 3)
if st.session_state.data_privacy_accepted and not st.session_state.user_info_complete:
    st.write("### 📝 Let's get started by knowing you!")
    first_name = st.text_input("Enter your First Name:", key="user_first_name")
    last_name = st.text_input("Enter your Last Name:", key="user_last_name")
    email = st.text_input("Enter your Email Address:", key="user_email")
    org_name = st.text_input("Enter your Organization Name:", key="user_org_name")
    business_unit = st.text_input("Which Business Unit do you work in?", key="user_business_unit")

    if st.button("Start Assessment"):
        if not first_name or not last_name or not email:
            st.error("⚠️ Please fill in all required fields!")
        else:
            st.session_state.user_info_complete = True
            st.success(f"Great, {first_name}! Let's begin your Data Maturity Assessment.")

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
if st.session_state.user_info_complete and not st.session_state.data_governance_complete:
    st.write("## 🏛️ Section 1: Data Governance")
    st.write("This section assesses how well data governance is established in your organization.")

    if st.session_state.current_question == 1:
        gov_q1 = st.radio("1️⃣ **Does your organization have a formal Data Governance policy?**",
                          ["No governance exists (1)",
                           "Some informal rules, but not enforced (2)",
                           "Formal governance in place, but not consistently followed (3)",
                           "Governance is standardized and monitored (4)",
                           "Governance is automated, AI-driven, and continuously optimized (5)"], key="gov_q1")
        if st.button("Next"):
            st.session_state.gov_q1_response = gov_q1
            st.session_state.current_question = 2  # Move to the next question

    elif st.session_state.current_question == 2:
        gov_q2 = st.radio("2️⃣ **Are roles and responsibilities clearly defined? (e.g., Data Stewards, Chief Data Officer)?**",
                          ["No defined roles (1)",
                           "Some responsibilities exist but unclear (2)",
                           "Defined roles exist, but accountability is weak (3)",
                           "Roles are well-defined and monitored (4)",
                           "Governance roles are optimized and continuously improved (5)"], key="gov_q2")
        if st.button("Next"):
            st.session_state.gov_q2_response = gov_q2
            st.session_state.current_question = 3  # Move to the next question

    elif st.session_state.current_question == 3:
        gov_q3 = st.radio("3️⃣ **How frequently is your Data Governance policy reviewed and updated?**",
                          ["Never (1)",
                           "Ad-hoc updates with no schedule (2)",
                           "Reviewed every few years (3)",
                           "Reviewed annually (4)",
                           "Continuously improved with data-driven feedback (5)"], key="gov_q3")
        if st.button("Submit Governance Responses"):
            st.session_state.gov_q3_response = gov_q3
            st.session_state.data_governance_complete = True
            st.session_state.current_question = 1  # Reset for the next section
            st.success("✅ Responses recorded! Moving to the next section.")

# 📊 **SECTION 2: DATA QUALITY**
if st.session_state.data_governance_complete and not st.session_state.data_quality_complete:
    st.write("## 📊 Section 2: Data Quality")
    st.write("This section evaluates how well your organization maintains **accurate, complete, and reliable data**.")

    if st.session_state.current_question == 1:
        dq1 = st.radio("1️⃣ **How does your organization ensure data accuracy?**",
                       ["No process for accuracy (1)",
                        "Basic manual checks (2)",
                        "Defined validation rules (3)",
                        "Automated quality checks (4)",
                        "AI-powered real-time monitoring (5)"], key="dq1")
        if st.button("Next"):
            st.session_state.dq1_response = dq1
            st.session_state.current_question = 2  # Move to the next question

    elif st.session_state.current_question == 2:
        dq2 = st.radio("2️⃣ **How is data completeness ensured in your organization?**",
                       ["No strategy in place (1)",
                        "Manual data entry reviews (2)",
                        "Automated missing value checks (3)",
                        "Proactive data validation (4)",
                        "Machine learning-driven data integrity (5)"], key="dq2")
        if st.button("Next"):
            st.session_state.dq2_response = dq2
            st.session_state.current_question = 3  # Move to the next question

    elif st.session_state.current_question == 3:
        dq3 = st.radio("3️⃣ **How consistently is data updated and synchronized across systems?**",
                       ["No updates, data silos exist (1)",
                        "Periodic manual updates (2)",
                        "Automated scheduled updates (3)",
                        "Real-time data sync (4)",
                        "Self-healing, AI-driven consistency (5)"], key="dq3")
        if st.button("Submit Data Quality Responses"):
            st.session_state.dq3_response = dq3
            st.session_state.data_quality_complete = True
            st.session_state.current_question = 1  # Reset for the next section
            st.success("✅ Data Quality responses submitted! Moving to Metadata Management.")

# 🏷 **SECTION 3: METADATA MANAGEMENT**
if st.session_state.data_quality_complete and not st.session_state.metadata_management_complete:
    st.write("## 🏷 Section 3: Metadata Management")
    st.write("This section evaluates how well your organization manages **metadata, including data definitions, lineage, and classification.**")

    if st.session_state.current_question == 1:
        mm1 = st.radio("1️⃣ **Does your organization maintain a centralized metadata repository?**",
                       ["No metadata repository exists (1)",
                        "Some metadata exists in scattered documentation (2)",
                        "A structured metadata catalog is available (3)",
                        "A centralized metadata repository is maintained (4)",
                        "Fully automated metadata management with AI-driven lineage tracking (5)"], key="mm1")
        if st.button("Next"):
            st.session_state.mm1_response = mm1
            st.session_state.current_question = 2  # Move to the next question

    elif st.session_state.current_question == 2:
        mm2 = st.radio("2️⃣ **How well-defined and standardized are your data definitions?**",
                       ["No definitions exist (1)",
                        "Ad-hoc definitions in some areas (2)",
                        "Standardized definitions exist but not enforced (3)",
                        "Organization-wide metadata standards are enforced (4)",
                        "AI-driven metadata governance ensures full compliance (5)"], key="mm2")
        if st.button("Next"):
            st.session_state.mm2_response = mm2
            st.session_state.current_question = 3  # Move to the next question

    elif st.session_state.current_question == 3:
        mm3 = st.radio("3️⃣ **How is data lineage tracked in your organization?**",
                       ["No lineage tracking (1)",
                        "Basic manual lineage documentation (2)",
                        "Automated lineage tracking for some systems (3)",
                        "Comprehensive automated lineage tracking (4)",
                        "AI-driven lineage tracking with real-time anomaly detection (5)"], key="mm3")
        if st.button("Submit Metadata Management Responses"):
            st.session_state.mm3_response = mm3
            st.session_state.metadata_management_complete = True
            st.session_state.current_question = 1  # Reset for the next section
            st.success("✅ Metadata Management responses submitted! Moving to Data Integration.")

# 🔗 **SECTION 4: DATA INTEGRATION**
if st.session_state.metadata_management_complete and not st.session_state.data_integration_complete:
    st.write("## 🔗 Section 4: Data Integration")
    st.write("This section evaluates how well data is integrated across your organization, ensuring seamless interoperability.")

    if st.session_state.current_question == 1:
        di1 = st.radio("1️⃣ **How does your organization handle data integration between different systems?**",
                       ["No integration exists (1)",
                        "Manual data transfers (2)",
                        "Basic ETL processes in place (3)",
                        "Automated API-based data flows (4)",
                        "Real-time AI-driven integration across platforms (5)"], key="di1")
        if st.button("Next"):
            st.session_state.di1_response = di1
            st.session_state.current_question = 2  # Move to the next question

    elif st.session_state.current_question == 2:
        di2 = st.radio("2️⃣ **How frequently does your organization update and synchronize data across different platforms?**",
                       ["Never (1)",
                        "Occasionally with manual intervention (2)",
                        "Automated updates on a scheduled basis (3)",
                        "Near real-time synchronization (4)",
                        "AI-driven, self-healing data synchronization (5)"], key="di2")
        if st.button("Next"):
            st.session_state.di2_response = di2
            st.session_state.current_question = 3  # Move to the next question

    elif st.session_state.current_question == 3:
        di3 = st.radio("3️⃣ **Does your organization utilize cloud-based data integration platforms?**",
                       ["No cloud integration (1)",
                        "Limited use of cloud data storage (2)",
                        "Some cloud integration but no automation (3)",
                        "Fully automated cloud-based integration (4)",
                        "AI-optimized multi-cloud integration (5)"], key="di3")
        if st.button("Submit Data Integration Responses"):
            st.session_state.di3_response = di3
            st.session_state.data_integration_complete = True
            st.session_state.current_question = 1  # Reset for the next section
            st.success("✅ Data Integration responses submitted! Moving to Data Analytics & AI.")

# 📊 **SECTION 5: DATA ANALYTICS & AI**
if st.session_state.data_integration_complete and not st.session_state.data_analytics_complete:
    st.write("## 📊 Section 5: Data Analytics & AI")
    st.write("This section assesses your organization's ability to leverage data analytics and AI for decision-making.")

    if st.session_state.current_question == 1:
        ai1 = st.radio("1️⃣ **What is the level of adoption of business intelligence and reporting in your organization?**",
                       ["No formal reporting (1)",
                        "Basic manual reports with spreadsheets (2)",
                        "Automated dashboards with static reports (3)",
                        "Interactive BI tools with real-time data (4)",
                        "AI-driven predictive analytics and self-service BI (5)"], key="ai1")
        if st.button("Next"):
            st.session_state.ai1_response = ai1
            st.session_state.current_question = 2  # Move to the next question

    elif st.session_state.current_question == 2:
        ai2 = st.radio("2️⃣ **How is machine learning used in your organization?**",
                       ["Not used at all (1)",
                        "Basic experiments without production deployment (2)",
                        "Some predictive models used in decision-making (3)",
                        "Machine learning models are embedded in core processes (4)",
                        "AI-driven automation and decision intelligence across the business (5)"], key="ai2")
        if st.button("Next"):
            st.session_state.ai2_response = ai2
            st.session_state.current_question = 3  # Move to the next question

    elif st.session_state.current_question == 3:
        ai3 = st.radio("3️⃣ **How well is AI governance and ethics considered in your organization?**",
                       ["No AI governance in place (1)",
                        "Basic awareness but no formal guidelines (2)",
                        "AI policies exist but are inconsistently followed (3)",
                        "AI governance is well-defined and monitored (4)",
                        "AI ethics, bias detection, and compliance are actively managed (5)"], key="ai3")
        if st.button("Submit Data Analytics & AI Responses"):
            st.session_state.ai3_response = ai3
            st.session_state.data_analytics_complete = True
            st.session_state.current_question = 1  # Reset for the next section
            st.success("✅ Data Analytics & AI responses submitted! Moving to Data Security & Privacy.")

# 🔒 **SECTION 6: DATA SECURITY & PRIVACY**
if st.session_state.data_analytics_complete and not st.session_state.data_security_complete:
    st.write("## 🔒 Section 6: Data Security & Privacy")
    st.write("This section evaluates how well your organization ensures data security, privacy, and compliance with regulations.")

    if st.session_state.current_question == 1:
        sp1 = st.radio("1️⃣ **How is access to sensitive data controlled in your organization?**",
                       ["No access control (1)",
                        "Basic password protection (2)",
                        "Role-based access control (RBAC) in place (3)",
                        "Multi-factor authentication and encryption (4)",
                        "Zero-trust security model with continuous monitoring (5)"], key="sp1")
        if st.button("Next"):
            st.session_state.sp1_response = sp1
            st.session_state.current_question = 2  # Move to the next question

    elif st.session_state.current_question == 2:
        sp2 = st.radio("2️⃣ **Does your organization comply with data protection regulations (e.g., GDPR, HIPAA, Kenya Data Protection Act)?**",
                       ["No compliance efforts (1)",
                        "Minimal awareness, but no formal compliance (2)",
                        "Compliance policies exist but are inconsistently followed (3)",
                        "Fully compliant with regular audits (4)",
                        "Continuous compliance monitoring and automated reporting (5)"], key="sp2")
        if st.button("Next"):
            st.session_state.sp2_response = sp2
            st.session_state.current_question = 3  # Move to the next question

    elif st.session_state.current_question == 3:
        sp3 = st.radio("3️⃣ **How well does your organization handle data encryption and secure storage?**",
                       ["No encryption (1)",
                        "Basic encryption for some data (2)",
                        "Encryption used for sensitive data (3)",
                        "Industry-standard encryption applied across systems (4)",
                        "End-to-end encryption with automated security updates (5)"], key="sp3")
        if st.button("Submit Data Security & Privacy Responses"):
            st.session_state.sp3_response = sp3
            st.session_state.data_security_complete = True
            st.session_state.current_question = 1  # Reset for the next section
            st.success("✅ Data Security & Privacy responses submitted! Assessment complete.")
            st.session_state.all_sections_completed = True

# ✅ Display Data Maturity Score after all sections are completed
if st.session_state.all_sections_completed:
    # Calculate the average maturity score
    scores = {
        "Data Governance": extract_score(st.session_state.get("gov_q1_response", " (1)")),
        "Data Quality": extract_score(st.session_state.get("dq1_response", " (1)")),
        "Metadata Management": extract_score(st.session_state.get("mm1_response", " (1)")),
        "Data Integration": extract_score(st.session_state.get("di1_response", " (1)")),
        "Data Analytics & AI": extract_score(st.session_state.get("ai1_response", " (1)")),
        "Data Security & Privacy": extract_score(st.session_state.get("sp1_response", " (1)"))
    }

    # Calculate the average maturity score (between 1 and 5)
    avg_score = sum(scores.values()) / len(scores)

    # Create and display the gauge chart
    st.plotly_chart(create_gauge_chart(avg_score))

    # Determine Maturity Level & Recommendations
    if avg_score <= 1.5:
        maturity_level = "🔴 Initial/Ad Hoc"
        recommendation = "You are at the beginning point for Data Management. Start by defining data governance policies and improving data quality."
    elif avg_score <= 2.5:
        maturity_level = "🟠 Developing"
        recommendation = "You have basic policies but lack consistency. Focus on standardizing processes and improving data integration."
    elif avg_score <= 3.5:
        maturity_level = "🟡 Defined"
        recommendation = "You have structured processes, but there is room for more automation and real-time analytics."
    elif avg_score <= 4.5:
        maturity_level = "🟢 Managed"
        recommendation = "Your organization has well-established data governance. Continue refining automation and advanced analytics adoption."
    else:
        maturity_level = "🔵 Optimized"
        recommendation = "Your organization is at the highest level of data maturity! Continue leveraging AI-driven insights for optimization."

    # Display the score and recommendation
    st.write(f"### 🎯 Your Organization's Maturity Level: {maturity_level}")
    st.write(f"📊 **Average Maturity Score:** {avg_score:.2f}/5")
    st.write(f"💡 **Recommendation:** {recommendation}")

    # Display Individual Scores Breakdown
    st.write("### 📌 Breakdown by Category")
    for category, score in scores.items():
        st.write(f"✅ **{category}**: {score}/5")

    st.success("🎉 Congratulations on completing The Virtual Narrative: Data Maturity Assessment!")
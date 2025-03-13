import streamlit as st
import base64
import plotly.graph_objects as go
import re
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# ✅ Function to Extract Numeric Scores from Responses
def extract_score(response):
    """Extract numeric score from the selected response."""
    match = re.search(r"\((\d+)\)", response)
    return int(match.group(1)) if match else 1

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

# ✅ Function to Send Email with PDF Attachment
def send_email_with_pdf(receiver_email, pdf_path):
    """Send an email with the PDF report attached."""
    sender_email = "your_email@gmail.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your email password

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Your Data Maturity Assessment Report"

    # Attach the PDF
    with open(pdf_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(pdf_path)}",
        )
        msg.attach(part)

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        st.success("📧 Email sent successfully! Check your inbox.")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# ✅ Set page configuration to wide mode (MUST be the first Streamlit command)
st.set_page_config(page_title="The Virtual Narrative", page_icon="🌐", layout="wide")

# ✅ Initialize Session State Variables (Only Once)
session_defaults = {
    "start_assessment": False,
    "data_privacy_accepted": False,
    "user_info_complete": False,
    "dynamic_weights_set": False,
    "data_governance_complete": False,
    "data_quality_complete": False,
    "metadata_management_complete": False,
    "data_integration_complete": False,
    "data_analytics_complete": False,
    "data_security_complete": False,
    "all_sections_completed": False,
    "weights": {
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
    "current_question": 1
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
        background-color: #1e2a47;
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
    st.session_state.data_privacy_accepted = False
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
        st.session_state.data_privacy_accepted = True

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

# ✅ Dynamic Weighting Section
if st.session_state.user_info_complete and not st.session_state.dynamic_weights_set:
    st.write("## ⚖️ Dynamic Weighting")
    st.write("This section helps us understand your organization's priorities to tailor the assessment.")

    governance_score = st.radio("1️⃣ **How important is it for your organization to have clear data ownership and accountability?**",
                                ["Not Important (1)",
                                 "Slightly Important (2)",
                                 "Moderately Important (3)",
                                 "Very Important (4)",
                                 "Extremely Important (5)"], key="gov_weight")
    quality_score = st.radio("2️⃣ **How critical is data accuracy and completeness for your organization's decision-making?**",
                             ["Not Critical (1)",
                              "Slightly Critical (2)",
                              "Moderately Critical (3)",
                              "Very Critical (4)",
                              "Extremely Critical (5)"], key="dq_weight")
    metadata_score = st.radio("3️⃣ **How important is it for your organization to have a centralized metadata repository?**",
                              ["Not Important (1)",
                               "Slightly Important (2)",
                               "Moderately Important (3)",
                               "Very Important (4)",
                               "Extremely Important (5)"], key="mm_weight")
    integration_score = st.radio("4️⃣ **How important is seamless data integration across different systems for your organization?**",
                                 ["Not Important (1)",
                                  "Slightly Important (2)",
                                  "Moderately Important (3)",
                                  "Very Important (4)",
                                  "Extremely Important (5)"], key="di_weight")
    analytics_score = st.radio("5️⃣ **How important is leveraging data analytics and AI for decision-making in your organization?**",
                               ["Not Important (1)",
                                "Slightly Important (2)",
                                "Moderately Important (3)",
                                "Very Important (4)",
                                "Extremely Important (5)"], key="ai_weight")
    security_score = st.radio("6️⃣ **How important is ensuring data security and compliance with regulations for your organization?**",
                              ["Not Important (1)",
                               "Slightly Important (2)",
                               "Moderately Important (3)",
                               "Very Important (4)",
                               "Extremely Important (5)"], key="sp_weight")

    if st.button("Set Weights"):
        governance_score = extract_score(governance_score)
        quality_score = extract_score(quality_score)
        metadata_score = extract_score(metadata_score)
        integration_score = extract_score(integration_score)
        analytics_score = extract_score(analytics_score)
        security_score = extract_score(security_score)

        total_score = governance_score + quality_score + metadata_score + integration_score + analytics_score + security_score

        st.session_state.weights = {
            "Data Governance": governance_score / total_score,
            "Data Quality": quality_score / total_score,
            "Metadata Management": metadata_score / total_score,
            "Data Integration": integration_score / total_score,
            "Data Analytics & AI": analytics_score / total_score,
            "Data Security & Privacy": security_score / total_score
        }

        st.session_state.dynamic_weights_set = True
        st.success("✅ Weights set! Moving to the next section.")

# ✅ Track Completion Progress
total_sections = 6
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
    st.progress(progress)
    st.write(f"🟢 **Progress: {progress}% Complete**")

# 🏛️ **SECTION 1: DATA GOVERNANCE**
if st.session_state.dynamic_weights_set and not st.session_state.data_governance_complete:
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
            st.session_state.current_question = 2

    elif st.session_state.current_question == 2:
        gov_q2 = st.radio("2️⃣ **Are roles and responsibilities clearly defined? (e.g., Data Stewards, Chief Data Officer)?**",
                          ["No defined roles (1)",
                           "Some responsibilities exist but unclear (2)",
                           "Defined roles exist, but accountability is weak (3)",
                           "Roles are well-defined and monitored (4)",
                           "Governance roles are optimized and continuously improved (5)"], key="gov_q2")
        if st.button("Next"):
            st.session_state.gov_q2_response = gov_q2
            st.session_state.current_question = 3

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
            st.session_state.current_question = 1
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
            st.session_state.current_question = 2

    elif st.session_state.current_question == 2:
        dq2 = st.radio("2️⃣ **How is data completeness ensured in your organization?**",
                       ["No strategy in place (1)",
                        "Manual data entry reviews (2)",
                        "Automated missing value checks (3)",
                        "Proactive data validation (4)",
                        "Machine learning-driven data integrity (5)"], key="dq2")
        if st.button("Next"):
            st.session_state.dq2_response = dq2
            st.session_state.current_question = 3

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
            st.session_state.current_question = 1
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
            st.session_state.current_question = 2

    elif st.session_state.current_question == 2:
        mm2 = st.radio("2️⃣ **How well-defined and standardized are your data definitions?**",
                       ["No definitions exist (1)",
                        "Ad-hoc definitions in some areas (2)",
                        "Standardized definitions exist but not enforced (3)",
                        "Organization-wide metadata standards are enforced (4)",
                        "AI-driven metadata governance ensures full compliance (5)"], key="mm2")
        if st.button("Next"):
            st.session_state.mm2_response = mm2
            st.session_state.current_question = 3

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
            st.session_state.current_question = 1
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
            st.session_state.current_question = 2

    elif st.session_state.current_question == 2:
        di2 = st.radio("2️⃣ **How frequently does your organization update and synchronize data across different platforms?**",
                       ["Never (1)",
                        "Occasionally with manual intervention (2)",
                        "Automated updates on a scheduled basis (3)",
                        "Near real-time synchronization (4)",
                        "AI-driven, self-healing data synchronization (5)"], key="di2")
        if st.button("Next"):
            st.session_state.di2_response = di2
            st.session_state.current_question = 3

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
            st.session_state.current_question = 1
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
            st.session_state.current_question = 2

    elif st.session_state.current_question == 2:
        ai2 = st.radio("2️⃣ **How is machine learning used in your organization?**",
                       ["Not used at all (1)",
                        "Basic experiments without production deployment (2)",
                        "Some predictive models used in decision-making (3)",
                        "Machine learning models are embedded in core processes (4)",
                        "AI-driven automation and decision intelligence across the business (5)"], key="ai2")
        if st.button("Next"):
            st.session_state.ai2_response = ai2
            st.session_state.current_question = 3

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
            st.session_state.current_question = 1
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
            st.session_state.current_question = 2

    elif st.session_state.current_question == 2:
        sp2 = st.radio("2️⃣ **Does your organization comply with data protection regulations (e.g., GDPR, HIPAA, Kenya Data Protection Act)?**",
                       ["No compliance efforts (1)",
                        "Minimal awareness, but no formal compliance (2)",
                        "Compliance policies exist but are inconsistently followed (3)",
                        "Fully compliant with regular audits (4)",
                        "Continuous compliance monitoring and automated reporting (5)"], key="sp2")
        if st.button("Next"):
            st.session_state.sp2_response = sp2
            st.session_state.current_question = 3

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
            st.session_state.current_question = 1
            st.success("✅ Data Security & Privacy responses submitted! Assessment complete.")
            st.session_state.all_sections_completed = True

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

# ✅ Function to Generate PDF Report
def generate_pdf_report(maturity_level, weighted_avg_score, recommendation, weighted_scores, insights, current_capabilities, recommendations, roadmap):
    pdf = FPDF()
    pdf.add_page()

    # Use a built-in font (e.g., Arial or Helvetica)
    pdf.set_font("Arial", size=12)

    # Add Virtual Analytics logo
    logo_path = "logo.png"  # Ensure the logo file is in the same directory
    pdf.image(logo_path, x=50, w=100)  # Center the logo and set width to 100
    pdf.ln(20)  # Add some space after the logo

    # Add title
    pdf.set_font("Arial", "B", 16)  # Bold and larger font for the title
    pdf.cell(200, 10, txt="The Virtual Narrative: Data Maturity Assessment Report", ln=True, align="C")
    pdf.ln(10)  # Add some space after the title

    # Add maturity level and score
    pdf.set_font("Arial", "B", 14)  # Bold for section titles
    pdf.cell(200, 10, txt="Maturity Level and Score", ln=True)
    pdf.set_font("Arial", size=12)  # Regular font for content
    pdf.cell(200, 10, txt=f"Your organization's data maturity level is: {maturity_level.replace('🔴', 'Initial/Ad Hoc').replace('🟠', 'Developing').replace('🟡', 'Defined').replace('🟢', 'Managed').replace('🔵', 'Optimized')}", ln=True)
    pdf.cell(200, 10, txt=f"Weighted Average Maturity Score: {weighted_avg_score:.2f}/5", ln=True)
    pdf.cell(200, 10, txt=f"Recommendation: {recommendation}", ln=True)
    pdf.ln(10)  # Add some space after the section

    # Add weighted scores breakdown
    pdf.set_font("Arial", "B", 14)  # Bold for section titles
    pdf.cell(200, 10, txt="Breakdown by Category (Weighted Scores)", ln=True)
    pdf.set_font("Arial", size=12)  # Regular font for content
    for category, score in weighted_scores.items():
        pdf.cell(200, 10, txt=f"{category}: {score:.2f}/5", ln=True)
    pdf.ln(10)  # Add some space after the section

    # Add AI-driven insights
    pdf.set_font("Arial", "B", 14)  # Bold for section titles
    pdf.cell(200, 10, txt="AI-Driven Insights", ln=True)
    pdf.set_font("Arial", size=12)  # Regular font for content
    for insight in insights:
        pdf.multi_cell(200, 10, txt=f"- {insight.replace('🔴', 'Initial/Ad Hoc').replace('🟠', 'Developing').replace('🟡', 'Defined').replace('🟢', 'Managed').replace('🔵', 'Optimized')}", align="L")
    pdf.ln(10)  # Add some space after the section

    # Add current analytics capabilities
    pdf.set_font("Arial", "B", 14)  # Bold for section titles
    if maturity_level in ["🔴 Initial/Ad Hoc", "🟠 Developing"]:
        pdf.set_text_color(255, 0, 0)  # Red for lower maturity levels
    else:
        pdf.set_text_color(0, 128, 0)  # Green for higher maturity levels
    pdf.cell(200, 10, txt="Current Analytics Capabilities", ln=True)
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.set_font("Arial", size=12)  # Regular font for content
    for capability in current_capabilities["capabilities"]:
        # Split the capability into type and description
        capability_type, capability_desc = capability.split(":", 1)
        pdf.set_font("Arial", "B", 12)  # Bold for capability type
        pdf.cell(200, 10, txt=f"- {capability_type}:", ln=True)
        pdf.set_font("Arial", size=12)  # Regular font for description
        pdf.multi_cell(200, 10, txt=f"  {capability_desc.strip()}", align="L")
    pdf.cell(200, 10, txt=f"Example: {current_capabilities['example']}", ln=True)
    pdf.ln(10)  # Add some space after the section

    # Add dynamic recommendations
    pdf.set_font("Arial", "B", 14)  # Bold for section titles
    pdf.cell(200, 10, txt="Recommendations for Improvement", ln=True)
    pdf.set_font("Arial", size=12)  # Regular font for content
    for rec in recommendations["recommendations"]:
        pdf.multi_cell(200, 10, txt=f"- {rec}", align="L")
    pdf.set_font("Arial", "B", 12)  # Bold for subheadings
    pdf.cell(200, 10, txt="Next Steps:", ln=True)
    pdf.set_font("Arial", size=12)  # Regular font for content
    for step in recommendations["next_steps"]:
        pdf.multi_cell(200, 10, txt=f"- {step}", align="L")
    pdf.ln(10)  # Add some space after the section

    # Add roadmap
    pdf.set_font("Arial", "B", 14)  # Bold for section titles
    pdf.cell(200, 10, txt="Roadmap to Higher Maturity Levels", ln=True)
    pdf.set_font("Arial", size=12)  # Regular font for content
    for stage, details in roadmap.items():
        pdf.set_font("Arial", "B", 12)  # Bold for subheadings
        pdf.cell(200, 10, txt=f"{stage}:", ln=True)
        pdf.set_font("Arial", size=12)  # Regular font for content
        for capability in details["capabilities"]:
            # Split the capability into type and description
            capability_type, capability_desc = capability.split(":", 1)
            pdf.set_font("Arial", "B", 12)  # Bold for capability type
            pdf.cell(200, 10, txt=f"- {capability_type}:", ln=True)
            pdf.set_font("Arial", size=12)  # Regular font for description
            pdf.multi_cell(200, 10, txt=f"  {capability_desc.strip()}", align="L")
        pdf.cell(200, 10, txt=f"Example: {details['example']}", ln=True)
    pdf.ln(10)  # Add some space after the section

    # Add a concluding note
    pdf.set_font("Arial", "I", 12)  # Italic for the concluding note
    pdf.cell(200, 10, txt="Thank you for using The Virtual Narrative: Data Maturity Assessment Tool!", ln=True, align="C")
    pdf.ln(10)  # Add some space after the note

    # Add a creative call to action
    pdf.set_font("Arial", "B", 14)  # Bold for the call to action
    pdf.set_text_color(0, 0, 255)  # Blue for emphasis
    pdf.cell(200, 10, txt="Need a Helping Hand Across the Chasm to Data Maturity?", ln=True, align="C")
    pdf.set_font("Arial", size=12)  # Regular font for content
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.cell(200, 10, txt="Embarking on the journey to data maturity can be challenging, but you don't have to do it alone.", ln=True, align="C")
    pdf.cell(200, 10, txt="Reach out to us for expert guidance and support:", ln=True, align="C")
    pdf.set_font("Arial", "B", 12)  # Bold for contact details
    pdf.cell(200, 10, txt="Virtual Analytics", ln=True, align="C")
    pdf.cell(200, 10, txt="www.virtualanalytics.co.ke | info@virtualanalytics.co.ke", ln=True, align="C")
    pdf.set_font("Arial", size=12)  # Regular font for content
    pdf.cell(200, 10, txt="Let us help you unlock the full potential of your data!", ln=True, align="C")

    # Save the PDF
    pdf.output("data_maturity_report.pdf")

# ✅ Function to Send Email with PDF Attachment
def send_email_with_pdf(receiver_email, pdf_path):
    """Send an email with the PDF report attached."""
    sender_email = "your_email@gmail.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your email password

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Your Data Maturity Assessment Report"

    # Attach the PDF
    with open(pdf_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(pdf_path)}",
        )
        msg.attach(part)

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        st.success("📧 Email sent successfully! Check your inbox.")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# ✅ Display Data Maturity Score after all sections are completed
if st.session_state.all_sections_completed:
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

    # Add a button to send the report via email
    if st.button("Send Report via Email"):
        send_email_with_pdf(st.session_state.user_email, "data_maturity_report.pdf")

    st.success("🎉 Congratulations on completing The Virtual Narrative: Data Maturity Assessment!")
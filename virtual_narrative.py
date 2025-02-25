import streamlit as st
import re  # Import regex for extracting numeric scores
import pandas as pd  # Import pandas for DataFrame representation
import plotly.graph_objects as go  # For the gauge chart

st.markdown(
    """
    <style>
        header {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Display Logo & Title (Only Once)
st.image("logo.png", width=250)  # Adjust width as needed
st.title("The Virtual Narrative: Data Maturity Assessment Tool")
st.write("Welcome to 'The Virtual Narrative' – an interactive tool to assess your organization's data maturity.")

# ✅ Initialize Session State Variables (Only Once)
session_defaults = {
    "start_assessment": False,
    "data_governance_complete": False,
    "data_quality_complete": False,
    "metadata_management_complete": False,
    "data_integration_complete": False,
    "data_analytics_complete": False,
    "data_security_complete": False
}
for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ✅ User Information Collection (Only Once, Avoiding Duplicate Keys)
st.write("### 📝 Let's get started by knowing you!")

first_name = st.text_input("Enter your First Name:", key="user_first_name")
last_name = st.text_input("Enter your Last Name:", key="user_last_name")
email = st.text_input("Enter your Email Address:", key="user_email")
org_name = st.text_input("Enter your Organization Name:", key="user_org_name")
business_unit = st.text_input("Which Business Unit do you work in?", key="user_business_unit")

# ✅ Start Assessment Button
if st.button("Start Assessment"):
    if not first_name or not last_name or not email:
        st.error("⚠️ Please fill in all required fields!")
    else:
        st.session_state.start_assessment = True
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

progress = calculate_progress()

st.progress(progress)  # Show progress bar
st.write(f"🟢 **Progress: {progress}% Complete**")

# 🏛️ **SECTION 1: DATA GOVERNANCE**
if st.session_state.start_assessment and not st.session_state.data_governance_complete:
    st.write("## 🏛️ Section 1: Data Governance")
    st.write("This section assesses how well data governance is established in your organization.")

    # ✅ Store values correctly without modifying session_state
    gov_q1 = st.radio("1️⃣ **Does your organization have a formal Data Governance policy?**",
                      ["No governance exists (1)",
                       "Some informal rules, but not enforced (2)",
                       "Formal governance in place, but not consistently followed (3)",
                       "Governance is standardized and monitored (4)",
                       "Governance is automated, AI-driven, and continuously optimized (5)"], key="gov_q1")

    # Conditional flow based on governance policy answer
    if gov_q1 != "No governance exists (1)":
        gov_q2 = st.radio("2️⃣ **Are roles and responsibilities clearly defined? (e.g., Data Stewards, Chief Data Officer)?**",
                          ["No defined roles (1)",
                           "Some responsibilities exist but unclear (2)",
                           "Defined roles exist, but accountability is weak (3)",
                           "Roles are well-defined and monitored (4)",
                           "Governance roles are optimized and continuously improved (5)"], key="gov_q2")

        gov_q3 = st.radio("3️⃣ **How frequently is your Data Governance policy reviewed and updated?**",
                          ["Never (1)",
                           "Ad-hoc updates with no schedule (2)",
                           "Reviewed every few years (3)",
                           "Reviewed annually (4)",
                           "Continuously improved with data-driven feedback (5)"], key="gov_q3")

    if st.button("Submit Governance Responses"):
        st.session_state.data_governance_complete = True
        st.success("✅ Responses recorded! Moving to the next section.")

# 📊 **SECTION 2: DATA QUALITY**
if st.session_state.data_governance_complete and not st.session_state.data_quality_complete:
    st.write("## 📊 Section 2: Data Quality")
    st.write("This section evaluates how well your organization maintains **accurate, complete, and reliable data**.")

    # ✅ Store values correctly without modifying session_state
    dq1 = st.radio("1️⃣ **How does your organization ensure data accuracy?**",
                   ["No process for accuracy (1)",
                    "Basic manual checks (2)",
                    "Defined validation rules (3)",
                    "Automated quality checks (4)",
                    "AI-powered real-time monitoring (5)"], key="dq1")

    # Conditional flow based on data accuracy
    if dq1 != "No process for accuracy (1)":
        dq2 = st.radio("2️⃣ **How is data completeness ensured in your organization?**",
                       ["No strategy in place (1)",
                        "Manual data entry reviews (2)",
                        "Automated missing value checks (3)",
                        "Proactive data validation (4)",
                        "Machine learning-driven data integrity (5)"], key="dq2")

    if dq1 != "No process for accuracy (1)" and dq2 != "No strategy in place (1)":
        dq3 = st.radio("3️⃣ **How consistently is data updated and synchronized across systems?**",
                       ["No updates, data silos exist (1)",
                        "Periodic manual updates (2)",
                        "Automated scheduled updates (3)",
                        "Real-time data sync (4)",
                        "Self-healing, AI-driven consistency (5)"], key="dq3")

    if st.button("Submit Data Quality Responses"):
        st.session_state.data_quality_complete = True
        st.success("✅ Data Quality responses submitted! Moving to Metadata Management.")

# 🏷 **SECTION 3: METADATA MANAGEMENT**
if st.session_state.data_quality_complete and not st.session_state.metadata_management_complete:
    st.write("## 🏷 Section 3: Metadata Management")
    st.write("This section evaluates how well your organization manages **metadata, including data definitions, lineage, and classification.**")

    # ✅ Store values correctly without modifying session_state
    mm1 = st.radio("1️⃣ **Does your organization maintain a centralized metadata repository?**",
                   ["No metadata repository exists (1)",
                    "Some metadata exists in scattered documentation (2)",
                    "A structured metadata catalog is available (3)",
                    "A centralized metadata repository is maintained (4)",
                    "Fully automated metadata management with AI-driven lineage tracking (5)"], key="mm1")

    # Conditional flow based on metadata repository
    if mm1 != "No metadata repository exists (1)":
        mm2 = st.radio("2️⃣ **How well-defined and standardized are your data definitions?**",
                       ["No definitions exist (1)",
                        "Ad-hoc definitions in some areas (2)",
                        "Standardized definitions exist but not enforced (3)",
                        "Organization-wide metadata standards are enforced (4)",
                        "AI-driven metadata governance ensures full compliance (5)"], key="mm2")

    if mm1 != "No metadata repository exists (1)" and mm2 != "No definitions exist (1)":
        mm3 = st.radio("3️⃣ **How is data lineage tracked in your organization?**",
                       ["No lineage tracking (1)",
                        "Basic manual lineage documentation (2)",
                        "Automated lineage tracking for some systems (3)",
                        "Comprehensive automated lineage tracking (4)",
                        "AI-driven lineage tracking with real-time anomaly detection (5)"], key="mm3")

    if st.button("Submit Metadata Management Responses"):
        st.session_state.metadata_management_complete = True
        st.success("✅ Metadata Management responses submitted! Moving to Data Integration.")
    
    # 🔗 **SECTION 4: DATA INTEGRATION**
if st.session_state.data_governance_complete and not st.session_state.data_integration_complete:
    st.write("## 🔗 Section 4: Data Integration")
    st.write("This section evaluates how well data is integrated across your organization, ensuring seamless interoperability.")

    # ✅ Store values correctly without modifying `session_state`
    di1 = st.radio("1️⃣ **How does your organization handle data integration between different systems?**",
                   ["No integration exists (1)",
                    "Manual data transfers (2)",
                    "Basic ETL processes in place (3)",
                    "Automated API-based data flows (4)",
                    "Real-time AI-driven integration across platforms (5)"], key="di1")

    # Conditional flow based on integration status
    if di1 != "No integration exists (1)":
        di2 = st.radio("2️⃣ **How frequently does your organization update and synchronize data across different platforms?**",
                       ["Never (1)",
                        "Occasionally with manual intervention (2)",
                        "Automated updates on a scheduled basis (3)",
                        "Near real-time synchronization (4)",
                        "AI-driven, self-healing data synchronization (5)"], key="di2")

    if di1 != "No integration exists (1)" and di2 != "Never (1)":
        di3 = st.radio("3️⃣ **Does your organization utilize cloud-based data integration platforms?**",
                       ["No cloud integration (1)",
                        "Limited use of cloud data storage (2)",
                        "Some cloud integration but no automation (3)",
                        "Fully automated cloud-based integration (4)",
                        "AI-optimized multi-cloud integration (5)"], key="di3")

    if st.button("Submit Data Integration Responses"):
        st.session_state.data_integration_complete = True
        st.success("✅ Data Integration responses submitted! Moving to Data Analytics & AI.")

# 📊 **SECTION 5: DATA ANALYTICS & AI**
if st.session_state.data_integration_complete and not st.session_state.data_analytics_complete:
    st.write("## 📊 Section 5: Data Analytics & AI")
    st.write("This section assesses your organization's ability to leverage data analytics and AI for decision-making.")

    # ✅ Store values correctly without modifying `session_state`
    ai1 = st.radio("1️⃣ **What is the level of adoption of business intelligence and reporting in your organization?**",
                   ["No formal reporting (1)",
                    "Basic manual reports with spreadsheets (2)",
                    "Automated dashboards with static reports (3)",
                    "Interactive BI tools with real-time data (4)",
                    "AI-driven predictive analytics and self-service BI (5)"], key="ai1")

    # Conditional flow based on AI adoption
    if ai1 != "No formal reporting (1)":
        ai2 = st.radio("2️⃣ **How is machine learning used in your organization?**",
                       ["Not used at all (1)",
                        "Basic experiments without production deployment (2)",
                        "Some predictive models used in decision-making (3)",
                        "Machine learning models are embedded in core processes (4)",
                        "AI-driven automation and decision intelligence across the business (5)"], key="ai2")

        # Only show ai3 if ai2 is not "Not used at all (1)"
        if ai2 != "Not used at all (1)":
            ai3 = st.radio("3️⃣ **How well is AI governance and ethics considered in your organization?**",
                           ["No AI governance in place (1)",
                            "Basic awareness but no formal guidelines (2)",
                            "AI policies exist but are inconsistently followed (3)",
                            "AI governance is well-defined and monitored (4)",
                            "AI ethics, bias detection, and compliance are actively managed (5)"], key="ai3")

    if st.button("Submit Data Analytics & AI Responses"):
        st.session_state.data_analytics_complete = True
        st.success("✅ Data Analytics & AI responses submitted! Moving to Data Security & Privacy.")

# 🔒 **SECTION 6: DATA SECURITY & PRIVACY**
if st.session_state.data_analytics_complete and not st.session_state.data_security_complete:
    st.write("## 🔒 Section 6: Data Security & Privacy")
    st.write("This section evaluates how well your organization ensures data security, privacy, and compliance with regulations.")

    # ✅ Store values correctly without modifying `session_state`
    sp1 = st.radio("1️⃣ **How is access to sensitive data controlled in your organization?**",
                   ["No access control (1)",
                    "Basic password protection (2)",
                    "Role-based access control (RBAC) in place (3)",
                    "Multi-factor authentication and encryption (4)",
                    "Zero-trust security model with continuous monitoring (5)"], key="sp1")

    # Conditional flow based on data security policies
    if sp1 != "No access control (1)":
        sp2 = st.radio("2️⃣ **Does your organization comply with data protection regulations (e.g., GDPR, HIPAA, Kenya Data Protection Act)?**",
                       ["No compliance efforts (1)",
                        "Minimal awareness, but no formal compliance (2)",
                        "Compliance policies exist but are inconsistently followed (3)",
                        "Fully compliant with regular audits (4)",
                        "Continuous compliance monitoring and automated reporting (5)"], key="sp2")

        # Only show sp3 if sp2 is not "No compliance efforts (1)"
        if sp2 != "No compliance efforts (1)":
            sp3 = st.radio("3️⃣ **How well does your organization handle data encryption and secure storage?**",
                           ["No encryption (1)",
                            "Basic encryption for some data (2)",
                            "Encryption used for sensitive data (3)",
                            "Industry-standard encryption applied across systems (4)",
                            "End-to-end encryption with automated security updates (5)"], key="sp3")

    if st.button("Submit Data Security & Privacy Responses"):
        st.session_state.data_security_complete = True
        st.success("✅ Data Security & Privacy responses submitted! Assessment complete.")

# Function to create the gauge chart
def create_gauge_chart(score):
    # Define the gauge chart
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

# ✅ Function to Extract Numeric Scores from Responses
def extract_score(response):
    """Extract numeric score from the selected response."""
    match = re.search(r"\((\d+)\)", response)  # Look for a number inside parentheses
    return int(match.group(1)) if match else 1  # Default to 1 if no match

# ✅ Retrieve Scores Using extract_score() Only If At Least One Section is Completed
if any([
    st.session_state.data_governance_complete,
    st.session_state.data_quality_complete,
    st.session_state.metadata_management_complete,
    st.session_state.data_integration_complete,
    st.session_state.data_analytics_complete,
    st.session_state.data_security_complete
]):
    # Calculate the average maturity score
    scores = {
        "Data Governance": extract_score(st.session_state.get("gov_q1", " (1)")),
        "Data Quality": extract_score(st.session_state.get("dq1", " (1)")),
        "Metadata Management": extract_score(st.session_state.get("mm1", " (1)")),
        "Data Integration": extract_score(st.session_state.get("di1", " (1)")),
        "Data Analytics & AI": extract_score(st.session_state.get("ai1", " (1)")),
        "Data Security & Privacy": extract_score(st.session_state.get("sp1", " (1)"))
    }

    # ✅ Calculate the average maturity score (between 1 and 5)
    avg_score = sum(scores.values()) / len(scores)

    # ✅ Create and display the gauge chart
    st.plotly_chart(create_gauge_chart(avg_score))

    # ✅ Determine Maturity Level & Recommendations
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

    # ✅ Display the score and recommendation
    st.write(f"### 🎯 Your Organization's Maturity Level: {maturity_level}")
    st.write(f"📊 **Average Maturity Score:** {avg_score:.2f}/5")
    st.write(f"💡 **Recommendation:** {recommendation}")

    # ✅ Display Individual Scores Breakdown
    st.write("### 📌 Breakdown by Category")
    for category, score in scores.items():
        st.write(f"✅ **{category}**: {score}/5")

    st.success("🎉 Congratulations on completing The Virtual Narrative: Data Maturity Assessment!")

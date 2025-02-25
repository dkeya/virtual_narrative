import streamlit as st

# Set the title and description
st.title("The Virtual Narrative: Data Maturity Assessment Tool")
st.subheader("🚀 Assess your organization's data maturity and get actionable insights!")

# User Information Collection
st.write("### 📝 Let's get started by knowing you!")
first_name = st.text_input("Enter your First Name:")
last_name = st.text_input("Enter your Last Name:")
email = st.text_input("Enter your Email Address:")
org_name = st.text_input("Enter your Organization Name:")
business_unit = st.text_input("Which Business Unit do you work in?")

# Start Assessment Button
if st.button("Start Assessment"):
    if not first_name or not last_name or not email:
        st.error("⚠️ Please fill in all required fields!")
    else:
        st.success(f"Great, {first_name}! Let's begin your Data Maturity Assessment.")

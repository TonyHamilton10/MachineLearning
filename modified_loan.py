import streamlit as st
import numpy as np
import joblib
import time

# Page config
st.set_page_config(
    page_title="Loan Approval System",
    page_icon="💼",
    layout="wide"
)

# Custom CSS for animations
st.markdown("""
<style>
/* Fade-in animation */
.fade-in {
    animation: fadeIn 1.2s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Button styling */
.stButton>button {
    background-color: #2E86C1;
    color: white;
    border-radius: 8px;
    padding: 0.6em 1.2em;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #1B4F72;
    transform: scale(1.05);
}

/* Card style */
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f8f9fa;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# Load model
model = joblib.load('randomfReg.pkl')

# Header
st.markdown("<h1 class='fade-in' style='text-align: center;'>💼 Loan Approval Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<p class='fade-in' style='text-align: center; color: grey;'>Estimate loan eligibility using financial data</p>", unsafe_allow_html=True)

st.divider()

# Sidebar inputs
st.sidebar.header("📊 Applicant Information")

age = st.sidebar.number_input('Age', min_value=18, value=25)
creditscore = st.sidebar.number_input('Credit Score', min_value=300, max_value=850, value=650)
monthlydebtpayment = st.sidebar.number_input('Monthly Debt ($)', value=200)
monthlyIncome = st.sidebar.number_input('Monthly Income ($)', value=2000)
monthlyLoanPayment = st.sidebar.number_input('Loan Payment ($)', value=150.0)
riskscore = st.sidebar.number_input('Risk Score', value=30.0)

st.divider()

# Layout
col1, col2 = st.columns(2)

# Input summary with animation
with col1:
    st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)
    st.subheader("📌 Applicant Summary")
    st.write(f"**Age:** {age}")
    st.write(f"**Credit Score:** {creditscore}")
    st.write(f"**Monthly Debt:** ${monthlydebtpayment:,.2f}")
    st.write(f"**Monthly Income:** ${monthlyIncome:,.2f}")
    st.write(f"**Loan Payment:** ${monthlyLoanPayment:,.2f}")
    st.write(f"**Risk Score:** {riskscore}")
    st.markdown("</div>", unsafe_allow_html=True)

# Prediction section with animation
with col2:
    st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)
    st.subheader("📈 Prediction")

    if st.button('🔍 Calculate Loan Amount'):

        # Progress animation
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        # Model prediction
        x = np.array([[age, creditscore, monthlydebtpayment,
                       monthlyIncome, monthlyLoanPayment, riskscore]])

        prediction = model.predict(x)[0]

        st.success(f"💰 Estimated Loan Amount: **${prediction:,.2f}**")

    else:
        st.info("Click the button to generate prediction")

    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# Footer
st.markdown("<p class='fade-in' style='text-align: center; color: grey;'>© 2026 Loan Analytics System</p>", unsafe_allow_html=True)
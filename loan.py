import streamlit as st 
import numpy as np 
import joblib

# Page configuration
st.set_page_config(page_title="Loan Approval System", layout="wide", initial_sidebar_state="collapsed")

model = joblib.load('randomfReg.pkl')

# Custom CSS for professional styling
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 0;
    }
    
    .header-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px;
        border-radius: 0;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: slideDown 0.6s ease-out;
    }
    
    .header-section h1 {
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        animation: fadeInUp 0.8s ease-out;
    }
    
    .header-section p {
        font-size: 1.1em;
        opacity: 0.95;
        animation: fadeInUp 1s ease-out;
    }
    
    .card-container {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        animation: slideUp 0.6s ease-out;
    }
    
    .card-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .input-group {
        margin-bottom: 20px;
    }
    
    .input-label {
        font-weight: 600;
        color: #333;
        display: block;
        margin-bottom: 8px;
        font-size: 0.95em;
    }
    
    .form-section {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .form-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #f0f4ff 100%);
        border: 2px solid #e0e7ff;
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    .form-card:hover {
        border-color: #667eea;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.15);
    }
    
    .button-container {
        display: flex;
        justify-content: center;
        margin: 30px 0;
        animation: fadeIn 1.2s ease-out;
    }
    
    .predict-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 50px;
        font-size: 1.1em;
        font-weight: 600;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .predict-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
    }
    
    .predict-button:active {
        transform: translateY(0px);
    }
    
    .result-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: scaleIn 0.6s ease-out;
    }
    
    .result-container h2 {
        font-size: 1.5em;
        margin-bottom: 15px;
        opacity: 0.9;
    }
    
    .result-amount {
        font-size: 3em;
        font-weight: 700;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }
    
    .stat-card {
        background: white;
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateX(5px);
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9em;
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .stat-value {
        color: #667eea;
        font-size: 1.8em;
        font-weight: 700;
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 30px 0;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .info-box {
        background: linear-gradient(135deg, #e0e7ff 0%, #f0f4ff 100%);
        border-left: 4px solid #667eea;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 20px 0;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="header-section">
    <h1>💰 Loan Amount Approval System</h1>
    <p>Advanced ML-Powered Loan Estimation</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Information Box
st.markdown("""
<div class="info-box">
    <strong>ℹ️ How it works:</strong> Enter your financial details below and our machine learning model will estimate your loan amount eligibility.
</div>
""", unsafe_allow_html=True)

# Main Content
st.markdown('<div class="card-container">', unsafe_allow_html=True)
st.markdown('<h2 style="color: #333; margin-bottom: 25px;">📋 Applicant Information</h2>', unsafe_allow_html=True)

# Form in a grid layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<label class="input-label">👤 Applicant Age</label>', unsafe_allow_html=True)
    age = st.number_input('Age', value=18, step=1, label_visibility="collapsed", key="age")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<label class="input-label">📊 Credit Score</label>', unsafe_allow_html=True)
    creditscore = st.number_input('Credit Score', value=343, step=5, label_visibility="collapsed", key="credit")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<label class="input-label">💳 Risk Score</label>', unsafe_allow_html=True)
    riskscore = st.number_input('Risk Score', value=28.80, step=1.0, label_visibility="collapsed", key="risk")
    st.markdown('</div>', unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<label class="input-label">📈 Monthly Income</label>', unsafe_allow_html=True)
    monthlyIncome = st.number_input('Monthly Income', value=1250, step=100, label_visibility="collapsed", key="income")
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<label class="input-label">💰 Monthly Debt Payments</label>', unsafe_allow_html=True)
    monthlydebtpayment = st.number_input('Monthly Debts', value=50, step=50, label_visibility="collapsed", key="debt")
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<label class="input-label">📋 Monthly Loan Payment</label>', unsafe_allow_html=True)
    monthlyLoanPayment = st.number_input('Monthly Loan Payment', value=97.03, step=1.0, label_visibility="collapsed", key="loan")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Button Section
st.markdown('<div class="button-container">', unsafe_allow_html=True)
st.markdown('<div style="display: flex; gap: 10px; justify-content: center;">', unsafe_allow_html=True)
prediction_clicked = st.button('🚀 Calculate Loan Amount', use_container_width=False, key="predict_btn")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Prepare data
X = [age, creditscore, monthlydebtpayment, monthlyIncome, monthlyLoanPayment, riskscore]

# Display Results
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if prediction_clicked:
    x1 = np.array(X)
    prediction = model.predict([x1])
    
    # Result Section with Animation
    st.markdown("""
    <div class="result-container">
        <h2>✅ Loan Estimation Result</h2>
        <div class="result-amount">
            ${:,.2f}
        </div>
        <p style="margin-top: 15px; font-size: 1.1em; opacity: 0.9;">Estimated Loan Amount to be Disbursed</p>
    </div>
    """.format(prediction[0]), unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
    
    # Display Summary Stats
    st.markdown('<h3 style="color: #333; margin-bottom: 20px;">📊 Your Application Summary</h3>', unsafe_allow_html=True)
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Monthly Income</div>
            <div class="stat-value">${monthlyIncome:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Credit Score</div>
            <div class="stat-value">{creditscore}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Risk Score</div>
            <div class="stat-value">{riskscore:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 40px; color: #666;">
        <p style="font-size: 1.2em;">👆 Click the button above to calculate your estimated loan amount</p>
    </div>
    """, unsafe_allow_html=True)

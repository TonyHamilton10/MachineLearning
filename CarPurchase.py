import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os
from datetime import datetime

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title='Car Purchase Price Estimator',
    page_icon='🚗',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ===== PROFESSIONAL CSS STYLING =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* ===== HEADER STYLING ===== */
    .header-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        margin-bottom: 30px;
        animation: slideDown 0.8s ease;
    }
    
    .header-title {
        font-size: 2.8em;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        letter-spacing: 0.5px;
    }
    
    .header-subtitle {
        font-size: 1.1em;
        color: rgba(255, 255, 255, 0.95);
        margin: 10px 0 0 0;
        font-weight: 300;
    }
    
    /* ===== INPUT SECTION STYLING ===== */
    .input-section {
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        margin-bottom: 25px;
        border-top: 4px solid #1e3c72;
    }
    
    .section-title {
        font-size: 1.4em;
        font-weight: 700;
        color: #333;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #1e3c72;
        letter-spacing: 0.3px;
    }
    
    .input-label {
        font-size: 1em;
        font-weight: 600;
        color: #555;
        margin-bottom: 8px;
        display: block;
    }
    
    .input-hint {
        font-size: 0.85em;
        color: #999;
        margin-top: 5px;
        font-style: italic;
    }
    
    /* ===== RESULT CARD STYLING ===== */
    .result-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 15px 50px rgba(30, 60, 114, 0.3);
        animation: scaleIn 0.6s ease;
        color: white;
    }
    
    .result-label {
        font-size: 1.1em;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 15px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .result-price {
        font-size: 3.2em;
        font-weight: 800;
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        margin: 15px 0;
    }
    
    .price-currency {
        font-size: 0.6em;
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* ===== METRIC CARD ===== */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        text-align: center;
        border-top: 3px solid #1e3c72;
    }
    
    .metric-icon {
        font-size: 2em;
        margin-bottom: 10px;
    }
    
    .metric-label {
        font-size: 0.9em;
        color: #999;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 1.8em;
        font-weight: 700;
        color: #1e3c72;
    }
    
    /* ===== INFO CARDS ===== */
    .info-card {
        background: #f0f4ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1e3c72;
        margin-bottom: 15px;
    }
    
    .info-label {
        font-weight: 600;
        color: #1e3c72;
        margin-bottom: 5px;
        font-size: 0.95em;
    }
    
    .info-value {
        color: #555;
        font-size: 0.9em;
    }
    
    /* ===== ANIMATIONS ===== */
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
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    /* ===== SIDEBAR STYLING ===== */
    .sidebar-header {
        font-size: 1.2em;
        font-weight: 700;
        color: #1e3c72;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #1e3c72;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        margin-top: 50px;
        padding-top: 30px;
        border-top: 2px solid #e0e0e0;
        text-align: center;
        color: #999;
        font-size: 0.9em;
    }
    
    .footer-text {
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ===== LOAD MODELS WITH ERROR HANDLING =====
@st.cache_resource
def load_models():
    """Load the pre-trained scaler and model"""
    try:
        if not os.path.exists('scaler.pkl'):
            st.error("❌ Scaler file not found: 'scaler.pkl'")
            return None, None
        if not os.path.exists('linear.pkl'):
            st.error("❌ Model file not found: 'linear.pkl'")
            return None, None
            
        scaler = joblib.load('scaler.pkl')
        model = joblib.load('linear.pkl')
        return scaler, model
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        return None, None

# Load models
scaler, model = load_models()

if scaler is None or model is None:
    st.error("❌ **Unable to load required models.** Please ensure 'scaler.pkl' and 'linear.pkl' exist in the current directory.")
    st.stop()

# ===== INITIALIZE SESSION STATE =====
if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []

# ===== HEADER SECTION =====
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🚗 Car Purchase Price Estimator</h1>
    <p class="header-subtitle">Advanced ML-Powered Vehicle Valuation & Recommendation System</p>
</div>
""", unsafe_allow_html=True)

# ===== MODEL INFO SIDEBAR =====
with st.sidebar:
    st.markdown('<div class="sidebar-header">ℹ️ Model Information</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <div class="info-label">🤖 Model Type</div>
        <div class="info-value">Linear Regression</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <div class="info-label">📊 Features Used</div>
        <div class="info-value">Age, Salary, Net Worth</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <div class="info-label">🎯 Purpose</div>
        <div class="info-value">Budget-Based Vehicle Suggestion</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <div class="info-label">⏱️ Last Updated</div>
        <div class="info-value">2026-05-09</div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.predictions_history) > 0:
        st.markdown("""
        <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #e0e0e0;">
            <div class="sidebar-header">📋 Estimation History</div>
        </div>
        """, unsafe_allow_html=True)
        
        for i, pred in enumerate(st.session_state.predictions_history[-5:], 1):
            st.markdown(f"""
            <div class="info-card">
                <div class="info-label">Estimate #{i}</div>
                <div class="info-value">${float(pred['price']):,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

# ===== MAIN INPUT SECTION =====
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">💰 Personal Financial Information</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<label class="input-label">👤 Your Age</label>', unsafe_allow_html=True)
    age = st.slider(
        'Age',
        min_value=16,
        max_value=100,
        value=40,
        step=1,
        label_visibility='collapsed',
        help='Select your age (16-100 years)'
    )
    st.markdown('<div class="input-hint">Typical range: 25-65 years</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<label class="input-label">💵 Annual Salary</label>', unsafe_allow_html=True)
    salary = st.slider(
        'Annual Salary',
        min_value=1000,
        max_value=1000000,
        value=50000,
        step=5000,
        label_visibility='collapsed',
        help='Select your annual salary'
    )
    st.markdown(f'<div class="input-hint">Current: ${salary:,}</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<label class="input-label">💎 Net Worth</label>', unsafe_allow_html=True)
    networth = st.slider(
        'Net Worth',
        min_value=0,
        max_value=5000000,
        value=100000,
        step=20000,
        label_visibility='collapsed',
        help='Select your net worth'
    )
    st.markdown(f'<div class="input-hint">Current: ${networth:,}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===== INPUT SUMMARY =====
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Your Financial Profile Summary</div>', unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">👤</div>
        <div class="metric-label">Age</div>
        <div class="metric-value">{age} yrs</div>
    </div>
    """, unsafe_allow_html=True)

with col_s2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">💵</div>
        <div class="metric-label">Annual Salary</div>
        <div class="metric-value">${salary/1000:.0f}K</div>
    </div>
    """, unsafe_allow_html=True)

with col_s3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">💎</div>
        <div class="metric-label">Net Worth</div>
        <div class="metric-value">${networth/1000:.0f}K</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===== CALCULATE BUTTON =====
col_pred1, col_pred2 = st.columns([1, 1])

with col_pred1:
    calculate_button = st.button(
        '🚀 Calculate Car Budget',
        use_container_width=True,
        key='calculate_btn',
        help='Click to estimate your ideal car purchase price'
    )

with col_pred2:
    if st.button('🔄 Clear History', use_container_width=True, help='Clear estimation history'):
        st.session_state.predictions_history = []
        st.rerun()

# ===== MAKE PREDICTION =====
if calculate_button:
    try:
        # Input validation
        if age < 16 or age > 100:
            st.error("❌ **Invalid Age:** Must be between 16 and 100 years.")
        elif salary <= 0 or networth < 0:
            st.error("❌ **Invalid Financial Data:** Salary and net worth must be positive.")
        else:
            # Prepare and scale input
            X = np.array([[age, salary, networth]])
            X_scaled = scaler.transform(X)
            
            # Make prediction
            prediction = model.predict(X_scaled)[0]
            
            # Ensure positive price
            if prediction < 0:
                prediction = 0
            
            # Store in history
            prediction_entry = {
                'age': age,
                'salary': salary,
                'networth': networth,
                'price': float(prediction),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            st.session_state.predictions_history.append(prediction_entry)
            
            # Display result
            st.markdown("""
            <div style="margin-top: 30px; animation: fadeIn 0.8s ease;">
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">🚗 RECOMMENDED CAR PURCHASE BUDGET</div>
                <div class="result-price">
                    <span class="price-currency">$</span>{float(prediction):,.0f}
                </div>
                <div style="font-size: 0.95em; color: rgba(255, 255, 255, 0.9); margin-top: 20px;">
                    Based on Age {age}, Salary ${salary:,}, Net Worth ${networth:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Price range analysis
            price_variation = prediction * 0.10  # 10% variation
            budget_min = max(0, prediction - price_variation)
            budget_max = prediction + price_variation
            
            # Financial recommendations
            affordable_percentage = (prediction / salary) * 100 if salary > 0 else 0
            
            st.markdown(f"""
            <div style="margin-top: 25px; padding: 20px; background: #f0f4ff; border-radius: 10px; border-left: 4px solid #1e3c72;">
                <p style="margin: 0; color: #1e3c72; font-weight: 600; margin-bottom: 15px;">📊 Smart Budget Recommendations</p>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                    <div>
                        <p style="margin: 0 0 5px 0; color: #999; font-size: 0.85em;">Conservative Budget (Low)</p>
                        <p style="margin: 0; color: #1e3c72; font-weight: 700; font-size: 1.3em;">${budget_min:,.0f}</p>
                    </div>
                    <div>
                        <p style="margin: 0 0 5px 0; color: #999; font-size: 0.85em;">Optimistic Budget (High)</p>
                        <p style="margin: 0; color: #1e3c72; font-weight: 700; font-size: 1.3em;">${budget_max:,.0f}</p>
                    </div>
                </div>
                
                <div style="background: white; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                    <p style="margin: 0; color: #666; font-size: 0.95em;">
                        <strong>💡 Financial Insight:</strong> Your recommended car purchase represents approximately <strong>{affordable_percentage:.1f}%</strong> of your annual salary.
                    </p>
                </div>
                
                <p style="margin: 0; font-size: 0.85em; color: #999; font-style: italic;">
                    ℹ️ Industry standard: Car cost should be 10-20% of annual salary for sustainable ownership.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Vehicle category suggestions
            if prediction < 15000:
                category = "Budget-Friendly Compact"
                examples = "Hyundai Elantra, Toyota Corolla, Honda Civic"
            elif prediction < 30000:
                category = "Mid-Range Sedan"
                examples = "Honda Accord, Toyota Camry, Mazda6"
            elif prediction < 50000:
                category = "Premium Sedan / Compact SUV"
                examples = "BMW 3 Series, Audi A4, Lexus ES"
            else:
                category = "Luxury / Performance Vehicle"
                examples = "BMW 5 Series, Mercedes-Benz E-Class, Audi A6"
            
            st.markdown(f"""
            <div style="margin-top: 20px; padding: 20px; background: white; border-radius: 10px; border: 2px solid #1e3c72;">
                <p style="margin: 0; color: #1e3c72; font-weight: 600; margin-bottom: 10px;">🎯 Vehicle Category Recommendation</p>
                <p style="margin: 0; color: #555; font-size: 0.95em;">
                    <strong>Category:</strong> {category}<br>
                    <strong>Example Models:</strong> {examples}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success(f"✅ **Calculation Complete** | Confidence Level: High | Model: Linear Regression")
            
    except Exception as e:
        st.error(f"❌ **Calculation Error:** {str(e)}")
        st.info("Please check your input values and try again.")
else:
    st.info("👆 **Adjust your financial information above and click 'Calculate Car Budget' to get your personalized vehicle purchase recommendation.**")

# ===== FOOTER =====
st.markdown("""
<div class="footer">
    <div class="footer-text"><strong>© 2026 Car Purchase Price Estimator</strong></div>
    <div class="footer-text">🚗 Intelligent Vehicle Valuation System | Powered by Machine Learning</div>
    <div class="footer-text" style="margin-top: 10px; font-size: 0.8em;">
        ⚠️ <em>Disclaimer: This estimation is based on historical data and machine learning models. Actual car prices depend on market conditions, vehicle condition, and regional variations.</em>
    </div>
</div>
""", unsafe_allow_html=True)
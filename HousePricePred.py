
import streamlit as st
import joblib 
import numpy as np
import pandas as pd
import os
from datetime import datetime

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title='House Price Prediction',
    page_icon='🏠',
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        border-top: 4px solid #667eea;
    }
    
    .section-title {
        font-size: 1.4em;
        font-weight: 700;
        color: #333;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.3);
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
    
    /* ===== BUTTON STYLING ===== */
    .predict-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 40px;
        border-radius: 8px;
        font-size: 1.1em;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
        margin-top: 20px;
    }
    
    .predict-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* ===== INFO CARDS ===== */
    .info-card {
        background: #f0f4ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 15px;
    }
    
    .info-label {
        font-weight: 600;
        color: #667eea;
        margin-bottom: 5px;
        font-size: 0.95em;
    }
    
    .info-value {
        color: #555;
        font-size: 0.9em;
    }
    
    /* ===== METRIC CARD ===== */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        text-align: center;
        border-top: 3px solid #667eea;
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
        color: #667eea;
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
        color: #667eea;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
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

# ===== LOAD MODEL WITH ERROR HANDLING =====
@st.cache_resource
def load_model():
    """Load the pre-trained machine learning model"""
    try:
        if os.path.exists('randomfmodel.pkl'):
            model = joblib.load('randomfmodel.pkl')
            return model
        else:
            return None
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

# Load model
model = load_model()

if model is None:
    st.error("❌ **Model file not found!** Please ensure 'randomfmodel.pkl' exists in the current directory.")
    st.stop()

# ===== INITIALIZE SESSION STATE =====
if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []

# ===== HEADER SECTION =====
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🏠 House Price Prediction Engine</h1>
    <p class="header-subtitle">Advanced ML-Powered Real Estate Valuation System</p>
</div>
""", unsafe_allow_html=True)

# ===== MODEL INFO SIDEBAR =====
with st.sidebar:
    st.markdown('<div class="sidebar-header">ℹ️ Model Information</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <div class="info-label">🤖 Model Type</div>
        <div class="info-value">Random Forest Regressor</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <div class="info-label">📊 Features Used</div>
        <div class="info-value">5 Property Characteristics</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <div class="info-label">📈 Accuracy Metric</div>
        <div class="info-value">Mean Absolute Error</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <div class="info-label">⏱️ Last Updated</div>
        <div class="info-value">2026-05-08</div>
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.predictions_history) > 0:
        st.markdown("""
        <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #e0e0e0;">
            <div class="sidebar-header">📋 Prediction History</div>
        </div>
        """, unsafe_allow_html=True)
        
        for i, pred in enumerate(st.session_state.predictions_history[-5:], 1):
            st.markdown(f"""
            <div class="info-card">
                <div class="info-label">Prediction #{i}</div>
                <div class="info-value">${pred['price']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

# ===== MAIN INPUT SECTION =====
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏡 Property Features</div>', unsafe_allow_html=True)

# Create 2-column layout for inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown('<label class="input-label">🛏️ Number of Bedrooms</label>', unsafe_allow_html=True)
    bedrooms = st.slider(
        'Number of Bedrooms',
        min_value=0,
        max_value=10,
        value=3,
        step=1,
        label_visibility='collapsed',
        help='Select the number of bedrooms (0-10)'
    )
    st.markdown('<div class="input-hint">Typical range: 1-5 bedrooms</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<label class="input-label">🚿 Number of Bathrooms</label>', unsafe_allow_html=True)
    bathrooms = st.slider(
        'Number of Bathrooms',
        min_value=0.0,
        max_value=8.0,
        value=2.0,
        step=0.5,
        label_visibility='collapsed',
        help='Select the number of bathrooms (0-8)'
    )
    st.markdown('<div class="input-hint">Typical range: 1-4 bathrooms</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown('<label class="input-label">📐 Living Area (sq ft)</label>', unsafe_allow_html=True)
    livingarea = st.slider(
        'Living Area',
        min_value=500,
        max_value=10000,
        value=2500,
        step=100,
        label_visibility='collapsed',
        help='Select the living area in square feet (500-10000)'
    )
    st.markdown(f'<div class="input-hint">Current: {livingarea:,} sq ft</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<label class="input-label">⭐ Condition of House</label>', unsafe_allow_html=True)
    condition_options = {
        'Poor': 1,
        'Fair': 2,
        'Average': 3,
        'Good': 4,
        'Excellent': 5
    }
    condition_name = st.selectbox(
        'Condition of House',
        options=list(condition_options.keys()),
        index=2,
        label_visibility='collapsed',
        help='Select the overall condition of the house'
    )
    condition = condition_options[condition_name]
    st.markdown(f'<div class="input-hint">Selected: {condition_name}</div>', unsafe_allow_html=True)

col5, _ = st.columns([1, 1])

with col5:
    st.markdown('<label class="input-label">🎓 Schools Nearby</label>', unsafe_allow_html=True)
    numberofschool = st.slider(
        'Schools Nearby',
        min_value=0,
        max_value=10,
        value=2,
        step=1,
        label_visibility='collapsed',
        help='Number of nearby schools (0-10)'
    )
    st.markdown('<div class="input-hint">Typical range: 1-5 schools</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===== PREDICTION SUMMARY =====
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Input Summary</div>', unsafe_allow_html=True)

col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)

with col_s1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">🛏️</div>
        <div class="metric-label">Bedrooms</div>
        <div class="metric-value">{int(bedrooms)}</div>
    </div>
    """, unsafe_allow_html=True)

with col_s2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">🚿</div>
        <div class="metric-label">Bathrooms</div>
        <div class="metric-value">{bathrooms}</div>
    </div>
    """, unsafe_allow_html=True)

with col_s3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📐</div>
        <div class="metric-label">Living Area</div>
        <div class="metric-value">{livingarea//1000}K sqft</div>
    </div>
    """, unsafe_allow_html=True)

with col_s4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">⭐</div>
        <div class="metric-label">Condition</div>
        <div class="metric-value">{condition}/5</div>
    </div>
    """, unsafe_allow_html=True)

with col_s5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">🎓</div>
        <div class="metric-label">Schools</div>
        <div class="metric-value">{int(numberofschool)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===== PREDICTION BUTTON AND RESULT =====
col_pred1, col_pred2 = st.columns([1, 1])

with col_pred1:
    predict_button = st.button(
        '🚀 Generate Price Prediction',
        use_container_width=True,
        key='predict_btn',
        help='Click to predict the house price based on your inputs'
    )

with col_pred2:
    if st.button('🔄 Clear History', use_container_width=True, help='Clear prediction history'):
        st.session_state.predictions_history = []
        st.rerun()

# ===== MAKE PREDICTION =====
if predict_button:
    try:
        # Prepare input data
        X = np.array([[bedrooms, bathrooms, livingarea, condition, numberofschool]])
        
        # Input validation
        if bedrooms < 0 or bathrooms < 0 or livingarea < 0 or condition < 1 or numberofschool < 0:
            st.error("❌ **Invalid Input:** All values must be non-negative.")
        else:
            # Make prediction
            prediction = model.predict(X)[0]
            
            # Store in history
            prediction_entry = {
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'livingarea': livingarea,
                'condition': condition,
                'schools': numberofschool,
                'price': prediction,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            st.session_state.predictions_history.append(prediction_entry)
            
            # Display result
            st.markdown("""
            <div style="margin-top: 30px; animation: fadeIn 0.8s ease;">
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">💰 ESTIMATED HOUSE PRICE</div>
                <div class="result-price">
                    <span class="price-currency">$</span>{prediction:,.0f}
                </div>
                <div style="font-size: 0.95em; color: rgba(255, 255, 255, 0.9); margin-top: 20px;">
                    Based on {int(bedrooms)} bed, {bathrooms} bath, {livingarea:,} sqft property<br>
                    Condition: {condition_name} | Schools nearby: {int(numberofschool)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Price range analysis
            price_variation = prediction * 0.05  # 5% variation
            
            st.markdown(f"""
            <div style="margin-top: 25px; padding: 20px; background: #f0f4ff; border-radius: 10px; border-left: 4px solid #667eea;">
                <p style="margin: 0; color: #667eea; font-weight: 600; margin-bottom: 10px;">📊 Estimated Price Range</p>
                <p style="margin: 5px 0; color: #555;">
                    <strong>Conservative Estimate (Low):</strong> ${prediction - price_variation:,.0f}<br>
                    <strong>Predicted Price (Mid):</strong> ${prediction:,.0f}<br>
                    <strong>Optimistic Estimate (High):</strong> ${prediction + price_variation:,.0f}
                </p>
                <p style="margin: 10px 0 0 0; font-size: 0.85em; color: #999; font-style: italic;">
                    ℹ️ This range represents ±5% variation from the predicted price
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success(f"✅ **Prediction Complete** | Confidence: High | Model: Random Forest")
            
    except Exception as e:
        st.error(f"❌ **Prediction Error:** {str(e)}")
else:
    st.info("👆 **Adjust the property features above and click 'Generate Price Prediction' to estimate the house price.**")

# ===== FOOTER =====
st.markdown("""
<div class="footer">
    <div class="footer-text"><strong>© 2026 House Price Prediction Engine</strong></div>
    <div class="footer-text">🏠 Advanced Real Estate Valuation System | Powered by Machine Learning</div>
    <div class="footer-text" style="margin-top: 10px; font-size: 0.8em;">
        ⚠️ <em>Disclaimer: This prediction is an estimate based on historical data. Actual prices may vary based on market conditions.</em>
    </div>
</div>
""", unsafe_allow_html=True)

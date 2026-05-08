import streamlit as st
import numpy as np
import joblib

# Load model
model = joblib.load('rf_model.pkl')

# Page config
st.set_page_config(
    page_title="Laptop Price Estimator",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Premium Laptop Price Estimation System v1.0"}
)

# Professional Custom Styling with Animations
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        /* Gradient Background */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #1a202c;
        }
        
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Header Styling */
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            margin-bottom: 30px;
            animation: slideInDown 0.6s ease-out;
        }
        
        .header-title {
            color: white;
            font-size: 2.8em;
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            letter-spacing: -1px;
        }
        
        .header-subtitle {
            color: rgba(255, 255, 255, 0.95);
            font-size: 1.1em;
            margin-top: 12px;
            font-weight: 300;
            letter-spacing: 0.5px;
        }
        
        /* Input Container Styling */
        .input-container {
            background: white;
            padding: 35px;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
            margin-bottom: 25px;
            animation: fadeInUp 0.7s ease-out 0.2s both;
        }
        
        .input-section-title {
            color: #667eea;
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 3px solid #667eea;
            display: inline-block;
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            border: none;
            border-radius: 10px;
            height: 50px;
            font-size: 18px;
            font-weight: 700;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
            letter-spacing: 0.5px;
            text-transform: uppercase;
            cursor: pointer;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 28px rgba(102, 126, 234, 0.5);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        
        .stButton > button:active {
            transform: translateY(-1px);
        }
        
        /* Input Fields Styling */
        .stNumberInput input {
            border-radius: 8px;
            border: 2px solid #e2e8f0;
            padding: 12px 16px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .stNumberInput input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Success Message Animation */
        .success-container {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 8px 20px rgba(17, 153, 142, 0.3);
            animation: slideInUp 0.6s ease-out;
            margin-top: 20px;
        }
        
        /* Price Result Container */
        .price-result {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 12px 30px rgba(245, 87, 108, 0.3);
            text-align: center;
            animation: zoomIn 0.6s ease-out;
            margin-top: 20px;
        }
        
        .price-label {
            font-size: 0.95em;
            opacity: 0.9;
            margin-bottom: 8px;
            font-weight: 500;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        
        .price-value {
            font-size: 3.2em;
            font-weight: 800;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            letter-spacing: -1px;
        }
        
        /* Info Box */
        .info-box {
            background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
            color: #2d3748;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #667eea;
            margin-top: 20px;
            font-weight: 500;
            animation: fadeIn 0.6s ease-out;
        }
        
        /* Columns Container */
        .column-container {
            animation: fadeInUp 0.7s ease-out 0.1s both;
        }
        
        /* Label Styling */
        .input-label {
            color: #2d3748;
            font-weight: 700;
            font-size: 1.05em;
            margin-bottom: 8px;
        }
        
        /* Animations */
        @keyframes slideInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInUp {
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
        
        @keyframes zoomIn {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        /* Responsive Adjustments */
        @media (max-width: 768px) {
            .header-title {
                font-size: 2.2em;
            }
            .price-value {
                font-size: 2.4em;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Professional Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">💼 Laptop Price Estimator</h1>
        <p class="header-subtitle">Premium AI-Powered Valuation System</p>
    </div>
""", unsafe_allow_html=True)

# Input section with professional styling
st.markdown("""
    <div class="input-container">
        <div class="input-section-title">📊 System Specifications</div>
    </div>
""", unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown('<div class="input-label">⚙️ Processor Speed</div>', unsafe_allow_html=True)
        processor_speed = st.number_input(
            "Processor Speed (GHz)",
            min_value=0.5,
            max_value=6.0,
            value=2.5,
            step=0.1,
            label_visibility="collapsed"
        )

    with col2:
        st.markdown('<div class="input-label">🧠 RAM Memory</div>', unsafe_allow_html=True)
        ram_size = st.number_input(
            "RAM (GB)",
            min_value=2,
            max_value=128,
            value=16,
            step=2,
            label_visibility="collapsed"
        )

    with col3:
        st.markdown('<div class="input-label">💾 Storage Capacity</div>', unsafe_allow_html=True)
        storage_capacity = st.number_input(
            "Storage (GB)",
            min_value=128,
            max_value=4096,
            value=512,
            step=128,
            label_visibility="collapsed"
        )

# Specifications Summary
st.markdown(f"""
    <div class="info-box">
        <strong>📋 Current Configuration:</strong><br>
        ⚙️ Processor: {processor_speed} GHz | 🧠 RAM: {ram_size} GB | 💾 Storage: {storage_capacity} GB
    </div>
""", unsafe_allow_html=True)

# Prepare input
X = np.array([processor_speed, ram_size, storage_capacity]).reshape(1, -1)

# Prediction button with spacing
st.markdown("###")
predict_btn = st.button("🚀 Estimate Price", use_container_width=True)

# Output with professional animations and styling
if predict_btn:
    prediction = model.predict(X)[0]

    st.markdown("""
        <div class="success-container">
            ✅ <strong>Estimation Complete</strong>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="price-result">
            <div class="price-label">Estimated Market Price</div>
            <div class="price-value">${prediction:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Additional insights
    st.markdown(f"""
        <div class="info-box" style="margin-top: 20px;">
            <strong>💡 Pricing Insights</strong><br>
            This estimation is based on current market analysis using machine learning algorithms trained on real-world laptop pricing data. Your configuration represents a {'high-end' if prediction > 1500 else 'mid-range' if prediction > 800 else 'budget-friendly'} laptop segment.
        </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <div class="info-box">
            <strong>ℹ️ How to Use:</strong><br>
            Adjust the system specifications above (Processor Speed, RAM, and Storage Capacity), then click <strong>"🚀 Estimate Price"</strong> to get an AI-powered valuation of your laptop configuration.
        </div>
    """, unsafe_allow_html=True)
import streamlit as st
import numpy as np
import joblib

# Load model
model = joblib.load('rf_model.pkl')

# Page config
st.set_page_config(page_title="Laptop Price Estimator", layout="centered")

# Custom styling
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 100%;
            font-size: 16px;
        }
        .stNumberInput input {
            border-radius: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("💼 Laptop Price Estimator")
st.caption("Enter specifications below to estimate the market price of a laptop.")

# Input section inside a container
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        processor_speed = st.number_input(
            "Processor Speed (GHz)",
            min_value=0.5,
            max_value=6.0,
            value=2.5,
            step=0.1
        )

        ram_size = st.number_input(
            "RAM (GB)",
            min_value=2,
            max_value=128,
            value=16,
            step=2
        )

    with col2:
        storage_capacity = st.number_input(
            "Storage (GB)",
            min_value=128,
            max_value=4096,
            value=512,
            step=128
        )

# Prepare input
X = np.array([processor_speed, ram_size, storage_capacity]).reshape(1, -1)

# Button
st.markdown("###")
predict_btn = st.button("Estimate Price")

# Output
if predict_btn:
    prediction = model.predict(X)[0]

    st.success("Estimation Complete")

    st.metric(
        label="Estimated Laptop Price",
        value=f"${prediction:,.2f}"
    )

else:
    st.info("Enter specifications and click 'Estimate Price' to view results.")
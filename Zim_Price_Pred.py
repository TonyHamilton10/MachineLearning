import streamlit as st
import numpy as np
import joblib


model = joblib.load('Zim_Price_model.pkl')

#['Processor_Speed', 'RAM_Size', 'Storage_Capacity', 'Screen_Size', 'Weight']

st.title('Laptop Price Prediction')

st.divider()

st.write('Please enter the following details to predict the price of a laptop:')
st.divider()


processor_speed = st.number_input('Processor Speed (in GHz)', value=0.0, step=0.1)
ram_size = st.number_input('RAM Size (in GB)', value=0, step=2)
storage_capacity = st.number_input('Storage Capacity (in GB)', value=0, step=64)
screen_size = st.number_input('Screen Size (in inches)', value=0.0, step=0.1)
weight = st.number_input('Weight (in kg)', value=0.0, step=0.1)


X = [processor_speed, ram_size, storage_capacity, screen_size, weight ]

st.divider()

prediction = st.button('Price Estimation Button')

st.divider()

if prediction:
    x1 = np.array(X)
    prediction = model.predict([x1])[0]
    st.write('The predicted price of the laptop is: ${:.2f}'.format(prediction))
else:
    st.write('Please fill in the details and click the button to get the price estimation.')
    

    
import streamlit as st 
import numpy as np 
import joblib


model = joblib.load('randomfReg.pkl')

st.title('Loan Amount Approval')

st.divider()

st.write('Loan Amount to Be Disbursed To An Applicant')

st.divider()

# ['Age', 'CreditScore', 'MonthlyDebtPayments', 'MonthlyIncome', 'MonthlyLoanPayment', 'RiskScore']

age = st.number_input('Applicant Age' , value = 18 , step = 1)
creditscore = st.number_input('Applicant CreditScore' , value = 343 , step = 5)
monthlydebtpayment = st.number_input('Applicant Debts' , value = 50 , step = 50)
monthlyIncome = st.number_input('Applicant Monthly Income' , value = 1250 , step = 100)
monthlyLoanPayment = st.number_input('Applicant Monthly Loan Payment' , value = 97.03 , step = 100)
riskscore = st.number_input('Applicant RiskScore' , value = 28.80 , step = 1)


X = ['age' ,'creditscore' ,'monthlydebtpayment','monthlyIncome' , 'monthlyLoanPayment'  ,'riskscore'  ]

st.divider()

prediction = st.button('Loan Prediction Button!')

st.divider()

if prediction:
    
    x1 = np.array(X)
    prediction = model.predict([x1])
    st.write(f'Estimation Loan Amount ${prediction: ,.2f}')
    
else:
    st.write('Press the Button To Get Results')

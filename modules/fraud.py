from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Data Loading and Preprocessing
data = pd.read_csv('D:/New folder/Projects/bank Fraud Detection/dataset/data.csv')
columns_to_retain = ['LoanAmountRequested', 'LoanTerm', 'ExistingLiabilities', 'PreviousLoans', 'Dependents', 'Occupation', 'IncomeLevel', 'ResidentialStatus', 'CreditScore', 'IsFraud']
data = data[columns_to_retain]

# Data Preprocessing
imputer = SimpleImputer(strategy='mean')
for col in data.columns:
    if data[col].dtype == 'object':
        imputer = SimpleImputer(strategy='most_frequent')
    data[col] = imputer.fit_transform(data[col].values.reshape(-1, 1)).ravel()

label_encoders = {}
for col in data.columns:
    if data[col].dtype == 'object':
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_encoders[col] = le

X = data.drop('IsFraud', axis=1)
y = data['IsFraud']

scaler = StandardScaler()
X = scaler.fit_transform(X)

# Model Building
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X.shape[1],)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)

# Prediction Function
def predict_fraud(LoanAmountRequested, LoanTerm, ExistingLiabilities, PreviousLoans, Dependents, Occupation, IncomeLevel, ResidentialStatus, CreditScore):
    input_data = pd.DataFrame({
        'LoanAmountRequested': [LoanAmountRequested],
        'LoanTerm': [LoanTerm],
        'ExistingLiabilities': [ExistingLiabilities],
        'PreviousLoans': [PreviousLoans],
        'Dependents': [Dependents],
        'Occupation': [Occupation],
        'IncomeLevel': [IncomeLevel],
        'ResidentialStatus': [ResidentialStatus],
        'CreditScore': [CreditScore]
    })

    for col in input_data.columns:
        if input_data[col].dtype == 'object' and col in label_encoders:
            input_data[col] = label_encoders[col].transform(input_data[col])

    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)
    return "Fraud" if prediction > 0.5 else "Not Fraud"

# Flask Blueprint
bp = Blueprint('fraud', __name__, url_prefix='/fraud')

@bp.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        # Extract loan details from form
        LoanAmountRequested = float(request.form['LoanAmountRequested'])
        LoanTerm = int(request.form['LoanTerm'])
        ExistingLiabilities = int(request.form['ExistingLiabilities'])
        PreviousLoans = int(request.form['PreviousLoans'])
        Dependents = int(request.form['Dependents'])
        Occupation = request.form['Occupation']
        IncomeLevel = float(request.form['IncomeLevel'])
        ResidentialStatus = request.form['ResidentialStatus']
        CreditScore = int(request.form['CreditScore'])

        result = predict_fraud(LoanAmountRequested, LoanTerm, ExistingLiabilities, PreviousLoans, Dependents, Occupation, IncomeLevel, ResidentialStatus, CreditScore)
        return redirect(url_for('fraud.result', prediction=result))

    return render_template('fraud_prediction.html')

@bp.route('/result', methods=['GET'])
def result():
    prediction_result = request.args.get('prediction', 'Error occurred')
    return render_template('result.html', prediction=prediction_result)

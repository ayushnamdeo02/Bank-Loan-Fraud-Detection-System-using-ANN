from flask import Flask, render_template, redirect, url_for
import pandas as pd
from modules import kyc, fraud
import os
import secrets  # Importing the secrets library

app = Flask(__name__)

# Setting the secret key for the Flask app
app.secret_key = secrets.token_hex(16)

# Load customer_data for KYC verification
customer_data = pd.read_csv('D:/New folder/Projects/bank Fraud Detection/dataset/customer_data.csv')

# Define the default route to redirect to KYC verification
@app.route('/')
def index():
    return redirect(url_for('kyc.verification'))

# Register the blueprints (i.e., routes defined in the modules)
app.register_blueprint(kyc.bp)
app.register_blueprint(fraud.bp)

if __name__ == '__main__':
    app.run(debug=True)

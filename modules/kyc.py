from flask import Blueprint, render_template, request, redirect, url_for, flash
import pandas as pd

# Load customer_data for KYC verification using the absolute path
customer_data = pd.read_csv('D:/New folder/Projects/bank Fraud Detection/dataset/customer_data.csv')

# Create a Blueprint for KYC routes
bp = Blueprint('kyc', __name__, url_prefix='/kyc')

@bp.route('/', methods=['GET', 'POST'])
def verification():
    if request.method == 'POST':
        # Extract user details from form
        full_name = request.form.get('full_name')
        dob = request.form.get('dob')
        pan_number = request.form.get('pan_number')
        
        # Filter the customer data based on the input
        matched_data = customer_data[
            (customer_data['Name'] == full_name) & 
            (customer_data['DateofBirth'] == dob) & 
            (customer_data['PANNumber'] == pan_number)
        ]
        
        # Check if the user exists in customer_data and is verified
        if not matched_data.empty and matched_data.iloc[0]['AccountStatus'] == 'Verified':
            return redirect(url_for('fraud.prediction'))  # Assuming the fraud prediction route is named 'prediction' in the fraud blueprint
        else:
            flash('User not found or not verified. Please check your details.', 'error')
    
    return render_template('kyc_verification.html')

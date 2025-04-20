import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import streamlit as st

def preprocess_data(data, is_train=True):
    """Preprocess the dataset for model training or prediction"""
    # Drop 'Loan_ID' (it's not useful for prediction)
    if 'Loan_ID' in data.columns:
        data = data.drop(['Loan_ID'], axis=1)
    
    # Encode categorical variables
    categorical_columns = ['Gender', 'Married', 'Dependents', 'Education', 
                           'Self_Employed', 'Property_Area']
    for column in categorical_columns:
        if column in data.columns:
            data[column] = LabelEncoder().fit_transform(data[column].astype(str))
    
    # Fill missing values for numeric columns
    numeric_columns = data.select_dtypes(include=['number']).columns
    data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())
    
    # If training data, encode 'Loan_Status'
    if is_train and 'Loan_Status' in data.columns:
        data['Loan_Status'] = data['Loan_Status'].map({'Y': 1, 'N': 0})
    
    return data

@st.cache_data
def load_and_process_data():
    """Load and preprocess datasets, then split into training and validation sets"""
    try:
        # Load datasets and preprocess them
        train_data = preprocess_data(pd.read_csv('../datasets/loan-train.csv'), is_train=True)
        test_data = preprocess_data(pd.read_csv('../datasets/loan-test.csv'), is_train=False)
        
        # Split features and target for training data
        X = train_data.drop(['Loan_Status'], axis=1)
        y = train_data['Loan_Status']
        
        # Split training data into train and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        return train_data, test_data, X_train, X_val, y_train, y_val
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None, None, None

def prepare_input_data(gender, married, dependents, education, self_employed,
                       applicant_income, coapplicant_income, loan_amount, 
                       loan_amount_term, credit_history, property_area):
    """Transform user input into a DataFrame for prediction"""
    # Process input data
    input_data = pd.DataFrame({
        'Gender': [1 if gender == 'Male' else 0],
        'Married': [1 if married == 'Yes' else 0],
        'Dependents': [0 if dependents == '0' else (1 if dependents == '1' else (2 if dependents == '2' else 3))],
        'Education': [1 if education == 'Graduate' else 0],
        'Self_Employed': [1 if self_employed == 'Yes' else 0],
        'ApplicantIncome': [applicant_income],
        'CoapplicantIncome': [coapplicant_income],
        'LoanAmount': [loan_amount],
        'Loan_Amount_Term': [loan_amount_term],
        'Credit_History': [credit_history],
        'Property_Area': [0 if property_area == 'Urban' else (1 if property_area == 'Semiurban' else 2)]
    })
    
    return input_data
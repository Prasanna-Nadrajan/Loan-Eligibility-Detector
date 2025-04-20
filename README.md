# Loan Eligibility Predictor

A machine learning application built with Streamlit that predicts loan approval eligibility based on various personal and financial factors.

## Project Overview

This application uses a Random Forest classifier to predict whether a loan application is likely to be approved or rejected. The model is trained on historical loan application data and considers factors such as credit history, income, loan amount, and personal details.

## Features

- Interactive web interface for loan eligibility prediction
- Real-time prediction with confidence score
- Key factor analysis for each prediction
- Model insights and data visualizations
- Detailed information about loan approval factors

## Project Structure

- `app.py` - Main application file that runs the Streamlit app
- `data_processor.py` - Functions for data loading and preprocessing
- `model.py` - Model training, evaluation, and prediction functions
- `visualizations.py` - Functions for creating charts and plots
- `ui_components.py` - UI-related functions and components
- `config.py` - Configuration settings for the application

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install streamlit pandas numpy scikit-learn joblib matplotlib plotly
   ```
3. Make sure your dataset files (`loan-train.csv` and `loan-test.csv`) are in the `../datasets/` directory

## Usage

Run the application with:

```
streamlit run app.py
```

Then open your web browser and go to `http://localhost:8501` to use the application.

## Data Requirements

The application expects two CSV files:
1. `loan-train.csv` - Training data with known loan approval outcomes
2. `loan-test.csv` - Test data for new predictions

Both files should contain the following columns:
- `Loan_ID` (optional)
- `Gender`
- `Married`
- `Dependents`
- `Education`
- `Self_Employed`
- `ApplicantIncome`
- `CoapplicantIncome`
- `LoanAmount`
- `Loan_Amount_Term`
- `Credit_History`
- `Property_Area`
- `Loan_Status` (only required in train data)

## Model

The application uses a Random Forest Classifier with 100 estimators. The model is trained on historical loan data and validated using a 80-20 train-validation split.

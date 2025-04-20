import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import streamlit as st

@st.cache_resource
def train_model(X_train, y_train):
    """Build and train the Random Forest model"""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def get_feature_importance(model, X_train):
    """Extract feature importance from the trained model"""
    feature_importance = pd.DataFrame(
        {'feature': X_train.columns, 'importance': model.feature_importances_}
    ).sort_values('importance', ascending=False)
    return feature_importance

def save_model(model, filename='loan_model.pkl'):
    """Save the trained model to a file"""
    joblib.dump(model, filename)

def load_model(filename='loan_model.pkl'):
    """Load a trained model from a file"""
    try:
        return joblib.load(filename)
    except:
        return None

def evaluate_model(model, X_val, y_val):
    """Evaluate model performance on validation data"""
    y_val_pred = model.predict(X_val)
    accuracy = accuracy_score(y_val, y_val_pred)
    return accuracy

def get_prediction_details(model, input_data):
    """Get prediction and probability for input data"""
    prediction_proba = model.predict_proba(input_data)[0]
    prediction = model.predict(input_data)[0]
    
    # Get feature importance for this prediction
    feature_imp = pd.DataFrame(
        {'Feature': input_data.columns, 'Value': input_data.values[0], 'Importance': model.feature_importances_}
    ).sort_values('Importance', ascending=False)
    
    return prediction, prediction_proba, feature_imp
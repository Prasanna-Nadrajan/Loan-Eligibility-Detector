import streamlit as st
import time
from config import PAGE_CONFIG, MODEL_PATH
from data_processor import load_and_process_data, prepare_input_data
from model import train_model, evaluate_model, save_model, get_prediction_details
from ui_components import (set_custom_style, display_header, display_application_form,
                          display_prediction_result, display_about_section, 
                          display_help_section, display_model_insights)

def main():
    # Set page configuration
    st.set_page_config(**PAGE_CONFIG)
    
    # Apply custom styles
    set_custom_style()
    
    # Display header
    display_header()
    
    # Load data and train model
    train_data, test_data, X_train, X_val, y_train, y_val = load_and_process_data()
    
    if train_data is None:
        st.warning("Please make sure the dataset files are in the correct location.")
        return
    
    # Train or load model
    model = train_model(X_train, y_train)
    
    # Evaluate the model
    accuracy = evaluate_model(model, X_val, y_val)
    
    # Save the model
    save_model(model, MODEL_PATH)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Application Form", "📊 Model Insights", "ℹ️ About", "❓ Help"])
    
    with tab1:
        # Display application form and get user inputs
        inputs = display_application_form()
        gender, married, dependents, education, self_employed, applicant_income, coapplicant_income, loan_amount, loan_amount_term, credit_history, property_area = inputs
        
        # Add prediction button
        if st.button("Check Eligibility", use_container_width=True):
            with st.spinner("Processing your application..."):
                # Add a small delay to show the spinner
                time.sleep(1)
                
                # Prepare input data
                input_data = prepare_input_data(
                    gender, married, dependents, education, self_employed,
                    applicant_income, coapplicant_income, loan_amount, 
                    loan_amount_term, credit_history, property_area
                )
                
                # Get prediction
                prediction, prediction_proba, feature_imp = get_prediction_details(model, input_data)
                
                # Display prediction result
                display_prediction_result(prediction, prediction_proba, feature_imp)
    
    with tab2:
        # Display model insights
        display_model_insights(model, X_train, accuracy, train_data)
    
    with tab3:
        # Display about section
        display_about_section()
    
    with tab4:
        # Display help and FAQ section
        display_help_section(accuracy)

if __name__ == "__main__":
    main()
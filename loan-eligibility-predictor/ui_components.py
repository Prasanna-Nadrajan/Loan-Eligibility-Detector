import streamlit as st

def set_custom_style():
    """Set custom CSS styles for the application"""
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #2563EB;
            margin-bottom: 1rem;
        }
        .info-text {
            font-size: 1rem;
            color: #4B5563;
        }
        .prediction-box-approved {
            background-color: #16C47F;
            padding: 20px;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            text-align: center;
            font-size: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .prediction-box-rejected {
            background-color: #F72C5B;
            padding: 20px;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            text-align: center;
            font-size: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #76ABAE;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding: 10px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #76ABAE;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    """Display the main application header"""
    st.markdown('<h1 class="main-header">Loan Eligibility Predictor</h1>', unsafe_allow_html=True)

def display_application_form():
    """Display the loan application form and return user inputs"""
    st.markdown('<h2 class="sub-header">Enter Your Details</h2>', unsafe_allow_html=True)
    
    # Create columns for form layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Personal Information")
        gender = st.selectbox("Gender", ['Male', 'Female'])
        married = st.selectbox("Married", ['Yes', 'No'])
        dependents = st.selectbox("Dependents", ['0', '1', '2', '3+'])
        education = st.selectbox("Education", ['Graduate', 'Not Graduate'])
        self_employed = st.selectbox("Self Employed", ['Yes', 'No'])
    
    with col2:
        st.subheader("Financial Information")
        applicant_income = st.number_input("Applicant Income (₹)", min_value=0, help="Monthly income in rupees")
        coapplicant_income = st.number_input("Coapplicant Income (₹)", min_value=0, help="Monthly income of coapplicant in rupees")
        loan_amount = st.number_input("Loan Amount (₹'000s)", min_value=0, help="Loan amount in thousands")
        loan_amount_term = st.number_input("Loan Term (months)", min_value=0, value=360, help="Term of loan in months")
        credit_history = st.radio("Credit History", [1, 0], format_func=lambda x: "Good (1)" if x == 1 else "Bad (0)", help="1 indicates all debts paid on time, 0 indicates delayed payments")
        property_area = st.selectbox("Property Area", ['Urban', 'Semiurban', 'Rural'])
    
    return gender, married, dependents, education, self_employed, applicant_income, coapplicant_income, loan_amount, loan_amount_term, credit_history, property_area

def display_prediction_result(prediction, prediction_proba, feature_imp):
    """Display loan application prediction results"""
    st.subheader("Loan Application Result")
    
    # Create columns for result and probability
    res_col1, res_col2 = st.columns([3, 2])
    
    with res_col1:
        if prediction == 1:
            st.markdown('<div class="prediction-box-approved">APPROVED ✅</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="prediction-box-rejected">NOT APPROVED ❌</div>', unsafe_allow_html=True)
    
    with res_col2:
        # Import and use visualization function here to avoid circular import
        from visualizations import create_prediction_chart
        fig = create_prediction_chart(prediction_proba)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Key Factors in Your Application")
    top_features = feature_imp.head(5)
    
    for _, row in top_features.iterrows():
        factor_name = row['Feature']
        factor_value = row['Value']
        factor_importance = row['Importance']
        
        # Create a more readable name
        readable_name = ' '.join(factor_name.split('_')).title()
        if factor_name == 'Credit_History':
            value_text = "Good" if factor_value == 1 else "Bad"
        elif factor_name == 'Property_Area':
            value_text = ["Urban", "Semiurban", "Rural"][int(factor_value)]
        else:
            value_text = str(factor_value)
        
        st.metric(
            label=readable_name,
            value=value_text,
            delta=f"Impact: {factor_importance:.2%}"
        )

def display_about_section():
    """Display information about the application"""
    st.markdown('<h2 class="sub-header">About This Application</h2>', unsafe_allow_html=True)
    
    st.info("""
    This loan eligibility predictor uses machine learning to assess the likelihood of loan approval based on various factors. 
    The model has been trained on historical loan application data and uses a Random Forest algorithm to make predictions.
    
    **How it works:**
    1. Enter your personal and financial information in the application form
    2. Click "Check Eligibility" to see the prediction
    3. View the key factors that influenced the prediction
    4. Explore model insights to understand the overall patterns
    
    **Note:** This application is for educational purposes only and should not be used as financial advice.
    """)
    
    # Loan approval criteria explanation
    st.markdown('<h3 class="sub-header">Understanding Loan Approval Factors</h3>', unsafe_allow_html=True)
    
    with st.expander("Key Factors That Influence Loan Approval"):
        st.markdown("""
        - **Credit History**: The most important factor. A good credit history significantly increases chances of approval.
        - **Income Levels**: Higher applicant and coapplicant incomes improve approval odds.
        - **Loan Amount**: Smaller loan amounts relative to income are more likely to be approved.
        - **Property Area**: Some areas may have higher approval rates than others.
        - **Education**: Graduate applicants may have slightly higher approval rates.
        - **Marital Status & Dependents**: These factors can influence the bank's assessment of financial stability.
        """)

def display_help_section(accuracy):
    """Display help and FAQ section"""
    st.markdown('<h2 class="sub-header">Help & FAQ</h2>', unsafe_allow_html=True)
    
    faq = {
        "What is this application for?": "This application helps you check your eligibility for a loan based on various personal and financial factors.",
        "How accurate is the prediction?": f"The model has an accuracy of {accuracy * 100:.2f}% on the validation dataset. However, actual bank decisions may consider additional factors.",
        "What does 'Credit History' mean?": "Credit History indicates whether you have paid your previous debts on time. '1' means good credit history, '0' means bad credit history.",
        "Why was my application rejected?": "The application shows the key factors that influenced the decision. Typically, bad credit history, low income relative to loan amount, or high number of dependents with low income can lead to rejection.",
        "Can I improve my chances of approval?": "Yes, improving your credit score, increasing your income, applying with a co-applicant, or requesting a lower loan amount can improve your chances.",
        "Is my data saved?": "No, this application does not store any of your personal information. All data is processed in your browser session only."
    }
    
    for question, answer in faq.items():
        with st.expander(question):
            st.write(answer)

def display_model_insights(model, X_train, accuracy, train_data):
    """Display model insights and visualizations"""
    st.markdown('<h2 class="sub-header">Model Insights</h2>', unsafe_allow_html=True)
    
    # Show model accuracy
    st.metric("Model Accuracy", f"{accuracy * 100:.2f}%")
    
    # Import visualization functions to avoid circular imports
    from visualizations import (create_feature_importance_chart, create_loan_status_chart, 
                                create_credit_history_chart, create_income_vs_loan_chart)
    
    # Feature importance plot
    st.subheader("Feature Importance")
    from model import get_feature_importance
    feature_importance = get_feature_importance(model, X_train)
    fig = create_feature_importance_chart(feature_importance)
    st.plotly_chart(fig, use_container_width=True)
    
    # Data distribution
    st.subheader("Data Distribution")
    
    dist_col1, dist_col2 = st.columns(2)
    
    with dist_col1:
        # Distribution of loan approval status
        fig = create_loan_status_chart(train_data)
        st.plotly_chart(fig, use_container_width=True)
    
    with dist_col2:
        # Credit History distribution
        fig = create_credit_history_chart(train_data)
        st.plotly_chart(fig, use_container_width=True)
    
    # Income vs Loan Amount
    st.subheader("Income vs Loan Amount")
    fig = create_income_vs_loan_chart(train_data)
    st.plotly_chart(fig, use_container_width=True)
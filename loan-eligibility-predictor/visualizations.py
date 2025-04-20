import plotly.express as px

def create_prediction_chart(prediction_proba):
    """Create a pie chart showing prediction confidence"""
    fig = px.pie(
        values=[prediction_proba[1], prediction_proba[0]],
        names=['Approval Chance', 'Rejection Chance'],
        title="Prediction Confidence",
        color_discrete_sequence=['#16C47F', '#F72C5B'],
        hole=0.4
    )
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    return fig

def create_feature_importance_chart(feature_importance):
    """Create a bar chart showing feature importance"""
    fig = px.bar(
        feature_importance,
        x='importance',
        y='feature',
        orientation='h',
        title='Feature Importance for Loan Approval',
        labels={'importance': 'Importance Score', 'feature': 'Feature'},
        color='importance',
        color_continuous_scale='Blues'
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig

def create_loan_status_chart(train_data):
    """Create a pie chart showing loan approval distribution"""
    approval_counts = train_data['Loan_Status'].value_counts()
    fig = px.pie(
        values=approval_counts.values,
        names=['Not Approved', 'Approved'] if len(approval_counts) == 2 else ['Approved'],
        title="Loan Approval Distribution in Training Data",
        color_discrete_sequence=['#F72C5B', '#16C47F']
    )
    return fig

def create_credit_history_chart(train_data):
    """Create a pie chart showing credit history distribution"""
    credit_counts = train_data['Credit_History'].value_counts()
    
    # Create dict mapping values to labels
    credit_labels = {0: 'Bad Credit', 1: 'Good Credit'}
    
    # Create labels list matching the order of values
    names = [credit_labels.get(i, f"Credit Type {i}") for i in credit_counts.index]
    
    fig = px.pie(
        values=credit_counts.values,
        names=names,
        title="Credit History Distribution",
        color_discrete_sequence=['#F72C5B', '#16C47F', '#4B5563'][:len(credit_counts)]
    )
    return fig

def create_income_vs_loan_chart(train_data):
    """Create a scatter plot of income vs loan amount"""
    # Create a DataFrame where 'Loan_Status' is represented as a string for better visualization
    viz_df = train_data.copy()
    viz_df['Loan_Status'] = viz_df['Loan_Status'].map({1: 'Approved', 0: 'Not Approved'})
    
    fig = px.scatter(
        viz_df,
        x='ApplicantIncome',
        y='LoanAmount',
        color='Loan_Status',
        color_discrete_map={'Approved': '#16C47F', 'Not Approved': '#F72C5B'},
        hover_data=['Education', 'Credit_History'],
        title="Applicant Income vs Loan Amount",
        labels={'ApplicantIncome': 'Applicant Income', 'LoanAmount': 'Loan Amount'}
    )
    return fig
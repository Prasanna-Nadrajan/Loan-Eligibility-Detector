# Application configuration parameters

# Page configuration
PAGE_CONFIG = {
    "page_title": "Loan Eligibility Predictor",
    "page_icon": "💰",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Model parameters
MODEL_PARAMS = {
    "n_estimators": 100,
    "random_state": 42
}

# Dataset paths
DATA_PATHS = {
    "train_data": "../datasets/loan-train.csv",
    "test_data": "../datasets/loan-test.csv"
}

# Model save path
MODEL_PATH = "loan_model.pkl"

# Color scheme
COLORS = {
    "approved": "#16C47F",
    "rejected": "#F72C5B",
    "primary": "#1E3A8A",
    "secondary": "#2563EB",
    "neutral": "#4B5563",
    "tab_bg": "#76ABAE"
}
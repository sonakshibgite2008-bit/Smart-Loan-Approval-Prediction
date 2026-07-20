import joblib
import pandas as pd
import os


# Model paths
MODEL_PATH = "models/loan_model.pkl"


# Load trained model
model = joblib.load(MODEL_PATH)


def predict_loan(data):

    """
    data should be a dictionary containing user inputs
    """

    # Convert input to dataframe
    input_df = pd.DataFrame([data])


    # Encode categorical values
    categorical_columns = [
        "Gender",
        "Married",
        "Dependents",
        "Education",
        "Self_Employed",
        "Property_Area"
    ]


    mappings = {
        "Gender": {
            "Male": 1,
            "Female": 0
        },

        "Married": {
            "Yes": 1,
            "No": 0
        },

        "Education": {
            "Graduate": 0,
            "Not Graduate": 1
        },

        "Self_Employed": {
            "Yes": 1,
            "No": 0
        },

        "Property_Area": {
            "Rural": 0,
            "Semiurban": 1,
            "Urban": 2
        },

        "Dependents": {
            "0": 0,
            "1": 1,
            "2": 2,
            "3+": 3
        }
    }


    for col in categorical_columns:
        input_df[col] = input_df[col].map(mappings[col])


    # Prediction
    result = model.predict(input_df)


    if result[0] == 1:
        return "Approved"
    else:
        return "Rejected"
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib

# =========================
# FastAPI Application Setup
# =========================
app = FastAPI(title="Credit Card Fraud Detection API")

# Use the same values as in the Streamlit interface
UNIT_PRICE = 8000
FRAUD_THRESHOLD = 100000

# =========================
# Load the trained model, scaler, and simulation dataset
# =========================
MODEL_PATH = "model.pkl"
SCALER_PATH = "scaler.pkl"
SIM_CSV_PATH = "api_simulation_samples.csv"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

sim_df = pd.read_csv(SIM_CSV_PATH)

# Assume that "Class" is the target column
FEATURE_COLS = [c for c in sim_df.columns if c != "Class"]

fraud_df = sim_df[sim_df["Class"] == 1].copy()
normal_df = sim_df[sim_df["Class"] == 0].copy()

# =========================
# Pydantic model for API request
# =========================
class CheckoutRequest(BaseModel):
    quantity: int


# =========================
# Helper function: Run model on a single transaction
# =========================
def predict_row(row: pd.Series):
    """
    Applies the same logic used in the notebook:
    - Takes one row and converts it into a DataFrame
    - Applies scaling on Time and Amount
    - Passes the data to the trained model for prediction
    """

    # Convert the row into a DataFrame with shape (1, n_features)
    X = row[FEATURE_COLS].to_frame().T

    # Apply scaling on Time and Amount columns
    X_scaled = X.copy()
    X_scaled[["Time", "Amount"]] = scaler.transform(X[["Time", "Amount"]])

    proba = model.predict_proba(X_scaled)[0, 1]
    pred = model.predict(X_scaled)[0]

    return bool(pred), float(proba)


# =========================
# Basic health check endpoint
# Used to verify that the API is running correctly
# =========================
@app.get("/")
def root():
    return {"message": "Fraud Detection API is running"}


# =========================
# Main endpoint: simulate_checkout
# This endpoint simulates a checkout transaction
# =========================
@app.post("/simulate_checkout")
def simulate_checkout(req: CheckoutRequest):
    quantity = max(req.quantity, 1)
    total_amount = quantity * UNIT_PRICE

    # # Select which dataset to sample from based on transaction size
    if total_amount > FRAUD_THRESHOLD:
        sample_row = fraud_df.sample(1).iloc[0]
        scenario = "high_amount_suspicious"
    else:
        sample_row = normal_df.sample(1).iloc[0]
        scenario = "normal_amount"

    is_fraud, fraud_proba = predict_row(sample_row)

    return {
        "unit_price": UNIT_PRICE,
        "quantity": quantity,
        "total_amount": total_amount,
        "scenario": scenario,
        "is_fraud_predicted": is_fraud,
        "fraud_probability": fraud_proba,
    }

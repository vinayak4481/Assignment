from flask import Flask, request, jsonify, send_file
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load the trained model
model = joblib.load("doctor_attendance_model.pkl")

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Convert request data to DataFrame
    df = pd.DataFrame([data])

    # Convert datetime features
    df["Login Hour"] = pd.to_datetime(df["Login Time"]).dt.hour
    df["Logout Hour"] = pd.to_datetime(df["Logout Time"]).dt.hour
    df.drop(columns=["Login Time", "Logout Time"], inplace=True)

    # Make prediction
    prediction = model.predict(df)[0]
    result = "Likely to attend" if prediction == 1 else "Unlikely to attend"

    return jsonify({"prediction": result})

# Route to download predictions
@app.route("/download", methods=["GET"])
def download_predictions():
    # Create a sample predictions DataFrame
    predictions = pd.DataFrame([
        {"NPI": "1234567890", "Prediction": "Likely to attend"},
        {"NPI": "0987654321", "Prediction": "Unlikely to attend"}
    ])

    file_path = "predictions.xlsx"
    predictions.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

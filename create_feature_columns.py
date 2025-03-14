import pandas as pd
import joblib

# Load dataset (Update the filename if necessary)
file_path = "doctors_data.xlsx"  # Change to your actual dataset file
sheet_name = "Dataset"  # Update if your sheet name is different

try:
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Check if required column exists
    if "NPI" not in df.columns:
        raise ValueError("❌ Error: Dataset must contain 'NPI' column.")

    # Convert Login Time to Hour
    df["Login Hour"] = pd.to_datetime(df["Login Time"], errors="coerce").dt.hour

    # One-hot encode categorical columns
    df = pd.get_dummies(df, columns=["Region", "Speciality"], drop_first=True)

    # Remove unnecessary columns
    df = df.drop(columns=["Login Time", "Logout Time", "State"])  # Drop unused features

    # Save the final feature list
    feature_columns = [col for col in df.columns if col != "NPI"]
    joblib.dump(feature_columns, "feature_columns.pkl")

    print("✅ Feature columns saved successfully!")

except FileNotFoundError:
    print(f"❌ Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"❌ Error: {e}")

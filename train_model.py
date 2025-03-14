import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Load data
file_path = "doctors_data.xlsx"  # Make sure this file exists
df = pd.read_excel(file_path)

# Check column names
print("Excel Columns:", df.columns)

# Rename columns to match expected names
df.rename(columns={
    "Count of Survey Attempts": "Survey_Count"
}, inplace=True)

# Define target variable (Assuming doctors with Survey_Count > 0 attended)
df["Attended"] = (df["Survey_Count"] > 0).astype(int)

# Convert datetime features **before dropping them**
df["Login Hour"] = pd.to_datetime(df["Login Time"]).dt.hour
df["Logout Hour"] = pd.to_datetime(df["Logout Time"]).dt.hour

# Define features and target **before dropping columns**
features = ["State", "Login Hour", "Logout Hour", "Usage Time (mins)", "Region", "Speciality"]
target = "Attended"

# Drop unnecessary columns
df.drop(columns=["Login Time", "Logout Time"], inplace=True)

# One-hot encoding for categorical features
categorical_features = ["State", "Region", "Speciality"]
numeric_features = ["Login Hour", "Logout Hour", "Usage Time (mins)"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ("num", "passthrough", numeric_features)
])

# Define model
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# Split data
X = df[features]  # ✅ Now 'Login Hour' & 'Logout Hour' are used instead of missing columns
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "doctor_attendance_model.pkl")
print("✅ Model training complete. Model saved as doctor_attendance_model.pkl")

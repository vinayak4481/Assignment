import pandas as pd

# Update the file path if needed
file_path = "doctors_data.xlsx"
sheet_name = "Dataset"  # Update if your sheet name is different

try:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print("📌 Column Names in Your Dataset:")
    print(df.columns.tolist())  # Print all column names

except FileNotFoundError:
    print(f"❌ Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"❌ Error: {e}")

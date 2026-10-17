import pandas as pd
import os

def validate_amazon_data():
    file_path = 'silver_amazon_data.csv'
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        return False
    
    df = pd.read_csv(file_path)
    print("--- Starting Data Quality & Validation Checks ---")
    
    # Check 1: Missing values check
    missing_values = df.isnull().sum()
    print("\n[Check 1] Missing Values Summary:")
    print(missing_values[missing_values > 0] if not missing_values[missing_values > 0].empty else "No missing values found!")
    
    # Check 2: Negative or zero TotalAmount check
    if 'TotalAmount' in df.columns:
        invalid_amounts = df[df['TotalAmount'] <= 0]
        print(f"\n[Check 2] Invalid TotalAmount (<= 0): {len(invalid_amounts)} records found.")
    
    # Check 3: Negative Quantity check
    if 'Quantity' in df.columns:
        invalid_qty = df[df['Quantity'] <= 0]
        print(f"\n[Check 3] Invalid Quantity (<= 0): {len(invalid_qty)} records found.")
        
    # Check 4: Duplicate OrderID check
    if 'OrderID' in df.columns:
        duplicates = df.duplicated(subset=['OrderID']).sum()
        print(f"\n[Check 4] Duplicate Order IDs: {duplicates} found.")
        
    print("\n--- Data Validation Completed Successfully ---")
    return True

if __name__ == "__main__":
    validate_amazon_data()

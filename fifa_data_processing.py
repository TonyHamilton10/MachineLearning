import pandas as pd
import numpy as np
import re
import os

# Load the FIFA data
fifa_path = r"C:\Users\user\Desktop\Machine Learning Full\archive (1)\FIFA18_official_data.csv"
print(f"Loading FIFA data from: {fifa_path}")
print(f"File exists: {os.path.exists(fifa_path)}")
fifa_data = pd.read_csv(fifa_path)

print("Original shape:", fifa_data.shape)
print("\nOriginal columns:", fifa_data.columns.tolist())

# 1. Drop Photo, Flag, Club Logo columns
fifa_data = fifa_data.drop(columns=['Photo', 'Flag', 'Club Logo'], errors='ignore')
print("\nColumns after dropping Photo, Flag, Club Logo:", fifa_data.columns.tolist())

# 2. Clean Value column (remove currency symbols and convert to numeric)
if 'Value' in fifa_data.columns:
    # Remove K, M, and currency symbols, then convert
    fifa_data['Value'] = fifa_data['Value'].astype(str).str.replace(r'[^\d.KM]', '', regex=True)
    
    def convert_value(val):
        if pd.isna(val) or val == '':
            return np.nan
        if 'M' in str(val):
            return float(val.replace('M', '')) * 1_000_000
        elif 'K' in str(val):
            return float(val.replace('K', '')) * 1_000
        else:
            try:
                return float(val)
            except:
                return np.nan
    
    fifa_data['Value'] = fifa_data['Value'].apply(convert_value)
    print("\nValue column cleaned. Sample values:")
    print(fifa_data['Value'].head(10))

# 3. Clean Wage column (remove currency symbols and convert to numeric)
if 'Wage' in fifa_data.columns:
    # Remove K, M, and currency symbols, then convert
    fifa_data['Wage'] = fifa_data['Wage'].astype(str).str.replace(r'[^\d.KM]', '', regex=True)
    
    def convert_wage(val):
        if pd.isna(val) or val == '':
            return np.nan
        if 'M' in str(val):
            return float(val.replace('M', '')) * 1_000_000
        elif 'K' in str(val):
            return float(val.replace('K', '')) * 1_000
        else:
            try:
                return float(val)
            except:
                return np.nan
    
    fifa_data['Wage'] = fifa_data['Wage'].apply(convert_wage)
    print("\nWage column cleaned. Sample values:")
    print(fifa_data['Wage'].head(10))

# 4. Clean Release Clause column (remove currency symbols and convert to numeric)
if 'Release Clause' in fifa_data.columns:
    # Remove K, M, and currency symbols, then convert
    fifa_data['Release Clause'] = fifa_data['Release Clause'].astype(str).str.replace(r'[^\d.KM]', '', regex=True)
    
    def convert_release_clause(val):
        if pd.isna(val) or val == '':
            return np.nan
        if 'M' in str(val):
            return float(val.replace('M', '')) * 1_000_000
        elif 'K' in str(val):
            return float(val.replace('K', '')) * 1_000
        else:
            try:
                return float(val)
            except:
                return np.nan
    
    fifa_data['Release Clause'] = fifa_data['Release Clause'].apply(convert_release_clause)
    print("\nRelease Clause column cleaned. Sample values:")
    print(fifa_data['Release Clause'].head(10))

# 5. Convert Weight from lbs to kg (assuming Weight is in lbs)
if 'Weight' in fifa_data.columns:
    fifa_data['Weight'] = fifa_data['Weight'].astype(str).str.extract(r'(\d+\.?\d*)', expand=False)
    fifa_data['Weight'] = pd.to_numeric(fifa_data['Weight'], errors='coerce')
    fifa_data['Weight'] = fifa_data['Weight'] * 0.453592  # Convert lbs to kg
    print("\nWeight converted to kg. Sample values:")
    print(fifa_data['Weight'].head(10))

# 6. Convert Height from ft'in" to cm (assuming Height is in feet and inches format)
if 'Height' in fifa_data.columns:
    def convert_height_to_cm(height_str):
        if pd.isna(height_str):
            return np.nan
        try:
            # Parse feet and inches format (e.g., "6'1")
            parts = str(height_str).replace('"', '').split("'")
            feet = float(parts[0])
            inches = float(parts[1]) if len(parts) > 1 and parts[1] else 0
            total_inches = (feet * 12) + inches
            total_cm = total_inches * 2.54
            return total_cm
        except:
            return np.nan
    
    fifa_data['Height'] = fifa_data['Height'].apply(convert_height_to_cm)
    print("\nHeight converted to cm. Sample values:")
    print(fifa_data['Height'].head(10))

print("\nFinal shape:", fifa_data.shape)
print("\nFinal columns:", fifa_data.columns.tolist())
print("\nData types:")
print(fifa_data.dtypes)
print("\nFirst few rows:")
print(fifa_data.head())

# Save the cleaned data
output_path = r"C:\Users\user\Desktop\MyMasterPiece\fifa_data_cleaned.csv"
fifa_data.to_csv(output_path, index=False)
print(f"\nCleaned data saved to: {output_path}")

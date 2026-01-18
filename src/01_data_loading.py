"""
Step 1: Data Loading
Load all split CSV files and combine them into single dataframes
"""

import pandas as pd
import os
import sys

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import (
    RAW_DATA_DIR, 
    ENROLLMENT_FILES, 
    BIOMETRIC_FILES, 
    DEMOGRAPHIC_FILES
)


def load_split_files(file_list, data_dir, dataset_name):
    """
    Load multiple CSV files and combine them into a single dataframe
    
    Parameters:
    -----------
    file_list : list
        List of CSV filenames to load
    data_dir : str
        Directory containing the files
    dataset_name : str
        Name of the dataset (for logging)
    
    Returns:
    --------
    pd.DataFrame
        Combined dataframe
    """
    print(f"\n{'='*60}")
    print(f"Loading {dataset_name} data...")
    print(f"{'='*60}")
    
    dataframes = []
    total_rows = 0
    
    for i, filename in enumerate(file_list, 1):
        file_path = os.path.join(data_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"⚠️  WARNING: File not found: {filename}")
            continue
        
        # Load CSV
        try:
            df = pd.read_csv(file_path)
            rows = len(df)
            total_rows += rows
            
            print(f"  [{i}/{len(file_list)}] ✓ {filename}")
            print(f"       Rows: {rows:,} | Columns: {df.shape[1]}")
            
            dataframes.append(df)
            
        except Exception as e:
            print(f"  ✗ Error loading {filename}: {str(e)}")
            continue
    
    # Combine all dataframes
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        print(f"\n✓ Successfully combined {len(dataframes)} files")
        print(f"  Total rows: {total_rows:,}")
        print(f"  Final shape: {combined_df.shape}")
        return combined_df
    else:
        print(f"✗ No files were loaded for {dataset_name}")
        return None


def inspect_dataframe(df, dataset_name):
    """
    Print basic information about the dataframe
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe to inspect
    dataset_name : str
        Name of the dataset
    """
    print(f"\n{'='*60}")
    print(f"{dataset_name} - Data Inspection")
    print(f"{'='*60}")
    
    print(f"\n📊 Basic Info:")
    print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print(f"\n📋 Columns:")
    for col in df.columns:
        print(f"  - {col} ({df[col].dtype})")
    
    print(f"\n🔍 First 5 rows:")
    print(df.head())
    
    print(f"\n📉 Missing values:")
    missing = df.isnull().sum()
    if missing.any():
        print(missing[missing > 0])
    else:
        print("  No missing values found! ✓")
    
    print(f"\n📅 Date range:")
    if 'date' in df.columns:
        try:
            df['date_temp'] = pd.to_datetime(df['date'], format='%d-%m-%y', errors='coerce')
            print(f"  From: {df['date_temp'].min()}")
            print(f"  To: {df['date_temp'].max()}")
            print(f"  Unique dates: {df['date_temp'].nunique()}")
            df.drop('date_temp', axis=1, inplace=True)
        except:
            print("  Could not parse dates")
    
    print(f"\n🌍 Geographic coverage:")
    if 'state' in df.columns:
        print(f"  States: {df['state'].nunique()}")
    if 'district' in df.columns:
        print(f"  Districts: {df['district'].nunique()}")
    if 'pincode' in df.columns:
        print(f"  Pincodes: {df['pincode'].nunique()}")


def main():
    """
    Main function to load all datasets
    """
    print("\n" + "="*60)
    print("AADHAAR DATA LOADING - STEP 1")
    print("="*60)
    
    # Load Enrollment data
    df_enrollment = load_split_files(
        ENROLLMENT_FILES, 
        RAW_DATA_DIR, 
        "ENROLLMENT"
    )
    if df_enrollment is not None:
        inspect_dataframe(df_enrollment, "ENROLLMENT")
    
    # Load Biometric data
    df_biometric = load_split_files(
        BIOMETRIC_FILES, 
        RAW_DATA_DIR, 
        "BIOMETRIC"
    )
    if df_biometric is not None:
        inspect_dataframe(df_biometric, "BIOMETRIC")
    
    # Load Demographic data
    df_demographic = load_split_files(
        DEMOGRAPHIC_FILES, 
        RAW_DATA_DIR, 
        "DEMOGRAPHIC"
    )
    if df_demographic is not None:
        inspect_dataframe(df_demographic, "DEMOGRAPHIC")
    
    # Summary
    print(f"\n{'='*60}")
    print("LOADING SUMMARY")
    print(f"{'='*60}")
    print(f"✓ Enrollment: {len(df_enrollment):,} records" if df_enrollment is not None else "✗ Enrollment: Failed")
    print(f"✓ Biometric: {len(df_biometric):,} records" if df_biometric is not None else "✗ Biometric: Failed")
    print(f"✓ Demographic: {len(df_demographic):,} records" if df_demographic is not None else "✗ Demographic: Failed")
    
    if all(df is not None for df in [df_enrollment, df_biometric, df_demographic]):
        total_records = len(df_enrollment) + len(df_biometric) + len(df_demographic)
        print(f"\n🎉 Total records loaded: {total_records:,}")
        print(f"✓ All datasets loaded successfully!")
        
        # Return dataframes for next steps
        return df_enrollment, df_biometric, df_demographic
    else:
        print("\n⚠️  Some datasets failed to load. Check file paths.")
        return None, None, None


if __name__ == "__main__":
    df_enrollment, df_biometric, df_demographic = main()
    
    print("\n" + "="*60)
    print("Next step: Run 02_data_cleaning.py")
    print("="*60)
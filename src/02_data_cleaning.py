"""
Step 2: Data Cleaning and Merging
Standardize dates, state names, and create merged dataset
Includes comprehensive state name standardization (replaces quickfix.py)
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    ENROLLMENT_FILES,
    BIOMETRIC_FILES,
    DEMOGRAPHIC_FILES,
    START_DATE,
    END_DATE
)


def load_datasets():
    """
    Load all three datasets
    Returns: df_enrollment, df_biometric, df_demographic
    """
    print("\n" + "="*60)
    print("LOADING DATASETS")
    print("="*60)
    
    # Load enrollment
    enrollment_dfs = []
    for file in ENROLLMENT_FILES:
        df = pd.read_csv(os.path.join(RAW_DATA_DIR, file))
        enrollment_dfs.append(df)
    df_enrollment = pd.concat(enrollment_dfs, ignore_index=True)
    print(f"✓ Enrollment: {len(df_enrollment):,} records")
    
    # Load biometric
    biometric_dfs = []
    for file in BIOMETRIC_FILES:
        df = pd.read_csv(os.path.join(RAW_DATA_DIR, file))
        biometric_dfs.append(df)
    df_biometric = pd.concat(biometric_dfs, ignore_index=True)
    print(f"✓ Biometric: {len(df_biometric):,} records")
    
    # Load demographic
    demographic_dfs = []
    for file in DEMOGRAPHIC_FILES:
        df = pd.read_csv(os.path.join(RAW_DATA_DIR, file))
        demographic_dfs.append(df)
    df_demographic = pd.concat(demographic_dfs, ignore_index=True)
    print(f"✓ Demographic: {len(df_demographic):,} records")
    
    return df_enrollment, df_biometric, df_demographic


def standardize_dates(df, date_column='date'):
    """
    Standardize date formats across datasets
    Handles both DD-MM-YY and DD-MM-YYYY formats
    """
    print(f"\n📅 Standardizing dates in {date_column} column...")
    
    # Try multiple date formats
    date_formats = ['%d-%m-%y', '%d-%m-%Y', '%d-%m-%Y', '%Y-%m-%d']
    
    df[date_column] = pd.to_datetime(df[date_column], format='mixed', errors='coerce')
    
    # Check for parsing errors
    null_dates = df[date_column].isna().sum()
    if null_dates > 0:
        print(f"  ⚠️  WARNING: {null_dates:,} dates could not be parsed")
        # Show sample of problematic dates
        problematic = df[df[date_column].isna()][date_column].head(5)
        print(f"  Sample problematic dates: {problematic.tolist()}")
    else:
        print(f"  ✓ All dates parsed successfully")
    
    # Show date range
    min_date = df[date_column].min()
    max_date = df[date_column].max()
    unique_dates = df[date_column].nunique()
    
    print(f"  Date range: {min_date.date()} to {max_date.date()}")
    print(f"  Unique dates: {unique_dates}")
    
    return df


def standardize_state_names(df):
    """
    COMPREHENSIVE STATE NAME STANDARDIZATION
    Handles all variations found in UIDAI datasets
    Replaces need for separate quickfix.py script
    """
    print(f"\n🗺️  Comprehensive State Name Standardization...")
    print(f"  States BEFORE standardization: {df['state'].nunique()}")
    
    # COMPREHENSIVE STATE NAME MAPPING
    # Covers all variations, typos, and invalid entries
    STATE_NAME_MAPPING = {
        # Odisha variations
        'ODISHA': 'Odisha',
        'odisha': 'Odisha',
        'Orissa': 'Odisha',
        
        # West Bengal variations (most problematic)
        'WEST BENGAL': 'West Bengal',
        'WESTBENGAL': 'West Bengal',
        'Westbengal': 'West Bengal',
        'west Bengal': 'West Bengal',
        'West Bangal': 'West Bengal',
        'West Bengli': 'West Bengal',
        'West  Bengal': 'West Bengal',  # double space
        'west bengal': 'West Bengal',
        'West bengal': 'West Bengal',
        
        # Chhattisgarh variations
        'Chhatisgarh': 'Chhattisgarh',
        'CHHATTISGARH': 'Chhattisgarh',
        
        # Tamil Nadu variations
        'Tamilnadu': 'Tamil Nadu',
        'TAMIL NADU': 'Tamil Nadu',
        
        # Andhra Pradesh variations
        'andhra pradesh': 'Andhra Pradesh',
        'ANDHRA PRADESH': 'Andhra Pradesh',
        
        # Jammu and Kashmir variations
        'Jammu And Kashmir': 'Jammu and Kashmir',
        'Jammu & Kashmir': 'Jammu and Kashmir',
        'JAMMU AND KASHMIR': 'Jammu and Kashmir',
        
        # Uttarakhand variations
        'Uttaranchal': 'Uttarakhand',
        'UTTARAKHAND': 'Uttarakhand',
        
        # Puducherry variations
        'Pondicherry': 'Puducherry',
        'PUDUCHERRY': 'Puducherry',
        
        # Andaman & Nicobar variations
        'Andaman and Nicobar Islands': 'Andaman & Nicobar Islands',
        'Andaman & Nicobar': 'Andaman & Nicobar Islands',
        'A & N Islands': 'Andaman & Nicobar Islands',
        'ANDAMAN & NICOBAR ISLANDS': 'Andaman & Nicobar Islands',
        
        # Dadra & Nagar Haveli and Daman & Diu (merged UT in 2020)
        'Dadra & Nagar Haveli': 'Dadra & Nagar Haveli and Daman & Diu',
        'Daman & Diu': 'Dadra & Nagar Haveli and Daman & Diu',
        'Dadra and Nagar Haveli': 'Dadra & Nagar Haveli and Daman & Diu',
        'Daman and Diu': 'Dadra & Nagar Haveli and Daman & Diu',
        'The Dadra And Nagar Haveli And Daman And Diu': 'Dadra & Nagar Haveli and Daman & Diu',
        'Dadra and Nagar Haveli and Daman and Diu': 'Dadra & Nagar Haveli and Daman & Diu',
                
        # Delhi variations
        'NCT of Delhi': 'Delhi',
        'New Delhi': 'Delhi',
        'DELHI': 'Delhi',
        
        # Other case variations
        'MANIPUR': 'Manipur',
        'TRIPURA': 'Tripura',
        'ASSAM': 'Assam',
        'BIHAR': 'Bihar',
        'GOA': 'Goa',
        'GUJARAT': 'Gujarat',
        'HARYANA': 'Haryana',
        'HIMACHAL PRADESH': 'Himachal Pradesh',
        'JHARKHAND': 'Jharkhand',
        'KARNATAKA': 'Karnataka',
        'KERALA': 'Kerala',
        'MADHYA PRADESH': 'Madhya Pradesh',
        'MAHARASHTRA': 'Maharashtra',
        'MEGHALAYA': 'Meghalaya',
        'MIZORAM': 'Mizoram',
        'NAGALAND': 'Nagaland',
        'PUNJAB': 'Punjab',
        'RAJASTHAN': 'Rajasthan',
        'SIKKIM': 'Sikkim',
        'TELANGANA': 'Telangana',
        'UTTAR PRADESH': 'Uttar Pradesh',
        'CHANDIGARH': 'Chandigarh',
        'LADAKH': 'Ladakh',
        'LAKSHADWEEP': 'Lakshadweep',
        
        # INVALID ENTRIES - Districts/localities mistakenly in state column
        # Map to correct state based on known geography
        'BALANAGAR': 'Telangana',
        'Darbhanga': 'Bihar',
        'Jaipur': 'Rajasthan',
        'Madanapalle': 'Andhra Pradesh',
        'Nagpur': 'Maharashtra',
        'Puttenahalli': 'Karnataka',
        'Raja Annamalai Puram': 'Tamil Nadu',
        
        # Invalid pincode/numeric entries - will be removed
        '100000': None,
    }
    
    # Show problematic states before fixing
    all_states = df['state'].unique()
    problematic = [s for s in all_states if s in STATE_NAME_MAPPING]
    
    if len(problematic) > 0:
        print(f"  ⚠️  Found {len(problematic)} state name variations to fix:")
        for state in sorted(problematic)[:15]:  # Show first 15
            target = STATE_NAME_MAPPING.get(state, state)
            if target:
                print(f"      '{state}' → '{target}'")
        if len(problematic) > 15:
            print(f"      ... and {len(problematic) - 15} more")
    
    # Apply state name standardization
    records_before = len(df)
    df['state'] = df['state'].replace(STATE_NAME_MAPPING)
    
    # Remove rows with None state (invalid entries like pincode '100000')
    df = df[df['state'].notna()].copy()
    records_removed = records_before - len(df)
    
    if records_removed > 0:
        print(f"  🗑️  Removed {records_removed:,} records with invalid state entries")
    
    # Trim whitespace from all state names
    df['state'] = df['state'].str.strip()
    
    # Final count
    final_states = df['state'].nunique()
    print(f"  ✓ States AFTER standardization: {final_states}")
    print(f"  ✓ Total records: {len(df):,}")
    
    # List all final states for verification
    if final_states <= 40:  # Only show if reasonable number
        print(f"\n  📋 Final state list ({final_states} states/UTs):")
        for state in sorted(df['state'].unique()):
            count = len(df[df['state'] == state])
            print(f"      {state:40s} ({count:,} records)")
    
    return df


def validate_geography(df):
    """
    Validate that pincode-district-state combinations are consistent
    """
    print(f"\n🔍 Validating geographic consistency...")
    
    # Group by pincode and check if it maps to multiple districts/states
    pincode_geo = df.groupby('pincode').agg({
        'district': lambda x: x.nunique(),
        'state': lambda x: x.nunique()
    }).reset_index()
    
    # Find inconsistent pincodes
    inconsistent_district = pincode_geo[pincode_geo['district'] > 1]
    inconsistent_state = pincode_geo[pincode_geo['state'] > 1]
    
    print(f"  Pincodes mapping to multiple districts: {len(inconsistent_district):,}")
    print(f"  Pincodes mapping to multiple states: {len(inconsistent_state):,}")
    
    if len(inconsistent_district) > 0:
        print(f"  ⚠️  WARNING: Some pincodes map to multiple districts")
        print(f"  Sample: {inconsistent_district.head(3)['pincode'].tolist()}")
    
    if len(inconsistent_state) > 0:
        print(f"  ⚠️  WARNING: Some pincodes map to multiple states")
        print(f"  Sample: {inconsistent_state.head(3)['pincode'].tolist()}")
    
    return df


def create_date_range_report(df_enrollment, df_biometric, df_demographic):
    """
    Report on date coverage in each dataset
    """
    print(f"\n📊 Date Coverage Analysis:")
    print("="*60)
    
    datasets = {
        'Enrollment': df_enrollment,
        'Biometric': df_biometric,
        'Demographic': df_demographic
    }
    
    for name, df in datasets.items():
        if df['date'].isna().all():
            print(f"\n{name}:")
            print(f"  ❌ All dates are null - parsing failed!")
            continue
        
        min_date = df['date'].min()
        max_date = df['date'].max()
        unique_dates = df['date'].nunique()
        
        # Calculate expected date range
        expected_days = (max_date - min_date).days + 1
        coverage = (unique_dates / expected_days) * 100
        
        print(f"\n{name}:")
        print(f"  Date range: {min_date.date()} to {max_date.date()}")
        print(f"  Expected days: {expected_days}")
        print(f"  Unique dates: {unique_dates}")
        print(f"  Coverage: {coverage:.1f}% (daily data would be 100%)")
        
        # Check if weekly or monthly data
        if coverage < 20:
            print(f"  📌 Appears to be MONTHLY data")
        elif coverage < 50:
            print(f"  📌 Appears to be WEEKLY data")
        else:
            print(f"  📌 Appears to be DAILY or near-daily data")


def merge_datasets(df_enrollment, df_biometric, df_demographic):
    """
    Merge all three datasets on date, state, district, pincode
    """
    print(f"\n🔗 Merging datasets...")
    print("="*60)
    
    # Create copy to avoid modifying originals
    df_enroll = df_enrollment.copy()
    df_bio = df_biometric.copy()
    df_demo = df_demographic.copy()
    
    # Add total columns
    df_enroll['total_enrollment'] = (
        df_enroll['age_0_5'] + 
        df_enroll['age_5_17'] + 
        df_enroll['age_18_greater']
    )
    
    df_bio['total_biometric_updates'] = (
        df_bio['bio_age_5_17'] + 
        df_bio['bio_age_17_']
    )
    
    df_demo['total_demographic_updates'] = (
        df_demo['demo_age_5_17'] + 
        df_demo['demo_age_17_']
    )
    
    # Merge enrollment and biometric
    print("\n  Merging Enrollment + Biometric...")
    df_merged = pd.merge(
        df_enroll,
        df_bio,
        on=['date', 'state', 'district', 'pincode'],
        how='outer',
        suffixes=('', '_bio')
    )
    print(f"  ✓ Shape after Enrollment + Biometric: {df_merged.shape}")
    
    # Merge with demographic
    print("\n  Merging + Demographic...")
    df_merged = pd.merge(
        df_merged,
        df_demo,
        on=['date', 'state', 'district', 'pincode'],
        how='outer',
        suffixes=('', '_demo')
    )
    print(f"  ✓ Final shape: {df_merged.shape}")
    
    # Fill NaN values with 0 (outer join creates NaN for non-matches)
    numeric_columns = df_merged.select_dtypes(include=[np.number]).columns
    df_merged[numeric_columns] = df_merged[numeric_columns].fillna(0)
    
    # Calculate total updates
    df_merged['total_updates'] = (
        df_merged['total_biometric_updates'] + 
        df_merged['total_demographic_updates']
    )
    
    # Calculate UE Ratio
    df_merged['ue_ratio'] = np.where(
        df_merged['total_enrollment'] > 0,
        df_merged['total_updates'] / df_merged['total_enrollment'],
        0
    )
    
    print(f"\n  ✓ Merged dataset created!")
    print(f"  Total records: {len(df_merged):,}")
    print(f"  Columns: {df_merged.shape[1]}")
    
    return df_merged


def save_cleaned_data(df_enrollment, df_biometric, df_demographic, df_merged):
    """
    Save cleaned datasets to processed data directory
    """
    print(f"\n💾 Saving cleaned datasets...")
    print("="*60)
    
    # Save individual cleaned datasets
    df_enrollment.to_csv(
        os.path.join(PROCESSED_DATA_DIR, 'enrollment_clean.csv'),
        index=False
    )
    print(f"  ✓ Saved: enrollment_clean.csv")
    
    df_biometric.to_csv(
        os.path.join(PROCESSED_DATA_DIR, 'biometric_clean.csv'),
        index=False
    )
    print(f"  ✓ Saved: biometric_clean.csv")
    
    df_demographic.to_csv(
        os.path.join(PROCESSED_DATA_DIR, 'demographic_clean.csv'),
        index=False
    )
    print(f"  ✓ Saved: demographic_clean.csv")
    
    # Save merged dataset
    df_merged.to_csv(
        os.path.join(PROCESSED_DATA_DIR, 'merged_data.csv'),
        index=False
    )
    print(f"  ✓ Saved: merged_data.csv ({len(df_merged):,} records)")
    
    # Save a summary report
    with open(os.path.join(PROCESSED_DATA_DIR, 'data_cleaning_report.txt'), 'w') as f:
        f.write("="*60 + "\n")
        f.write("DATA CLEANING REPORT\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("DATASETS:\n")
        f.write(f"  Enrollment: {len(df_enrollment):,} records\n")
        f.write(f"  Biometric: {len(df_biometric):,} records\n")
        f.write(f"  Demographic: {len(df_demographic):,} records\n")
        f.write(f"  Merged: {len(df_merged):,} records\n\n")
        
        f.write("DATE RANGES:\n")
        f.write(f"  Enrollment: {df_enrollment['date'].min().date()} to {df_enrollment['date'].max().date()}\n")
        f.write(f"  Biometric: {df_biometric['date'].min().date()} to {df_biometric['date'].max().date()}\n")
        f.write(f"  Demographic: {df_demographic['date'].min().date() if not df_demographic['date'].isna().all() else 'PARSING FAILED'} to {df_demographic['date'].max().date() if not df_demographic['date'].isna().all() else 'PARSING FAILED'}\n\n")
        
        f.write("GEOGRAPHIC COVERAGE:\n")
        f.write(f"  States: {df_merged['state'].nunique()}\n")
        f.write(f"  Districts: {df_merged['district'].nunique()}\n")
        f.write(f"  Pincodes: {df_merged['pincode'].nunique()}\n\n")
        
        f.write("STATE STANDARDIZATION:\n")
        f.write(f"  Final states: {df_merged['state'].nunique()}\n")
        f.write(f"  States list:\n")
        for state in sorted(df_merged['state'].unique()):
            f.write(f"    - {state}\n")
        f.write("\n")
        
        f.write("KEY COLUMNS IN MERGED DATASET:\n")
        for col in df_merged.columns:
            f.write(f"  - {col}\n")
    
    print(f"  ✓ Saved: data_cleaning_report.txt")


def main():
    """
    Main data cleaning workflow
    INCLUDES COMPREHENSIVE STATE STANDARDIZATION (replaces quickfix.py)
    """
    print("\n" + "="*60)
    print("AADHAAR DATA CLEANING - STEP 2")
    print("Includes Comprehensive State Name Standardization")
    print("="*60)
    
    # Step 1: Load datasets
    df_enrollment, df_biometric, df_demographic = load_datasets()
    
    # Step 2: Standardize dates
    df_enrollment = standardize_dates(df_enrollment, 'date')
    df_biometric = standardize_dates(df_biometric, 'date')
    df_demographic = standardize_dates(df_demographic, 'date')
    
    # Step 3: COMPREHENSIVE State name standardization (replaces quickfix.py)
    print("\n" + "="*60)
    print("COMPREHENSIVE STATE NAME STANDARDIZATION")
    print("(Replaces need for separate quickfix.py)")
    print("="*60)
    df_enrollment = standardize_state_names(df_enrollment)
    df_biometric = standardize_state_names(df_biometric)
    df_demographic = standardize_state_names(df_demographic)
    
    # Step 4: Validate geography
    print("\nValidating Enrollment geography:")
    df_enrollment = validate_geography(df_enrollment)
    print("\nValidating Biometric geography:")
    df_biometric = validate_geography(df_biometric)
    print("\nValidating Demographic geography:")
    df_demographic = validate_geography(df_demographic)
    
    # Step 5: Date coverage report
    create_date_range_report(df_enrollment, df_biometric, df_demographic)
    
    # Step 6: Merge datasets
    df_merged = merge_datasets(df_enrollment, df_biometric, df_demographic)
    
    # Step 7: Save cleaned data
    save_cleaned_data(df_enrollment, df_biometric, df_demographic, df_merged)
    
    # Final summary
    print("\n" + "="*60)
    print("DATA CLEANING COMPLETE!")
    print("="*60)
    print(f"\n✓ Cleaned datasets saved to: {PROCESSED_DATA_DIR}")
    print(f"✓ Merged dataset: {len(df_merged):,} records")
    print(f"✓ States standardized: {df_merged['state'].nunique()} clean states")
    print(f"✓ Districts: {df_merged['district'].nunique()}")
    print(f"✓ Pincodes: {df_merged['pincode'].nunique()}")
    print(f"✓ Ready for analysis!")
    
    print("\n" + "="*60)
    print("✅ NOTE: quickfix.py is NO LONGER NEEDED")
    print("   State standardization is now integrated in this script")
    print("="*60)
    
    print("\n" + "="*60)
    print("Next step: Run 03_dimension1_coverage.py")
    print("="*60)
    
    return df_enrollment, df_biometric, df_demographic, df_merged


if __name__ == "__main__":
    df_enrollment, df_biometric, df_demographic, df_merged = main()
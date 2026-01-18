# # # import pandas as pd

# # # # Load merged data



# # # merged_path = r'C:\Users\atharv\Desktop\aadhaar_analysis\data\processed\merged_data.csv'
# # # df = pd.read_csv(merged_path)

# # # # Method 1: Unique district names (validation approach)
# # # unique_districts = df['district'].nunique()
# # # print(f"Unique district names: {unique_districts}")

# # # # Method 2: State-district combinations (analysis approach)
# # # state_district_pairs = df.groupby(['state', 'district']).size()
# # # print(f"State-district pairs: {len(state_district_pairs)}")

# # # # Method 3: Check for duplicate district names across states
# # # district_state_mapping = df.groupby('district')['state'].nunique()
# # # duplicates = district_state_mapping[district_state_mapping > 1]
# # # print(f"\nDistricts appearing in multiple states:")
# # # print(duplicates)

# # # # Method 4: Full breakdown
# # # full_breakdown = df.groupby(['state', 'district']).size().reset_index(name='records')
# # # print(f"\nTotal state-district combinations: {len(full_breakdown)}")
# # # print("\nFirst 10 rows:")
# # # print(full_breakdown.head(10))

# # # # Method 5: Check what the analysis actually used
# # # district_agg = df.groupby(['state', 'district']).agg({
# # #     'age_0_5': 'sum',
# # #     'age_5_17': 'sum',
# # #     'age_18_greater': 'sum',
# # #     'bio_age_5_17': 'sum',
# # #     'bio_age_17_': 'sum',
# # #     'demo_age_5_17': 'sum',
# # #     'demo_age_17_': 'sum'
# # # }).reset_index()

# # # district_agg['total_enrollment'] = (
# # #     district_agg['age_0_5'] + 
# # #     district_agg['age_5_17'] + 
# # #     district_agg['age_18_greater']
# # # )

# # # district_agg['total_updates'] = (
# # #     district_agg['bio_age_5_17'] + district_agg['bio_age_17_'] +
# # #     district_agg['demo_age_5_17'] + district_agg['demo_age_17_']
# # # )

# # # print(f"\nAfter aggregation: {len(district_agg)} districts")

# # # # Filter to only districts with data
# # # district_agg_filtered = district_agg[
# # #     (district_agg['total_enrollment'] > 0) | 
# # #     (district_agg['total_updates'] > 0)
# # # ]

# # # print(f"After filtering (enrollment OR update > 0): {len(district_agg_filtered)}")

# # # # Check median thresholds
# # # median_enrollment = district_agg_filtered['total_enrollment'].median()
# # # median_updates = district_agg_filtered['total_updates'].median()
# # # print(f"\nMedian enrollment: {median_enrollment}")
# # # print(f"Median updates: {median_updates}")


# # import pandas as pd
# # import numpy as np

# # print("="*70)
# # print("READINESS GAP ANALYSIS - MISSING DISTRICTS INVESTIGATION")
# # print("="*70)

# # # Load merged data
# # merged_path = 'data/processed/merged_data.csv'
# # df = pd.read_csv(merged_path)

# # print("\n[1] INITIAL DISTRICT COUNT")
# # print("-"*70)

# # # Total state-district pairs
# # total_pairs = df.groupby(['state', 'district']).size()
# # print(f"Total state-district pairs in merged data: {len(total_pairs)}")

# # # Aggregate by state-district
# # district_agg = df.groupby(['state', 'district']).agg({
# #     'bio_age_5_17': 'sum',
# #     'bio_age_17_': 'sum',
# #     'age_5_17': 'sum'
# # }).reset_index()

# # print(f"Districts after aggregation: {len(district_agg)}")

# # # Calculate total biometric updates
# # district_agg['total_bio_updates'] = (
# #     district_agg['bio_age_5_17'] + district_agg['bio_age_17_']
# # )

# # print("\n[2] BIOMETRIC UPDATE DISTRIBUTION")
# # print("-"*70)

# # # Check how many districts have zero bio updates
# # zero_bio = district_agg[district_agg['total_bio_updates'] == 0]
# # print(f"Districts with ZERO biometric updates: {len(zero_bio)}")

# # non_zero_bio = district_agg[district_agg['total_bio_updates'] > 0]
# # print(f"Districts with bio updates > 0: {len(non_zero_bio)}")

# # print("\n[3] READINESS SCORE CALCULATION")
# # print("-"*70)

# # # Calculate readiness score (only for districts with bio updates)
# # district_agg['readiness_score'] = np.where(
# #     district_agg['total_bio_updates'] > 0,
# #     (district_agg['bio_age_5_17'] / district_agg['total_bio_updates']) * 100,
# #     np.nan  # NaN for districts with zero bio updates
# # )

# # # Count districts with calculable readiness scores
# # calculable = district_agg[~district_agg['readiness_score'].isna()]
# # print(f"Districts with calculable readiness score: {len(calculable)}")

# # not_calculable = district_agg[district_agg['readiness_score'].isna()]
# # print(f"Districts with NO readiness score (NaN): {len(not_calculable)}")

# # print("\n[4] READINESS CATEGORY CLASSIFICATION")
# # print("-"*70)

# # # Define thresholds (from utils/config.py)
# # GOOD_READINESS = 30
# # MODERATE_READINESS = 15
# # CRITICAL_READINESS = 10

# # # Classify only districts with calculable scores
# # district_agg['readiness_category'] = pd.cut(
# #     district_agg['readiness_score'],
# #     bins=[0, CRITICAL_READINESS, MODERATE_READINESS, GOOD_READINESS, 100],
# #     labels=['Critical', 'Low', 'Moderate', 'Good']
# # )

# # # Count by category (excluding NaN)
# # print("\nReadiness Category Distribution:")
# # category_counts = district_agg['readiness_category'].value_counts()
# # for category in ['Good', 'Moderate', 'Low', 'Critical']:
# #     count = category_counts.get(category, 0)
# #     print(f"  {category:12s}: {count:4d}")

# # print(f"  {'Unclassified':12s}: {district_agg['readiness_category'].isna().sum():4d}")

# # total_classified = category_counts.sum()
# # print(f"\n  Total Classified: {total_classified}")
# # print(f"  Total Districts:  {len(district_agg)}")
# # print(f"  Missing:          {len(district_agg) - total_classified}")

# # print("\n[5] DETAILED BREAKDOWN OF MISSING DISTRICTS")
# # print("-"*70)

# # # Get the unclassified districts
# # unclassified = district_agg[district_agg['readiness_category'].isna()].copy()

# # print(f"\nTotal unclassified districts: {len(unclassified)}")
# # print(f"\nBreakdown by reason:")

# # # Reason 1: Zero bio updates
# # zero_bio_updates = unclassified[unclassified['total_bio_updates'] == 0]
# # print(f"  - Zero biometric updates: {len(zero_bio_updates)}")

# # # Reason 2: Zero youth enrollment (can't assess readiness)
# # zero_youth = unclassified[
# #     (unclassified['total_bio_updates'] > 0) & 
# #     (unclassified['age_5_17'] == 0)
# # ]
# # print(f"  - Zero youth enrollment: {len(zero_youth)}")

# # # Reason 3: Other (edge cases)
# # other = unclassified[
# #     (unclassified['total_bio_updates'] > 0) & 
# #     (unclassified['age_5_17'] > 0)
# # ]
# # print(f"  - Other reasons: {len(other)}")

# # print("\n[6] SAMPLE OF UNCLASSIFIED DISTRICTS")
# # print("-"*70)

# # if len(unclassified) > 0:
# #     print("\nFirst 10 unclassified districts:")
# #     sample = unclassified.head(10)[['state', 'district', 'total_bio_updates', 
# #                                      'bio_age_5_17', 'age_5_17', 'readiness_score']]
# #     print(sample.to_string(index=False))
    
# #     print(f"\n... and {max(0, len(unclassified) - 10)} more")

# # print("\n[7] STATE-WISE BREAKDOWN OF UNCLASSIFIED DISTRICTS")
# # print("-"*70)

# # if len(unclassified) > 0:
# #     state_breakdown = unclassified['state'].value_counts()
# #     print("\nTop 10 states with most unclassified districts:")
# #     print(state_breakdown.head(10))

# # print("\n[8] VERIFICATION AGAINST EXPECTED NUMBERS")
# # print("-"*70)

# # expected_good = 798
# # expected_moderate = 122
# # expected_low = 22
# # expected_critical = 27
# # expected_total_classified = 969

# # actual_good = category_counts.get('Good', 0)
# # actual_moderate = category_counts.get('Moderate', 0)
# # actual_low = category_counts.get('Low', 0)
# # actual_critical = category_counts.get('Critical', 0)
# # actual_total_classified = total_classified

# # print(f"\nExpected vs Actual:")
# # print(f"  Good:       {expected_good:4d} (expected) vs {actual_good:4d} (actual)")
# # print(f"  Moderate:   {expected_moderate:4d} (expected) vs {actual_moderate:4d} (actual)")
# # print(f"  Low:        {expected_low:4d} (expected) vs {actual_low:4d} (actual)")
# # print(f"  Critical:   {expected_critical:4d} (expected) vs {actual_critical:4d} (actual)")
# # print(f"  Total:      {expected_total_classified:4d} (expected) vs {actual_total_classified:4d} (actual)")

# # matches = (
# #     actual_good == expected_good and
# #     actual_moderate == expected_moderate and
# #     actual_low == expected_low and
# #     actual_critical == expected_critical
# # )

# # if matches:
# #     print("\n✅ VERIFICATION PASSED: All categories match expected values!")
# # else:
# #     print("\n⚠️  VERIFICATION WARNING: Some discrepancies found")

# # print("\n[9] FINAL SUMMARY")
# # print("-"*70)

# # print(f"""
# # Total state-district pairs:        {len(district_agg)}
# # Districts with bio updates:        {len(non_zero_bio)}
# # Districts with zero bio updates:   {len(zero_bio)}

# # Classified districts:              {total_classified}
# #   ├─ Good (≥30%):                  {actual_good}
# #   ├─ Moderate (15-30%):            {actual_moderate}
# #   ├─ Low (10-15%):                 {actual_low}
# #   └─ Critical (<10%):              {actual_critical}

# # Unclassified districts:            {len(unclassified)}

# # Missing from analysis:             {len(district_agg) - total_classified}
# # Expected missing (1,051 - 969):    82
# # """)

# # print("="*70)
# # print("ANALYSIS COMPLETE")
# # print("="*70)  


# import pandas as pd
# df = pd.read_csv('data/processed/merged_data.csv')

# # Search for all variations of Champaran
# champaran = df[df['district'].str.contains('Champaran', case=False, na=False)]
# unique_champaran = champaran.groupby(['state', 'district']).size()
# print(unique_champaran)


# import pandas as pd
# import numpy as np
# df = pd.read_csv('data/processed/merged_data.csv')
# agg = df.groupby(['state','district']).agg({'bio_age_5_17':'sum','bio_age_17_':'sum','age_5_17':'sum'}).reset_index()
# agg['total_bio'] = agg['bio_age_5_17'] + agg['bio_age_17_']
# agg['readiness'] = np.where(agg['total_bio']>0, (agg['bio_age_5_17']/agg['total_bio'])*100, np.nan)
# other = agg[(agg['total_bio']>0) & (agg['age_5_17']>0) & (agg['readiness'].isna())]
# print(other[['state','district','total_bio','bio_age_5_17','age_5_17','readiness']])




# import pandas as pd

# # Load final merged dataset (single source of truth)
# df = pd.read_csv("data/processed/merged_data.csv")

# print("=" * 70)
# print("PINCODE ↔ DISTRICT MAPPING VALIDATION")
# print("=" * 70)

# # -------------------------------------------------------------------
# # 1. Districts with ZERO pincodes
# # -------------------------------------------------------------------
# print("\n[1] DISTRICTS WITH ZERO PINCODES")

# # All districts present in dataset
# all_districts = (
#     df[['state', 'district']]
#     .drop_duplicates()
#     .reset_index(drop=True)
# )

# # Districts that have at least one non-null pincode
# districts_with_pincode = (
#     df[df['pincode'].notna()]
#     [['state', 'district']]
#     .drop_duplicates()
# )

# # Left-anti join: districts without pincodes
# districts_without_pincode = (
#     all_districts
#     .merge(
#         districts_with_pincode,
#         on=['state', 'district'],
#         how='left',
#         indicator=True
#     )
#     .query("_merge == 'left_only'")
#     .drop(columns="_merge")
# )

# print(f"Total districts (state–district pairs): {len(all_districts)}")
# print(f"Districts with NO pincodes: {len(districts_without_pincode)}")

# if len(districts_without_pincode) > 0:
#     print("\nList of districts with no pincodes:")
#     for _, row in districts_without_pincode.iterrows():
#         print(f"  - {row['district']} ({row['state']})")
# else:
#     print("✓ All districts have at least one pincode")

# # -------------------------------------------------------------------
# # 2. Pincodes mapped to MULTIPLE districts
# # -------------------------------------------------------------------
# print("\n[2] PINCODES MAPPED TO MULTIPLE DISTRICTS")

# # Count unique districts per pincode
# pincode_district_counts = (
#     df[df['pincode'].notna()]
#     .groupby('pincode')[['state', 'district']]
#     .nunique()
#     .reset_index()
# )

# # Pincodes appearing in more than one district
# shared_pincodes = pincode_district_counts[
#     (pincode_district_counts['district'] > 1) |
#     (pincode_district_counts['state'] > 1)
# ]

# print(f"Total unique pincodes: {df['pincode'].nunique()}")
# print(f"Pincodes mapped to multiple districts: {len(shared_pincodes)}")

# if len(shared_pincodes) > 0:
#     print("\nSample of problematic pincodes:")
#     for pincode in shared_pincodes['pincode'].head(10):
#         mappings = (
#             df[df['pincode'] == pincode][['state', 'district']]
#             .drop_duplicates()
#         )
#         print(f"\nPincode {pincode} appears in:")
#         for _, row in mappings.iterrows():
#             print(f"  - {row['district']} ({row['state']})")
# else:
#     print("✓ No pincodes are shared across districts")

# # -------------------------------------------------------------------
# # Summary
# # -------------------------------------------------------------------
# print("\n" + "=" * 70)
# print("SUMMARY")
# print("=" * 70)
# print(f"Districts without pincodes: {len(districts_without_pincode)}")
# print(f"Pincodes mapped to multiple districts: {len(shared_pincodes)}")
# print("=" * 70)



import pandas as pd

df = pd.read_csv('data/processed/merged_data.csv')

# Find all districts that might be duplicates (similar names)
from collections import defaultdict
import difflib

# Get all unique state-district pairs
districts = df.groupby(['state', 'district']).size().reset_index()

# For each state, check for similar district names
print("POTENTIAL DISTRICT NAME DUPLICATES")
print("="*70)

for state in districts['state'].unique():
    state_districts = districts[districts['state'] == state]['district'].tolist()
    
    # Find similar names
    similar_groups = defaultdict(list)
    checked = set()
    
    for i, d1 in enumerate(state_districts):
        if d1 in checked:
            continue
        
        group = [d1]
        for d2 in state_districts[i+1:]:
            if d2 in checked:
                continue
            
            # Check similarity (80% threshold)
            similarity = difflib.SequenceMatcher(None, d1.lower(), d2.lower()).ratio()
            if similarity > 0.8:
                group.append(d2)
                checked.add(d2)
        
        if len(group) > 1:
            checked.add(d1)
            similar_groups[state].append(group)
    
    if similar_groups[state]:
        print(f"\n{state}:")
        for group in similar_groups[state]:
            print(f"  {group}")

print("\n" + "="*70)
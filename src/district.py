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



# import pandas as pd

# df = pd.read_csv('data/processed/merged_data.csv')

# # Find all districts that might be duplicates (similar names)
# from collections import defaultdict
# import difflib

# # Get all unique state-district pairs
# districts = df.groupby(['state', 'district']).size().reset_index()

# # For each state, check for similar district names
# print("POTENTIAL DISTRICT NAME DUPLICATES")
# print("="*70)

# for state in districts['state'].unique():
#     state_districts = districts[districts['state'] == state]['district'].tolist()
    
#     # Find similar names
#     similar_groups = defaultdict(list)
#     checked = set()
    
#     for i, d1 in enumerate(state_districts):
#         if d1 in checked:
#             continue
        
#         group = [d1]
#         for d2 in state_districts[i+1:]:
#             if d2 in checked:
#                 continue
            
#             # Check similarity (80% threshold)
#             similarity = difflib.SequenceMatcher(None, d1.lower(), d2.lower()).ratio()
#             if similarity > 0.8:
#                 group.append(d2)
#                 checked.add(d2)
        
#         if len(group) > 1:
#             checked.add(d1)
#             similar_groups[state].append(group)
    
#     if similar_groups[state]:
#         print(f"\n{state}:")
#         for group in similar_groups[state]:
#             print(f"  {group}")

# print("\n" + "="*70)



"""
Pincode Analysis Script
Identifies pincodes with geographic inconsistencies (mapping to multiple states/districts)
Similar to district.py but for pincode-level issues
"""

import pandas as pd
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import PROCESSED_DATA_DIR

print("="*80)
print("PINCODE GEOGRAPHIC CONSISTENCY ANALYSIS")
print("="*80)
print()

# Load merged dataset
print("Loading merged dataset...")
df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'merged_data.csv'))
print(f"✓ Loaded {len(df):,} records")
print()

# =============================================================================
# ANALYSIS 1: PINCODES MAPPING TO MULTIPLE STATES
# =============================================================================
print("="*80)
print("ANALYSIS 1: PINCODES MAPPING TO MULTIPLE STATES")
print("="*80)
print()

# Group by pincode and check unique states
pincode_states = df.groupby('pincode')['state'].unique().reset_index()
pincode_states['num_states'] = pincode_states['state'].apply(len)

# Find problematic pincodes
multi_state_pincodes = pincode_states[pincode_states['num_states'] > 1].copy()
multi_state_pincodes = multi_state_pincodes.sort_values('num_states', ascending=False)

print(f"Total unique pincodes: {len(pincode_states):,}")
print(f"Pincodes mapping to MULTIPLE states: {len(multi_state_pincodes):,}")
print(f"Percentage: {(len(multi_state_pincodes)/len(pincode_states)*100):.2f}%")
print()

if len(multi_state_pincodes) > 0:
    print("Top 20 pincodes by number of states:")
    print("-" * 80)
    for idx, row in multi_state_pincodes.head(20).iterrows():
        pincode = row['pincode']
        states = row['state']
        num_states = row['num_states']
        
        print(f"  Pincode {pincode}: maps to {num_states} states")
        print(f"    States: {', '.join(states)}")
        
        # Get sample records
        sample = df[df['pincode'] == pincode][['state', 'district']].drop_duplicates().head(5)
        for _, s in sample.iterrows():
            print(f"      • {s['state']} / {s['district']}")
        print()

# =============================================================================
# ANALYSIS 2: PINCODES MAPPING TO MULTIPLE DISTRICTS
# =============================================================================
print("="*80)
print("ANALYSIS 2: PINCODES MAPPING TO MULTIPLE DISTRICTS")
print("="*80)
print()

# Group by pincode and check unique districts
pincode_districts = df.groupby('pincode')['district'].unique().reset_index()
pincode_districts['num_districts'] = pincode_districts['district'].apply(len)

# Find problematic pincodes
multi_district_pincodes = pincode_districts[pincode_districts['num_districts'] > 1].copy()
multi_district_pincodes = multi_district_pincodes.sort_values('num_districts', ascending=False)

print(f"Pincodes mapping to MULTIPLE districts: {len(multi_district_pincodes):,}")
print(f"Percentage: {(len(multi_district_pincodes)/len(pincode_districts)*100):.2f}%")
print()

if len(multi_district_pincodes) > 0:
    print("Top 20 pincodes by number of districts:")
    print("-" * 80)
    for idx, row in multi_district_pincodes.head(20).iterrows():
        pincode = row['pincode']
        districts = row['district']
        num_districts = row['num_districts']
        
        print(f"  Pincode {pincode}: maps to {num_districts} districts")
        print(f"    Districts: {', '.join(districts[:5])}")
        if num_districts > 5:
            print(f"    ... and {num_districts - 5} more")
        
        # Get states for this pincode
        states_for_pincode = df[df['pincode'] == pincode]['state'].unique()
        print(f"    State(s): {', '.join(states_for_pincode)}")
        print()

# =============================================================================
# ANALYSIS 3: CATEGORIZE PINCODE ISSUES
# =============================================================================
print("="*80)
print("ANALYSIS 3: CATEGORIZATION OF ISSUES")
print("="*80)
print()

# Merge the two analyses
pincode_analysis = pincode_states.merge(
    pincode_districts, 
    on='pincode', 
    suffixes=('_state', '_district')
)

# Categorize issues
def categorize_issue(row):
    if row['num_states'] > 1 and row['num_districts'] > 1:
        return 'CRITICAL: Multiple States AND Districts'
    elif row['num_states'] > 1:
        return 'HIGH: Multiple States (Same Districts)'
    elif row['num_districts'] > 1:
        return 'MEDIUM: Multiple Districts (Same State)'
    else:
        return 'OK: Consistent'

pincode_analysis['issue_category'] = pincode_analysis.apply(categorize_issue, axis=1)

# Count by category
issue_counts = pincode_analysis['issue_category'].value_counts()
print("Pincode Issues by Category:")
print("-" * 80)
for category, count in issue_counts.items():
    pct = (count / len(pincode_analysis)) * 100
    print(f"  {category}: {count:,} ({pct:.2f}%)")
print()

# =============================================================================
# ANALYSIS 4: SPECIFIC EXAMPLES OF CRITICAL CASES
# =============================================================================
print("="*80)
print("ANALYSIS 4: DETAILED EXAMPLES OF CRITICAL CASES")
print("="*80)
print()

critical_pincodes = pincode_analysis[
    pincode_analysis['issue_category'] == 'CRITICAL: Multiple States AND Districts'
].copy()

if len(critical_pincodes) > 0:
    print(f"Found {len(critical_pincodes):,} CRITICAL pincodes")
    print()
    print("Top 10 Critical Cases:")
    print("-" * 80)
    
    for idx, row in critical_pincodes.head(10).iterrows():
        pincode = row['pincode']
        states = row['state']
        districts = row['district']
        
        print(f"\nPincode: {pincode}")
        print(f"  States ({len(states)}): {', '.join(states)}")
        print(f"  Districts ({len(districts)}): {', '.join(districts[:10])}")
        if len(districts) > 10:
            print(f"  ... and {len(districts) - 10} more districts")
        
        # Get all state-district combinations for this pincode
        combinations = df[df['pincode'] == pincode][['state', 'district']].drop_duplicates()
        print(f"  All combinations ({len(combinations)}):")
        for _, combo in combinations.head(10).iterrows():
            record_count = len(df[(df['pincode'] == pincode) & 
                                 (df['state'] == combo['state']) & 
                                 (df['district'] == combo['district'])])
            print(f"    • {combo['state']} / {combo['district']} ({record_count} records)")
        if len(combinations) > 10:
            print(f"    ... and {len(combinations) - 10} more combinations")

# =============================================================================
# ANALYSIS 5: COMMON PATTERNS
# =============================================================================
print()
print("="*80)
print("ANALYSIS 5: COMMON PATTERNS IN PROBLEMATIC PINCODES")
print("="*80)
print()

# Check if certain states are more problematic
state_pincode_issues = []
for state in df['state'].unique():
    pincodes_in_state = df[df['state'] == state]['pincode'].unique()
    problematic = len([p for p in pincodes_in_state if p in multi_state_pincodes['pincode'].values])
    total = len(pincodes_in_state)
    pct = (problematic / total * 100) if total > 0 else 0
    state_pincode_issues.append({
        'state': state,
        'total_pincodes': total,
        'problematic_pincodes': problematic,
        'percentage': pct
    })

state_issues_df = pd.DataFrame(state_pincode_issues).sort_values('problematic_pincodes', ascending=False)

print("Top 10 States with Most Problematic Pincodes:")
print("-" * 80)
for idx, row in state_issues_df.head(10).iterrows():
    print(f"  {row['state']:40s}: {row['problematic_pincodes']:4d} / {row['total_pincodes']:5d} ({row['percentage']:5.2f}%)")

# =============================================================================
# ANALYSIS 6: POTENTIAL CAUSES
# =============================================================================
print()
print("="*80)
print("ANALYSIS 6: POTENTIAL ROOT CAUSES")
print("="*80)
print()

print("Investigating potential causes for pincode inconsistencies:")
print("-" * 80)
print()

# Cause 1: Border area pincodes
print("1. BORDER AREA PINCODES")
print("   Some pincodes may genuinely span state/district boundaries")
print("   (e.g., Chandigarh-Punjab-Haryana border)")
print()

border_states = ['Chandigarh', 'Delhi', 'Puducherry']
border_pincodes = df[df['state'].isin(border_states)]['pincode'].unique()
border_problematic = len([p for p in border_pincodes if p in multi_state_pincodes['pincode'].values])
print(f"   Border UTs with issues: {border_problematic} / {len(border_pincodes)} pincodes")
print()

# Cause 2: Data entry errors
print("2. DATA ENTRY ERRORS")
print("   Check for pincodes with leading zeros or format issues")
print()

# Check pincode lengths
df['pincode_str'] = df['pincode'].astype(str)
df['pincode_len'] = df['pincode_str'].str.len()
pincode_len_dist = df['pincode_len'].value_counts().sort_index()
print("   Pincode length distribution:")
for length, count in pincode_len_dist.items():
    print(f"     {length} digits: {count:,} records")
print()

# Cause 3: Invalid pincodes
print("3. POTENTIALLY INVALID PINCODES")
print("   India pincodes should be 6 digits (100001-855555)")
print()

invalid_pincodes = df[(df['pincode'] < 100000) | (df['pincode'] > 855555)]['pincode'].unique()
print(f"   Pincodes outside valid range: {len(invalid_pincodes):,}")
if len(invalid_pincodes) > 0:
    print(f"   Examples: {invalid_pincodes[:10].tolist()}")
print()

# Cause 4: District reorganization
print("4. DISTRICT REORGANIZATION")
print("   New districts created in 2023-2024 may cause confusion")
print()

# Check if certain districts appear more frequently
district_with_multi_pincode = df[df['pincode'].isin(multi_district_pincodes['pincode'])]['district'].value_counts().head(10)
print("   Top 10 districts with most multi-mapped pincodes:")
for district, count in district_with_multi_pincode.items():
    print(f"     {district:40s}: {count:,} records")

# =============================================================================
# SAVE RESULTS
# =============================================================================
print()
print("="*80)
print("SAVING ANALYSIS RESULTS")
print("="*80)
print()

output_dir = os.path.join(os.path.dirname(PROCESSED_DATA_DIR), 'outputs', 'tables')

# Save critical pincodes
critical_file = os.path.join(output_dir, 'pincode_critical_issues.csv')
critical_pincodes_detailed = df[df['pincode'].isin(critical_pincodes['pincode'])][
    ['pincode', 'state', 'district']
].drop_duplicates().sort_values(['pincode', 'state', 'district'])
critical_pincodes_detailed.to_csv(critical_file, index=False)
print(f"✓ Saved: pincode_critical_issues.csv ({len(critical_pincodes_detailed)} records)")

# Save all multi-state pincodes
multi_state_file = os.path.join(output_dir, 'pincode_multi_state.csv')
multi_state_detailed = df[df['pincode'].isin(multi_state_pincodes['pincode'])][
    ['pincode', 'state', 'district']
].drop_duplicates().sort_values(['pincode', 'state', 'district'])
multi_state_detailed.to_csv(multi_state_file, index=False)
print(f"✓ Saved: pincode_multi_state.csv ({len(multi_state_detailed)} records)")

# Save summary
summary_file = os.path.join(output_dir, 'pincode_analysis_summary.csv')
pincode_analysis.to_csv(summary_file, index=False)
print(f"✓ Saved: pincode_analysis_summary.csv ({len(pincode_analysis)} records)")

# Save state-level summary
state_summary_file = os.path.join(output_dir, 'pincode_issues_by_state.csv')
state_issues_df.to_csv(state_summary_file, index=False)
print(f"✓ Saved: pincode_issues_by_state.csv ({len(state_issues_df)} records)")

# =============================================================================
# RECOMMENDATIONS
# =============================================================================
print()
print("="*80)
print("RECOMMENDATIONS")
print("="*80)
print()

print("Based on this analysis, recommended actions:")
print()

print("1. IMMEDIATE PRIORITY:")
print(f"   ✓ Investigate {len(critical_pincodes):,} CRITICAL pincodes")
print("     (mapping to multiple states AND districts)")
print("   ✓ Cross-reference with official India Post pincode database")
print("   ✓ Identify data entry errors vs. genuine edge cases")
print()

print("2. HIGH PRIORITY:")
print(f"   ✓ Review {len(multi_state_pincodes):,} pincodes mapping to multiple states")
print("   ✓ Determine if border-area pincodes are legitimate")
print("   ✓ Create pincode correction mapping for known errors")
print()

print("3. MEDIUM PRIORITY:")
print(f"   ✓ Validate {len(invalid_pincodes):,} pincodes outside valid range")
print("   ✓ Check for leading zero issues in pincode storage")
print("   ✓ Verify district assignments for recently reorganized areas")
print()

print("4. LONG-TERM:")
print("   ✓ Implement pincode validation at data entry")
print("   ✓ Create authoritative pincode-district-state mapping table")
print("   ✓ Regular audits of geographic consistency")
print()

print("="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print()
print("Review the generated CSV files for detailed pincode-level data:")
print(f"  • {critical_file}")
print(f"  • {multi_state_file}")
print(f"  • {summary_file}")
print(f"  • {state_summary_file}")
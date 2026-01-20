# # """
# # GROUND TRUTH VALIDATION SCRIPT
# # ===============================
# # Establishes authoritative numbers from cleaned datasets (BEFORE merging)
# # Compares against PDF claims to identify all discrepancies

# # This script loads the CLEANED datasets (after state/district standardization)
# # but BEFORE the merge operation that uses fillna(0) which creates phantom records.

# # Author: Validation Analysis
# # Date: 2026-01-20
# # """

# # import pandas as pd
# # import numpy as np
# # import os
# # import sys

# # # Paths (adjust if needed)
# # PROCESSED_DATA_DIR = 'data/processed'

# # print("="*80)
# # print("GROUND TRUTH VALIDATION")
# # print("="*80)
# # print("\nLoading CLEANED datasets (before merging)...")
# # print("These represent the TRUE source data after standardization\n")

# # # ============================================================================
# # # STEP 1: Load cleaned datasets (BEFORE merge with fillna)
# # # ============================================================================

# # try:
# #     df_enrollment = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'enrollment_clean.csv'))
# #     df_biometric = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'biometric_clean.csv'))
# #     df_demographic = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'demographic_clean.csv'))
# #     df_merged = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'merged_data.csv'))
    
# #     print("✓ All datasets loaded successfully\n")
# #     print(f"  Enrollment records:  {len(df_enrollment):>12,}")
# #     print(f"  Biometric records:   {len(df_biometric):>12,}")
# #     print(f"  Demographic records: {len(df_demographic):>12,}")
# #     print(f"  Merged records:      {len(df_merged):>12,}")
    
# # except FileNotFoundError as e:
# #     print(f"❌ ERROR: Could not find processed data files")
# #     print(f"   Make sure you've run 02_data_cleaning.py first")
# #     print(f"   Error: {e}")
# #     sys.exit(1)

# # # ============================================================================
# # # STEP 2: Calculate TRUE ENROLLMENT TOTALS
# # # ============================================================================

# # print("\n" + "="*80)
# # print("GROUND TRUTH: ENROLLMENT TOTALS")
# # print("="*80)

# # # From ENROLLMENT dataset only (no merge artifacts)
# # total_age_0_5 = df_enrollment['age_0_5'].sum()
# # total_age_5_17 = df_enrollment['age_5_17'].sum()
# # total_age_18_greater = df_enrollment['age_18_greater'].sum()
# # total_enrollments_TRUE = total_age_0_5 + total_age_5_17 + total_age_18_greater

# # print(f"\n✓ TRUE Enrollment Totals (from enrollment_clean.csv):")
# # print(f"  Age 0-5:        {total_age_0_5:>12,}  ({(total_age_0_5/total_enrollments_TRUE)*100:>5.1f}%)")
# # print(f"  Age 5-17:       {total_age_5_17:>12,}  ({(total_age_5_17/total_enrollments_TRUE)*100:>5.1f}%)")
# # print(f"  Age 18+:        {total_age_18_greater:>12,}  ({(total_age_18_greater/total_enrollments_TRUE)*100:>5.1f}%)")
# # print(f"  {'─'*50}")
# # print(f"  TOTAL:          {total_enrollments_TRUE:>12,}  (100.0%)")

# # child_enrollment_pct = ((total_age_0_5 + total_age_5_17) / total_enrollments_TRUE) * 100
# # print(f"\n  Children (0-17): {child_enrollment_pct:>11.1f}%")
# # print(f"  Adults (18+):    {((total_age_18_greater/total_enrollments_TRUE)*100):>11.1f}%")

# # # ============================================================================
# # # STEP 3: Calculate TRUE UPDATE TOTALS
# # # ============================================================================

# # print("\n" + "="*80)
# # print("GROUND TRUTH: UPDATE TOTALS")
# # print("="*80)

# # # From BIOMETRIC dataset only
# # total_bio_age_5_17 = df_biometric['bio_age_5_17'].sum()
# # total_bio_age_17_plus = df_biometric['bio_age_17_'].sum()
# # total_biometric_updates = total_bio_age_5_17 + total_bio_age_17_plus

# # # From DEMOGRAPHIC dataset only
# # total_demo_age_5_17 = df_demographic['demo_age_5_17'].sum()
# # total_demo_age_17_plus = df_demographic['demo_age_17_'].sum()
# # total_demographic_updates = total_demo_age_5_17 + total_demo_age_17_plus

# # # TOTAL
# # total_updates_TRUE = total_biometric_updates + total_demographic_updates

# # print(f"\n✓ TRUE Biometric Updates (from biometric_clean.csv):")
# # print(f"  Age 5-17:       {total_bio_age_5_17:>12,}")
# # print(f"  Age 17+:        {total_bio_age_17_plus:>12,}")
# # print(f"  {'─'*50}")
# # print(f"  TOTAL BIO:      {total_biometric_updates:>12,}")

# # print(f"\n✓ TRUE Demographic Updates (from demographic_clean.csv):")
# # print(f"  Age 5-17:       {total_demo_age_5_17:>12,}")
# # print(f"  Age 17+:        {total_demo_age_17_plus:>12,}")
# # print(f"  {'─'*50}")
# # print(f"  TOTAL DEMO:     {total_demographic_updates:>12,}")

# # print(f"\n✓ TRUE Total Updates:")
# # print(f"  Bio + Demo:     {total_updates_TRUE:>12,}")

# # # Youth bio updates (for readiness analysis)
# # youth_bio_pct = (total_bio_age_5_17 / total_biometric_updates) * 100
# # print(f"\n  Youth (5-17) % of bio updates: {youth_bio_pct:.1f}%")

# # # ============================================================================
# # # STEP 4: Calculate TRUE UE RATIO
# # # ============================================================================

# # print("\n" + "="*80)
# # print("GROUND TRUTH: UE RATIO")
# # print("="*80)

# # ue_ratio_TRUE = total_updates_TRUE / total_enrollments_TRUE

# # print(f"\n✓ TRUE UE Ratio Calculation:")
# # print(f"  Total Updates:      {total_updates_TRUE:>12,}")
# # print(f"  Total Enrollments:  {total_enrollments_TRUE:>12,}")
# # print(f"  {'─'*50}")
# # print(f"  UE Ratio:           {ue_ratio_TRUE:>12.2f}×")
# # print(f"  (Updates outnumber enrollments by {ue_ratio_TRUE:.1f}×)")

# # # ============================================================================
# # # STEP 5: Geographic Coverage
# # # ============================================================================

# # print("\n" + "="*80)
# # print("GROUND TRUTH: GEOGRAPHIC COVERAGE")
# # print("="*80)

# # states_enrollment = df_enrollment['state'].nunique()
# # districts_enrollment = df_enrollment['district'].nunique()
# # pincodes_enrollment = df_enrollment['pincode'].nunique()

# # states_merged = df_merged['state'].nunique()
# # districts_merged = df_merged['district'].nunique()
# # pincodes_merged = df_merged['pincode'].nunique()

# # print(f"\n✓ From Enrollment Dataset:")
# # print(f"  States:    {states_enrollment:>6,}")
# # print(f"  Districts: {districts_enrollment:>6,}")
# # print(f"  Pincodes:  {pincodes_enrollment:>6,}")

# # print(f"\n✓ From Merged Dataset (union of all):")
# # print(f"  States:    {states_merged:>6,}")
# # print(f"  Districts: {districts_merged:>6,}")
# # print(f"  Pincodes:  {pincodes_merged:>6,}")

# # # ============================================================================
# # # STEP 6: Compare Against MERGED Dataset (to show the problem)
# # # ============================================================================

# # print("\n" + "="*80)
# # print("PROBLEM DEMONSTRATION: MERGED vs CLEAN DATASETS")
# # print("="*80)

# # # Calculate from merged dataset (with fillna artifacts)
# # total_enrollment_merged = df_merged['age_0_5'].sum() + df_merged['age_5_17'].sum() + df_merged['age_18_greater'].sum()

# # print(f"\n⚠️  Enrollment totals COMPARISON:")
# # print(f"  From enrollment_clean.csv: {total_enrollments_TRUE:>12,}  ✓ CORRECT")
# # print(f"  From merged_data.csv:      {total_enrollment_merged:>12,}  ✗ WRONG")
# # print(f"  {'─'*50}")
# # print(f"  Difference (phantom):      {total_enrollment_merged - total_enrollments_TRUE:>12,}")
# # print(f"\n  The merged dataset has {total_enrollment_merged - total_enrollments_TRUE:,} phantom enrollments")
# # print(f"  caused by fillna(0) after outer join!")

# # # ============================================================================
# # # STEP 7: Compare Against PDF Claims
# # # ============================================================================

# # print("\n" + "="*80)
# # print("PDF VERIFICATION: GROUND TRUTH vs PDF CLAIMS")
# # print("="*80)

# # # PDF claims (from your document)
# # pdf_claims = {
# #     'total_enrollments': 7_392_727,
# #     'total_updates': 139_373_139,
# #     'ue_ratio': 18.85,
# #     'child_0_5_pct': 67.2,
# #     'child_5_17_pct': 30.1,
# #     'adult_pct': 2.9,  # or 2.7
# #     'child_total_pct': 97.3,
# #     'states': 36,
# #     'districts': 865,
# #     'pincodes': 19_814,
# #     'bio_updates': 84_386_737,
# #     'demo_updates': 54_986_402,
# # }

# # def compare_values(name, ground_truth, pdf_claim, is_percentage=False):
# #     """Compare ground truth vs PDF claim and show status"""
# #     if is_percentage:
# #         diff = abs(ground_truth - pdf_claim)
# #         match = diff < 0.1  # Within 0.1%
# #         status = "✓" if match else "✗"
# #         return f"  {name:30s} {ground_truth:>8.1f}%  vs  {pdf_claim:>8.1f}%  {status}"
# #     else:
# #         diff = abs(ground_truth - pdf_claim)
# #         match = diff == 0
# #         status = "✓" if match else "✗"
# #         diff_str = f"(Δ {diff:,})" if not match else ""
# #         return f"  {name:30s} {ground_truth:>12,}  vs  {pdf_claim:>12,}  {status} {diff_str}"

# # print("\nComparison Table:")
# # print("  Metric                         Ground Truth      PDF Claim      Status")
# # print("  " + "─"*76)

# # # Enrollments
# # print(compare_values("Total Enrollments", total_enrollments_TRUE, pdf_claims['total_enrollments']))
# # print(compare_values("Total Updates", total_updates_TRUE, pdf_claims['total_updates']))
# # print(compare_values("UE Ratio", ue_ratio_TRUE, pdf_claims['ue_ratio']))

# # print("")
# # print(compare_values("Child 0-5 %", (total_age_0_5/total_enrollments_TRUE)*100, pdf_claims['child_0_5_pct'], True))
# # print(compare_values("Child 5-17 %", (total_age_5_17/total_enrollments_TRUE)*100, pdf_claims['child_5_17_pct'], True))
# # print(compare_values("Adult 18+ %", (total_age_18_greater/total_enrollments_TRUE)*100, pdf_claims['adult_pct'], True))
# # print(compare_values("Children Total (0-17) %", child_enrollment_pct, pdf_claims['child_total_pct'], True))

# # print("")
# # print(compare_values("States", states_merged, pdf_claims['states']))
# # print(compare_values("Districts", districts_merged, pdf_claims['districts']))
# # print(compare_values("Pincodes", pincodes_merged, pdf_claims['pincodes']))

# # print("")
# # print(compare_values("Bio Updates", total_biometric_updates, pdf_claims['bio_updates']))
# # print(compare_values("Demo Updates", total_demographic_updates, pdf_claims['demo_updates']))

# # # ============================================================================
# # # STEP 8: Summary of Issues
# # # ============================================================================

# # print("\n" + "="*80)
# # print("SUMMARY: ISSUES FOUND")
# # print("="*80)

# # issues = []

# # # Issue 1: Enrollment count
# # if total_enrollments_TRUE != pdf_claims['total_enrollments']:
# #     issues.append({
# #         'id': 1,
# #         'severity': 'CRITICAL',
# #         'metric': 'Total Enrollments',
# #         'ground_truth': f"{total_enrollments_TRUE:,}",
# #         'pdf_claim': f"{pdf_claims['total_enrollments']:,}",
# #         'root_cause': 'Using merged_data.csv with fillna(0) instead of enrollment_clean.csv',
# #         'impact': 'All enrollment-based calculations are wrong'
# #     })

# # # Issue 2: Child percentages
# # child_0_5_pct_true = (total_age_0_5/total_enrollments_TRUE)*100
# # child_5_17_pct_true = (total_age_5_17/total_enrollments_TRUE)*100
# # if abs(child_0_5_pct_true - pdf_claims['child_0_5_pct']) > 0.1:
# #     issues.append({
# #         'id': 2,
# #         'severity': 'HIGH',
# #         'metric': 'Child Age Percentages',
# #         'ground_truth': f"0-5: {child_0_5_pct_true:.1f}%, 5-17: {child_5_17_pct_true:.1f}%",
# #         'pdf_claim': f"0-5: {pdf_claims['child_0_5_pct']}%, 5-17: {pdf_claims['child_5_17_pct']}%",
# #         'root_cause': 'Unknown - need to check dimension 1 code',
# #         'impact': 'Child enrollment analysis is incorrect'
# #     })

# # # Issue 3: UE Ratio
# # if abs(ue_ratio_TRUE - pdf_claims['ue_ratio']) > 0.01:
# #     issues.append({
# #         'id': 3,
# #         'severity': 'CRITICAL',
# #         'metric': 'UE Ratio',
# #         'ground_truth': f"{ue_ratio_TRUE:.2f}",
# #         'pdf_claim': f"{pdf_claims['ue_ratio']}",
# #         'root_cause': 'Using wrong enrollment denominator',
# #         'impact': 'System maturity assessment is wrong'
# #     })

# # if issues:
# #     print(f"\n❌ Found {len(issues)} critical issues:\n")
# #     for issue in issues:
# #         print(f"Issue #{issue['id']} - {issue['severity']}")
# #         print(f"  Metric:       {issue['metric']}")
# #         print(f"  Ground Truth: {issue['ground_truth']}")
# #         print(f"  PDF Claim:    {issue['pdf_claim']}")
# #         print(f"  Root Cause:   {issue['root_cause']}")
# #         print(f"  Impact:       {issue['impact']}")
# #         print()
# # else:
# #     print("\n✓ No issues found - all PDF claims match ground truth!")

# # # ============================================================================
# # # STEP 9: Corrected PDF Numbers
# # # ============================================================================

# # print("\n" + "="*80)
# # print("CORRECTED NUMBERS FOR PDF UPDATE")
# # print("="*80)

# # print("\nUse these AUTHORITATIVE numbers in your PDF:\n")

# # print("Page 1 (Cover):")
# # print(f"  Total Enrollments:  {total_enrollments_TRUE:,}  (currently shows: {pdf_claims['total_enrollments']:,})")
# # print(f"  Total Updates:      {total_updates_TRUE:,}  (currently shows: {pdf_claims['total_updates']:,})")
# # print(f"  UE Ratio:           {ue_ratio_TRUE:.2f}×  (currently shows: {pdf_claims['ue_ratio']}×)")

# # print("\nPage 7 (Dataset Statistics):")
# # print(f"  Total enrollments tracked:  {total_enrollments_TRUE:,}")
# # print(f"  Total bio updates tracked:  {total_biometric_updates:,}")
# # print(f"  Total demo updates tracked: {total_demographic_updates:,}")

# # print("\nPage 12-13 (Age Distribution):")
# # print(f"  Age 0-5:     {total_age_0_5:,}  ({(total_age_0_5/total_enrollments_TRUE)*100:.1f}%)")
# # print(f"  Age 5-17:    {total_age_5_17:,}  ({(total_age_5_17/total_enrollments_TRUE)*100:.1f}%)")
# # print(f"  Age 18+:     {total_age_18_greater:,}  ({(total_age_18_greater/total_enrollments_TRUE)*100:.1f}%)")
# # print(f"  Children:    {child_enrollment_pct:.1f}%")
# # print(f"  Adults:      {(total_age_18_greater/total_enrollments_TRUE)*100:.1f}%")

# # print("\nPage 16 (Readiness):")
# # print(f"  Youth Bio Updates:  {total_bio_age_5_17:,}")
# # print(f"  Youth % of Bio:     {youth_bio_pct:.1f}%")

# # print("\n" + "="*80)
# # print("VALIDATION COMPLETE")
# # print("="*80)
# # print("\nNext Steps:")
# # print("1. Review the issues found above")
# # print("2. Proceed to analyze dimension code files to find calculation errors")
# # print("3. Update PDF with corrected numbers")
# # print("="*80)


# import pandas as pd

# df_merged = pd.read_csv('data/processed/merged_data.csv')

# print("Columns in merged dataset:")
# print(df_merged.columns.tolist())

# print("\nColumn counts:")
# print(f"Total columns: {len(df_merged.columns)}")

# # Check for duplicate column patterns
# bio_cols = [col for col in df_merged.columns if 'bio' in col.lower()]
# demo_cols = [col for col in df_merged.columns if 'demo' in col.lower()]

# print(f"\nBio columns: {bio_cols}")
# print(f"Demo columns: {demo_cols}")

# # Check totals
# print(f"\nUpdate totals from merged dataset:")
# if 'total_biometric_updates' in df_merged.columns:
#     print(f"  total_biometric_updates sum: {df_merged['total_biometric_updates'].sum():,}")
# if 'total_demographic_updates' in df_merged.columns:
#     print(f"  total_demographic_updates sum: {df_merged['total_demographic_updates'].sum():,}")



import pandas as pd

# Load individual files
df_bio = pd.read_csv('data/processed/biometric_clean.csv')
df_demo = pd.read_csv('data/processed/demographic_clean.csv')

# Calculate totals directly
bio_5_17 = df_bio['bio_age_5_17'].sum()
bio_17_plus = df_bio['bio_age_17_'].sum()
total_bio_direct = bio_5_17 + bio_17_plus

demo_5_17 = df_demo['demo_age_5_17'].sum()
demo_17_plus = df_demo['demo_age_17_'].sum()
total_demo_direct = demo_5_17 + demo_17_plus

print("Direct calculation from clean files:")
print(f"  Bio total: {total_bio_direct:,}")
print(f"  Demo total: {total_demo_direct:,}")

# Now check if biometric_clean.csv has total_biometric_updates column
if 'total_biometric_updates' in df_bio.columns:
    print(f"\n  total_biometric_updates column sum: {df_bio['total_biometric_updates'].sum():,}")
    
if 'total_demographic_updates' in df_demo.columns:
    print(f"  total_demographic_updates column sum: {df_demo['total_demographic_updates'].sum():,}")

# Check for duplicates
print(f"\nDuplicate check:")
print(f"  Biometric records: {len(df_bio):,}")
print(f"  Unique (date, state, district, pincode): {df_bio.groupby(['date', 'state', 'district', 'pincode']).ngroups:,}")

print(f"  Demographic records: {len(df_demo):,}")
print(f"  Unique (date, state, district, pincode): {df_demo.groupby(['date', 'state', 'district', 'pincode']).ngroups:,}")
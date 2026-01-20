"""
Step 3: Dimension 1 - Coverage Gap Analysis (Update Paradox)
Analyze enrollment equity gaps at district level despite high national saturation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import (
    PROCESSED_DATA_DIR,
    FIGURES_DIR,
    TABLES_DIR,
    NATIONAL_UE_RATIO,
    HIGH_UE_RATIO,
    LOW_UE_RATIO,
    NATIONAL_BIRTH_RATE,
    ANALYSIS_MONTHS,
    COLOR_SCHEME,
    FIG_SIZE_LARGE,
    DPI
)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = FIG_SIZE_LARGE
plt.rcParams['font.size'] = 10


def load_merged_data():
    """Load the cleaned merged dataset"""
    print("\n" + "="*60)
    print("DIMENSION 1: COVERAGE GAP ANALYSIS")
    print("="*60)
    
    df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'merged_data.csv'))
    
    # Parse date if not already
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"\n✓ Loaded merged dataset: {len(df):,} records")
    print(f"  Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"  Districts: {df['district'].nunique()}")
    print(f"  States: {df['state'].nunique()}")
    
    return df


def calculate_district_metrics(df):
    """
    Calculate key metrics at district level
    """
    print(f"\n📊 Calculating district-level metrics...")
    
    # Aggregate by district (sum across all dates)
    district_agg = df.groupby(['state', 'district']).agg({
        'total_enrollment': 'sum',
        'total_updates': 'sum',
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum',
        'bio_age_5_17': 'sum',
        'bio_age_17_': 'sum'
    }).reset_index()
    
    # Calculate UE Ratio
    district_agg['ue_ratio'] = np.where(
        district_agg['total_enrollment'] > 0,
        district_agg['total_updates'] / district_agg['total_enrollment'],
        0
    )
    
    # Calculate enrollment velocity (enrollments per month)
    district_agg['enrollment_velocity'] = district_agg['total_enrollment'] / ANALYSIS_MONTHS
    
    # Calculate update velocity
    district_agg['update_velocity'] = district_agg['total_updates'] / ANALYSIS_MONTHS
    
    print(f"  ✓ Calculated metrics for {len(district_agg)} districts")
    print(f"\n  District-level statistics:")
    print(f"    Avg enrollments per district: {district_agg['total_enrollment'].mean():,.0f}")
    print(f"    Avg updates per district: {district_agg['total_updates'].mean():,.0f}")
    print(f"    Avg UE Ratio: {district_agg['ue_ratio'].mean():.2f}")
    print(f"    Median UE Ratio: {district_agg['ue_ratio'].median():.2f}")
    
    return district_agg


def classify_districts_2x2(district_agg):
    """
    Classify districts into 2x2 matrix based on enrollment and update activity
    """
    print(f"\n📈 Classifying districts into 2x2 matrix...")
    
    # Define thresholds (median split)
    median_enrollment = district_agg['total_enrollment'].median()
    median_updates = district_agg['total_updates'].median()
    
    print(f"  Thresholds:")
    print(f"    Median enrollments: {median_enrollment:,.0f}")
    print(f"    Median updates: {median_updates:,.0f}")
    
    # Classify
    def classify_quadrant(row):
        high_enroll = row['total_enrollment'] >= median_enrollment
        high_update = row['total_updates'] >= median_updates
        
        if high_enroll and high_update:
            return 'Healthy & Growing'
        elif not high_enroll and high_update:
            return 'Saturation/Coverage Gap'  # Update Paradox!
        elif high_enroll and not high_update:
            return 'New Users Need Engagement'
        else:
            return 'Crisis Zone'
    
    district_agg['quadrant'] = district_agg.apply(classify_quadrant, axis=1)
    
    # Count districts in each quadrant
    quadrant_counts = district_agg['quadrant'].value_counts()
    print(f"\n  District classification:")
    for quadrant, count in quadrant_counts.items():
        pct = (count / len(district_agg)) * 100
        print(f"    {quadrant}: {count} ({pct:.1f}%)")
    
    return district_agg


def identify_child_coverage_gaps(district_agg):
    """
    Identify districts with low child (0-5 and 5-17) enrollment
    CORRECTED: Calculate percentages from TOTALS, not record-level averages
    """
    print(f"\n👶 Analyzing child coverage gaps...")
    
    # CORRECT CALCULATION: Use absolute totals
    # Calculate what % of total enrollments are children
    district_agg['child_0_5_pct'] = (
        district_agg['age_0_5'] / district_agg['total_enrollment']
    ) * 100
    
    district_agg['child_5_17_pct'] = (
        district_agg['age_5_17'] / district_agg['total_enrollment']
    ) * 100
    
    district_agg['child_total_pct'] = (
        (district_agg['age_0_5'] + district_agg['age_5_17']) / 
        district_agg['total_enrollment']
    ) * 100
    
    # Handle division by zero
    district_agg['child_0_5_pct'] = district_agg['child_0_5_pct'].fillna(0)
    district_agg['child_5_17_pct'] = district_agg['child_5_17_pct'].fillna(0)
    district_agg['child_total_pct'] = district_agg['child_total_pct'].fillna(0)
    
    # National-level statistics (CORRECT)
    total_enrollments_national = district_agg['total_enrollment'].sum()
    total_child_0_5 = district_agg['age_0_5'].sum()
    total_child_5_17 = district_agg['age_5_17'].sum()
    total_adult = district_agg['age_18_greater'].sum()
    
    national_child_pct = ((total_child_0_5 + total_child_5_17) / total_enrollments_national) * 100
    
    print(f"  ✓ Analyzed {len(district_agg)} districts")
    print(f"\n  NATIONAL STATISTICS (Correct Calculation):")
    print(f"    Total enrollments: {total_enrollments_national:,.0f}")
    print(f"    Age 0-5: {total_child_0_5:,.0f} ({(total_child_0_5/total_enrollments_national)*100:.1f}%)")
    print(f"    Age 5-17: {total_child_5_17:,.0f} ({(total_child_5_17/total_enrollments_national)*100:.1f}%)")
    print(f"    Age 18+: {total_adult:,.0f} ({(total_adult/total_enrollments_national)*100:.1f}%)")
    print(f"    Children (0-17): {national_child_pct:.1f}%")
    
    # Identify low child enrollment districts
    # National average is 96.9% children (0-17)
    # Districts below 80% are concerning (significantly below average)
    low_child_threshold = 80
    
    low_child_districts = district_agg[
        district_agg['child_total_pct'] < low_child_threshold
    ].copy()
    
    print(f"\n  Average child (0-17) enrollment % across districts: {district_agg['child_total_pct'].mean():.1f}%")
    print(f"  Median child enrollment %: {district_agg['child_total_pct'].median():.1f}%")
    print(f"  Districts with <{low_child_threshold}% child enrollment: {len(low_child_districts)}")
    
    # Sort by child enrollment percentage
    low_child_districts = low_child_districts.sort_values('child_total_pct')
    
    # Also identify districts with VERY HIGH child enrollment (>98% = almost all children)
    very_high_child_threshold = 98
    very_high_child_districts = district_agg[
        district_agg['child_total_pct'] > very_high_child_threshold
    ].copy()
    
    print(f"  Districts with >{very_high_child_threshold}% child enrollment: {len(very_high_child_districts)} (exclusive child focus)")
    
    return district_agg, low_child_districts


def calculate_ue_ratio_statistics(district_agg):
    """
    Calculate UE Ratio statistics and identify anomalies
    """
    print(f"\n🔢 UE Ratio statistical analysis...")
    
    # Filter out zeros
    ue_ratios = district_agg[district_agg['ue_ratio'] > 0]['ue_ratio']
    
    # Calculate statistics
    mean_ue = ue_ratios.mean()
    median_ue = ue_ratios.median()
    std_ue = ue_ratios.std()
    
    print(f"  Mean UE Ratio: {mean_ue:.2f}")
    print(f"  Median UE Ratio: {median_ue:.2f}")
    print(f"  Std Dev: {std_ue:.2f}")
    print(f"  National baseline (config): {NATIONAL_UE_RATIO}")
    
    # Classify UE ratios
    district_agg['ue_category'] = pd.cut(
        district_agg['ue_ratio'],
        bins=[0, LOW_UE_RATIO, NATIONAL_UE_RATIO, HIGH_UE_RATIO, float('inf')],
        labels=['Low', 'Normal', 'High', 'Very High']
    )
    
    ue_dist = district_agg['ue_category'].value_counts()
    print(f"\n  UE Ratio distribution:")
    for category, count in ue_dist.items():
        pct = (count / len(district_agg)) * 100
        print(f"    {category}: {count} districts ({pct:.1f}%)")
    
    return district_agg


def create_visualizations(district_agg, low_child_districts):
    """
    Create visualizations for Dimension 1
    """
    print(f"\n📊 Creating visualizations...")
    
    # 1. UE Ratio Distribution Histogram
    plt.figure(figsize=(12, 6))
    ue_data = district_agg[district_agg['ue_ratio'] > 0]['ue_ratio']
    plt.hist(ue_data, bins=50, color=COLOR_SCHEME['neutral'], alpha=0.7, edgecolor='black')
    plt.axvline(NATIONAL_UE_RATIO, color=COLOR_SCHEME['high'], 
                linestyle='--', linewidth=2, label=f'National Baseline ({NATIONAL_UE_RATIO})')
    plt.axvline(ue_data.median(), color=COLOR_SCHEME['low'], 
                linestyle='--', linewidth=2, label=f'Median ({ue_data.median():.2f})')
    plt.xlabel('UE Ratio (Updates / Enrollments)', fontsize=12)
    plt.ylabel('Number of Districts', fontsize=12)
    plt.title('Distribution of District-Level UE Ratios', fontsize=14, fontweight='bold')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'dim1_ue_ratio_distribution.png'), dpi=DPI)
    plt.close()
    print(f"  ✓ Saved: dim1_ue_ratio_distribution.png")
    
    # 2. 2x2 Matrix Scatter Plot
    plt.figure(figsize=(12, 8))
    colors = {
        'Healthy & Growing': COLOR_SCHEME['low'],
        'Saturation/Coverage Gap': COLOR_SCHEME['high'],
        'New Users Need Engagement': COLOR_SCHEME['moderate'],
        'Crisis Zone': COLOR_SCHEME['critical']
    }
    
    for quadrant, color in colors.items():
        subset = district_agg[district_agg['quadrant'] == quadrant]
        plt.scatter(subset['total_enrollment'], subset['total_updates'], 
                   c=color, label=quadrant, alpha=0.6, s=50)
    
    plt.xlabel('Total Enrollments', fontsize=12)
    plt.ylabel('Total Updates', fontsize=12)
    plt.title('District Classification: Enrollment vs Updates (2x2 Matrix)', 
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'dim1_2x2_matrix.png'), dpi=DPI)
    plt.close()
    print(f"  ✓ Saved: dim1_2x2_matrix.png")
    
    # 3. Top 20 Districts with Lowest Child Enrollment %
    if len(low_child_districts) > 0:
        plt.figure(figsize=(14, 8))
        top_20_low_child = low_child_districts.head(20)
        
        y_positions = range(len(top_20_low_child))
        plt.barh(y_positions, top_20_low_child['child_total_pct'], 
                 color=COLOR_SCHEME['critical'], alpha=0.7)
        plt.yticks(y_positions, 
                   [f"{row['district']}, {row['state']}" for _, row in top_20_low_child.iterrows()],
                   fontsize=9)
        plt.xlabel('Child Enrollment % (Age 0-17)', fontsize=12)
        plt.title('Top 20 Districts with Lowest Child Enrollment Percentage', 
                  fontsize=14, fontweight='bold')
        plt.axvline(80, color='black', linestyle='--', linewidth=1, label='Threshold (80%)')
        plt.axvline(96.9, color='green', linestyle='--', linewidth=1, label='National Avg (96.9%)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, 'dim1_low_child_enrollment.png'), dpi=DPI)
        plt.close()
        print(f"  ✓ Saved: dim1_low_child_enrollment.png")
    else:
        print(f"  ⚠️  No districts with low child enrollment (<80%) - skipping chart")
    
    # 3b. Districts with VERY HIGH Child Enrollment (>98%)
    very_high_child = district_agg[district_agg['child_total_pct'] > 98].nlargest(20, 'child_total_pct')
    
    if len(very_high_child) > 0:
        plt.figure(figsize=(14, 8))
        y_positions = range(len(very_high_child))
        plt.barh(y_positions, very_high_child['child_total_pct'], 
                 color=COLOR_SCHEME['low'], alpha=0.7)
        plt.yticks(y_positions, 
                   [f"{row['district']}, {row['state']}" for _, row in very_high_child.iterrows()],
                   fontsize=9)
        plt.xlabel('Child Enrollment % (Age 0-17)', fontsize=12)
        plt.title('Top 20 Districts with Highest Child Enrollment % (>98%)', 
                  fontsize=14, fontweight='bold')
        plt.axvline(98, color='black', linestyle='--', linewidth=1, label='Very High Threshold (98%)')
        plt.axvline(96.9, color='orange', linestyle='--', linewidth=1, label='National Avg (96.9%)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, 'dim1_very_high_child_enrollment.png'), dpi=DPI)
        plt.close()
        print(f"  ✓ Saved: dim1_very_high_child_enrollment.png")
    
    # 4. State-level aggregation - UE Ratio by State
    state_agg = district_agg.groupby('state').agg({
        'total_enrollment': 'sum',
        'total_updates': 'sum',
        'ue_ratio': 'mean'
    }).reset_index()
    state_agg = state_agg.sort_values('ue_ratio', ascending=False).head(20)
    
    plt.figure(figsize=(14, 8))
    plt.barh(range(len(state_agg)), state_agg['ue_ratio'], 
             color=COLOR_SCHEME['neutral'], alpha=0.7)
    plt.yticks(range(len(state_agg)), state_agg['state'], fontsize=10)
    plt.xlabel('Average UE Ratio', fontsize=12)
    plt.title('Top 20 States by Average UE Ratio', fontsize=14, fontweight='bold')
    plt.axvline(NATIONAL_UE_RATIO, color=COLOR_SCHEME['high'], 
                linestyle='--', linewidth=2, label=f'National Baseline ({NATIONAL_UE_RATIO})')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'dim1_state_ue_ratios.png'), dpi=DPI)
    plt.close()
    print(f"  ✓ Saved: dim1_state_ue_ratios.png")


def generate_priority_lists(district_agg, low_child_districts):
    """
    Generate priority lists for enrollment drives
    """
    print(f"\n📋 Generating priority lists...")
    
    # Priority List 1: Saturation/Coverage Gap districts
    coverage_gap = district_agg[
        district_agg['quadrant'] == 'Saturation/Coverage Gap'
    ].sort_values('ue_ratio', ascending=False)
    
    coverage_gap_file = os.path.join(TABLES_DIR, 'dim1_coverage_gap_districts.csv')
    coverage_gap.to_csv(coverage_gap_file, index=False)
    print(f"  ✓ Saved: dim1_coverage_gap_districts.csv ({len(coverage_gap)} districts)")
    
    # Priority List 2: Low child enrollment districts
    low_child_file = os.path.join(TABLES_DIR, 'dim1_low_child_enrollment_districts.csv')
    low_child_districts.to_csv(low_child_file, index=False)
    print(f"  ✓ Saved: dim1_low_child_enrollment_districts.csv ({len(low_child_districts)} districts)")
    
    # Priority List 3: Crisis Zone districts (all)
    crisis_zone = district_agg[
        district_agg['quadrant'] == 'Crisis Zone'
    ].sort_values('total_enrollment')
    
    crisis_file = os.path.join(TABLES_DIR, 'dim1_crisis_zone_districts.csv')
    crisis_zone.to_csv(crisis_file, index=False)
    print(f"  ✓ Saved: dim1_crisis_zone_districts.csv ({len(crisis_zone)} districts)")
    
    # Priority List 4: Top 10 Crisis Zone districts (NEW)
    top_10_crisis = crisis_zone.head(10)
    
    top_10_crisis_file = os.path.join(TABLES_DIR, 'dim1_top10_crisis_zone_districts.csv')
    top_10_crisis.to_csv(top_10_crisis_file, index=False)
    print(f"  ✓ Saved: dim1_top10_crisis_zone_districts.csv (Top 10 most critical)")
    
    # Summary statistics
    summary = {
        'Total Districts Analyzed': len(district_agg),
        'Coverage Gap Districts': len(coverage_gap),
        'Low Child Enrollment Districts': len(low_child_districts),
        'Crisis Zone Districts': len(crisis_zone),
        'Top 10 Crisis Zone Districts': len(top_10_crisis),
        'Average UE Ratio': district_agg['ue_ratio'].mean(),
        'Median UE Ratio': district_agg['ue_ratio'].median()
    }
    
    summary_df = pd.DataFrame([summary])
    summary_file = os.path.join(TABLES_DIR, 'dim1_summary_statistics.csv')
    summary_df.to_csv(summary_file, index=False)
    print(f"  ✓ Saved: dim1_summary_statistics.csv")
    
    return coverage_gap, low_child_districts, crisis_zone


def main():
    """
    Main function for Dimension 1 analysis
    """
    print("\n" + "="*60)
    print("DIMENSION 1: COVERAGE GAP (UPDATE PARADOX)")
    print("="*60)
    print("\n📌 Objective: Identify enrollment equity gaps at district level")
    print("   Despite high national saturation, which districts are missing")
    print("   new enrollments (especially children)?")
    
    # Load data
    df = load_merged_data()
    
    # Calculate district metrics
    district_agg = calculate_district_metrics(df)
    
    # Classify into 2x2 matrix
    district_agg = classify_districts_2x2(district_agg)
    
    # Identify child coverage gaps
    district_agg, low_child_districts = identify_child_coverage_gaps(district_agg)
    
    # Calculate UE ratio statistics
    district_agg = calculate_ue_ratio_statistics(district_agg)
    
    # Create visualizations
    create_visualizations(district_agg, low_child_districts)
    
    # Generate priority lists
    coverage_gap, low_child_districts, crisis_zone = generate_priority_lists(
        district_agg, low_child_districts
    )
    
    # Final summary
    print("\n" + "="*60)
    print("DIMENSION 1 ANALYSIS COMPLETE!")
    print("="*60)
    print(f"\n🎯 Key Findings:")
    print(f"   • {len(coverage_gap)} districts show 'Saturation/Coverage Gap'")
    print(f"   • {len(low_child_districts)} districts have low child enrollment (<80%)")
    print(f"   • {len(crisis_zone)} districts in 'Crisis Zone'")
    print(f"   • Top 10 Crisis Zone districts saved for priority intervention")
    print(f"   • Average UE Ratio: {district_agg['ue_ratio'].mean():.2f}")
    
    print(f"\n📁 Outputs saved to:")
    print(f"   • Figures: {FIGURES_DIR}")
    print(f"   • Tables: {TABLES_DIR}")
    
    print("\n" + "="*60)
    print("Next step: Run 04_dimension2_readiness_gap.py")
    print("="*60)
    
    return district_agg, coverage_gap, low_child_districts, crisis_zone


if __name__ == "__main__":
    district_agg, coverage_gap, low_child_districts, crisis_zone = main()
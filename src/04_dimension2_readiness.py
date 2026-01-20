"""
Step 4: Dimension 2 - Readiness Gap Analysis (Authentication Crisis)
Analyze youth (5-17) biometric update rates and predict authentication failures at age 18+
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from scipy import stats

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import (
    PROCESSED_DATA_DIR,
    FIGURES_DIR,
    TABLES_DIR,
    GOOD_READINESS,
    MODERATE_READINESS,
    CRITICAL_READINESS,
    COLOR_SCHEME,
    FIG_SIZE_LARGE,
    DPI,
    ANALYSIS_MONTHS
)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = FIG_SIZE_LARGE
plt.rcParams['font.size'] = 10


def load_merged_data():
    """Load the cleaned merged dataset"""
    print("\n" + "="*60)
    print("DIMENSION 2: READINESS GAP ANALYSIS")
    print("="*60)
    
    df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'merged_data.csv'))
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"\n✓ Loaded merged dataset: {len(df):,} records")
    print(f"  Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    
    return df


def calculate_district_readiness(df):
    """
    Calculate transition readiness scores at district level
    """
    print(f"\n📊 Calculating district-level readiness metrics...")
    
    # Aggregate by district
    district_agg = df.groupby(['state', 'district']).agg({
        'bio_age_5_17': 'sum',
        'bio_age_17_': 'sum',
        'age_5_17': 'sum',  # Total enrollments in 5-17 age group
        'age_0_5': 'sum',
        'age_18_greater': 'sum'
    }).reset_index()
    
    # Calculate total biometric updates
    district_agg['total_bio_updates'] = (
        district_agg['bio_age_5_17'] + district_agg['bio_age_17_']
    )
    
    # Calculate total enrollments
    district_agg['total_enrollments'] = (
        district_agg['age_0_5'] + 
        district_agg['age_5_17'] + 
        district_agg['age_18_greater']
    )
    
    # Transition Readiness Score: What % of bio updates are from youth (5-17)?
    # High score = good (youth are updating their biometrics)
    district_agg['readiness_score'] = np.where(
        district_agg['total_bio_updates'] > 0,
        (district_agg['bio_age_5_17'] / district_agg['total_bio_updates']) * 100,
        0
    )
    
    
    
    
    # Classify readiness
    # Handle case where MODERATE_READINESS == CRITICAL_READINESS
    if MODERATE_READINESS == CRITICAL_READINESS:
        # Use only 3 categories instead of 4
        district_agg['readiness_category'] = pd.cut(
            district_agg['readiness_score'],
            bins=[0, CRITICAL_READINESS, GOOD_READINESS, 100],
            labels=['Critical', 'Moderate', 'Good']
        )
    else:
        district_agg['readiness_category'] = pd.cut(
            district_agg['readiness_score'],
            bins=[0, CRITICAL_READINESS, MODERATE_READINESS, GOOD_READINESS, 100],
            labels=['Critical', 'Low', 'Moderate', 'Good']
        )
    
    print(f"  ✓ Calculated readiness for {len(district_agg)} districts")
    print(f"\n  National Statistics:")
    print(f"    Total youth (5-17) bio updates: {district_agg['bio_age_5_17'].sum():,.0f}")
    print(f"    Total adult (17+) bio updates: {district_agg['bio_age_17_'].sum():,.0f}")
    print(f"    Total bio updates: {district_agg['total_bio_updates'].sum():,.0f}")
    print(f"    Youth % of bio updates: {(district_agg['bio_age_5_17'].sum() / district_agg['total_bio_updates'].sum()) * 100:.1f}%")
    
    print(f"\n  Readiness Score Distribution:")
    print(f"    Mean: {district_agg['readiness_score'].mean():.1f}")
    print(f"    Median: {district_agg['readiness_score'].median():.1f}")
    print(f"    Std Dev: {district_agg['readiness_score'].std():.1f}")
    
    # Readiness category breakdown
    readiness_dist = district_agg['readiness_category'].value_counts()
    print(f"\n  Districts by Readiness Category:")
    for category in readiness_dist.index:
        count = readiness_dist[category]
        pct = (count / len(district_agg)) * 100
        print(f"    {category}: {count} districts ({pct:.1f}%)")
    
    return district_agg


def calculate_state_readiness(district_agg):
    """
    Calculate readiness at state level
    """
    print(f"\n🗺️  Calculating state-level readiness...")
    
    state_agg = district_agg.groupby('state').agg({
        'bio_age_5_17': 'sum',
        'bio_age_17_': 'sum',
        'total_bio_updates': 'sum',
        'age_5_17': 'sum'
    }).reset_index()
    
    # Calculate state readiness score
    state_agg['readiness_score'] = (
        state_agg['bio_age_5_17'] / state_agg['total_bio_updates']
    ) * 100
    
    
    
    # Sort by readiness score
    state_agg = state_agg.sort_values('readiness_score', ascending=False)
    
    print(f"  ✓ Calculated readiness for {len(state_agg)} states")
    print(f"\n  Top 5 states (highest youth bio update %):")
    for idx, row in state_agg.head(5).iterrows():
        print(f"    {row['state']}: {row['readiness_score']:.1f}%")
    
    print(f"\n  Bottom 5 states (lowest youth bio update %):")
    for idx, row in state_agg.tail(5).iterrows():
        print(f"    {row['state']}: {row['readiness_score']:.1f}%")
    
    return state_agg


def predict_authentication_failures(district_agg):
    """
    Identify at-risk districts based on readiness scores
    Districts with low youth bio update activity are flagged for intervention
    """
    print(f"\n🔮 Identifying at-risk districts based on readiness scores...")
    
    # National statistics
    total_youth_bio = district_agg['bio_age_5_17'].sum()
    total_adult_bio = district_agg['bio_age_17_'].sum()
    total_bio = total_youth_bio + total_adult_bio
    total_youth_enrollments = district_agg['age_5_17'].sum()
    
    # National youth bio update percentage
    national_youth_bio_pct = (total_youth_bio / total_bio * 100) if total_bio > 0 else 0
    
    print(f"\n  National Benchmarks:")
    print(f"    Total youth (5-17) enrollments: {total_youth_enrollments:,.0f}")
    print(f"    Total youth bio updates: {total_youth_bio:,.0f}")
    print(f"    Total adult bio updates: {total_adult_bio:,.0f}")
    print(f"    Youth % of all bio updates: {national_youth_bio_pct:.1f}%")
    print(f"    National median readiness score: {district_agg['readiness_score'].median():.1f}%")
    
    # Calculate readiness gap for each district
    # Gap = How much below the national median is this district?
    national_median = district_agg['readiness_score'].median()
    
    district_agg['readiness_gap'] = np.maximum(
        0,
        national_median - district_agg['readiness_score']
    )
    
    # Estimate youth at risk
    # Districts with large readiness gaps have more youth potentially at risk
    # Assumption: Readiness gap indicates proportion of youth who may not be updating
    district_agg['estimated_at_risk_youth'] = (
        district_agg['age_5_17'] * (district_agg['readiness_gap'] / 100)
    ).round(0).astype(int)
    
    # Total estimated at-risk youth nationally
    total_at_risk = district_agg['estimated_at_risk_youth'].sum()
    
    print(f"\n  Risk Assessment:")
    print(f"    Districts below national median: {len(district_agg[district_agg['readiness_gap'] > 0])}")
    print(f"    Estimated at-risk youth (nationally): {total_at_risk:,.0f}")
    
    # Identify high-risk districts (below critical threshold)
    high_risk_districts = district_agg[
        district_agg['readiness_score'] < CRITICAL_READINESS
    ].sort_values('estimated_at_risk_youth', ascending=False)
    
    print(f"\n  High-Risk Districts (Readiness < {CRITICAL_READINESS}%):")
    print(f"    Count: {len(high_risk_districts)}")
    if len(high_risk_districts) > 0:
        print(f"    Total at-risk youth in these districts: {high_risk_districts['estimated_at_risk_youth'].sum():,.0f}")
        print(f"\n    Top 5 districts by at-risk youth:")
        for idx, row in high_risk_districts.head(5).iterrows():
            print(f"      {row['district']}, {row['state']}: {row['estimated_at_risk_youth']:,.0f} at-risk youth (Readiness: {row['readiness_score']:.1f}%)")
    
    return district_agg, total_at_risk, high_risk_districts


def create_visualizations(district_agg, state_agg, high_risk_districts):
    """
    Create visualizations for Dimension 2
    """
    print(f"\n📊 Creating visualizations...")
    
    # 1. Readiness Score Distribution
    plt.figure(figsize=(12, 6))
    readiness_data = district_agg[district_agg['readiness_score'] > 0]['readiness_score']
    
    plt.hist(readiness_data, bins=50, color=COLOR_SCHEME['neutral'], alpha=0.7, edgecolor='black')
    plt.axvline(GOOD_READINESS, color=COLOR_SCHEME['low'], 
                linestyle='--', linewidth=2, label=f'Good ({GOOD_READINESS}%)')
    plt.axvline(MODERATE_READINESS, color=COLOR_SCHEME['moderate'], 
                linestyle='--', linewidth=2, label=f'Moderate ({MODERATE_READINESS}%)')
    plt.axvline(CRITICAL_READINESS, color=COLOR_SCHEME['critical'], 
                linestyle='--', linewidth=2, label=f'Critical ({CRITICAL_READINESS}%)')
    plt.axvline(readiness_data.median(), color='black', 
                linestyle='-', linewidth=2, label=f'Median ({readiness_data.median():.1f}%)')
    
    plt.xlabel('Transition Readiness Score (Youth Bio Updates %)', fontsize=12)
    plt.ylabel('Number of Districts', fontsize=12)
    plt.title('Distribution of District-Level Transition Readiness Scores', 
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'dim2_readiness_distribution.png'), dpi=DPI)
    plt.close()
    print(f"  ✓ Saved: dim2_readiness_distribution.png")
    
    # 2. State-Level Readiness (Top 20)
    plt.figure(figsize=(14, 8))
    top_20_states = state_agg.head(20)
    
    colors = [COLOR_SCHEME['low'] if score >= GOOD_READINESS 
              else COLOR_SCHEME['moderate'] if score >= MODERATE_READINESS 
              else COLOR_SCHEME['high'] if score >= CRITICAL_READINESS
              else COLOR_SCHEME['critical']
              for score in top_20_states['readiness_score']]
    
    plt.barh(range(len(top_20_states)), top_20_states['readiness_score'], 
             color=colors, alpha=0.7)
    plt.yticks(range(len(top_20_states)), top_20_states['state'], fontsize=10)
    plt.xlabel('Readiness Score (Youth Bio Updates %)', fontsize=12)
    plt.title('Top 20 States by Transition Readiness Score', 
              fontsize=14, fontweight='bold')
    plt.axvline(GOOD_READINESS, color='black', linestyle='--', 
                linewidth=1, label=f'Good Threshold ({GOOD_READINESS}%)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'dim2_state_readiness.png'), dpi=DPI)
    plt.close()
    print(f"  ✓ Saved: dim2_state_readiness.png")
    
    # 3. Readiness Category Pie Chart
    plt.figure(figsize=(10, 8))
    readiness_counts = district_agg['readiness_category'].value_counts()
    
    colors_pie = {
        'Good': COLOR_SCHEME['low'],
        'Moderate': COLOR_SCHEME['moderate'],
        'Low': COLOR_SCHEME['high'],
        'Critical': COLOR_SCHEME['critical']
    }
    colors_list = [colors_pie[cat] for cat in readiness_counts.index]
    
    plt.pie(readiness_counts.values, labels=readiness_counts.index, 
            autopct='%1.1f%%', colors=colors_list, startangle=90)
    plt.title('Districts by Readiness Category', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'dim2_readiness_categories.png'), dpi=DPI)
    plt.close()
    print(f"  ✓ Saved: dim2_readiness_categories.png")
    
    # 4. High-Risk Districts (Top 20 by at-risk youth)
    if len(high_risk_districts) > 0:
        plt.figure(figsize=(14, 8))
        top_20_risk = high_risk_districts.head(20)
        
        plt.barh(range(len(top_20_risk)), top_20_risk['estimated_at_risk_youth'],  # ← NEW
                 color=COLOR_SCHEME['critical'], alpha=0.7)
        plt.yticks(range(len(top_20_risk)), 
                   [f"{row['district']}, {row['state']}" for _, row in top_20_risk.iterrows()],
                   fontsize=9)
        plt.xlabel('Estimated At-Risk Youth', fontsize=12)  # ← UPDATED
        plt.title('Top 20 High-Risk Districts by Estimated At-Risk Youth',  # ← UPDATED
                  fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, 'dim2_high_risk_districts.png'), dpi=DPI)
        plt.close()
        print(f"  ✓ Saved: dim2_high_risk_districts.png")
    
    # 5. Readiness Score vs Youth Update Rate Scatter
    plt.figure(figsize=(12, 8))
    
    # Filter reasonable values
    scatter_data = district_agg[
        (district_agg['readiness_score'] > 0) & 
        (district_agg['estimated_at_risk_youth'] > 0)
    ]
    
    colors_scatter = scatter_data['readiness_category'].map({
        'Good': COLOR_SCHEME['low'],
        'Moderate': COLOR_SCHEME['moderate'],
        'Low': COLOR_SCHEME['high'],
        'Critical': COLOR_SCHEME['critical']
    })
    
    plt.scatter(scatter_data['readiness_gap'], 
                scatter_data['estimated_at_risk_youth'],
                c=colors_scatter, alpha=0.6, s=50)
    
    plt.xlabel('Readiness Gap (Below Median %)', fontsize=12)
    plt.ylabel('Estimated At-Risk Youth', fontsize=12)
    plt.title('Readiness Gap vs Estimated At-Risk Youth', 
              fontsize=14, fontweight='bold')
    
    # Add reference lines
    plt.axhline(GOOD_READINESS, color='black', linestyle='--', alpha=0.5)
    plt.axhline(MODERATE_READINESS, color='black', linestyle='--', alpha=0.5)
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'dim2_scatter_readiness_vs_update_rate.png'), dpi=DPI)
    plt.close()
    print(f"  ✓ Saved: dim2_scatter_readiness_vs_update_rate.png")
    
    # 6. Readiness Gap Distribution by State
    plt.figure(figsize=(14, 8))
    
    # Calculate state-level readiness gaps
    state_gaps = district_agg.groupby('state').agg({
        'readiness_gap': 'mean',
        'estimated_at_risk_youth': 'sum'
    }).sort_values('estimated_at_risk_youth', ascending=False).head(15)
    
    plt.barh(range(len(state_gaps)), state_gaps['estimated_at_risk_youth'],
             color=COLOR_SCHEME['high'], alpha=0.7)
    plt.yticks(range(len(state_gaps)), state_gaps.index, fontsize=10)
    plt.xlabel('Estimated At-Risk Youth', fontsize=12)
    plt.title('Top 15 States by Estimated At-Risk Youth', 
              fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'dim2_state_risk_ranking.png'), dpi=DPI)
    plt.close()
    print(f"  ✓ Saved: dim2_state_risk_ranking.png")


def generate_priority_lists(district_agg, high_risk_districts, state_agg):
    """
    Generate priority lists for mobile biometric camps
    """
    print(f"\n📋 Generating priority lists...")
    
    # Priority List 1: Critical readiness districts
    critical_districts = district_agg[
        district_agg['readiness_category'] == 'Critical'
    ].sort_values('estimated_at_risk_youth', ascending=False)
    
    critical_file = os.path.join(TABLES_DIR, 'dim2_critical_readiness_districts.csv')
    critical_districts.to_csv(critical_file, index=False)
    print(f"  ✓ Saved: dim2_critical_readiness_districts.csv ({len(critical_districts)} districts)")
    
    # Priority List 2: Low/Moderate readiness districts (depending on category structure)
    if 'Low' in district_agg['readiness_category'].values:
        low_districts = district_agg[
            district_agg['readiness_category'] == 'Low'
        ].sort_values('estimated_at_risk_youth', ascending=False)
        
        low_file = os.path.join(TABLES_DIR, 'dim2_low_readiness_districts.csv')
        low_districts.to_csv(low_file, index=False)
        print(f"  ✓ Saved: dim2_low_readiness_districts.csv ({len(low_districts)} districts)")
    else:
        # If only 3 categories, use Moderate as the middle priority
        low_districts = district_agg[
            district_agg['readiness_category'] == 'Moderate'
        ].sort_values('estimated_at_risk_youth', ascending=False)
        
        low_file = os.path.join(TABLES_DIR, 'dim2_moderate_readiness_districts.csv')
        low_districts.to_csv(low_file, index=False)
        print(f"  ✓ Saved: dim2_moderate_readiness_districts.csv ({len(low_districts)} districts)")
    
    # Priority List 3: State-level priorities
    state_file = os.path.join(TABLES_DIR, 'dim2_state_readiness_ranking.csv')
    state_agg.to_csv(state_file, index=False)
    print(f"  ✓ Saved: dim2_state_readiness_ranking.csv ({len(state_agg)} states)")
    
    # Priority List 4: All At-Risk Districts (Low + Critical combined) - NEW
    if 'Low' in district_agg['readiness_category'].values:
        at_risk_districts = district_agg[
            district_agg['readiness_category'].isin(['Critical', 'Low'])
        ].sort_values('estimated_at_risk_youth', ascending=False)
    else:
        # If only 3 categories, combine Critical and Moderate
        at_risk_districts = district_agg[
            district_agg['readiness_category'].isin(['Critical', 'Moderate'])
        ].sort_values('estimated_at_risk_youth', ascending=False)
    
    at_risk_file = os.path.join(TABLES_DIR, 'dim2_all_at_risk_districts.csv')
    at_risk_districts.to_csv(at_risk_file, index=False)
    print(f"  ✓ Saved: dim2_all_at_risk_districts.csv ({len(at_risk_districts)} districts)")
    
    # Priority List 5: Top 10 At-Risk Districts - NEW
    top_10_at_risk = at_risk_districts.head(10)
    
    top_10_at_risk_file = os.path.join(TABLES_DIR, 'dim2_top10_at_risk_districts.csv')
    top_10_at_risk.to_csv(top_10_at_risk_file, index=False)
    print(f"  ✓ Saved: dim2_top10_at_risk_districts.csv (Top 10 highest risk)")
    
    # Summary statistics
    summary = {
        'Total Districts Analyzed': len(district_agg),
        'Critical Readiness Districts': len(critical_districts),
        'Low Readiness Districts': len(low_districts),
        'All At-Risk Districts (Low+Critical)': len(at_risk_districts),
        'High Risk Districts': len(high_risk_districts),
        'Average Readiness Score': district_agg['readiness_score'].mean(),
        'Median Readiness Score': district_agg['readiness_score'].median(),
        'Total Estimated At-Risk Youth': district_agg['estimated_at_risk_youth'].sum()  # ← NEW
    }
    
    summary_df = pd.DataFrame([summary])
    summary_file = os.path.join(TABLES_DIR, 'dim2_summary_statistics.csv')
    summary_df.to_csv(summary_file, index=False)
    print(f"  ✓ Saved: dim2_summary_statistics.csv")
    
    return critical_districts, low_districts, at_risk_districts


def main():
    """
    Main function for Dimension 2 analysis
    """
    print("\n" + "="*60)
    print("DIMENSION 2: READINESS GAP (AUTHENTICATION CRISIS)")
    print("="*60)
    print("\n📌 Objective: Identify districts where youth (5-17) haven't")
    print("   updated biometrics and will face authentication failures at 18+")
    
    # Load data
    df = load_merged_data()
    
    # Calculate district readiness
    district_agg = calculate_district_readiness(df)
    
    # Calculate state readiness
    state_agg = calculate_state_readiness(district_agg)
    
    # Predict authentication failures
    district_agg, predicted_failures, high_risk_districts = predict_authentication_failures(district_agg)
    
    # Create visualizations
    create_visualizations(district_agg, state_agg, high_risk_districts)
    
    # Generate priority lists
    critical_districts, low_districts, at_risk_districts = generate_priority_lists(
        district_agg, high_risk_districts, state_agg
    )
    
    # Final summary
    print("\n" + "="*60)
    print("DIMENSION 2 ANALYSIS COMPLETE!")
    print("="*60)
    print(f"\n🎯 Key Findings:")
    print(f"   • Estimated at-risk youth (nationally): {predicted_failures:,.0f}")
    print(f"   • Critical readiness districts: {len(critical_districts)}")
    print(f"   • Low readiness districts: {len(low_districts)}")
    print(f"   • All At-Risk districts (Low+Critical): {len(at_risk_districts)}")
    print(f"   • Top 10 At-Risk districts saved for priority intervention")
    print(f"   • Average readiness score: {district_agg['readiness_score'].mean():.1f}%")
    print(f"   • Median readiness score: {district_agg['readiness_score'].median():.1f}%")
    
    print(f"\n📁 Outputs saved to:")
    print(f"   • Figures: {FIGURES_DIR}")
    print(f"   • Tables: {TABLES_DIR}")
    
    print("\n" + "="*60)
    print("Next step: Run 05_dimension3_integrity_gap.py")
    print("="*60)
    
    return district_agg, state_agg, critical_districts, predicted_failures


if __name__ == "__main__":
    district_agg, state_agg, critical_districts, predicted_failures = main()
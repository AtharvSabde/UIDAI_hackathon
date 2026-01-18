"""
Configuration file for Aadhaar Analysis Project

All constants are explicitly classified as:
- UIDAI-STATED (with page references)
- DERIVED (analytical, defined by us)

Primary Source:
UIDAI Annual Report 2024–25
“Aadhaar Annual Report – Mera Aadhaar, Meri Pehchaan”
"""

import os

# =============================================================================
# PROJECT STRUCTURE
# =============================================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')

OUTPUTS_DIR = os.path.join(PROJECT_ROOT, 'outputs')
FIGURES_DIR = os.path.join(OUTPUTS_DIR, 'figures')
TABLES_DIR = os.path.join(OUTPUTS_DIR, 'tables')

os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# =============================================================================
# RAW FILE LISTS
# =============================================================================

ENROLLMENT_FILES = [
    'api_data_aadhar_enrolment_0_500000.csv',
    'api_data_aadhar_enrolment_500000_1000000.csv',
    'api_data_aadhar_enrolment_1000000_1006029.csv'
]

BIOMETRIC_FILES = [
    'api_data_aadhar_biometric_0_500000.csv',
    'api_data_aadhar_biometric_500000_1000000.csv',
    'api_data_aadhar_biometric_1000000_1500000.csv',
    'api_data_aadhar_biometric_1500000_1861108.csv'
]

DEMOGRAPHIC_FILES = [
    'api_data_aadhar_demographic_0_500000.csv',
    'api_data_aadhar_demographic_500000_1000000.csv',
    'api_data_aadhar_demographic_1000000_1500000.csv',
    'api_data_aadhar_demographic_1500000_2000000.csv',
    'api_data_aadhar_demographic_2000000_2071700.csv'
]

# =============================================================================
# PROCESSED FILE NAMES
# =============================================================================

PROCESSED_ENROLLMENT = 'enrollment_clean.csv'
PROCESSED_BIOMETRIC = 'biometric_clean.csv'
PROCESSED_DEMOGRAPHIC = 'demographic_clean.csv'
PROCESSED_MERGED = 'merged_data.csv'

# =============================================================================
# STANDARDIZED COLUMNS
# =============================================================================

ENROLLMENT_COLUMNS = [
    'date', 'state', 'district', 'pincode',
    'age_0_5', 'age_5_17', 'age_18_greater'
]

BIOMETRIC_COLUMNS = [
    'date', 'state', 'district', 'pincode',
    'bio_age_5_17', 'bio_age_17_'
]

DEMOGRAPHIC_COLUMNS = [
    'date', 'state', 'district', 'pincode',
    'demo_age_5_17', 'demo_age_17_'
]

# =============================================================================
# UIDAI-STATED CONSTANTS (WITH PAGE REFERENCES)
# =============================================================================

# Total Aadhaar generated as of 31 March 2025
# Exact quote: "More than 141.80 crore Aadhaar numbers have been generated..."
# Source: UIDAI Annual Report 2024–25, Chapter 1.4.1
# PDF page ~20–21 (printed page 5–6)
TOTAL_AADHAAR_GENERATED = 141.80  # crore

# UIDAI reporting cutoff date
# Source: Same section as above
UIDAI_REPORTING_CUTOFF = "2025-03-31"

# Mandatory Biometric Update (MBU) ages
# Source: Chapter 3 – Enrolment and Update Ecosystem
# Sections 3.2 & 3.6
# PDF pages ~40–41 (printed page 25–26)
MBU_AGES = [5, 15]

# UIDAI does NOT publish a national saturation percentage
# Coverage described as ">90% in 28 States/UTs"
# Source: Section 3.2.3, PDF page ~44
NATIONAL_SATURATION = None

# =============================================================================
# FY 2024–25 AGGREGATES (DERIVED FROM UIDAI FIGURES)
# =============================================================================

# New enrolments during FY 2024–25
# Derived from Graph 3 – Year-wise Aadhaar Updates
# PDF pages ~41–42
NEW_ENROLLMENTS_2024_25 = 2.24  # crore (DERIVED)

# Total updates during FY 2024–25 (biometric + demographic)
# Derived from Section 3.6.6 and Graph 3
# PDF page ~41
TOTAL_UPDATES_2024_25 = 28.30  # crore (DERIVED)

# =============================================================================
# AUTHENTICATION TRANSACTIONS (EXPLICIT UIDAI TABLES)
# =============================================================================

# Source: Chapter 9 – Receipts from Services
# Tables 7, 8, 14
# PDF pages ~49–50 and ~101–102
YES_NO_AUTH_2024_25 = 2237.94   # crore
EKYC_AUTH_2024_25 = 469.24      # crore
FACE_AUTH_2024_25 = 102.31      # crore

# =============================================================================
# DEMOGRAPHIC CONTEXT (EXTERNAL OFFICIAL SOURCE)
# =============================================================================

# Source: Sample Registration System (Registrar General of India)
NATIONAL_BIRTH_RATE = 16.5  # births per 1000 population
EXPECTED_ANNUAL_BIRTHS = 23.3  # million (approximate, contextual)

# =============================================================================
# DERIVED ANALYTICAL METRICS (NOT UIDAI KPIs)
# =============================================================================

# UE Ratio = Updates ÷ Enrolments
# UIDAI does NOT define or publish this metric
# Used only for comparative stress analysis
DERIVED_UE_RATIO_BASELINE = 12.6  # 28.3 ÷ 2.24

# Backward compatibility alias (used in older scripts)
NATIONAL_UE_RATIO = DERIVED_UE_RATIO_BASELINE

HIGH_UE_RATIO = 18.0
LOW_UE_RATIO = 4.0
ANOMALY_UE_RATIO = 25.0

# =============================================================================
# UPDATE RATE HEURISTICS (ANALYTICAL)
# =============================================================================

IDEAL_UPDATE_RATE = 0.20
LOW_UPDATE_RATE = 0.07

# =============================================================================
# CHILD ENROLLMENT THRESHOLDS (ANALYTICAL)
# =============================================================================

CHILD_ENROLLMENT_THRESHOLD = 0.80   # <80% child enrollment = low
HIGH_CHILD_ENROLLMENT = 0.98        # >98% = extreme child dominance

# =============================================================================
# TRANSITION READINESS SCORE (SINGLE SOURCE OF TRUTH)
# =============================================================================

GOOD_READINESS = 30        # ≥30%
MODERATE_READINESS = 15   # 15–29%
CRITICAL_READINESS = 10   # <10%

# =============================================================================
# ANOMALY DETECTION THRESHOLDS (ANALYTICAL)
# =============================================================================

Z_SCORE_THRESHOLD = 3.0              # Statistical outlier threshold
TEMPORAL_SPIKE_MULTIPLIER = 3.0      # 3× baseline spike
AGE_CONCENTRATION_THRESHOLD = 0.80   # >80% in one age group

# =============================================================================
# ANALYSIS DATE RANGE (HACKATHON DATASET)
# =============================================================================

START_DATE = '2025-01-01'
END_DATE = '2025-12-31'
ANALYSIS_MONTHS = 12

# =============================================================================
# STATE SATURATION (ONLY <90%, OPERATIONALLY RELEVANT)
# =============================================================================

# UIDAI provides saturation bands, not precise decimals
# Values below are rounded indicators for classification only
# Source: Section 3.2.3, PDF page ~44
STATE_SATURATION = {
    'Nagaland': 69.0,
    'Arunachal Pradesh': 82.0,
    'Manipur': 83.0,
    'Meghalaya': 81.0,
    'Ladakh': 80.0,
    'Sikkim': 85.0,
    'Jammu and Kashmir': 88.0,
    'Bihar': 89.0
}

LOW_SATURATION_STATES = list(STATE_SATURATION.keys())

# =============================================================================
# VISUALIZATION SETTINGS
# =============================================================================

COLOR_SCHEME = {
    'critical': '#d32f2f',
    'high': '#f57c00',
    'moderate': '#fbc02d',
    'low': '#388e3c',
    'neutral': '#757575',
    'good': '#4caf50'
}

FIG_SIZE_SMALL = (8, 6)
FIG_SIZE_LARGE = (12, 8)
FIG_SIZE_WIDE = (14, 6)

DPI = 300

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def calculate_expected_births(population, months=12):
    annual_births = (population * NATIONAL_BIRTH_RATE) / 1000
    return int((annual_births * months) / 12)


def calculate_ue_ratio(total_updates, total_enrollments):
    if total_enrollments == 0:
        return 0.0
    return total_updates / total_enrollments


def classify_ue_ratio(ue_ratio):
    if ue_ratio >= ANOMALY_UE_RATIO:
        return 'Anomaly'
    elif ue_ratio >= HIGH_UE_RATIO:
        return 'High'
    elif ue_ratio >= LOW_UE_RATIO:
        return 'Normal'
    elif ue_ratio > 0:
        return 'Low'
    else:
        return 'Critical'


def calculate_transition_readiness_score(bio_updates_5_17, total_bio_updates):
    if total_bio_updates == 0:
        return 0.0
    return (bio_updates_5_17 / total_bio_updates) * 100


def classify_readiness_score(score):
    if score >= GOOD_READINESS:
        return 'Good'
    elif score >= MODERATE_READINESS:
        return 'Moderate'
    else:
        return 'Critical'


def get_state_saturation(state_name):
    return STATE_SATURATION.get(state_name)


def is_low_saturation_state(state_name):
    return state_name in LOW_SATURATION_STATES

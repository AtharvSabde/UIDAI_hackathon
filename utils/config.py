"""
Aadhaar Analysis Configuration
Verified constants from 2025 calendar year ground truth data
"""

import os

# =============================================================================
# PATHS
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
# DATA FILES
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
# ANALYSIS PERIOD
# =============================================================================

START_DATE = '2025-01-01'
END_DATE = '2025-12-31'
ANALYSIS_MONTHS = 12

# =============================================================================
# UE RATIO THRESHOLDS (Verified: 119.06M updates ÷ 5.44M enrollments = 21.90)
# =============================================================================

NATIONAL_UE_RATIO = 21.90
LOW_UE_RATIO = 10.0
HIGH_UE_RATIO = 30.0
ANOMALY_UE_RATIO = 40.0

# =============================================================================
# READINESS THRESHOLDS
# =============================================================================

GOOD_READINESS = 30
MODERATE_READINESS = 15
CRITICAL_READINESS = 10

# =============================================================================
# ANOMALY DETECTION
# =============================================================================

Z_SCORE_THRESHOLD = 3.0
TEMPORAL_SPIKE_MULTIPLIER = 3.0
AGE_CONCENTRATION_THRESHOLD = 0.80

# =============================================================================
# CHILD ENROLLMENT
# =============================================================================

CHILD_ENROLLMENT_THRESHOLD = 0.80
HIGH_CHILD_ENROLLMENT = 0.98

# =============================================================================
# DEMOGRAPHIC CONTEXT
# =============================================================================

NATIONAL_BIRTH_RATE = 16.5
MBU_AGES = [5, 15]

# =============================================================================
# VISUALIZATION
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
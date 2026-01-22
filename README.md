# UIDAI Aadhaar Analysis System

A three-dimensional diagnostic framework for identifying systemic gaps in India's Aadhaar identity ecosystem through analysis of 4.94 million transaction records from 2025. [1](#0-0) 

## Overview

This system processes raw Aadhaar enrollment and update data through a sequential pipeline to generate actionable insights about coverage gaps, readiness challenges, and data integrity issues. The analysis produces a comprehensive 50+ page PDF report with prioritized recommendations for UIDAI. [2](#0-1) 

## Key Features

### Three-Dimensional Analysis Framework

- **Coverage Gap Analysis**: Identifies districts with enrollment failures using 2×2 classification matrix and UE ratio analysis
- **Readiness Gap Analysis**: Calculates youth biometric compliance scores to predict authentication failures
- **Integrity Gap Analysis**: Multi-modal anomaly detection with composite risk scoring (0-15 points)

### Data Processing Pipeline

Sequential execution through 7 main scripts:
1. `00_data_quality_check.py` - Raw data validation
2. `01_data_loading.py` - Multi-file CSV concatenation
3. `02_data_cleaning.py` - Geographic standardization and deduplication
4. `03_dimension1_coverage.py` - Coverage gap analysis
5. `04_dimension2_readiness.py` - Readiness gap analysis  
6. `05_dimension3_integrity.py` - Integrity gap analysis
7. `06_report_generation.py` - Automated PDF report generation

### Validation System

Multi-layer validation including ground truth verification, phantom record detection, and geographic consistency checks before report generation. [3](#0-2) 

## Installation

### Prerequisites

- Python 3.11+
- Dependencies listed in `requirements.txt`

### Setup

1. Clone the repository:
```bash
git clone https://github.com/AtharvSabde/UIDAI_hackathon
cd UIDAI_hackathon
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Organize data files:
```
data/
├── raw/
│   ├── api_data_aadhar_enrolment_*.csv
│   ├── api_data_aadhar_biometric_*.csv
│   └── api_data_aadhar_demographic_*.csv
└── processed/  # Created automatically
```

## Usage

Execute the pipeline sequentially:

```bash
# Run data quality checks
python src/00_data_quality_check.py

# Load and concatenate data files
python src/01_data_loading.py

# Clean and merge datasets
python src/02_data_cleaning.py

# Run three-dimensional analysis
python src/03_dimension1_coverage.py
python src/04_dimension2_readiness.py
python src/05_dimension3_integrity.py

# Generate final report
python src/06_report_generation.py
```

### Configuration

All thresholds and paths are centrally managed in `utils/config.py`: [4](#0-3) 

- `NATIONAL_UE_RATIO = 21.90` - Baseline update-to-enrollment ratio
- `GOOD_READINESS = 30` - Youth biometric compliance threshold
- `Z_SCORE_THRESHOLD = 3.0` - Statistical outlier detection

## Outputs

### Data Artifacts
- **CSV Tables** (~30 files): Analytical results in `outputs/tables/`
- **PNG Visualizations** (~20 files): 300 DPI figures in `outputs/figures/`
- **PDF Report**: `UIDAI_Hackathon_Submission.pdf` in `outputs/report/`

### Key Metrics
- **Geographic Coverage**: 36 states, 888 state-district combinations, 19,814 pincodes
- **Data Volume**: 2,187,722 merged records (5.44M enrollments, 119.06M updates)
- **Analysis Results**: 57 coverage gap districts, 24 at-risk districts, 4,628 anomalous pincodes

## Technical Architecture

### Core Components

- **Data Processing**: Pandas-based ETL with geographic standardization
- **Analysis Engine**: NumPy/SciPy statistical computations with scikit-learn clustering
- **Visualization**: Matplotlib/Seaborn with consistent color schemes
- **Report Generation**: ReportLab PDF engine with custom styling

### Data Flow

```mermaid
graph LR
    A[Raw CSV Files] --> B[Data Loading]
    B --> C[Cleaning & Standardization]
    C --> D[Merged Dataset]
    D --> E[Three-Dimensional Analysis]
    E --> F[Validation]
    F --> G[PDF Report Generation]
```

## Validation & Quality Assurance

The system implements defense-in-depth validation:

1. **Ground Truth Verification**: Establishes authoritative totals from merged data
2. **Progressive Validation**: Validates each pipeline stage
3. **Phantom Record Detection**: Prevents data inflation artifacts
4. **Geographic Consistency**: Validates pincode-district mappings

All metrics are programmatically verified before PDF generation. [5](#0-4) 

## Repository Structure

```
UIDAI_hackathon/
├── data/
│   ├── raw/                      # Original UIDAI datasets
│   └── processed/                # Cleaned and merged datasets
├── outputs/
│   ├── tables/                   # CSV analytical outputs
│   ├── figures/                  # PNG visualizations
│   └── report/                   # Final PDF
├── src/                          # Analysis pipeline scripts
├── utils/
│   └── config.py                 # Centralized configuration
└── requirements.txt              # Python dependencies
```

## Key Findings

- **Coverage**: 57 districts show enrollment gaps potentially excluding marginalized populations
- **Readiness**: 24 districts face authentication challenges (12 critical, 12 low priority)
- **Integrity**: 48 pincodes require immediate data quality investigation

## Contributing

This project was developed for the UIDAI Hackathon. The complete source code is available for technical review and reproducibility verification. [6](#0-5) 

## License

Please refer to the LICENSE file for licensing information.

---

**Note**: This analysis uses only anonymised datasets provided by UIDAI for the hackathon. No personally identifiable information or biometric identifiers were accessed during development. [7](#0-6) 

## Notes

The README is based on the comprehensive system documentation available in the wiki "Overview" page and the actual implementation in the codebase. Key technical details about the three-dimensional analysis framework, data processing pipeline, and validation mechanisms are derived from the source code in `src/06_report_generation.py`, `utils/config.py`, and related analysis scripts.

Wiki pages you might want to explore:
- [Overview (AtharvSabde/UIDAI_hackathon)](/wiki/AtharvSabde/UIDAI_hackathon#1)

### Citations

**File:** src/06_report_generation.py (L611-620)
```python
    "<b>Total records:</b> 2,187,722 (after merging and deduplication)",
    "<b>Unique dates:</b> 92 (weekly aggregation from Jan 3 - Dec 31, 2025)",
    "<b>Geographic coverage:</b> 36 states, 888 state-district combinations* (865 unique district names), 19,814 pincodes",
    "<b>Total enrollments tracked:</b> 5,435,484",
    "<b>Total biometric updates tracked:</b> 69,763,095",
    "<b>Total demographic updates tracked:</b> 49,295,185",
    "<b>Total updates tracked:</b> 119,058,280",
    "<b>National UE Ratio:</b> 21.90× (updates per enrollment)",
    "<b>Data completeness:</b> No missing values in core metrics",
    "<b>Note:</b> *783,737 duplicate records removed during data cleaning (same date-state-district-pincode combinations aggregated)"
```

**File:** src/06_report_generation.py (L1316-1326)
```python
        India's Aadhaar system has successfully transitioned from enrollment expansion to update-driven maintenance, 
        with 96.9% of new enrollments targeting children and a national UE ratio of 21.9×. However, critical equity 
        gaps persist: 57 districts show coverage gaps potentially excluding marginalized populations, 24 districts face 
        authentication readiness challenges (12 critical, 12 low priority), and 48 pincodes require immediate data 
        quality investigation (32 critical + 16 high risk).<br/><br/>

        Our three-dimensional framework provides UIDAI with a replicable diagnostic tool for precision interventions. 
        The transition to universal coverage requires targeted action-mobile camps to 24 at-risk districts, enrollment 
        drives to 57 coverage gap districts, audit of 48 high-priority pincodes-not mass campaigns. By analyzing 888 
        state-district combinations across 19,814 pincodes, these findings are actionable, geographically specific, 
        and resource-optimized for immediate deployment.
```

**File:** src/06_report_generation.py (L1378-1382)
```python
        • <b>Data Sources:</b> Exclusively anonymised Aadhaar enrolment and update datasets provided 
        by UIDAI for this hackathon<br/>
        • <b>Privacy Compliance:</b> No personally identifiable information (PII), biometric identifiers, 
        or authentication logs were accessed at any stage<br/>
        • <b>Execution Time:</b> Approximately 15-20 minutes on standard laptop
```

**File:** src/06_report_generation.py (L1553-1559)
```python
        <b>Code Availability:</b> The complete, fully documented source code for this analytical pipeline is available at:  
        https://github.com/AtharvSabde/UIDAI_hackathon

        This repository includes end-to-end data processing scripts, analytical modules, 
        validation tests, and PDF report generation code. Access is provided for optional 
        technical review and reproducibility verification.
        """
```

**File:** src/06_report_generation.py (L2494-2532)
```python
        c1_text = """
        All numerical values, classifications, and figures reported in this document were verified using 
        an automated validation script (src/validation_test.py) executed after completion of the 
        analytical pipeline and immediately before PDF generation.
        """
        story.append(Paragraph(c1_text, styles['BodyJustified']))
        story.append(Spacer(1, 0.06*inch))

        c1_bullets = """
        The validation script recomputes all headline metrics directly from the final merged dataset and 
        cross-checks them against:<br/>
        • Generated analytical tables and figures<br/>
        • Values presented in the PDF (by section and page)
        """
        story.append(Paragraph(c1_bullets, styles['BodyJustified']))
        story.append(Spacer(1, 0.08*inch))
        
        c1_purpose = """
        The purpose of this step is to ensure internal consistency, completeness, and freedom from 
        manual transcription errors.
        """
        story.append(Paragraph(c1_purpose, styles['BodyJustified']))
        story.append(Spacer(1, 0.12*inch))

        # C.2 Validation Coverage
        c2_heading = Paragraph("C.2 Validation Coverage", styles['SubsectionHeading'])
        story.append(c2_heading)
        story.append(Spacer(1, 0.08*inch))

        c2_bullets = """
        The script performs checks across the following stages:<br/>
        • <b>Authoritative Number Derivation:</b> Calculated directly from merged_data.csv<br/>
        • <b>Data Integrity:</b> Checks on raw, cleaned, and merged datasets<br/>
        • <b>Dimension-wise Output:</b> Validation of Coverage, Readiness, and Integrity metrics<br/>
        • <b>Risk Stratification:</b> Verification of anomaly counts and categories<br/>
        • <b>Completeness:</b> Presence of all required tables, figures, and diagrams<br/><br/>
        All checks are deterministic and based on fixed aggregation logic and thresholds defined in 
        utils/config.py.
        """
```

**File:** src/06_report_generation.py (L2550-2572)
```python
        validation_data = [
    # Header Row
    ['Metric', 'Validation Output', 'Reported in PDF', 'Page(s)'],
    
    # General Metrics
    ['States', '36', '36', '2'],
    ['Districts', '865', '888*', '2, 8'],
    ['Pincodes', '19,814', '19,814', '2'],
    ['Merged Records', '2,187,722', '2.19M', '2, 7'],
    ['Total Enrollments', '5,435,484', '5.44M', '2, 12'],
    ['Total Biometric Updates', '69,763,095', '69.76M', '7, 12'],
    ['Total Demographic Updates', '49,295,185', '49.30M', '7, 12'],
    ['Total Updates', '119,058,280', '119.06M', '2, 12'],
    ['National UE Ratio', '21.90', '21.9×', '2, 12'],
    ['Child Enrollment (0–17)', '96.9%', '96.9%', '12–13'],
    
    # Dimension Specific Metrics
    ['Coverage Gap Districts', '57', '57', '12, 14'],
    ['Crisis Zone Districts', '387', '387', '14, 17'],
    ['Critical Readiness Districts', '12', '12', '12, 15'],
    ['Low Readiness Districts', '12', '12', '12, 15'],
    ['Anomalous Pincodes', '4,628', '4,628', '16'],
    ['Critical + High Risk Pincodes', '48', '48', '12, 16']
```

**File:** utils/config.py (L1-32)
```python
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
```

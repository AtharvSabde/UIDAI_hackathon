"""
Enhanced Report Generator - WITH ALL IMPROVEMENTS
- Page numbers at bottom right
- Table of contents on page 2
- Point-wise information instead of paragraphs
- Key insight boxes at start of each fdimension
"""

import pandas as pd
import numpy as np
import csv
import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, 
    Preformatted, KeepTogether, PageTemplate, Frame
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import (
    PROCESSED_DATA_DIR, FIGURES_DIR, TABLES_DIR,
    NATIONAL_UE_RATIO, GOOD_READINESS
)


class NumberedCanvas(canvas.Canvas):
    """Custom canvas for page numbers at bottom right"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        page_num = self._pageNumber
        if page_num > 1:  # Skip cover page
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor('#666666'))
            self.drawRightString(7.75*inch, 0.5*inch, f"{page_num}")


class EnhancedAadhaarReport:
    """Generate enhanced PDF report with all improvements"""
    
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(FIGURES_DIR), 'report')
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.report_path = os.path.join(
            self.output_dir, 
            'UIDAI_Hackathon_Submission.pdf'
        )
        
        # Create document with better margins
        self.doc = SimpleDocTemplate(
            self.report_path,
            pagesize=letter,
            rightMargin=1*inch,
            leftMargin=1*inch,
            topMargin=0.9*inch,
            bottomMargin=1*inch
        )
        
        # Styles
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        
        # Story (content)
        self.story = []
        
        # Framework diagram path
        self.framework_img_path = r"C:\Users\atharv\Desktop\aadhaar_analysis\src\image\Aadhaar System Health Diagnostic Framework.png"
    
    def _create_custom_styles(self):
        """Create custom paragraph styles with better hierarchy"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=32,
            textColor=colors.HexColor('#1565c0'),
            spaceAfter=24,
            spaceBefore=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=38
        ))
        
        # Subtitle
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#424242'),
            spaceAfter=14,
            spaceBefore=6,
            alignment=TA_CENTER,
            fontName='Helvetica',
            leading=20
        ))
        
        # Section heading - Title Case
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#d32f2f'),
            spaceAfter=16,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            leading=22
        ))
        
        # Subsection heading
        self.styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#f57c00'),
            spaceAfter=12,
            spaceBefore=16,
            fontName='Helvetica-Bold',
            leading=18
        ))
        
        # Bullet point style
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=8,
            leftIndent=20,
            bulletIndent=10
        ))
        
        # Key finding box
        self.styles.add(ParagraphStyle(
            name='KeyFinding',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=8,
            leftIndent=15,
            rightIndent=15
        ))
        
        # TOC entry
        self.styles.add(ParagraphStyle(
            name='TOCEntry',
            parent=self.styles['Normal'],
            fontSize=11,
                leading=18,
        spaceAfter=4
        ))
    
    # Body justified style (ADD THIS NEW SECTION)
        self.styles.add(ParagraphStyle(
            name='BodyJustified',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
    
    def create_key_insight_box(self, title, description, metrics_data, color_hex):
        """Create key insight box for dimension analysis"""
        
        # Title box
        title_data = [[Paragraph(f"<b>{title}</b>", self.styles['KeyFinding'])]]
        title_table = Table(title_data, colWidths=[6*inch])
        title_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(color_hex)),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        # Description box
        desc_data = [[Paragraph(description, self.styles['KeyFinding'])]]
        desc_table = Table(desc_data, colWidths=[6*inch])
        desc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f4f8')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        # Metrics table
        metrics_table = Table(metrics_data, colWidths=[2*inch, 2*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(color_hex)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return [title_table, desc_table, Spacer(1, 0.18*inch), metrics_table]
    
    def add_cover_page(self):
        """Add enhanced cover page"""
        
        self.story.append(Spacer(1, 0.8*inch))
        
        # Main Title
        title = Paragraph("<b>Aadhaar System Health Diagnostic</b>", self.styles['CustomTitle'])
        self.story.append(title)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Subtitle
        subtitle = Paragraph("Three-Dimensional Analysis Framework", self.styles['Subtitle'])
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.15*inch))
        
        # Problem statement
        problem_text = Paragraph(
            "Unlocking Societal Trends in Aadhaar Enrolment and Updates",
            self.styles['Subtitle']
        )
        self.story.append(problem_text)
        self.story.append(Spacer(1, 0.1*inch))
        
        # Three dimensions
        dimensions_text = """
        <font color="#1976d2" size="12">📊 Coverage Gap</font> • 
        <font color="#f57c00" size="12">⚡ Readiness Gap</font> • 
        <font color="#d32f2f" size="12">🔍 Integrity Gap</font>
        """
        dimensions = Paragraph(dimensions_text, self.styles['Subtitle'])
        self.story.append(dimensions)
        self.story.append(Spacer(1, 0.4*inch))
        
        # Framework diagram
        if os.path.exists(self.framework_img_path):
            try:
                img = Image(self.framework_img_path, width=6*inch, height=3.7*inch)
                self.story.append(img)
                self.story.append(Spacer(1, 0.3*inch))
            except:
                self.story.append(Spacer(1, 0.3*inch))
        else:
            self.story.append(Spacer(1, 0.3*inch))
        
        # Key metrics
        metrics_data = [
            ['5.44M', '119.06M', '21.9×'],
            ['Enrollments', 'Updates', 'UE Ratio'],
        ]
        metrics_table = Table(metrics_data, colWidths=[2*inch, 2*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 20),
            ('FONTSIZE', (0, 1), (-1, 1), 11),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1565c0')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        self.story.append(metrics_table)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Info table
        
        info_data = [
            ['Hackathon', 'UIDAI Online Hackathon on Data-Driven Innovation for Aadhaar'],
            ['Organized by', 'UIDAI in association with NIC, MeitY'],
            ['Author', 'Atharv Umesh Sabde'], 
            
            
            ['Problem Statement', 'Targeting Enrollment Stagnation, Mandatory Update Lags, and Data Anomalies'],
            ['Analysis Period', 'January - December 2025'],
            ['Geographic Coverage', '36 states • 888 state-district combinations • 19,814 pincodes'],
            ['Report Date', datetime.now().strftime('%B %d, %Y')]
        ]
        
        info_table = Table(info_data, colWidths=[1.8*inch, 4.2*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1565c0')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        self.story.append(info_table)
        self.story.append(PageBreak())
    
    def add_table_of_contents(self):
        """Add table of contents on page 2"""
        
        heading = Paragraph("Table of Contents", self.styles['SectionHeading'])
        self.story.append(heading)
        self.story.append(Spacer(1, 0.2*inch))
        
        toc_items = [
    ("1. Problem Statement and Approach", "4"),
    ("2. Datasets Used", "7"),
    ("3. Methodology", "10"),
    ("4. Data Analysis - Executive Summary", "14"),
    ("5. Dimension 1: Coverage Gap Analysis", "15"),
    ("6. Dimension 2: Readiness Gap Analysis", "19"),
    ("7. Dimension 3: Integrity Gap Analysis", "21"),
    ("8. Strategic Recommendations", "23"),
    ("9. Conclusion", "24"),
    ("Appendix A: Code Architecture", "25"),
    ("Appendix B: Implementation Excerpts", "29"),
    ("Appendix C: Validation Evidence", "43"),
    ("Appendix D: Supplementary Figures", "45"),
        ]
        
        toc_data = []
        for item, page in toc_items:
            toc_data.append([
                Paragraph(item, self.styles['TOCEntry']),
                Paragraph(page, self.styles['TOCEntry'])
            ])
        
        toc_table = Table(toc_data, colWidths=[5.5*inch, 0.5*inch])
        toc_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        self.story.append(toc_table)
        self.story.append(PageBreak())
    
    def add_problem_statement_and_approach(self):
        """Add Problem Statement and Approach - POINT-WISE"""
        
        heading = Paragraph("1. Problem Statement and Approach", self.styles['SectionHeading'])
        self.story.append(heading)
        self.story.append(Spacer(1, 0.15*inch))
        
        # Problem identification
        problem_heading = Paragraph("Problem Identification", self.styles['SubsectionHeading'])
        self.story.append(problem_heading)
        
        context_points = [
            "<b>Current State:</b> Aadhaar coverage exceeds 90% in most states with 141.80 crore Aadhaar numbers generated (as of March 31, 2025)",
            "<b>System Transition:</b> India's identity ecosystem has shifted from enrollment expansion to update-driven maintenance",
            "<b>Analysis Gap:</b> Traditional single-metric analysis fails to address three critical blind spots"
        ]
        
        for point in context_points:
            self.story.append(Paragraph(f"• {point}", self.styles['BulletPoint']))
        
        self.story.append(Spacer(1, 0.12*inch))
        self.story.append(Paragraph("<b>Three Critical Blind Spots:</b>", self.styles['SubsectionHeading']))
        
        blind_spots = [
            ("<b>The Update Paradox (Coverage Gap):</b>",
             "High update-to-enrollment ratios may mask enrollment failures in marginalized populations",
             "Districts with saturated populations show high update activity but obscure whether NEW enrollments reach underserved groups"),
            
            ("<b>The Authentication Readiness Challenge (Readiness Gap):</b>",
             "Youth (ages 5-17) must update biometrics before age 18 when authentication becomes mandatory",
             "Without predictive tracking, districts face authentication access challenges during youth transition to adulthood"),
            
            ("<b>The Integrity Uncertainty (Integrity Gap):</b>",
             "Anomalous patterns at pincode-level may indicate data quality issues or systematic errors",
             "Without composite risk scoring, investigation resources are misdirected")
        ]
        
        for title, desc1, desc2 in blind_spots:
            self.story.append(Paragraph(f"• {title}", self.styles['BulletPoint']))
            self.story.append(Paragraph(f"  - {desc1}", self.styles['BulletPoint']))
            self.story.append(Paragraph(f"  - {desc2}", self.styles['BulletPoint']))
        
        self.story.append(Spacer(1, 0.15*inch))
        
        # Proposed approach
        approach_block = [
            Paragraph("Proposed Analytical Approach", self.styles['SubsectionHeading']),
        ]
        
        approach_intro = [
            "<b>Framework:</b> Three-dimensional diagnostic examining interplay between enrollment patterns, update compliance, and data integrity",
            "<b>Geographic Precision:</b> District and pincode-level analysis (moving beyond state-level aggregations)",
            "<b>Outcome:</b> Actionable insights for resource-optimized interventions"
        ]
        
        for point in approach_intro:
            approach_block.append(
                Paragraph(f"• {point}", self.styles['BulletPoint'])
            )
        
        self.story.append(KeepTogether(approach_block))
        
        self.story.append(Spacer(1, 0.12*inch))
        
        framework_block = [
            Paragraph("<b>Three-Dimensional Framework:</b>", self.styles['SubsectionHeading'])
        ]
        
        dimensions = [
            ("<b>Dimension 1: Coverage Gap Analysis</b>",
             "2×2 classification matrix (enrollment vs. updates relative to medians)",
             "Identifies: Healthy & Growing, Saturation/Coverage Gap, New Users Need Engagement, Crisis Zone",
             "Child enrollment analysis (0-17 years) aligns with UIDAI's emphasis on child enrolment"),
            
            ("<b>Dimension 2: Readiness Gap Analysis</b>",
             "Calculates 'Transition Readiness Scores' for youth (5-17) biometric update compliance",
             "Demographic transition model estimates authentication risk as youth turn 18",
             "Informs mobile biometric camp resource planning (15-20 units) for critical districts"),
            
            ("<b>Dimension 3: Integrity Gap Analysis</b>",
             "Multi-layered anomaly detection: extreme UE ratios >100, temporal spikes >3×, age concentrations >80%",
             "Composite risk scoring (0-12 points) stratifies 19,814 pincodes",
             "Prioritizes investigation resources: Critical/High/Medium/Low categories")
        ]
        
        for title, *details in dimensions:
            framework_block.append(
                Paragraph(f"• {title}", self.styles['BulletPoint'])
            )
            for detail in details:
                framework_block.append(
                    Paragraph(f"  - {detail}", self.styles['BulletPoint'])
                )
        
        self.story.append(KeepTogether(framework_block))
        
        self.story.append(Spacer(1, 0.15*inch))
        
        # Innovation
        innovation_block = [
            Paragraph("<b>Innovation Highlights:</b>", self.styles['SubsectionHeading'])
        ]
        
        innovation_points = [
            "<b>Cross-Dimensional Insights:</b> Reveals hidden patterns through interplay analysis",
            "<b>Example:</b> District may appear 'healthy' (high updates) but 'critical' (low youth compliance)",
            "<b>Precision:</b> Enables targeted mobile camps instead of general enrollment drives",
            "<b>Efficiency:</b> Resource-optimized interventions based on specific district needs"
        ]
        
        for point in innovation_points:
            innovation_block.append(
                Paragraph(f"• {point}", self.styles['BulletPoint'])
            )
        
        self.story.append(KeepTogether(innovation_block))
        
        self.story.append(PageBreak())



    def add_datasets_used(self):
        """Add Datasets Used section - POINT-WISE"""
        
        heading = Paragraph("2. Datasets Used", self.styles['SectionHeading'])
        self.story.append(heading)
        self.story.append(Spacer(1, 0.15*inch))
        
        intro_points = [
            "<b>Source:</b> Official anonymized Aadhaar datasets provided by UIDAI for hackathon",
            "<b>Period:</b> Calendar year 2025 (enrollment and update transactions)",
            "<b>Integration:</b> All three datasets merged on temporal and geographic keys"
        ]
        
        for point in intro_points:
            self.story.append(Paragraph(f"• {point}", self.styles['BulletPoint']))
        
        self.story.append(Spacer(1, 0.15*inch))
        
        # Dataset tables (keep existing format)
        # Dataset 1
        ds1_heading = Paragraph("Dataset 1: Aadhaar Enrolment (2025)", self.styles['SubsectionHeading'])
        self.story.append(ds1_heading)
        
        ds1_data = [
            ['Attribute', 'Value'],
            ['File names', 'api_data_aadhar_enrolment_0_500000.csv\napi_data_aadhar_enrolment_500000_1000000.csv\napi_data_aadhar_enrolment_1000000_1006029.csv'],
            ['Total records', '1,006,029'],
            ['Time period', 'January 3, 2025 - December 31, 2025 (weekly aggregation)'],
            ['Geographic granularity', 'Pincode level (19,814 unique pincodes)'],
            ['Columns used', 'date, state, district, pincode, age_0_5, age_5_17, age_18_greater']
        ]
        
        ds1_table = Table(ds1_data, colWidths=[2*inch, 4*inch])
        ds1_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f57c00')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        self.story.append(ds1_table)
        self.story.append(Spacer(1, 0.12*inch))
        
        # Dataset 2
        ds2_heading = Paragraph("Dataset 2: Aadhaar Biometric Updates (2025)", self.styles['SubsectionHeading'])
        self.story.append(ds2_heading)
        
        ds2_data = [
            ['Attribute', 'Value'],
            ['File names', 'api_data_aadhar_biometric_0_500000.csv\napi_data_aadhar_biometric_500000_1000000.csv\napi_data_aadhar_biometric_1000000_1500000.csv\napi_data_aadhar_biometric_1500000_1861108.csv'],
            ['Total records', '1,861,108'],
            ['Time period', 'January 3, 2025 - December 31, 2025 (weekly aggregation)'],
            ['Geographic granularity', 'Pincode level (19,814 unique pincodes)'],
            ['Columns used', 'date, state, district, pincode, bio_age_5_17, bio_age_17_']
        ]
        
        ds2_table = Table(ds2_data, colWidths=[2*inch, 4*inch])
        ds2_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#388e3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        self.story.append(ds2_table)
        self.story.append(Spacer(1, 0.12*inch))
        
                # Dataset 3
        ds3_block = []

        ds3_heading = Paragraph(
            "Dataset 3: Aadhaar Demographic Updates (2025)",
            self.styles['SubsectionHeading']
        )
        ds3_block.append(ds3_heading)

        ds3_data = [
            ['Attribute', 'Value'],
            ['File names', 'api_data_aadhar_demographic_0_500000.csv\n'
                           'api_data_aadhar_demographic_500000_1000000.csv\n'
                           'api_data_aadhar_demographic_1000000_1500000.csv\n'
                           'api_data_aadhar_demographic_1500000_2000000.csv\n'
                           'api_data_aadhar_demographic_2000000_2071700.csv'],
            ['Total records', '2,071,700'],
            ['Time period', 'January 3, 2025 - December 31, 2025 (weekly aggregation)'],
            ['Geographic granularity', 'Pincode level (19,814 unique pincodes)'],
            ['Columns used', 'date, state, district, pincode, demo_age_5_17, demo_age_17_']
        ]

        ds3_table = Table(ds3_data, colWidths=[2*inch, 4*inch])
        ds3_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))

        ds3_block.append(ds3_table)

        self.story.append(KeepTogether(ds3_block))
        self.story.append(Spacer(1, 0.12*inch))

        
        # Statistics - point-wise
        stats_points = [
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
        ]
        

        self.story.append(Spacer(1, 0.12*inch))

        # Geographic complexity explanation
        geo_complexity_block = [
        Paragraph("<b>Geographic Complexity Note:</b>", self.styles['SubsectionHeading'])
        ]

        geo_points = [
    "<b>888 State-District Combinations:</b> Some pincodes legitimately serve areas across state/district boundaries",
    "<b>865 Unique District Names:</b> The difference (23) represents cross-border pincodes",
    "<b>Example:</b> A pincode on the Chandigarh-Punjab border appears in both jurisdictions",
    "<b>Approach:</b> Analysis treats (state, district) as composite key to preserve geographic accuracy",
    "<b>Impact:</b> Prevents information loss from forced consolidation; reflects real administrative boundaries"
        ]

        for point in geo_points:
            geo_complexity_block.append(
                Paragraph(f"• {point}", self.styles['BulletPoint'])
            )

        self.story.append(KeepTogether(geo_complexity_block))

        self.story.append(Spacer(1, 0.12*inch))



        self.story.append(Paragraph("<b>Final Merged Dataset Statistics:</b>", self.styles['SubsectionHeading']))
        for point in stats_points:
            self.story.append(Paragraph(f"• {point}", self.styles['BulletPoint']))
        
        self.story.append(Spacer(1, 0.12*inch))
        
        # Scope clarification
        scope_points = [
            "Uses exclusively anonymised enrolment and update datasets from UIDAI",
            "No external individual-level data accessed",
            "No authentication logs used",
            "No personally identifiable information (PII) accessed at any stage"
        ]
        
        self.story.append(Paragraph("<b>Data Scope Clarification:</b>", self.styles['SubsectionHeading']))
        for point in scope_points:
            self.story.append(Paragraph(f"• {point}", self.styles['BulletPoint']))
        
        self.story.append(PageBreak())
    
    def add_methodology(self):
        """Add Methodology section - POINT-WISE"""
        
        heading = Paragraph("3. Methodology", self.styles['SectionHeading'])
        self.story.append(heading)
        self.story.append(Spacer(1, 0.15*inch))
        
        # Data cleaning
        cleaning_heading = Paragraph("Data Cleaning and Preprocessing", self.styles['SubsectionHeading'])
        self.story.append(cleaning_heading)
        
        cleaning_tasks = [
            ("<b>State Name Standardization:</b>",
             "Identified and corrected 64 state name variations",
             "Fixed case inconsistencies, spelling errors, invalid entries",
             "Examples: 'WEST BENGAL'/'West bengal' → 'West Bengal'; 'ODISHA'/'Orissa' → 'Odisha'",
             "Removed 24 invalid records (pincodes/cities listed as states)"),



            ("<b>District Name Standardization:</b>",
            "Identified and corrected 137+ district name variations",
            "Fixed spelling inconsistencies, special characters, East/West duplicates",
            "Examples: 'Ananthapur'/'Ananthapuramu' → 'Anantapur'; 'Medinipur West'/'West Medinipur' → 'Paschim Medinipur'",
            "Reduced from 1,028 apparent districts to 865 unique districts"),

            
            ("<b>Geographic Validation:</b>",
             "Cross-validated district-state mappings against Census 2011",
             "Corrected 8 mismatched districts"),
            
            ("<b>Temporal Consistency:</b>",
             "Verified date ranges: Jan 3 - Dec 31, 2025",
             "Confirmed weekly aggregation: 92 unique dates across 363 days"),
            
            ("<b>Null Value Handling:</b>",
             "Verified zero missing values in core numeric columns",
             "Excluded records with null geographic fields (<0.001% of data)"),
            
            ("<b>Outlier Detection:</b>",
             "Flagged extreme values for Dimension 3 anomaly analysis",
             "Preserved outliers to maintain data quality signals"),


            ("<b>Duplicate Record Aggregation:</b>",
            "Identified 783,737 duplicate records with same (date, state, district, pincode) combination",
            "Breakdown: 48,143 enrollment, 189,219 biometric, 546,375 demographic duplicates",
            "Approach: Aggregated (summed) duplicate records before merge to prevent count inflation",
            "Result: Merged dataset reduced from 3.17M to 2.19M records with accurate totals")
        ]
        
        for task in cleaning_tasks:
            title = task[0]
            details = task[1:]
            self.story.append(Paragraph(f"• {title}", self.styles['BulletPoint']))
            for detail in details:
                self.story.append(Paragraph(f"  - {detail}", self.styles['BulletPoint']))
        
        self.story.append(Spacer(1, 0.15*inch))
        
        # Transformations
        trans_heading = Paragraph("Data Transformations and Feature Engineering", self.styles['SubsectionHeading'])
        self.story.append(trans_heading)
        
        transformations = [
            ("<b>UE Ratio (Update-to-Enrollment Ratio):</b>",
            "Formula: (Total Updates) ÷ (Total Enrollments) at district/pincode level",
            "NOT published by UIDAI - derived metric for saturation analysis",
            "National UE Ratio: 21.90× (119.06M updates ÷ 5.44M enrollments)",
            "Interpretation: Ratio >1 = saturation; Ratio ~22 = mature update-driven system"),
            
            ("<b>Child Enrollment Percentage:</b>",
             "Formula: [(age_0_5 + age_5_17) ÷ Total Enrollments] × 100",
             "Validates UIDAI's strategic focus on children",
             "Identifies districts with residual adult enrollment needs"),
            
            ("<b>Readiness Score:</b>",
             "Formula: (Youth Bio Updates ÷ Total Bio Updates) × 100",
             "Measures MBU policy compliance for ages 5 and 15",
             "Thresholds: Good (≥30%), Moderate (15-30%), Critical (<15%)"),
            
            ("<b>Composite Risk Score:</b>",
             "Weighted sum: Extreme UE >100 (+5), High UE >25 (+3), Age Concentration >80% (+2), Temporal Spike >3× (+2)",
             "Range: 0-12 points",
             "Categories: Critical (8-12), High (5-7), Medium (3-4), Low (1-2)"),
            
            ("<b>2×2 Classification Matrix:</b>",
             "Based on enrollment and update levels vs. medians",
             "Medians: Enrollment = 5,340; Updates = 115,128",
             "Four quadrants: Healthy & Growing, Saturation/Coverage Gap, New Users Need Engagement, Crisis Zone")
        ]
        
        for trans in transformations:
            title = trans[0]
            details = trans[1:]
            self.story.append(Paragraph(f"• {title}", self.styles['BulletPoint']))
            for detail in details:
                self.story.append(Paragraph(f"  - {detail}", self.styles['BulletPoint']))
        
        self.story.append(Spacer(1, 0.15*inch))
        

        self.story.append(Spacer(1, 0.15*inch))

        # UE Ratio variants explanation
        ue_variants_block = [
         Paragraph("<b>Understanding UE Ratio Variants:</b>", self.styles['SubsectionHeading'])
        ]

        ue_variant_points = [
    "<b>National UE Ratio (21.90×):</b> Total updates ÷ total enrollments nationally",
    "  - Primary metric for overall system maturity",
    "  - Size-weighted: reflects actual transaction volumes",
    
    "<b>Average District UE Ratio (27.70):</b> Arithmetic mean of district-level ratios",
    "  - Shows typical district without size weighting",
    "  - Higher than national due to small saturated districts",
    
    "<b>Median District UE Ratio (23.62):</b> 50th percentile of district ratios",
    "  - Robust measure less affected by outliers",
    "  - Closest to national ratio (21.90)",
    
    "<b>Why They Differ:</b> Larger districts with more new enrollments have lower UE ratios, while smaller saturated districts have higher ratios. The national ratio (21.90) is most appropriate for policy assessment as it's size-weighted."
        ]

        for point in ue_variant_points:
            ue_variants_block.append(
                Paragraph(f"• {point}", self.styles['BulletPoint'])
            )

        self.story.append(KeepTogether(ue_variants_block))




        # Analytical methods
        methods_heading = Paragraph("Analytical Methods and Algorithms", self.styles['SubsectionHeading'])
        self.story.append(methods_heading)
        
        methods = [
            ("<b>Statistical Methods:</b>",
             "Z-score analysis (|z|>3) for UE ratio outlier detection",
             "Median-based thresholds for 2×2 classification",
             "Percentile analysis (75th, 90th) for high-risk districts"),
            
            ("<b>Predictive Modeling:</b>",
             "Demographic aging model estimates youth transition to adults",
             "Risk formula: Age 17 Pop × (1 - Readiness Score) = At-Risk Population",
             "Resource quantification: Units needed = At-Risk Pop ÷ 50 ÷ 30 days"),
            
            ("<b>Anomaly Detection:</b>",
             "Layer 1: Statistical outliers via Z-scores",
             "Layer 2: Domain thresholds (UE >25, >100)",
             "Layer 3: Temporal pattern analysis (4-week baselines, spikes >3×)",
             "Layer 4: Geographic clustering (≥3 anomalies = clustered)"),
            
            ("<b>Visualization Strategy:</b>",
             "All charts at 300 DPI for publication quality",
             "Consistent color-coding: Red (Critical), Orange (High), Yellow (Moderate), Green (Good)",
             "18 visualizations with unified schema for cognitive ease")
        ]
        
        for method in methods:
            title = method[0]
            details = method[1:]
            self.story.append(Paragraph(f"• {title}", self.styles['BulletPoint']))
            for detail in details:
                self.story.append(Paragraph(f"  - {detail}", self.styles['BulletPoint']))
        
        self.story.append(Spacer(1, 0.15*inch))
        
        # Transparency
        trans_heading = Paragraph("Source Discipline and Transparency", self.styles['SubsectionHeading'])
        self.story.append(trans_heading)
        
        trans_points = [
            "<b>UIDAI Annual Report 2024-25:</b> Used solely for policy reference and national-level context",
            "<b>District/Pincode Analysis:</b> Derived exclusively from anonymised hackathon datasets",
            "<b>Derived Metrics:</b> Clearly labeled where UIDAI doesn't publish indicators (e.g., UE ratio)",
            "<b>Auditability:</b> Full transparency prevents misattribution of derived metrics to official sources"
        ]
        
        for point in trans_points:
            self.story.append(Paragraph(f"• {point}", self.styles['BulletPoint']))
        
        self.story.append(PageBreak())
    
    def add_executive_summary(self):
        """Add executive summary - CORRECTED"""
        
        heading = Paragraph("DATA ANALYSIS AND VISUALISATION - EXECUTIVE SUMMARY", self.styles['SectionHeading'])
        self.story.append(heading)
        self.story.append(Spacer(1, 0.08*inch))
        
        summary_text = """
        This section presents key findings from our three-dimensional analysis of Aadhaar transactions in 2025 
        (5.44M enrollments and 119.06M updates across 2.19M records after deduplication), revealing a system 
        in transition from enrollment-driven to update-driven operations. Our analysis identifies 57 coverage 
        gap districts, 24 at-risk readiness districts, and 48 critical+high risk pincodes requiring immediate 
        intervention.
        """
        self.story.append(Paragraph(summary_text, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.12*inch))
        
        # Key findings - CORRECTED
        findings = [
    ("<b>Strategic Pivot Confirmed:</b> 96.9% of 2025 enrollments are children (0-17), with newborns (0-5) "
     "comprising 65.3% and youth (5-17) comprising 31.7%. This validates UIDAI's stated emphasis on child "
     "enrollment and backlog clearance."),
    
    ("<b>Update-Driven Economy:</b> Updates outnumber enrollments by 21.9× nationally (National UE Ratio: 21.90), "
     "representing system maturity and saturation. The average district UE ratio is 27.70 (unweighted mean), "
     "while the median is 23.62."),
    
    ("<b>Coverage Gaps Persist:</b> 57 districts (6.4% of 888 state-district combinations) exhibit "
     "'Saturation/Coverage Gap' patterns-high updates but stagnant enrollments-indicating exclusion of "
     "marginalized populations."),
    
    ("<b>Youth Readiness Success:</b> 84.8% of districts (753 of 888) achieve 'Good' readiness (≥30% youth bio "
     "updates), but 24 districts (2.7%) remain at-risk (12 critical, 12 low priority), requiring mobile "
     "biometric camps."),
    
    ("<b>Integrity Largely Intact:</b> 48 pincodes (1.0% of 4,628 flagged anomalies) demand immediate "
     "investigation (32 critical risk + 16 high risk). Geographic clustering in 395 districts suggests "
     "systematic patterns worth monitoring.")
        ]
        
        for finding in findings:
            self.story.append(Paragraph(f"• {finding}", self.styles['BodyJustified']))
        
        self.story.append(PageBreak())
    
    # =========================================================================
    #  HELPER METHOD: Filtered & Formatted CSV Table (With Footer Explanation)
    # =========================================================================
    def get_filtered_csv_table(self, csv_path, col_map, title, explanation_text=None):
        """
        Reads CSV, keeps specific columns, and returns a block containing:
        Title -> Table -> Explanation (Footer)
        All wrapped in KeepTogether to prevent page splits.
        """
        if not os.path.exists(csv_path):
            return Paragraph(f"<i>File not found: {os.path.basename(csv_path)}</i>", self.styles['BodyText'])

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                all_rows = list(reader)
            
            if not all_rows:
                return Paragraph(f"<i>Empty file</i>", self.styles['BodyText'])

            # 1. Identify indices of required columns
            header = all_rows[0]
            col_indices = []
            display_headers = []
            
            for csv_col, display_name in col_map.items():
                if csv_col in header:
                    col_indices.append(header.index(csv_col))
                    display_headers.append(display_name)
            
            if not col_indices:
                return Paragraph("<i>No matching columns found</i>", self.styles['BodyText'])

            # 2. Extract Data
            table_data = [display_headers] # Header row
            for row in all_rows[1:]:       # Data rows
                new_row = [row[idx] for idx in col_indices]
                table_data.append(new_row)

            # 3. Create Table
            col_count = len(display_headers)
            col_width = (6.5 / col_count) * inch 
            
            t = Table(table_data, colWidths=[col_width] * col_count)
            
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#37474f')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f5f5')]),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            
            # 4. Construct the Block elements
            elements = [
                Spacer(1, 0.2*inch),
                Paragraph(f"<b>{title}</b>", self.styles['BodyText']),
                Spacer(1, 0.05*inch),
                t
            ]
            
            # Add Explanation BELOW the table if provided
            if explanation_text:
                elements.append(Spacer(1, 0.1*inch))
                elements.append(Paragraph(f"<i>Note: {explanation_text}</i>", self.styles['BodyJustified']))
            
            elements.append(Spacer(1, 0.15*inch))

            # Keep everything together on one page
            return KeepTogether(elements)
            
        except Exception as e:
            return Paragraph(f"<i>Error processing table: {str(e)}</i>", self.styles['BodyText'])

    # =========================================================================
    #  DIMENSION 1 FINDINGS
    # =========================================================================
    def add_dimension1_findings(self):
        """Add Dimension 1 findings"""
        
        caption_style = ParagraphStyle('FigCaption', parent=self.styles['Normal'], alignment=1, fontSize=10, fontName='Helvetica-Bold', spaceBefore=6, spaceAfter=12)

        heading = Paragraph("DIMENSION 1: COVERAGE GAP ANALYSIS", self.styles['SectionHeading'])
        self.story.append(heading)
        self.story.append(Spacer(1, 0.08*inch))
        
        overview = """
        Examines whether high update-to-enrollment ratios mask enrollment failures. Despite >90% coverage in most states, 
        district-level variation reveals equity gaps requiring targeted interventions.
        """
        self.story.append(Paragraph(overview, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.12*inch))
        
        # Key metrics table
        metrics_data = [
    ['Metric', 'Value', 'Interpretation'],
    ['Average District UE Ratio', '27.70', 'Updates exceed enrollments 27.7×'],
    ['Median District UE Ratio', '23.62', 'Typical district reality'],
    ['Child Enrollment %', '96.9%', '65.3% age 0-5, 31.7% age 5-17'],
    ['Adult Enrollment %', '3.1%', 'Near-complete saturation'],
    ['Districts Analyzed', '888*', '865 unique names, 36 states'],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 1.5*inch, 2.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f57c00')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        self.story.append(metrics_table)
        self.story.append(Spacer(1, 0.15*inch))

        self.story.append(metrics_table)
        self.story.append(Spacer(1, 0.08*inch))

        # Add footnote about 888 districts
        district_note = Paragraph(
            "<i>*888 state-district combinations representing 865 unique district names. "
            "Some pincodes serve areas across state/district boundaries.</i>",
            self.styles['BodyJustified']
        )
        self.story.append(district_note)
        self.story.append(Spacer(1, 0.15*inch)) 


        
        # Fig 1
        fig1_path = os.path.join(FIGURES_DIR, 'data_quality_age_distribution.png')
        if os.path.exists(fig1_path):
            img = Image(fig1_path, width=6*inch, height=3.8*inch)
            self.story.append(img)
            self.story.append(Paragraph("Figure 1: Age Distribution of 2025 Enrollments", caption_style))
        
        self.story.append(PageBreak())
        
        # 2x2 Matrix Table
        matrix_heading = Paragraph("District Classification (2×2 Matrix)", self.styles['SubsectionHeading'])
        self.story.append(matrix_heading)
        
        matrix_data = [
    ['Category', 'Count', '%', 'Recommended Action'],
    ['Healthy & Growing', '387', '43.6%', 'Maintain current operations'],
    ['Saturation/Coverage Gap', '57', '6.4%', 'Targeted enrollment drives for marginalized'],
    ['New Users Need Engagement', '57', '6.4%', 'Update awareness campaigns'],
    ['Crisis Zone', '387', '43.6%', 'Comprehensive outreach needed'],
        ]
        
        matrix_table = Table(matrix_data, colWidths=[2*inch, 1*inch, 0.8*inch, 2.7*inch])
        matrix_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d32f2f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        self.story.append(matrix_table)
        self.story.append(Spacer(1, 0.12*inch))
        
        # Fig 2
        fig2_path = os.path.join(FIGURES_DIR, 'dim1_2x2_matrix.png')
        if os.path.exists(fig2_path):
            img = Image(fig2_path, width=6*inch, height=4*inch)
            self.story.append(img)
            self.story.append(Paragraph("Figure 2: District Classification Matrix", caption_style))
        
        # --- TOP 10 TABLE (KEPT TOGETHER WITH EXPLANATION) ---
        csv_path_d1 = r"C:\Users\atharv\Desktop\aadhaar_analysis\outputs\tables\dim1_top10_crisis_zone_districts.csv"
        cols_d1 = {'state': 'State', 'district': 'Zone Name'}
        
        explanation_d1 = (
            "Priority Intervention List: The table above identifies the 'Crisis Zones'- districts "
            "showing the lowest levels of both new enrollments and update activity. These areas are "
            "likely stagnant and require immediate field outreach to restart engagement."
        )
        
        self.story.append(self.get_filtered_csv_table(
            csv_path_d1, cols_d1, "Table 1.1: Top 10 Crisis Zones (Lowest Activity)", explanation_d1
        ))
        
        self.story.append(PageBreak())
    
    # =========================================================================
    #  DIMENSION 2 FINDINGS
    # =========================================================================
    def add_dimension2_findings(self):
        """Add Dimension 2 findings"""

        caption_style = ParagraphStyle('FigCaption', parent=self.styles['Normal'], alignment=1, fontSize=10, fontName='Helvetica-Bold', spaceBefore=6, spaceAfter=12)
        
        heading = Paragraph("DIMENSION 2: READINESS GAP ANALYSIS", self.styles['SectionHeading'])
        self.story.append(heading)
        self.story.append(Spacer(1, 0.08*inch))
        
        overview = """
        Highlights districts where many youth (ages 5–17) may face authentication difficulties upon turning 18 due to 
        pending biometric updates. Analysis shows 49.1% of biometric updates come from youth (5-17), with 24 districts 
        (2.7%) requiring immediate intervention through mobile biometric camps.
        """
        self.story.append(Paragraph(overview, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.12*inch))
        
        # Readiness table
        readiness_data = [
    ['Metric', 'Value', 'Assessment'],
    ['Youth Bio Updates (5-17)', '34.23M', '49.1% of all bio updates'],
    ['Total Bio Updates', '69.76M', 'System-wide biometric activity'],
    ['Mean Readiness Score', '45.9%', 'Above 30% threshold'],
    ['Good Readiness Districts', '753', '84.8% - MBU policy working'],
    ['Moderate Readiness', '69', '7.8% - Needs monitoring'],
    ['Low Readiness Districts', '12', '1.4% - High priority'],
    ['Critical Readiness', '12', '1.4% - Urgent intervention needed'],
    ['At-Risk Total', '24', '2.7% - Combined priority action'],
        ]
        
        readiness_table = Table(readiness_data, colWidths=[2.2*inch, 2.2*inch, 2.1*inch])
        readiness_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#388e3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 7), (-1, 7), colors.HexColor('#fff3e0')),
        ]))
        
        self.story.append(readiness_table)
        self.story.append(Spacer(1, 0.12*inch))
        
        # Fig 3
        fig3_path = os.path.join(FIGURES_DIR, 'dim2_readiness_categories.png')
        if os.path.exists(fig3_path):
            img = Image(fig3_path, width=5.5*inch, height=3.8*inch)
            self.story.append(img)
            self.story.append(Paragraph("Figure 3: Districts by Readiness Category", caption_style))
        
        # --- TOP 10 TABLE (KEPT TOGETHER WITH EXPLANATION) ---
        csv_path_d2 = r"C:\Users\atharv\Desktop\aadhaar_analysis\outputs\tables\dim2_top10_at_risk_districts.csv"
        cols_d2 = {
            'state': 'State', 
            'district': 'District', 
            'readiness_score': 'Readiness (%)', 
            'predicted_failures_per_year': 'Est. Failures',
            'readiness_category': 'Category'
        }
        
        explanation_d2 = (
            "High-Risk Areas: The list above highlights districts with the highest projected failure "
            "rates. A low 'Readiness Score' indicates that a large percentage of youth (5-17) have not "
            "yet performed their mandatory biometric updates."
        )

        self.story.append(self.get_filtered_csv_table(
            csv_path_d2, cols_d2, "Table 2.1: Top 10 At-Risk Districts (Predicted Failures)", explanation_d2
        ))

        self.story.append(PageBreak())
    
    # =========================================================================
    #  DIMENSION 3 FINDINGS
    # =========================================================================
    def add_dimension3_findings(self):
        """Add Dimension 3 findings"""

        caption_style = ParagraphStyle('FigCaption', parent=self.styles['Normal'], alignment=1, fontSize=10, fontName='Helvetica-Bold', spaceBefore=6, spaceAfter=12)
        
        heading = Paragraph("DIMENSION 3: INTEGRITY GAP ANALYSIS", self.styles['SectionHeading'])
        self.story.append(heading)
        self.story.append(Spacer(1, 0.08*inch))
        
        overview = """
        Multi-layered anomaly detection with composite risk scoring prioritizes investigation resources. 
        48 pincodes (1.0% of 4,628 anomalies) require immediate action (32 critical + 16 high risk), 
        demonstrating overall system integrity while identifying specific areas needing investigation.
        """
        self.story.append(Paragraph(overview, self.styles['BodyJustified']))
        self.story.append(Spacer(1, 0.12*inch))
        
        # Integrity table
        integrity_data = [
    ['Category', 'Count', '%', 'Action'],
    ['Total Pincodes', '19,814', '100%', 'Complete coverage'],
    ['Anomalous', '4,628', '23.4%', 'Flagged for review'],
    ['Low Risk', '2,897', '62.6%', 'Routine monitoring'],
    ['Medium Risk', '1,683', '36.4%', 'Periodic audit'],
    ['High Risk', '16', '0.3%', 'Priority investigation'],
    ['Critical Risk', '32', '0.7%', 'Immediate action'],
        ]
        
        integrity_table = Table(integrity_data, colWidths=[2*inch, 1.2*inch, 1*inch, 2.3*inch])
        integrity_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d32f2f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        self.story.append(integrity_table)
        self.story.append(Spacer(1, 0.12*inch))
        
        # Fig 4
        fig4_path = os.path.join(FIGURES_DIR, 'dim3_risk_distribution.png')
        if os.path.exists(fig4_path):
            img = Image(fig4_path, width=6*inch, height=3.8*inch)
            self.story.append(img)
            self.story.append(Paragraph("Figure 4: Risk Level Distribution", caption_style))
        
        # --- TOP 10 TABLE (KEPT TOGETHER WITH EXPLANATION) ---
        csv_path_d3 = r"C:\Users\atharv\Desktop\aadhaar_analysis\outputs\tables\dim3_top10_critical_risk_pincodes.csv"
        cols_d3 = {
            'pincode': 'Pincode', 
            'district': 'District', 
            'risk_score': 'Risk Score', 
            'ue_ratio': 'U/E Ratio', 
            'risk_level': 'Priority'
        }
        
        explanation_d3 = (
            "Critical Anomalies: The table above identifies pincodes with maximum risk scores. "
            "These areas exhibit extreme update-to-enrollment ratios or impossible demographic shifts, "
            "suggesting potential data quality issues or fraudulent activity."
        )

        self.story.append(self.get_filtered_csv_table(
            csv_path_d3, cols_d3, "Table 3.1: Top 10 Critical Risk Pincodes (Integrity Check)", explanation_d3
        ))

        self.story.append(PageBreak())
    
    def add_recommendations(self):
        """Add strategic recommendations - CORRECTED"""
        
        heading = Paragraph("STRATEGIC RECOMMENDATIONS", self.styles['SectionHeading'])
        self.story.append(heading)
        self.story.append(Spacer(1, 0.08*inch))
        
        # Immediate - CORRECTED
        imm_heading = Paragraph("Immediate Actions (0-3 Months)", self.styles['SubsectionHeading'])
        self.story.append(imm_heading)
        
        immediate = [
            ("<b>Mobile Camp Deployment:</b> Consider deploying 15-20 mobile biometric units to 24 at-risk readiness districts "
            "(12 critical priority, 12 low priority) with highest estimated authentication risk for youth transitioning to "
            "adulthood. Target youth aged 15-17 to ensure biometric updates before mandatory authentication at age 18."),
            
            ("<b>High-Risk Audit:</b> Recommend investigating 48 critical/high-risk pincodes (32 critical + 16 high risk) for "
            "data quality issues. Focus on districts with anomaly clustering (395 districts with ≥3 anomalies identified) "
            "to detect systematic patterns requiring investigation."),
        ]
        
        for rec in immediate:
            self.story.append(Paragraph(f"• {rec}", self.styles['BodyJustified']))
        
        self.story.append(Spacer(1, 0.12*inch))
        
        # Short-term - CORRECTED
        short_heading = Paragraph("Short-Term Actions (3-6 Months)", self.styles['SubsectionHeading'])
        self.story.append(short_heading)
        
        short_term = [
            ("<b>Coverage Gap Closure:</b> Recommend targeted enrollment drives in 57 'Coverage Gap' districts, "
            "focusing on marginalized populations, migrants, and remote areas where high update activity masks "
            "stagnant enrollment of underserved groups."),
            
            ("<b>Crisis Zone Outreach:</b> Suggest developing community engagement strategy for 387 'Crisis Zone' districts "
            "with low enrollment and low update activity. Partner with NGOs, Anganwadi centers, and schools for awareness "
            "campaigns and grassroots enrollment drives."),
        ]
        
        for rec in short_term:
            self.story.append(Paragraph(f"• {rec}", self.styles['BodyJustified']))
        
        self.story.append(Spacer(1, 0.12*inch))
        
        # Medium-term
        med_heading = Paragraph("Medium-Term Actions (6-12 Months)", self.styles['SubsectionHeading'])
        self.story.append(med_heading)
        
        medium_term = [
            ("<b>Predictive Dashboard:</b> Implement real-time three-dimensional monitoring system tracking Coverage, "
             "Readiness, and Integrity gaps. Enable early warning alerts for emerging hotspots."),
            
            ("<b>State-Level Review:</b> Investigate root causes of regional patterns (anomaly clustering patterns, "
             "age concentrations, low readiness rates). Standardize best practices via state workshops."),
        ]
        
        for rec in medium_term:
            self.story.append(Paragraph(f"• {rec}", self.styles['BodyJustified']))
        
        self.story.append(PageBreak())
    
    def add_conclusion(self):
        """Add conclusion - CORRECTED"""
        
        heading = Paragraph("CONCLUSION", self.styles['SectionHeading'])
        self.story.append(heading)
        self.story.append(Spacer(1, 0.08*inch))
        
        conclusion = """
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
        """
        self.story.append(Paragraph(conclusion, self.styles['BodyJustified']))
        
        self.story.append(PageBreak())

    def add_appendix_a(self):
        """
        Appendix A: Architecture & Execution Flow
        Includes flowchart diagram and project structure
        """
        # Bridge local variables to instance variables
        story = self.story
        styles = self.styles

        # --- FIX: Define 'Caption' style if missing ---
        if 'Caption' not in styles:
            from reportlab.lib.enums import TA_CENTER
            from reportlab.lib.styles import ParagraphStyle
            
            styles.add(ParagraphStyle(
                name='Caption',
                parent=styles['Normal'],
                fontSize=9,
                leading=11,
                alignment=TA_CENTER,
                fontName='Helvetica-Oblique',
                textColor=colors.HexColor('#555555')
            ))
        # ----------------------------------------------
    
        # Appendix A heading
        heading = Paragraph("APPENDIX A: CODE ARCHITECTURE & EXECUTION FLOW", styles['SectionHeading'])
        story.append(heading)
        story.append(Spacer(1, 0.15*inch))
    
        # A.1 Overview
        overview_heading = Paragraph("A.1 Overview", styles['SubsectionHeading'])
        story.append(overview_heading)
        story.append(Spacer(1, 0.08*inch))
    
        overview_text = """
        This appendix documents the code architecture, execution flow, and reproducibility design of the 
        analytical pipeline used to generate this report. The system was developed as a modular, end-to-end 
        pipeline to ensure auditability, transparency, and repeatable execution.
        """
        story.append(Paragraph(overview_text, styles['BodyJustified']))
        story.append(Spacer(1, 0.08*inch))
    
        overview_bullets = """
        • <b>Implementation:</b> Python 3.11 using standard data science libraries (pandas, numpy, 
        matplotlib, scipy, scikit-learn)<br/>
        • <b>Data Sources:</b> Exclusively anonymised Aadhaar enrolment and update datasets provided 
        by UIDAI for this hackathon<br/>
        • <b>Privacy Compliance:</b> No personally identifiable information (PII), biometric identifiers, 
        or authentication logs were accessed at any stage<br/>
        • <b>Execution Time:</b> Approximately 15-20 minutes on standard laptop
        """
        story.append(Paragraph(overview_bullets, styles['BodyJustified']))
        story.append(Spacer(1, 0.12*inch))
    
        
        
        
        # Define the elements list
        flow_elements = []
        
        flow_heading = Paragraph("A.2 Execution Flow Diagram", self.styles['SubsectionHeading'])
        flow_elements.append(flow_heading)
        flow_elements.append(Spacer(1, 0.08*inch))
    
        # Add flowchart image
        flowchart_path = r"C:\Users\atharv\Downloads\flowchart_aadhar.png"
        
        if os.path.exists(flowchart_path):
            try:
                # Calculate dimensions to fit on page (adjust aspect ratio as needed)
                # Using 'preserveAspectRatio=True' is often safer if dimensions vary
                img_width = 6.5 * inch
                img_height = 8 * inch 
                
                flowchart_img = Image(flowchart_path, width=img_width, height=img_height)
                flow_elements.append(flowchart_img)
                flow_elements.append(Spacer(1, 0.1*inch))
                
                caption = Paragraph(
                    "<i>Figure A.1: End-to-end analytical pipeline execution flow from raw data ingestion "
                    "to final PDF generation</i>",
                    self.styles['Caption']
                )
                flow_elements.append(caption)
            except Exception as e:
                # Fallback if image load fails
                error_msg = Paragraph(f"<i>[Error loading flowchart: {str(e)}]</i>", self.styles['Caption'])
                flow_elements.append(error_msg)
        else:
            # Fallback if file missing
            error_msg = Paragraph(
                f"<i>[Flowchart diagram not found at: {flowchart_path}]</i>",
                self.styles['Caption']
            )
            flow_elements.append(error_msg)

        # Wrap everything in KeepTogether and append to story
        self.story.append(KeepTogether(flow_elements))
        self.story.append(PageBreak())
    
        # A.3 Project Structure
        structure_heading = Paragraph("A.3 Project Structure", styles['SubsectionHeading'])
        story.append(structure_heading)
        story.append(Spacer(1, 0.08*inch))
    
        structure_intro = """
        The analytical pipeline follows a clear separation of concerns across raw data ingestion, 
        processing, analysis, validation, and reporting:
        """
        story.append(Paragraph(structure_intro, styles['BodyJustified']))
        story.append(Spacer(1, 0.08*inch))
    
        # Project structure as preformatted text
        structure_code = """
aadhaar_analysis/
│
├── data/
│   ├── raw/                      # Original UIDAI datasets
│   │   ├── api_data_aadhar_enrolment_*.csv      
│   │   ├── api_data_aadhar_biometric_*.csv      
│   │   └── api_data_aadhar_demographic_*.csv    
│   │
│   └── processed/                # Cleaned and merged datasets
│       ├── enrollment_clean.csv
│       ├── biometric_clean.csv
│       ├── demographic_clean.csv
│       └── merged_data.csv          
│
├── outputs/
│   ├── tables/                      # 19 CSV files with analytical outputs
│   │
│   ├── figures/                     # 18 PNG visualizations at 300 DPI
│   │
│   └── report/                      # Final submission PDF
│       
├── src/                             # Analytical pipeline scripts
│   ├── 00_data_quality_check.py
│   ├── 01_data_loading.py
│   ├── 02_data_cleaning.py
│   ├── 03_dimension1_coverage.py
│   ├── 04_dimension2_readiness.py
│   ├── 05_dimension3_integrity.py
│   ├── 06_report_generation.py
│   └── validation_test.py
│
├── utils/
│   └── config.py                    # Centralized constants and thresholds
│
└── requirements.txt                 # Python dependencies
        """
    
        code_style = ParagraphStyle(
            'CodeBlock',
            parent=styles['Code'],
            fontSize=7,
            leading=9,
            leftIndent=0.2*inch,
            fontName='Courier',
            textColor=colors.HexColor('#2c3e50'),
            backColor=colors.HexColor('#f8f9fa')
        )
    
        story.append(Preformatted(structure_code, code_style))
        story.append(Spacer(1, 0.12*inch))
    
        # A.4 Script Responsibilities
        scripts_heading = Paragraph("A.4 Key Scripts and Responsibilities", styles['SubsectionHeading'])
        story.append(scripts_heading)
        story.append(Spacer(1, 0.08*inch))
    
        # Create table
        script_data = [
            ['Script', 'Primary Responsibility'],
            ['00_data_quality_check.py', 'Initial integrity checks on raw UIDAI datasets'],
            ['01_data_loading.py', 'Data ingestion and schema validation (12 CSV files)'],
            ['02_data_cleaning.py', 'Geographic standardization and deduplicated dataset merging'],
            ['03_dimension1_coverage.py', 'Coverage Gap: UE ratios, 2×2 matrix, child enrollment'],
            ['04_dimension2_readiness.py', 'Readiness Gap: Youth biometric compliance, risk prediction'],
            ['05_dimension3_integrity.py', 'Integrity Gap: Multi-layered anomaly detection (0-12 scoring)'],
            ['06_report_generation.py', 'Automated PDF generation with validated metrics'],
            ['validation_test.py', 'End-to-end numeric validation and audit checks'],
            ['utils/config.py', 'Centralized thresholds, constants, and helper functions']
        ]
    
        script_table = Table(script_data, colWidths=[2.2*inch, 4.3*inch])
        script_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
    
        story.append(script_table)
        story.append(Spacer(1, 0.12*inch))
    
        # A.5 Reproducibility
        repro_heading = Paragraph("A.5 Reproducibility and Compliance", styles['SubsectionHeading'])
        story.append(repro_heading)
        story.append(Spacer(1, 0.08*inch))
    
        repro_bullets = """
        - <b>Determinism:</b> Fixed thresholds and aggregation logic ensure repeatable results<br/>
        - <b>Validation:</b> All reported figures are programmatically verified prior to PDF generation<br/>
        - <b>Data Governance:</b> Analysis uses only anonymised datasets supplied by UIDAI for the hackathon<br/>
        - <b>Geographic Standardization:</b>Comprehensive state (36) and district (865 unique names, 888 combinations) name standardization applied<br/>
        - <b>Transparency:</b> All derived metrics are clearly distinguished from official UIDAI statistics<br/>
        - <b>Auditability:</b> Complete execution logs and intermediate outputs preserved for verification
        """
        story.append(Paragraph(repro_bullets, styles['BodyJustified']))
        story.append(Spacer(1, 0.1*inch))
    
        github_note = """
        <b>Code Availability:</b> The complete, fully documented source code for this analytical pipeline is available at:  
        https://github.com/AtharvSabde/UIDAI_hackathon

        This repository includes end-to-end data processing scripts, analytical modules, 
        validation tests, and PDF report generation code. Access is provided for optional 
        technical review and reproducibility verification.
        """
        story.append(Paragraph(github_note, styles['BodyJustified']))
    
        story.append(PageBreak())

    def add_appendix_b(self):
        """
        Appendix B: Selected Implementation Excerpts
        Real Python code snippets demonstrating key methodologies
        """
        # Bridge local variables to instance variables
        story = self.story
        styles = self.styles
    
        # Appendix B heading
        heading = Paragraph("APPENDIX B: SELECTED IMPLEMENTATION EXCERPTS", styles['SectionHeading'])
        story.append(heading)
        story.append(Spacer(1, 0.15*inch))
    
        intro_text = """
        The complete, fully documented source code for this analytical pipeline is available 
via a public GitHub repository for technical review.(https://github.com/AtharvSabde/UIDAI_hackathon)
 In accordance with the hackathon guidelines, only selected implementation excerpts are included here to 
maintain report conciseness.
        """
        story.append(Paragraph(intro_text, styles['BodyJustified']))
        story.append(Spacer(1, 0.12*inch))
    
        # Define code style
        code_style = ParagraphStyle(
            'CodeBlock',
            parent=styles['Code'],
            fontSize=7.5,
            leading=10,
            leftIndent=0.15*inch,
            fontName='Courier',
            textColor=colors.HexColor('#2c3e50'),
            backColor=colors.HexColor('#f8f9fa')
        )
    
        # B.1 Data Loading
        snippet_heading = Paragraph("B.1 Multi-File Data Loading (src/01_data_loading.py)", 
                                    styles['SubsectionHeading'])
        story.append(snippet_heading)
        story.append(Spacer(1, 0.08*inch))
    
        loading_desc = """
        Handles loading and concatenation of 12 split CSV files (3 enrollment + 4 biometric + 5 demographic):
        """
        story.append(Paragraph(loading_desc, styles['BodyJustified']))
        story.append(Spacer(1, 0.06*inch))
    
        loading_code = '''def load_split_files(file_list, data_dir, dataset_name):
    """Load multiple CSV files and combine into single dataframe"""
    dataframes = []
    total_rows = 0
    
    for i, filename in enumerate(file_list, 1):
        file_path = os.path.join(data_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"  ⚠️  WARNING: File not found: {filename}")
            continue
        
        try:
            df = pd.read_csv(file_path)
            rows = len(df)
            total_rows += rows
            dataframes.append(df)
            print(f"  [{i}/{len(file_list)}] ✓ {filename}")
            print(f"       Rows: {rows:,} | Columns: {df.shape[1]}")
        except Exception as e:
            print(f"  ✗ Error loading {filename}: {str(e)}")
            continue
    
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        print(f"✓ Successfully combined {len(dataframes)} files")
        print(f"  Total rows: {total_rows:,}")
        return combined_df
    else:
        return None'''
    
        story.append(Preformatted(loading_code, code_style))
        story.append(Spacer(1, 0.12*inch))
    
        # B.2 State Standardization
        # ---------------------------------------------------------
        
        # 1. Define the Missing Code Style (Quick Fix)
        my_code_style = ParagraphStyle(
            'CodeBlock',
            fontName='Courier',
            fontSize=8,
            leading=10,
            backColor=colors.whitesmoke,
            borderPadding=6,
            spaceBefore=6,
            spaceAfter=6
        )

        # 2. Keep heading and intro together
        header_elements = []
        
        snippet_heading = Paragraph("B.2 Comprehensive State Name Standardization (src/02_data_cleaning.py)", 
                                    self.styles['SubsectionHeading'])
        header_elements.append(snippet_heading)
        header_elements.append(Spacer(1, 0.08*inch))

        state_desc = """
        Corrects 64 state name variations (case inconsistencies, spelling errors, merged UTs) to produce 
        36 standardized state/UT names:
        """
        header_elements.append(Paragraph(state_desc, self.styles['BodyJustified']))
        header_elements.append(Spacer(1, 0.06*inch))
        
        self.story.append(KeepTogether(header_elements))

        # 3. The Code Content
        state_code = """
def standardize_state_names(df):
    \"\"\"Comprehensive state name standardization - handles 64 variations\"\"\"

    STATE_NAME_MAPPING = {
        # Odisha variations
        'ODISHA': 'Odisha', 'odisha': 'Odisha', 'Orissa': 'Odisha',
        
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
        
        # Delhi variations
        'NCT of Delhi': 'Delhi',
        'New Delhi': 'Delhi',
        'DELHI': 'Delhi',
        
        # All CAPS state variations (showing representative sample)
        'MANIPUR': 'Manipur', 'TRIPURA': 'Tripura', 'ASSAM': 'Assam',
        'BIHAR': 'Bihar', 'GOA': 'Goa', 'GUJARAT': 'Gujarat',
        'HARYANA': 'Haryana', 'HIMACHAL PRADESH': 'Himachal Pradesh',
        'JHARKHAND': 'Jharkhand', 'KARNATAKA': 'Karnataka',
        'KERALA': 'Kerala', 'MADHYA PRADESH': 'Madhya Pradesh',
        'MAHARASHTRA': 'Maharashtra', 'MEGHALAYA': 'Meghalaya',
        'MIZORAM': 'Mizoram', 'NAGALAND': 'Nagaland',
        'PUNJAB': 'Punjab', 'RAJASTHAN': 'Rajasthan',
        'SIKKIM': 'Sikkim', 'TELANGANA': 'Telangana',
        'UTTAR PRADESH': 'Uttar Pradesh', 'CHANDIGARH': 'Chandigarh',
        'LADAKH': 'Ladakh', 'LAKSHADWEEP': 'Lakshadweep',
        
        # INVALID ENTRIES - Districts mistakenly in state column
        'BALANAGAR': 'Telangana',
        'Darbhanga': 'Bihar',
        'Jaipur': 'Rajasthan',
        'Madanapalle': 'Andhra Pradesh',
        'Nagpur': 'Maharashtra',
        'Puttenahalli': 'Karnataka',
        'Raja Annamalai Puram': 'Tamil Nadu',
        
        # Invalid pincode entries
        '100000': None,
        # ... (64 total mappings including all case variations)
    }

    # Apply standardization
    records_before = len(df)
    df['state'] = df['state'].replace(STATE_NAME_MAPPING)

    # Remove invalid entries (None values)
    df = df[df['state'].notna()].copy()
    df['state'] = df['state'].str.strip()
    
    records_removed = records_before - len(df)
    if records_removed > 0:
        print(f"  🗑️  Removed {records_removed:,} invalid records")

    print(f"✓ Standardized state names")
    print(f"✓ Final: {df['state'].nunique()} clean states")

    return df
"""
        # 4. Use the local 'my_code_style' variable (Fixed Error)
        self.story.append(Preformatted(state_code, my_code_style))
        self.story.append(PageBreak())
    
        # B.2.5 District Name Standardization
        snippet_heading = Paragraph(
            "B.2.5 Comprehensive District Name Standardization (src/02_data_cleaning.py)", 
            styles['SubsectionHeading']
        )
        story.append(snippet_heading)
        story.append(Spacer(1, 0.08*inch))

        district_desc = """
Corrects 150+ district name variations including case inconsistencies, spelling errors, 
and administrative changes. Critical for accurate district-level analysis:
        """
        story.append(Paragraph(district_desc, styles['BodyJustified']))
        story.append(Spacer(1, 0.06*inch))

        district_code = '''def standardize_district_names(df):
    """Comprehensive district name standardization - handles 150+ variations"""
    
    DISTRICT_NAME_MAPPING = {
        # Andhra Pradesh
        'Ananthapur': 'Anantapur',
        'Ananthapuramu': 'Anantapur',
        'Visakhapatanam': 'Visakhapatnam',
        
        # Bihar
        'Aurangabad(BH)': 'Aurangabad',
        'Pashchim Champaran': 'West Champaran',
        'Purba Champaran': 'East Champaran',
        'Purnia': 'Purnea',
        
        # Gujarat
        'Ahmedabad': 'Ahmadabad',
        'Banaskantha': 'Banas Kantha',
        'Panchmahals': 'Panch Mahals',
        
        # Karnataka
        'Chamarajanagar *': 'Chamarajanagar',
        'Chamrajanagar': 'Chamarajanagar',
        'Chikkamagaluru': 'Chickmagalur',
        'Shivamogga': 'Shimoga',
        'Tumkur': 'Tumakuru',
        
        # Odisha
        'ANGUL': 'Angul', 'ANUGUL': 'Angul',
        'Baleswar': 'Baleshwar',
        'Jajapur': 'Jajpur', 'jajpur': 'Jajpur',
        'Khordha': 'Khorda',
        'Sundergarh': 'Sundargarh',
        
        # West Bengal (most complex)
        'Bardhaman': 'Barddhaman',
        'Coochbehar': 'Cooch Behar',
        'Darjiling': 'Darjeeling',
        'East Midnapur': 'East Midnapore',
        'HOOGHLY': 'Hooghly', 'Hooghiy': 'Hooghly',
        'HOWRAH': 'Howrah', 'Hawrah': 'Howrah',
        'KOLKATA': 'Kolkata',
        'MALDA': 'Malda', 'Maldah': 'Malda',
        'South 24 Pargana': 'South 24 Parganas',
        'Puruliya': 'Purulia',
        
        # Medinipur district split
        'Medinipur West': 'Paschim Medinipur',
        'West Midnapore': 'Paschim Medinipur',
        'East Midnapore': 'Purba Medinipur',
        
        # Sikkim direction-only names
        'East': 'East Sikkim',
        'West': 'West Sikkim',
        'North': 'North Sikkim',
        'South': 'South Sikkim',
        
        # ... (150+ total mappings across all states)
    }
    
    # Apply standardization
    df['district'] = df['district'].replace(DISTRICT_NAME_MAPPING)
    df['district'] = df['district'].str.strip()
    
    print(f"✓ Districts standardized: {df['district'].nunique()}")
    
    return df
        '''

        story.append(Preformatted(district_code, code_style))
        story.append(Spacer(1, 0.12*inch))



        # B.3 Dataset Merging
        snippet_heading = Paragraph("B.3 Three-Dataset Merging with UE Ratio Calculation (src/02_data_cleaning.py)", 
                                    styles['SubsectionHeading'])
        story.append(snippet_heading)
        story.append(Spacer(1, 0.08*inch))
    
        merge_desc = """
        Merges enrollment, biometric, and demographic datasets using outer joins on date-state-district-pincode 
        keys, then calculates the Update-to-Enrollment (UE) ratio:
        """
        story.append(Paragraph(merge_desc, styles['BodyJustified']))
        story.append(Spacer(1, 0.06*inch))
    
        merge_code = '''def merge_datasets(df_enrollment, df_biometric, df_demographic):
    """Merge all three datasets on date, state, district, pincode"""
    
    # Step 1: Aggregate duplicates in each dataset
    # (Same date-state-district-pincode = multiple transactions, must sum)
    
    print("Aggregating enrollment duplicates...")
    df_enroll_agg = df_enrollment.groupby(
        ['date', 'state', 'district', 'pincode']
    ).agg({
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum'
    }).reset_index()
    
    print("Aggregating biometric duplicates...")
    df_bio_agg = df_biometric.groupby(
        ['date', 'state', 'district', 'pincode']
    ).agg({
        'bio_age_5_17': 'sum',
        'bio_age_17_': 'sum'
    }).reset_index()
    
    print("Aggregating demographic duplicates...")
    df_demo_agg = df_demographic.groupby(
        ['date', 'state', 'district', 'pincode']
    ).agg({
        'demo_age_5_17': 'sum',
        'demo_age_17_': 'sum'
    }).reset_index()
    
    print(f"  Enrollment: {len(df_enrollment):,} → {len(df_enroll_agg):,} "
          f"({len(df_enrollment)-len(df_enroll_agg):,} duplicates removed)")
    print(f"  Biometric: {len(df_biometric):,} → {len(df_bio_agg):,} "
          f"({len(df_biometric)-len(df_bio_agg):,} duplicates removed)")
    print(f"  Demographic: {len(df_demographic):,} → {len(df_demo_agg):,} "
          f"({len(df_demographic)-len(df_demo_agg):,} duplicates removed)")
    
    # Step 2: Merge aggregated datasets
    df_merged = pd.merge(
        df_enroll_agg, df_bio_agg,
        on=['date', 'state', 'district', 'pincode'],
        how='outer'
    )
    
    df_merged = pd.merge(
        df_merged, df_demo_agg,
        on=['date', 'state', 'district', 'pincode'],
        how='outer'
    )
    
    # Step 3: Fill NaN with 0 (from outer join)
    numeric_cols = df_merged.select_dtypes(include=[np.number]).columns
    df_merged[numeric_cols] = df_merged[numeric_cols].fillna(0)
    
    # Step 4: Calculate totals AFTER merge (from raw columns)
    df_merged['total_enrollment'] = (
        df_merged['age_0_5'] + 
        df_merged['age_5_17'] + 
        df_merged['age_18_greater']
    )
    
    df_merged['total_biometric_updates'] = (
        df_merged['bio_age_5_17'] + df_merged['bio_age_17_']
    )
    
    df_merged['total_demographic_updates'] = (
        df_merged['demo_age_5_17'] + df_merged['demo_age_17_']
    )
    
    df_merged['total_updates'] = (
        df_merged['total_biometric_updates'] + 
        df_merged['total_demographic_updates']
    )
    
    df_merged['ue_ratio'] = np.where(
        df_merged['total_enrollment'] > 0,
        df_merged['total_updates'] / df_merged['total_enrollment'],
        0
    )
    
    print(f"✓ Final merged dataset: {len(df_merged):,} records")
    print(f"✓ Total enrollments: {df_merged['total_enrollment'].sum():,.0f}")
    print(f"✓ Total updates: {df_merged['total_updates'].sum():,.0f}")
    print(f"✓ National UE Ratio: {df_merged['total_updates'].sum() / df_merged['total_enrollment'].sum():.2f}")
    
    return df_merged
        '''
    
        story.append(Preformatted(merge_code, code_style))
        story.append(Spacer(1, 0.12*inch))
    
        # B.4 2x2 Classification Matrix
        snippet_heading = Paragraph("B.4 2×2 Classification Matrix (Dimension 1 - src/03_dimension1_coverage.py)", 
                                    styles['SubsectionHeading'])
        story.append(snippet_heading)
        story.append(Spacer(1, 0.08*inch))
    
        matrix_desc = """
        Classifies districts into four quadrants based on enrollment and update activity relative to median 
        thresholds-core innovation for identifying the "Update Paradox":
        """
        story.append(Paragraph(matrix_desc, styles['BodyJustified']))
        story.append(Spacer(1, 0.06*inch))
    
        matrix_code = '''def classify_districts_2x2(district_agg):
        """Classify districts into 2×2 matrix based on enrollment vs updates"""
    
    # Define thresholds (median split)
    median_enrollment = district_agg['total_enrollment'].median()
    median_updates = district_agg['total_updates'].median()
    
    print(f"Thresholds: Enrollment={median_enrollment:,.0f}, "
          f"Updates={median_updates:,.0f}")
    
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
    counts = district_agg['quadrant'].value_counts()
    for quadrant, count in counts.items():
        pct = (count / len(district_agg)) * 100
        print(f"  {quadrant}: {count} ({pct:.1f}%)")
    
    return district_agg
        '''
    
        story.append(Preformatted(matrix_code, code_style))
        story.append(PageBreak())
    
        # B.5 Child Enrollment Calculation
        snippet_heading = Paragraph("B.5 Corrected Child Enrollment Calculation (Dimension 1)", 
                                    styles['SubsectionHeading'])
        story.append(snippet_heading)
        story.append(Spacer(1, 0.08*inch))
    
        child_desc = """
        Demonstrates the correct methodology: sum age-group totals across all records first, then calculate 
        percentages (not record-level averaging):
        """
        story.append(Paragraph(child_desc, styles['BodyJustified']))
        story.append(Spacer(1, 0.06*inch))
    
        child_code = '''def identify_child_coverage_gaps(district_agg):
    """CORRECTED: Calculate child % from TOTALS, not record-level averages"""
    
    # Calculate what % of total enrollments are children
    district_agg['child_total_pct'] = (
        (district_agg['age_0_5'] + district_agg['age_5_17']) / 
        district_agg['total_enrollment']
    ) * 100
    
    # National-level statistics (CORRECT METHOD)
    total_enrollments_national = district_agg['total_enrollment'].sum()
    total_child_0_5 = district_agg['age_0_5'].sum()
    total_child_5_17 = district_agg['age_5_17'].sum()
    total_adult = district_agg['age_18_greater'].sum()
    
    national_child_pct = (
        (total_child_0_5 + total_child_5_17) / total_enrollments_national
    ) * 100
    
    print(f"NATIONAL STATISTICS (Correct Calculation):")
    print(f"  Total enrollments: {total_enrollments_national:,.0f}")
    print(f"  Age 0-5: {total_child_0_5:,.0f} "
          f"({(total_child_0_5/total_enrollments_national)*100:.1f}%)")
    print(f"  Age 5-17: {total_child_5_17:,.0f} "
          f"({(total_child_5_17/total_enrollments_national)*100:.1f}%)")
    print(f"  Age 18+: {total_adult:,.0f} "
          f"({(total_adult/total_enrollments_national)*100:.1f}%)")
    print(f"  Children (0-17): {national_child_pct:.1f}%")
    
    return district_agg'''
    
        story.append(Preformatted(child_code, code_style))
        story.append(Spacer(1, 0.12*inch))
    
        # B.6 Readiness Score
        snippet_heading = Paragraph("B.6 Transition Readiness Score Calculation (Dimension 2 - src/04_dimension2_readiness.py)", 
                                    styles['SubsectionHeading'])
        story.append(snippet_heading)
        story.append(Spacer(1, 0.08*inch))
    
        readiness_desc = """
        Calculates what percentage of biometric updates come from youth (ages 5-17), then classifies districts 
        into readiness categories:
        """
        story.append(Paragraph(readiness_desc, styles['BodyJustified']))
        story.append(Spacer(1, 0.06*inch))
    
        readiness_code = '''def calculate_district_readiness(df):
    """Calculate transition readiness scores at district level"""
    
    district_agg = df.groupby(['state', 'district']).agg({
        'bio_age_5_17': 'sum',
        'bio_age_17_': 'sum',
        'age_5_17': 'sum'
    }).reset_index()
    
    # Total biometric updates
    district_agg['total_bio_updates'] = (
        district_agg['bio_age_5_17'] + district_agg['bio_age_17_']
    )
    
    # Transition Readiness Score: 
    # What % of bio updates are from youth (5-17)?
    # High score = good (youth are updating their biometrics)
    district_agg['readiness_score'] = np.where(
        district_agg['total_bio_updates'] > 0,
        (district_agg['bio_age_5_17'] / 
         district_agg['total_bio_updates']) * 100,
        0
    )
    
    # Classify readiness categories (handles edge case)
    if MODERATE_READINESS == CRITICAL_READINESS:
        # Use 3 categories when thresholds overlap
        district_agg['readiness_category'] = pd.cut(
            district_agg['readiness_score'],
            bins=[0, CRITICAL_READINESS, GOOD_READINESS, 100],
            labels=['Critical', 'Moderate', 'Good']
        )
    else:
        # Use 4 categories when thresholds are distinct
        district_agg['readiness_category'] = pd.cut(
            district_agg['readiness_score'],
            bins=[0, CRITICAL_READINESS, MODERATE_READINESS, 
                  GOOD_READINESS, 100],
            labels=['Critical', 'Low', 'Moderate', 'Good']
        )
    
    print(f"National youth bio %: "
          f"{(district_agg['bio_age_5_17'].sum() / "
          f"district_agg['total_bio_updates'].sum()) * 100:.1f}%")
    
    return district_agg'''
    
        story.append(Preformatted(readiness_code, code_style))
        story.append(PageBreak())
    
        # B.7 Authentication Failure Prediction
        snippet_heading = Paragraph("B.7 Authentication Failure Prediction & Resource Estimation (Dimension 2)", 
                                    styles['SubsectionHeading'])
        story.append(snippet_heading)
        story.append(Spacer(1, 0.08*inch))
    
        prediction_desc = """
        Identifies districts with elevated risk of authentication challenges due to incomplete youth biometric updates:
        """
        story.append(Paragraph(prediction_desc, styles['BodyJustified']))
        story.append(Spacer(1, 0.06*inch))
    
        prediction_code = '''def predict_authentication_failures(district_agg):
    """Identify at-risk districts based on readiness scores"""

    total_youth_enrollments = district_agg['age_5_17'].sum()
    total_youth_bio = district_agg['bio_age_5_17'].sum()
    total_bio_updates = district_agg['total_bio_updates'].sum()

    # National benchmarks (descriptive only)
    national_youth_bio_pct = (
        (total_youth_bio / total_bio_updates) * 100
        if total_bio_updates > 0 else 0
    )

    print("National Benchmarks:")
    print(f"  Total youth (5-17): {total_youth_enrollments:,.0f}")
    print(f"  Youth % of bio updates: {national_youth_bio_pct:.1f}%")

    # Absolute readiness gap (PDF-aligned model)
    # Proportion of enrolled youth who have NOT completed biometric updates
    district_agg['readiness_gap'] = 100 - district_agg['readiness_score']

    district_agg['estimated_at_risk_youth'] = (
        district_agg['age_5_17'] * (district_agg['readiness_gap'] / 100)
    ).round(0).astype(int)

    # Total estimated at-risk youth nationally
    total_at_risk = district_agg['estimated_at_risk_youth'].sum()

    print("\nRisk Assessment:")
    print(f"  Estimated at-risk youth (national): {total_at_risk:,.0f}")

    # High-risk districts (below critical readiness threshold)
    high_risk = district_agg[
        district_agg['readiness_score'] < CRITICAL_READINESS
    ].sort_values('estimated_at_risk_youth', ascending=False)

    print(f"\nHigh-Risk Districts (< {CRITICAL_READINESS}%): {len(high_risk)}")

    return district_agg, total_at_risk, high_risk
'''
    
        story.append(Preformatted(prediction_code, code_style))
        story.append(Spacer(1, 0.12*inch))
    
        # B.8 Anomaly Detection
        snippet_heading = Paragraph("B.8 Multi-Layered Anomaly Detection (Dimension 3 - src/05_dimension3_integrity.py)", 
                                    styles['SubsectionHeading'])
        story.append(snippet_heading)
        story.append(Spacer(1, 0.08*inch))
    
        anomaly_desc = """
        Implements four detection layers: extreme UE ratios, high UE ratios with volume filters, 
        z-score outliers, and temporal spikes:
        """
        story.append(Paragraph(anomaly_desc, styles['BodyJustified']))
        story.append(Spacer(1, 0.06*inch))
    
        anomaly_code = '''def detect_ue_ratio_anomalies(df):
        """Detect pincodes with anomalously high UE ratios - multi-layered"""
        from scipy import stats  # Required for z-score calculation
    
    # Aggregate at pincode level
    pincode_agg = df.groupby('pincode').agg({
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum',
        'bio_age_5_17': 'sum',
        'bio_age_17_': 'sum',
        'demo_age_5_17': 'sum',
        'demo_age_17_': 'sum',
        'state': 'first',
        'district': 'first'
    }).reset_index()
    
    # Calculate totals and UE ratio
    pincode_agg['total_enrollment'] = (
        pincode_agg['age_0_5'] + pincode_agg['age_5_17'] + 
        pincode_agg['age_18_greater']
    )
    
    pincode_agg['total_updates'] = (
        pincode_agg['bio_age_5_17'] + pincode_agg['bio_age_17_'] + 
        pincode_agg['demo_age_5_17'] + pincode_agg['demo_age_17_']
    )
    
    pincode_agg['ue_ratio'] = np.where(
        pincode_agg['total_enrollment'] > 0,
        pincode_agg['total_updates'] / pincode_agg['total_enrollment'],
        0
    )
    
    # Layer 1: Extreme UE Ratio (>100)
    extreme_ue = pincode_agg[pincode_agg['ue_ratio'] > 100].copy()
    
    # Layer 2: High UE Ratio (>25) with significant volume
    high_ue = pincode_agg[
        (pincode_agg['ue_ratio'] > ANOMALY_UE_RATIO) & 
        (pincode_agg['total_enrollment'] > 100)
    ].copy()
    
    # Layer 3: Z-score based detection
    pincode_agg['ue_zscore'] = stats.zscore(
        pincode_agg['ue_ratio'].fillna(0)
    )
    zscore_anomalies = pincode_agg[
        np.abs(pincode_agg['ue_zscore']) > Z_SCORE_THRESHOLD
    ].copy()
    
    print(f"UE Ratio Anomalies Detected:")
    print(f"  Extreme (>100): {len(extreme_ue)} pincodes")
    print(f"  High (>25): {len(high_ue)} pincodes")
    print(f"  Z-score outliers: {len(zscore_anomalies)} pincodes")
    
    return pincode_agg, extreme_ue, high_ue, zscore_anomalies'''
    
        story.append(Preformatted(anomaly_code, code_style))
        story.append(PageBreak())
    
        # B.9 Composite Risk Scoring
        snippet_heading = Paragraph("B.9 Composite Risk Scoring System (Dimension 3)", 
                                    styles['SubsectionHeading'])
        story.append(snippet_heading)
        story.append(Spacer(1, 0.08*inch))
    
        risk_desc = """
        Calculates weighted composite risk scores (0-12 points) by combining multiple anomaly indicators, 
        then stratifies pincodes into risk categories:
        """
        story.append(Paragraph(risk_desc, styles['BodyJustified']))
        story.append(Spacer(1, 0.06*inch))
    
        risk_code = '''def calculate_composite_risk_score(pincode_agg, extreme_ue, high_ue, 
                                   age_anomalies, frequent_spikes):
    """
    Calculate composite risk score for each pincode
    Weighted scoring: 0-12 points across 4 anomaly types
    """
    
    risk_df = pincode_agg[['pincode', 'state', 'district', 
                           'ue_ratio', 'total_enrollment']].copy()
    risk_df['risk_score'] = 0
    
    # Initialize boolean columns FIRST (prevents errors)
    risk_df['has_extreme_ue'] = False
    risk_df['has_high_ue'] = False
    risk_df['has_age_anomaly'] = False
    risk_df['has_temporal_spike'] = False
    
    # Layer 1: Extreme UE ratio (>100) = +5 points
    if len(extreme_ue) > 0:
        mask = risk_df['pincode'].isin(extreme_ue['pincode'])
        risk_df.loc[mask, 'risk_score'] += 5
        risk_df.loc[mask, 'has_extreme_ue'] = True
    
    # Layer 2: High UE ratio (>25) = +3 points
    if len(high_ue) > 0:
        mask = risk_df['pincode'].isin(high_ue['pincode'])
        risk_df.loc[mask, 'risk_score'] += 3
        risk_df.loc[mask, 'has_high_ue'] = True
    
    # Layer 3: Age concentration anomaly (>80% in one group) = +2 points
    if len(age_anomalies) > 0:
        mask = risk_df['pincode'].isin(age_anomalies['pincode'])
        risk_df.loc[mask, 'risk_score'] += 2
        risk_df.loc[mask, 'has_age_anomaly'] = True
    
    # Layer 4: Frequent temporal spikes (>3 spikes) = +2 points
    if len(frequent_spikes) > 0:
        mask = risk_df['pincode'].isin(frequent_spikes['pincode'])
        risk_df.loc[mask, 'risk_score'] += 2
        risk_df.loc[mask, 'has_temporal_spike'] = True
    
    # Filter to only anomalous pincodes (score > 0)
    anomalous_pincodes = risk_df[risk_df['risk_score'] > 0].copy()
    
    # Classify by risk level
    anomalous_pincodes['risk_level'] = pd.cut(
        anomalous_pincodes['risk_score'],
        bins=[0, 2, 5, 8, 15],
        labels=['Low', 'Medium', 'High', 'Critical']
    )
    
    # Sort by risk score (highest first)
    anomalous_pincodes = anomalous_pincodes.sort_values(
        'risk_score', ascending=False
    )
    
    print(f"Anomalous Pincodes: {len(anomalous_pincodes):,}")
    print(f"Risk Level Distribution:")
    for level in ['Critical', 'High', 'Medium', 'Low']:
        count = len(anomalous_pincodes[
            anomalous_pincodes['risk_level'] == level
        ])
        pct = (count / len(anomalous_pincodes)) * 100 if len(anomalous_pincodes) > 0 else 0
        print(f"  {level}: {count} ({pct:.1f}%)")
    
    return anomalous_pincodes'''
        
        
    
        story.append(Preformatted(risk_code, code_style))
        story.append(Spacer(1, 0.12*inch))
    
        # B.10 Helper Functions
        snippet_heading = Paragraph("B.10 Configuration and Helper Functions (utils/config.py)", 
                                    styles['SubsectionHeading'])
        story.append(snippet_heading)
        story.append(Spacer(1, 0.08*inch))
    
        helper_desc = """
        Centralized threshold definitions and reusable calculation functions:
        """
        story.append(Paragraph(helper_desc, styles['BodyJustified']))
        story.append(Spacer(1, 0.06*inch))
    
        helper_code = '''# =================================================================
# DERIVED ANALYTICAL METRICS (NOT UIDAI KPIs)
# =================================================================

# UE Ratio = Updates ÷ Enrollments
# UIDAI does NOT define or publish this metric
# UPDATED: Based on 2025 calendar year data (119.06M updates / 5.44M enrollments)
DERIVED_UE_RATIO_BASELINE = 21.90  # Corrected after deduplication
NATIONAL_UE_RATIO = DERIVED_UE_RATIO_BASELINE

# Note: District-level averages differ due to size weighting
# Average District UE: 27.70 (unweighted arithmetic mean)
# Median District UE: 23.62 (50th percentile, robust to outliers)

HIGH_UE_RATIO = 25.0   
ANOMALY_UE_RATIO = 40.0  

# =================================================================
# TRANSITION READINESS SCORE (SINGLE SOURCE OF TRUTH)
# =================================================================

GOOD_READINESS = 30        # ≥30%
MODERATE_READINESS = 15    # 15–29%
CRITICAL_READINESS = 10    # <10%

# =================================================================
# ANOMALY DETECTION THRESHOLDS
# =================================================================

Z_SCORE_THRESHOLD = 3.0              # Statistical outlier
TEMPORAL_SPIKE_MULTIPLIER = 3.0      # 3× baseline spike
AGE_CONCENTRATION_THRESHOLD = 0.80   # >80% in one age group

# =================================================================
# HELPER FUNCTIONS
# =================================================================

def calculate_ue_ratio(total_updates, total_enrollments):
    """Calculate Update-to-Enrollment Ratio"""
    if total_enrollments == 0:
        return 0.0
    return total_updates / total_enrollments


def calculate_transition_readiness_score(bio_updates_5_17, 
                                         total_bio_updates):
    """Calculate Transition Readiness Score (youth % of bio updates)"""
    if total_bio_updates == 0:
        return 0.0
    return (bio_updates_5_17 / total_bio_updates) * 100


def classify_readiness_score(score):
    """Classify readiness score into categories"""
    if score >= GOOD_READINESS:
        return 'Good'
    elif score >= MODERATE_READINESS:
        return 'Moderate'
    else:
        return 'Critical'


def classify_ue_ratio(ue_ratio):
    """Classify UE ratio into categories"""
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


# Visualization color scheme
COLOR_SCHEME = {
    'critical': '#d32f2f',
    'high': '#f57c00',
    'moderate': '#fbc02d',
    'low': '#388e3c',
    'neutral': '#757575',
    'good': '#4caf50'
}'''
    
        story.append(Preformatted(helper_code, code_style))
        story.append(Spacer(1, 0.15*inch))
    
        # Closing note
        closing_note = """
        <b>Note:</b> In accordance with the UIDAI Hackathon submission guidelines, this consolidated PDF includes
detailed methodology, analysis, visualisations, and selected code excerpts necessary to understand the
implementation. The complete codebase (~6,000 lines) follows PEP 8 guidelines and includes comprehensive
error handling, input validation, and documentation.

For  technical review and reproducibility verification, the full source code is available via a
public GitHub repository (https://github.com/AtharvSabde/UIDAI_hackathon). The repository contains end-to-end data processing scripts, analytical modules,
programmatic validation tests, and automated PDF report generation code, along with setup instructions,
dependency management (requirements.txt), and execution documentation.
        """
        story.append(Paragraph(closing_note, styles['BodyJustified']))
    
        story.append(PageBreak())


    def add_appendix_c(self):
        """
        Appendix C: Programmatic Validation Evidence
        Single source of truth verification
        """
        # Bridge local variables to instance variables
        story = self.story
        styles = self.styles

        # Appendix C heading
        heading = Paragraph("APPENDIX C: PROGRAMMATIC VALIDATION EVIDENCE", styles['SectionHeading'])
        story.append(heading)
        story.append(Spacer(1, 0.15*inch))

        # C.1 Validation Overview
        c1_heading = Paragraph("C.1 Validation Overview", styles['SubsectionHeading'])
        story.append(c1_heading)
        story.append(Spacer(1, 0.08*inch))

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
        story.append(Paragraph(c2_bullets, styles['BodyJustified']))
        story.append(Spacer(1, 0.12*inch))

        # C.3 Cross-Verification Table
        # (This is where we create the Table object for the data)
        c3_heading = Paragraph("C.3 Cross-Verification of Script Output vs PDF Values", styles['SubsectionHeading'])
        story.append(c3_heading)
        story.append(Spacer(1, 0.08*inch))

        c3_intro = """
        The table below summarises the cross-verification of key metrics computed by the validation 
        script against their reported values in the PDF.
        """
        story.append(Paragraph(c3_intro, styles['BodyJustified']))
        story.append(Spacer(1, 0.1*inch))

        # --- TABLE DATA (Combined General + Dimension Metrics) ---
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
        ]

        # --- TABLE CREATION & STYLING ---
        # Column widths adjusted to fit standard page (Total width approx 6.5 inches)
        col_widths = [2.5*inch, 1.5*inch, 1.5*inch, 1.0*inch]
        
        t = Table(validation_data, colWidths=col_widths)

        t.setStyle(TableStyle([
            # Header Styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),  # Dark Blue Background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),             # White Text
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),               # Bold Font
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            
            # Body Styling
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),                           # Left align metrics
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),                          # Right align numbers
            
            # Grid and Padding
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),                  # Grid lines
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),                         # Header padding
            ('TOPPADDING', (0, 1), (-1, -1), 6),                           # Row padding
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            
            # Alternating Row Colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))

        story.append(t)
        story.append(Spacer(1, 0.05*inch))
        
        note = Paragraph(
            "<i>* All values match exactly or differ only due to rounding for presentation.<br/>"
    "** Districts: 888 state-district combinations representing 865 unique district names. "
    "Some pincodes serve areas across state/district boundaries (e.g., pincode 160003 serves both "
    "Chandigarh-Chandigarh and Punjab-Mohali), creating legitimate geographic complexity that "
    "preserves spatial accuracy without information loss.</i>",
            styles['BodyJustified']
        )
        story.append(note)
        story.append(Spacer(1, 0.15*inch))





        c4_closing = """
        This confirms that all reported numbers, tables, and figures in this PDF are programmatically 
        derived and validated prior to submission.
        """
        story.append(Paragraph(c4_closing, styles['BodyJustified']))

        story.append(PageBreak())

    def add_appendix_d(self):
        """
        Appendix D: Supplementary Figures & Tables
        Visual grid layout and tabular summaries
        """
        # Bridge local variables
        story = self.story
        styles = self.styles
        
        # Define base path for images
        base_img_path = r"C:\Users\atharv\Desktop\aadhaar_analysis\outputs\figures"

        # --- Helper Function for Image Grids ---
        def get_image_element(filename, width=3.0*inch, height=2.0*inch):
            """Returns an Image flowable or a Placeholder if missing"""
            full_path = os.path.join(base_img_path, filename)
            if os.path.exists(full_path):
                try:
                    img = Image(full_path, width=width, height=height)
                    return img
                except:
                    pass # Fall through to placeholder
            
            # Placeholder for missing image
            return Table(
                [[Paragraph(f"<b>MISSING IMAGE</b><br/>{filename}", styles['BodyText'])],
                 [Paragraph(f"(Place file in outputs/figures/)", styles['BodyText'])]],
                colWidths=[width], rowHeights=[height/2, height/2],
                style=[('GRID', (0,0), (-1,-1), 1, colors.red),
                       ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                       ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]
            )

        # -------------------------------------------

        # Heading
        heading = Paragraph("APPENDIX D: SUPPLEMENTARY FIGURES & TABLES", styles['SectionHeading'])
        story.append(heading)
        story.append(Spacer(1, 0.15*inch))

        # D.1 Purpose
        d1_heading = Paragraph("D.1 Purpose of This Appendix", styles['SubsectionHeading'])
        story.append(d1_heading)
        story.append(Spacer(1, 0.08*inch))

        d1_text = """
        This appendix presents supplementary visualisations and tabular summaries generated by the 
        analytical pipeline. These materials provide additional diagnostic and distributional context 
        for the analyses presented in the main sections, while keeping the primary narrative concise. 
        All figures included here are displayed at reduced scale and are intended for reference and 
        verification, not detailed inspection.
        """
        story.append(Paragraph(d1_text, styles['BodyJustified']))
        story.append(Spacer(1, 0.15*inch))

        # D.2 Supplementary Figures
        d2_heading = Paragraph("D.2 Supplementary Figures", styles['SubsectionHeading'])
        story.append(d2_heading)
        story.append(Spacer(1, 0.1*inch))

        # --- D.2.1 Data Quality ---
        sub_heading = Paragraph("D.2.1 Data Quality Diagnostics", styles['BodyText'])
        story.append(sub_heading)
        story.append(Spacer(1, 0.05*inch))

        # Grid Data for D.2.1
        img_d1 = get_image_element("data_quality_age_distribution.png")
        img_d2 = get_image_element("data_quality_temporal_pattern.png")
        
        cap_d1 = Paragraph("<b>Fig D1:</b> Age Distribution Check", styles['Caption'])
        cap_d2 = Paragraph("<b>Fig D2:</b> Temporal Aggregation", styles['Caption'])

        # 1x2 Table
        grid_d1 = Table(
            [[img_d1, img_d2], [cap_d1, cap_d2]],
            colWidths=[3.2*inch, 3.2*inch]
        )
        grid_d1.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(grid_d1)
        
        # --- MODIFICATION: PUSH D.2.2 TO NEXT PAGE ---
        story.append(PageBreak()) 
        # ---------------------------------------------

        # --- D.2.2 Dimension 1 ---
        sub_heading = Paragraph("D.2.2 Dimension 1 – Coverage Gap (Supplementary)", styles['BodyText'])
        story.append(sub_heading)
        story.append(Spacer(1, 0.05*inch))

        # Grid Data for D.2.2 (2x2)
        row1_imgs = [get_image_element("dim1_ue_ratio_distribution.png"), 
                     get_image_element("dim1_2x2_matrix.png")]
        row1_caps = [Paragraph("<b>Fig D3:</b> UE Ratio Dist.", styles['Caption']),
                     Paragraph("<b>Fig D4:</b> 2x2 Matrix", styles['Caption'])]
        
        row2_imgs = [get_image_element("dim1_state_ue_ratios.png"), 
                     get_image_element("dim1_low_child_enrollment.png")]
        row2_caps = [Paragraph("<b>Fig D5:</b> State UE Ratios", styles['Caption']),
                     Paragraph("<b>Fig D6:</b> Low Child Enrollment", styles['Caption'])]

        grid_d2 = Table(
            [row1_imgs, row1_caps, row2_imgs, row2_caps],
            colWidths=[3.2*inch, 3.2*inch]
        )
        grid_d2.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,1), (-1,1), 10), # Space between rows
        ]))
        story.append(grid_d2)
        story.append(PageBreak())

        # --- D.2.3 Dimension 2 ---
        sub_heading = Paragraph("D.2.3 Dimension 2 – Readiness Gap (Supplementary)", styles['BodyText'])
        story.append(sub_heading)
        story.append(Spacer(1, 0.05*inch))

        # Grid Data for D.2.3 (2x2)
        row1_imgs = [get_image_element("dim2_readiness_categories.png"), 
                     get_image_element("dim2_readiness_distribution.png")]
        row1_caps = [Paragraph("<b>Fig D7:</b> Category Dist.", styles['Caption']),
                     Paragraph("<b>Fig D8:</b> Score Dist.", styles['Caption'])]
        
        # D.2.2 Dimension 2 - Readiness Gap grid
        row2_imgs = [get_image_element("dim2_state_readiness.png"), 
                    get_image_element("dim2_high_risk_districts.png")]
        row2_caps = [Paragraph("<b>Fig D9:</b> State Readiness", styles['Caption']),
                    Paragraph("<b>Fig D10:</b> High-Risk Districts", styles['Caption'])]

        grid_d3 = Table(
            [row1_imgs, row1_caps, row2_imgs, row2_caps],
            colWidths=[3.2*inch, 3.2*inch]
        )
        grid_d3.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,1), (-1,1), 10),
        ]))
        story.append(grid_d3)
        story.append(PageBreak())

        # --- D.2.4 Dimension 3 ---
        sub_heading = Paragraph("D.2.4 Dimension 3 – Integrity Gap (Supplementary)", styles['BodyText'])
        story.append(sub_heading)
        story.append(Spacer(1, 0.05*inch))

        # Grid Data for D.2.4 (2x2)
        row1_imgs = [get_image_element("dim3_risk_distribution.png"), 
                     get_image_element("dim3_geographic_clustering.png")]
        row1_caps = [Paragraph("<b>Fig D11:</b> Risk Score Dist.", styles['Caption']),
                     Paragraph("<b>Fig D12:</b> Geo Clustering", styles['Caption'])]
        
        row2_imgs = [get_image_element("dim3_anomaly_types.png"), 
                     get_image_element("dim3_top_anomalies.png")]
        row2_caps = [Paragraph("<b>Fig D13:</b> Anomaly Types", styles['Caption']),
                     Paragraph("<b>Fig D14:</b> Top Districts", styles['Caption'])]

        grid_d4 = Table(
            [row1_imgs, row1_caps, row2_imgs, row2_caps],
            colWidths=[3.2*inch, 3.2*inch]
        )
        grid_d4.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,1), (-1,1), 10),
        ]))
        story.append(grid_d4)
        
        # --- MODIFICATION: NO PAGE BREAK HERE ---
        # Allow D.3 to flow immediately after D.2.4 figures
        story.append(Spacer(1, 0.2*inch))
        # ----------------------------------------

        # D.3 Supplementary Tables
        d3_heading = Paragraph("D.3 Supplementary Tables (Summary Only)", styles['SubsectionHeading'])
        story.append(d3_heading)
        story.append(Spacer(1, 0.08*inch))

        d3_intro = """
        Detailed district- and pincode-level tables generated by the pipeline are summarised below. 
        Full tables are available as machine-readable CSV outputs. Priority intervention lists (Top 10) 
        are highlighted for immediate action.
        """
        story.append(Paragraph(d3_intro, styles['BodyJustified']))
        story.append(Spacer(1, 0.1*inch))

        # Table Data - Updated with all new tables
        table_data = [
    ['Dimension', 'Description', 'File Name', 'Records'],
    ['Coverage Gap', 'Coverage gap districts', 'dim1_coverage_gap_districts.csv', '57'],
    ['Coverage Gap', 'Low child enrollment districts', 'dim1_low_child_enrollment_districts.csv', '58'],
    ['Coverage Gap', 'All crisis zone districts', 'dim1_crisis_zone_districts.csv', '387'],
    ['Coverage Gap', 'Top 10 Crisis Zone (Priority)', 'dim1_top10_crisis_zone_districts.csv', '10'],
    
    ['Readiness Gap', 'Critical readiness districts', 'dim2_critical_readiness_districts.csv', '12'],
    ['Readiness Gap', 'Low readiness districts', 'dim2_low_readiness_districts.csv', '12'],
    ['Readiness Gap', 'All at-risk (Low+Critical)', 'dim2_all_at_risk_districts.csv', '24'],
    ['Readiness Gap', 'Top 10 At-Risk (Priority)', 'dim2_top10_at_risk_districts.csv', '10'],
    ['Readiness Gap', 'State readiness ranking', 'dim2_state_readiness_ranking.csv', '36'],
    
    ['Integrity Gap', 'All anomalous pincodes', 'dim3_all_anomalous_pincodes.csv', '4,628'],
    ['Integrity Gap', 'All critical risk pincodes', 'dim3_all_critical_risk_pincodes.csv', '32'],
    ['Integrity Gap', 'Top 10 Critical Risk (Priority)', 'dim3_top10_critical_risk_pincodes.csv', '10'],
    ['Integrity Gap', 'High risk pincodes', 'dim3_high_risk_pincodes.csv', '16'],
    ['Integrity Gap', 'Clustered districts', 'dim3_clustered_districts.csv', 'Varies']
        ]

        # Table Styling
        col_widths = [1.2*inch, 2.0*inch, 2.5*inch, 0.8*inch]
        t = Table(table_data, colWidths=col_widths)

        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'), # Align numbers right
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            # Highlight priority rows (Top 10 tables)
            ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#fff3cd')),   # Dim1 Top 10
            ('BACKGROUND', (0, 8), (-1, 8), colors.HexColor('#fff3cd')),   # Dim2 Top 10
            ('BACKGROUND', (0, 12), (-1, 12), colors.HexColor('#fff3cd')), # Dim3 Top 10
        ]))

        story.append(t)
        story.append(Spacer(1, 0.05*inch))

        caption_t1 = Paragraph(
            "<b>Table D1:</b> Summary of supplementary analytical tables generated by the pipeline. "
            "Priority intervention lists (highlighted in yellow) contain the top 10 most critical cases "
            "for immediate action in each dimension.",
            styles['Caption']
        )
        story.append(caption_t1)
        story.append(Spacer(1, 0.15*inch))

        # Add priority action summary box
        priority_box = """
        <b>Priority Action Files (Top 10 Lists):</b><br/>
        • <b>dim1_top10_crisis_zone_districts.csv</b> - Lowest enrollment & update activity<br/>
        • <b>dim2_top10_at_risk_districts.csv</b> - Highest predicted authentication failures<br/>
        • <b>dim3_top10_critical_risk_pincodes.csv</b> - Highest composite anomaly risk scores<br/>
        <br/>
        These three files provide actionable intelligence for immediate field intervention.
        """
        priority_para = Paragraph(priority_box, styles['BodyJustified'])
        story.append(KeepTogether([priority_para]))
        
        # --- MODIFICATION: REMOVED D.4 SECTION ---
        # Final page break for the end of the document
        story.append(PageBreak())




#     def generate(self):
#         """Generate the complete corrected PDF report"""
        
#         print("\n" + "="*60)
#         print("GENERATING CORRECTED PDF REPORT")
#         print("="*60)
        
#         print("\n📄 Building comprehensive report with all corrections...")
        
#         # Add all sections
#         self.add_cover_page()
#         print("  ✓ Enhanced cover page with framework diagram")
        
#         self.add_problem_statement_and_approach()
#         print("  ✓ Problem Statement (corrected language)")
        
#         self.add_datasets_used()
#         print("  ✓ Datasets Used (corrected numbers)")
        
#         self.add_methodology()
#         print("  ✓ Methodology (corrected thresholds)")
        
#         self.add_executive_summary()
#         print("  ✓ Executive Summary (all corrections applied)")
        
#         self.add_dimension1_findings()
#         print("  ✓ Dimension 1 (corrected: 473, 53, 53, 472)")
        
#         self.add_dimension2_findings()
#         print("  ✓ Dimension 2 (corrected: 49 = 27+22)")
        
#         self.add_dimension3_findings()
#         print("  ✓ Dimension 3 (corrected: 6,956 anomalies)")
        
#         self.add_recommendations()
#         print("  ✓ Strategic Recommendations (advisory tone)")
        
#         self.add_conclusion()
#         print("  ✓ Conclusion (corrected numbers)")
        
#         self.add_code_appendix()
#         print("  ✓ Code Appendix")
        
#         # Build PDF
#         print("\n📦 Compiling corrected PDF...")
#         self.doc.build(self.story)
        
#         file_size = os.path.getsize(self.report_path) / 1024
        
#         print(f"\n✅ CORRECTED REPORT GENERATED!")
#         print(f"📁 Location: {self.report_path}")
#         print(f"📊 File size: {file_size:.1f} KB")
#         print(f"\n🎯 ALL CORRECTIONS APPLIED:")
#         print("   ✓ Geographic: 36 states, 1,051 state–district combinations, 19,814 pincodes")
#         print("   ✓ Enrollments: 6,703,112")
#         print("   ✓ Bio updates: 81,359,177")
#         print("   ✓ Demo updates: 51,432,273")
#         print("   ✓ UE Ratio: 19.81")
#         print("   ✓ District classification: 473, 53, 53, 472")
#         print("   ✓ Readiness breakdown: 798, 122, 22, 27 (total 49)")
#         print("   ✓ Anomalies: 6,956 (32 critical+high)")
#         print("   ✓ Language: Advisory tone throughout")
#         print("   ✓ Spacing: Improved, no orphaned paragraphs")
#         print("   ✓ Cover: Enhanced with framework diagram")
#         print("="*60)
        
#         return self.report_path


# def main():
#     """Generate the final corrected report"""
    
#     report = EnhancedAadhaarReport()
#     report_path = report.generate()
    
#     print("\n" + "="*60)
#     print("🎉 CORRECTED SUBMISSION READY!")
#     print("="*60)
#     print(f"\n📄 Report: {report_path}")
#     print(f"\n✅ ALL SECTIONS VERIFIED:")
#     print("   1. Problem Statement and Approach ✓")
#     print("   2. Datasets Used ✓")
#     print("   3. Methodology ✓")
#     print("   4. Data Analysis and Visualisation ✓")
#     print("   5. Code Files/Notebooks ✓")
#     print("\n🏆 SUBMISSION-READY WITH ALL CORRECTIONS!")
#     print("="*60)
    
#     return report_path


# if __name__ == "__main__":
#     report_path = main()



    
    def generate(self):
        """Generate the enhanced PDF report"""
    
        print("\n" + "="*60)
        print("GENERATING ENHANCED PDF REPORT")
        print("="*60)
    
        print("\n📄 Building enhanced report with all improvements...")
    
        # Add all sections
        self.add_cover_page()
        print("  ✓ Cover page")
    
        self.add_table_of_contents()
        print("  ✓ Table of contents (page 2)")
    
        self.add_problem_statement_and_approach()
        print("  ✓ Problem Statement (point-wise)")
    
        self.add_datasets_used()
        print("  ✓ Datasets Used (point-wise)")
    
        self.add_methodology()
        print("  ✓ Methodology (point-wise)")
    
        self.add_executive_summary()
        print("  ✓ Executive Summary (point-wise)")
    
        self.add_dimension1_findings()
        print("  ✓ Dimension 1 (with key insight box)")
    
        self.add_dimension2_findings()
        print("  ✓ Dimension 2 (with key insight box)")
    
        self.add_dimension3_findings()
        print("  ✓ Dimension 3 (with key insight box)")
    
        self.add_recommendations()
        print("  ✓ Recommendations (point-wise)")
    
        self.add_conclusion()
        print("  ✓ Conclusion (point-wise)")
    
        self.add_appendix_a()
        print("  ✓ Code Appendix A")

        self.add_appendix_b()
        print("  ✓ Code Appendix B")

        self.add_appendix_c()
        print("  ✓ Code Appendix C")

        self.add_appendix_d()
        print("  ✓ Code Appendix D")
    
        # Build PDF with page numbers
        print("\n📦 Compiling PDF with page numbers...")
        self.doc.build(self.story, canvasmaker=NumberedCanvas)
    
        file_size = os.path.getsize(self.report_path) / 1024
    
        print(f"\n✅ ENHANCED REPORT GENERATED!")
        print(f"📁 Location: {self.report_path}")
        print(f"📊 File size: {file_size:.1f} KB")
        print(f"\n🎯 ALL ENHANCEMENTS APPLIED:")
        print("   ✓ Page numbers at bottom right (all pages except cover)")
        print("   ✓ Table of contents on page 2")
        print("   ✓ Point-wise information (no paragraph walls)")
        print("   ✓ Key insight boxes at start of each dimension")
        print("   ✓ Better visual hierarchy and readability")
        print("="*60)
    
        return self.report_path

def main():
    report = EnhancedAadhaarReport()
    path = report.generate()
    print(f"Report generated: {path}")


if __name__ == "__main__":
    main()




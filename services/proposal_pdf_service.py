import io
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from models import TreatmentProposal, TreatmentRequest, Hospital, CostLineItem

def generate_proposal_pdf(proposal_id):
    """
    Generate a professional PDF for a TreatmentProposal.
    Returns the generated PDF as a bytes buffer.
    """
    # Fetch Data
    proposal = TreatmentProposal.query.get_or_404(proposal_id)
    req = TreatmentRequest.query.get(proposal.treatment_request_id)
    hospital = Hospital.query.get(proposal.hospital_id)
    line_items = CostLineItem.query.filter_by(proposal_id=proposal.id).all()
    
    # Create an in-memory buffer
    buffer = io.BytesIO()
    
    # Configure document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Define Brand Colors
    PRIMARY_COLOR = colors.HexColor("#0f3d81")
    SECONDARY_COLOR = colors.HexColor("#2a75d3")
    TEXT_MAIN = colors.HexColor("#1e293b")
    TEXT_MUTED = colors.HexColor("#64748b")
    AMBER_ACCENT = colors.HexColor("#d97706")
    
    # Custom Styles
    styles.add(ParagraphStyle(
        name='BrandTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=PRIMARY_COLOR,
        spaceAfter=6
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=SECONDARY_COLOR,
        spaceBefore=16,
        spaceAfter=8,
        borderPadding=4
    ))
    
    styles.add(ParagraphStyle(
        name='SubHeading',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=TEXT_MAIN,
        spaceBefore=10,
        spaceAfter=4
    ))
    
    styles.add(ParagraphStyle(
        name='NormalText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=TEXT_MAIN,
        leading=14,
        spaceAfter=6
    ))
    
    styles.add(ParagraphStyle(
        name='MutedText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=TEXT_MUTED,
        leading=12
    ))
    
    styles.add(ParagraphStyle(
        name='Disclaimer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        textColor=TEXT_MUTED,
        leading=12,
        spaceBefore=10,
        spaceAfter=15,
        borderWidth=1,
        borderColor=colors.HexColor("#e2e8f0"),
        borderPadding=8,
        backColor=colors.HexColor("#f8fafc")
    ))

    # Helper function for safe string conversion
    def safe_str(val, default="None specified"):
        return str(val) if val else default

    elements = []
    
    # ---------------- HEADER ----------------
    # Rather than a complex drawing, we use a Table for layout
    header_data = [
        [
            Paragraph("<b>MediBid</b>", styles['BrandTitle']), 
            Paragraph(f"<font color='{TEXT_MUTED}'><b>Treatment Estimate & Proposal</b></font><br/>"
                      f"<b>Request Ref:</b> {req.reference_id}<br/>"
                      f"<b>Submitted:</b> {safe_str(proposal.submitted_at.strftime('%Y-%m-%d') if proposal.submitted_at else 'N/A')}<br/>"
                      f"<b>Valid Until:</b> {safe_str(proposal.valid_until.strftime('%Y-%m-%d') if proposal.valid_until else 'N/A')}", 
                      styles['NormalText'])
        ]
    ]
    header_table = Table(header_data, colWidths=[3.5*inch, 3*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0"))
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 10))

    # ---------------- HOSPITAL INFO ----------------
    hospital_name = hospital.display_name or hospital.legal_name or "Unknown Hospital"
    verified_str = " (Verified)" if getattr(hospital, 'is_verified', False) else ""
    location = f"{safe_str(hospital.city, '')}, {safe_str(hospital.country, '')}".strip(", ")
    
    elements.append(Paragraph(f"<b>Providing Hospital:</b> {hospital_name}{verified_str}", styles['SubHeading']))
    if location:
        elements.append(Paragraph(f"Location: {location}", styles['MutedText']))
    
    elements.append(Spacer(1, 15))
    
    # ---------------- DISCLAIMER ----------------
    disclaimer_text = ("This document provides a preliminary treatment estimate based on currently available medical information. "
                       "The final treatment plan and costs may change following clinical evaluation, additional investigations, "
                       "or changes in patient condition.")
    elements.append(Paragraph(disclaimer_text, styles['Disclaimer']))
    
    # ---------------- MEDICAL ASSESSMENT ----------------
    elements.append(Paragraph("Medical Assessment & Treatment Plan", styles['SectionHeading']))
    elements.append(Paragraph("<b>Proposed Treatment / Procedure:</b>", styles['SubHeading']))
    elements.append(Paragraph(safe_str(proposal.proposed_treatment), styles['NormalText']))
    
    elements.append(Paragraph("<b>Clinical Assessment & Approach:</b>", styles['SubHeading']))
    elements.append(Paragraph(safe_str(proposal.treatment_plan).replace('\n', '<br/>'), styles['NormalText']))
    
    elements.append(Paragraph("<b>Treating Department:</b>", styles['SubHeading']))
    elements.append(Paragraph(safe_str(proposal.specialty), styles['NormalText']))
    
    elements.append(Paragraph("<b>Lead Doctor / Specialist:</b>", styles['SubHeading']))
    elements.append(Paragraph(safe_str(proposal.lead_doctor), styles['NormalText']))
    
    # ---------------- TREATMENT TIMELINE ----------------
    elements.append(Paragraph("Treatment Timeline", styles['SectionHeading']))
    duration_str = f"{proposal.estimated_duration_value} {proposal.estimated_duration_unit}" if proposal.estimated_duration_value else "None specified"
    elements.append(Paragraph(f"<b>Total Estimated Duration:</b> {duration_str}", styles['NormalText']))
    elements.append(Paragraph(f"<b>Hospital Stay:</b> {safe_str(proposal.hospital_stay_nights, '0')} nights", styles['NormalText']))
    elements.append(Paragraph(f"<b>Recovery Stay:</b> {safe_str(proposal.recovery_stay_days, '0')} days", styles['NormalText']))
    
    # ---------------- ESTIMATED COST ----------------
    elements.append(Paragraph("Estimated Cost", styles['SectionHeading']))
    currency = safe_str(proposal.currency, "USD")
    min_cost = f"{float(proposal.estimated_cost_min):,.2f}" if proposal.estimated_cost_min else "0.00"
    max_cost = f"{float(proposal.estimated_cost_max):,.2f}" if proposal.estimated_cost_max else "0.00"
    elements.append(Paragraph(f"<b>Total Estimated Range:</b> <font color='{AMBER_ACCENT}'>{currency} {min_cost} - {max_cost}</font>", styles['NormalText']))
    
    # ---------------- COST BREAKDOWN TABLE ----------------
    if line_items:
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("<b>Cost Breakdown:</b>", styles['SubHeading']))
        
        table_data = [['Description', 'Amount']]
        for item in line_items:
            amt = f"{currency} {float(item.amount):,.2f}" if item.amount else "N/A"
            table_data.append([item.description, amt])
            
        cost_table = Table(table_data, colWidths=[4.5*inch, 2*inch])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ('TEXTCOLOR', (0, 0), (-1, 0), TEXT_MAIN),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ]))
        elements.append(cost_table)
    
    # ---------------- INCLUSIONS & EXCLUSIONS ----------------
    elements.append(Paragraph("Inclusions & Exclusions", styles['SectionHeading']))
    elements.append(Paragraph("<b>Included in Estimate:</b>", styles['SubHeading']))
    elements.append(Paragraph(safe_str(proposal.inclusions).replace('\n', '<br/>'), styles['NormalText']))
    
    elements.append(Paragraph("<b>Not Included:</b>", styles['SubHeading']))
    elements.append(Paragraph(safe_str(proposal.exclusions).replace('\n', '<br/>'), styles['NormalText']))
    
    # ---------------- IMPORTANT NOTES ----------------
    elements.append(Paragraph("Important Notes", styles['SectionHeading']))
    elements.append(Paragraph("<b>Pre-treatment Requirements:</b>", styles['SubHeading']))
    elements.append(Paragraph(safe_str(proposal.requirements).replace('\n', '<br/>'), styles['NormalText']))
    
    elements.append(Paragraph("<b>Additional Notes:</b>", styles['SubHeading']))
    elements.append(Paragraph(safe_str(proposal.additional_notes).replace('\n', '<br/>'), styles['NormalText']))
    
    # ---------------- BUILD PDF WITH FOOTER ----------------
    def add_footer(canvas, doc):
        canvas.saveState()
        # Footer text
        footer_text = f"Generated by MediBid | Request Ref: {req.reference_id} | Page {doc.page}"
        privacy_text = "CONFIDENTIAL: This document contains sensitive medical estimates intended only for the requesting patient."
        
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(TEXT_MUTED)
        canvas.drawString(20*mm, 15*mm, footer_text)
        canvas.drawRightString(A4[0] - 20*mm, 15*mm, privacy_text)
        canvas.restoreState()

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    # Create suggested filename
    hospital_slug = hospital_name.replace(" ", "-").replace("/", "-")
    filename = f"MediBid_Proposal_{req.reference_id}_{hospital_slug}.pdf"
    
    return pdf_bytes, filename

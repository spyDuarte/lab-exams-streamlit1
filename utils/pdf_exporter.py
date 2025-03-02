"""
Exports exam results to PDF.
"""
import logging
import tempfile
from typing import Dict, List, Any, Optional
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from utils.formatter import get_status_from_values

class PDFExporter:
    """Exports exam results to a PDF file."""
    
    def __init__(self, exam_type: str, date: str, results: Dict) -> None:
        """
        Initialize the PDF exporter.
        
        Args:
            exam_type: Type of exam.
            date: Date string.
            results: Dictionary with exam results.
        """
        self.exam_type = exam_type
        self.date = date
        self.results = results
        self.styles = getSampleStyleSheet()
        self._setup()
        self.orientation: str = "portrait"
    
    def _setup(self) -> None:
        """Configure PDF styles."""
        self.styles.add(ParagraphStyle(
            name='CatHeader', 
            parent=self.styles['Heading2'], 
            spaceAfter=10, 
            spaceBefore=20
        ))
    
    def set_orientation(self, orientation: str) -> None:
        """
        Define the PDF orientation.
        
        Args:
            orientation: 'portrait' or 'landscape'.
            
        Raises:
            ValueError: If the orientation is invalid.
        """
        if orientation not in ("portrait", "landscape"):
            raise ValueError("Use 'portrait' or 'landscape'.")
        self.orientation = orientation
    
    def export(self) -> bytes:
        """
        Exports the results to a PDF file.
        
        Returns:
            PDF as bytes.
        """
        buffer = io.BytesIO()
        pagesize = A4 if self.orientation == "portrait" else (A4[1], A4[0])
        
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=pagesize,
            rightMargin=72, 
            leftMargin=72,
            topMargin=72, 
            bottomMargin=72
        )
        
        story: List[Any] = []
        self._add_header(story)
        
        for cat, data_exams in self.results.items():
            if data_exams:
                self._add_cat_header(story, cat)
                self._add_table(story, data_exams)
                
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        logging.info("PDF exported")
        return pdf_bytes
    
    def _add_header(self, story: List[Any]) -> None:
        """Add the header to the PDF."""
        story.append(Paragraph(f"Resultados de Exames - {self.exam_type}", self.styles['Heading1']))
        story.append(Paragraph(f"Data: {self.date}", self.styles['Normal']))
        story.append(Spacer(1, 20))
    
    def _add_cat_header(self, story: List[Any], cat: str) -> None:
        """Add a category header to the PDF."""
        story.append(Paragraph(cat, self.styles['CatHeader']))
    
    def _add_table(self, story: List[Any], data_exams: Dict[str, Any]) -> None:
        """
        Add a table with results to the PDF.
        
        Args:
            data_exams: Dictionary with exam data.
        """
        table_data: List[List[str]] = [["Exame", "Resultado", "Referência", "Status"]]
        
        for exam_name, vals in data_exams.items():
            st: str = get_status_from_values(vals['value'], vals['reference'])
            table_data.append([
                exam_name, 
                f"{vals['value']} {vals['unit']}", 
                f"{vals['reference']} {vals['unit']}", 
                st
            ])
        
        colw = [2 * inch, 1.5 * inch, 1.5 * inch, 1 * inch] if self.orientation == "portrait" else [3 * inch, 2 * inch, 2 * inch, 1 * inch]
        tbl = Table(table_data, colWidths=colw)
        
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(tbl)
        story.append(Spacer(1, 20))
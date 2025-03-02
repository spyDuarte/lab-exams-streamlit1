"""
Formats exam results for display and export.
"""
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime

def get_status_from_values(value_str: str, reference_str: str) -> str:
    """
    Determines the status (BAIXO, NORMAL, ALTO) based on the exam value and reference.
    
    Args:
        value_str: Exam value as string.
        reference_str: Reference range as string (e.g., "0-100").
        
    Returns:
        String representing the status.
    """
    try:
        value = float(value_str.replace(',', '.'))
    except ValueError:
        return "N/A"
        
    parts = reference_str.split('-')
    if len(parts) == 2:
        try:
            min_v, max_v = map(float, parts)
        except ValueError:
            return "N/A"
    else:
        return "N/A"
        
    if value < min_v:
        return "BAIXO"
    elif value > max_v:
        return "ALTO"
    return "NORMAL"

class ExamResultFormatter:
    """Formats exam results in simple text and tabular representations."""
    
    def __init__(self, exam_type: str, date: str, results: Dict) -> None:
        """
        Initialize the formatter.
        
        Args:
            exam_type: Type of exam.
            date: Date string.
            results: Dictionary with exam results.
        """
        self.exam_type = exam_type
        self.date = date
        self.results = results
        self._cached_text: Optional[str] = None
        self._cached_table: Optional[str] = None
    
    def format_text(self) -> str:
        """
        Returns a simple text representation of the results.
        
        Returns:
            Formatted string with results.
        """
        if self._cached_text is None:
            lines: List[str] = [f"Resultados de Exames - {self.exam_type}", f"Data: {self.date}", ""]
            
            for category, data_exams in self.results.items():
                if data_exams:
                    lines.append(category)
                    lines.append("-" * len(category))
                    
                    for exam_name, vals in data_exams.items():
                        status = get_status_from_values(vals['value'], vals['reference'])
                        l = f"{exam_name}: {vals['value']} {vals['unit']} (Ref: {vals['reference']} {vals['unit']}) - {status}"
                        lines.append(l)
                        
                    lines.append("")
                    
            self._cached_text = "\n".join(lines)
            
        return self._cached_text
    
    def format_tabular(self) -> str:
        """
        Returns a tabular representation of the results.
        
        Returns:
            String containing the result in table format.
        """
        if self._cached_table is None:
            self._cached_table = self._build_table()
        return self._cached_table
    
    def _build_table(self) -> str:
        """
        Builds a text table with the results.
        
        Returns:
            String formatted as a table.
        """
        rows: List[Tuple[str, str, str, str]] = []
        
        for cat, data_exams in self.results.items():
            if data_exams:
                rows.append(("", "", "", ""))
                rows.append((cat.upper(), "", "", ""))
                
                for exam_name, vals in data_exams.items():
                    status = get_status_from_values(vals['value'], vals['reference'])
                    rows.append((exam_name, f"{vals['value']} {vals['unit']}", f"{vals['reference']} {vals['unit']}", status))
        
        if not rows:
            return "No exams filled."
            
        w_exam: int = max(len(r[0]) for r in rows)
        w_val: int = max(len(r[1]) for r in rows)
        w_ref: int = max(len(r[2]) for r in rows)
        w_stat: int = max(len(r[3]) for r in rows)
        
        header: str = f"{'Exame':<{w_exam}} | {'Resultado':<{w_val}} | {'Referência':<{w_ref}} | {'Status':<{w_stat}}"
        sep: str = "-" * len(header)
        
        lines: List[str] = [f"Resultados de Exames - {self.exam_type}", f"Data: {self.date}", "", header, sep]
        
        for row in rows:
            if row == ("", "", "", ""):
                lines.append("")
            elif row[1] == "" and row[2] == "":
                total_w: int = (w_exam + w_val + w_ref + w_stat) + 9
                cat_text: str = f"{row[0]:^{total_w}}"
                lines.append(cat_text)
            else:
                exam, val, ref, status = row
                line: str = f"{exam:<{w_exam}} | {val:<{w_val}} | {ref:<{w_ref}} | {status:<{w_stat}}"
                lines.append(line)
                
        return "\n".join(lines)
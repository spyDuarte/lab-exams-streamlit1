"""
Validation logic for exam data.
"""
import logging
from datetime import datetime
from typing import Optional

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class ExamDataValidator:
    """Validates exam data."""
    
    @staticmethod
    def validate_date(date_obj: datetime) -> bool:
        """
        Validates the exam date.
        
        Args:
            date_obj: Date as a datetime object.
            
        Returns:
            True if the date is valid.
            
        Raises:
            ValidationError: If the date is empty or in the future.
        """
        if date_obj is None:
            logging.error("Exam date is required.")
            raise ValidationError("Exam date is required.")
            
        if date_obj > datetime.now():
            logging.error("Exam date cannot be in the future.")
            raise ValidationError("Exam date cannot be in the future.")
            
        return True
    
    @staticmethod
    def validate_numeric_value(value: str, exam_name: str) -> Optional[float]:
        """
        Validates a numeric exam value.
        
        Args:
            value: Value as string.
            exam_name: Exam name for error messages.
            
        Returns:
            Converted float value or None if empty.
            
        Raises:
            ValidationError: If the value is invalid or negative.
        """
        if not value.strip():
            return None
            
        try:
            val = float(value.replace(',', '.'))
        except ValueError as ve:
            logging.error(f"Invalid value for {exam_name}: {value}")
            raise ValidationError(f"Invalid value for {exam_name}: {value}") from ve
            
        if val < 0:
            logging.error(f"Negative value not allowed ({exam_name}).")
            raise ValidationError(f"Negative value not allowed ({exam_name}).")
            
        return val
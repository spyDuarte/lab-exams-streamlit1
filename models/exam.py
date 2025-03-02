"""
Data models for exam profiles and reference ranges.
"""
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from pydantic import BaseModel

class ReferenceRange(BaseModel):
    """Represents a reference range for an exam."""
    min: Optional[float] = None
    max: Optional[float] = None
    unit: str
    gender_specific: bool = False
    male_min: Optional[float] = None
    male_max: Optional[float] = None
    female_min: Optional[float] = None
    female_max: Optional[float] = None
    description: Optional[str] = None

class ExamProfile(BaseModel):
    """Represents an exam profile with categories and associated exams."""
    name: str
    categories: Dict[str, List[str]]
    description: str = ""
    is_default: bool = False
    created_at: datetime = datetime.now()
    last_used: datetime = datetime.now()
    
    def update_last_used(self) -> None:
        """Updates the timestamp of the last use of the profile."""
        self.last_used = datetime.now()
    
    def get_exam_count(self) -> int:
        """Returns the total number of exams contained in the profile."""
        return sum(len(exams) for exams in self.categories.values())
    
    def get_category_count(self) -> int:
        """Returns the number of categories with at least one exam."""
        return len([cat for cat, exams in self.categories.items() if exams])

class ExamResult(BaseModel):
    """Represents the result of a specific exam."""
    value: float
    unit: str
    reference: str
    status: str = "NORMAL"  # NORMAL, ALTO, BAIXO

class CategoryResults(BaseModel):
    """Represents the results for a category of exams."""
    category_name: str
    exams: Dict[str, ExamResult]

class CompleteExamResult(BaseModel):
    """Represents a complete set of exam results."""
    exam_type: str
    date: datetime
    results: Dict[str, Dict[str, ExamResult]] 
    
    class Config:
        arbitrary_types_allowed = True
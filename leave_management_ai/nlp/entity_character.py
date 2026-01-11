"""
Entity extraction from user text
"""
import re
import spacy
from leave_management_ai.nlp.date_parser import DateParser


class EntityExtractor:
    """Extract entities like employee ID, dates, leave type from text"""
    
    def __init__(self):
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("⚠ spaCy model not found. Run: python -m spacy download en_core_web_sm")
            raise
        
        self.date_parser = DateParser()
        
        # Leave type keywords
        self.leave_type_keywords = {
            'casual': ['casual', 'cl'],
            'sick': ['sick', 'medical', 'sl', 'health'],
            'vacation': ['vacation', 'holiday', 'vl', 'annual'],
            'general': ['leave', 'general']
        }
    
    def extract_employee_id(self, text):
        """
        Extract employee ID from text
        Patterns: EMP123, emp-123, E123, employee id 123, etc.
        """
        text_upper = text.upper()
        
        # Pattern 1: EMP followed by numbers
        match = re.search(r'EMP[-_]?(\d+)', text_upper)
        if match:
            return f"EMP{match.group(1)}"
        
        # Pattern 2: E followed by numbers
        match = re.search(r'\bE[-_]?(\d+)', text_upper)
        if match:
            return f"E{match.group(1)}"
        
        # Pattern 3: "employee id" or "emp id" followed by alphanumeric
        match = re.search(r'(?:EMPLOYEE|EMP)\s*(?:ID|CODE|NUMBER|NO)[:\s]*([A-Z0-9]+)', text_upper)
        if match:
            return match.group(1)
        
        # Pattern 4: Just alphanumeric ID at the end
        match = re.search(r'\b([A-Z]{2,4}\d{2,6})\b', text_upper)
        if match:
            return match.group(1)
        
        return None
    
    def extract_dates(self, text):
        """
        Extract date range from text
        Returns (start_date, end_date, days_count) or (None, None, 0)
        """
        start_date, end_date = self.date_parser.parse_date_range(text)
        
        if start_date and end_date:
            # Calculate days based on configuration
            from config.settings import BUSINESS_RULES
            days_count = self.date_parser.calculate_business_days(
                start_date, 
                end_date,
                include_weekends=BUSINESS_RULES['weekend_counts']
            )
            return start_date, end_date, days_count
        
        return None, None, 0
    
    def extract_leave_type(self, text):
        """
        Extract leave type from text
        Returns leave type key or 'general' as default
        """
        text_lower = text.lower()
        
        for leave_type, keywords in self.leave_type_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return leave_type
        
        return 'general'  # default
    
    def extract_all_entities(self, text):
        """
        Extract all entities from text
        Returns dict with employee_id, dates, leave_type
        """
        employee_id = self.extract_employee_id(text)
        start_date, end_date, days_count = self.extract_dates(text)
        leave_type = self.extract_leave_type(text)
        
        return {
            'employee_id': employee_id,
            'start_date': start_date,
            'end_date': end_date,
            'days_count': days_count,
            'leave_type': leave_type
        }
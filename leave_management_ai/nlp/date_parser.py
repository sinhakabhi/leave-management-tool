"""
Natural language date parsing
"""
import re
from datetime import datetime, timedelta
from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta


class DateParser:
    """Parse dates from natural language text"""
    
    def __init__(self):
        self.today = datetime.now().date()
        self.weekdays = {
            'monday': 0, 'mon': 0,
            'tuesday': 1, 'tue': 1, 'tues': 1,
            'wednesday': 2, 'wed': 2,
            'thursday': 3, 'thu': 3, 'thur': 3, 'thurs': 3,
            'friday': 4, 'fri': 4,
            'saturday': 5, 'sat': 5,
            'sunday': 6, 'sun': 6
        }
    
    def parse_single_date(self, text):
        """
        Parse a single date from text
        Returns datetime.date object or None
        """
        text = text.lower().strip()
        
        # Handle relative dates
        if text in ['today', 'now']:
            return self.today
        
        if text == 'tomorrow':
            return self.today + timedelta(days=1)
        
        if text == 'yesterday':
            return self.today - timedelta(days=1)
        
        # Next/This weekday
        match = re.search(r'(next|this)\s+(\w+)', text)
        if match:
            modifier, day = match.groups()
            return self._get_weekday_date(day, modifier == 'next')
        
        # Just a weekday
        for day_name, day_num in self.weekdays.items():
            if day_name in text:
                return self._get_next_weekday(day_num)
        
        # Try parsing with dateutil
        try:
            parsed = dateutil_parser.parse(text, fuzzy=True, default=datetime.now())
            return parsed.date()
        except:
            pass
        
        # Try common formats with regex
        # Format: DD/MM/YYYY or DD-MM-YYYY
        match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', text)
        if match:
            day, month, year = match.groups()
            year = int(year)
            if year < 100:
                year += 2000
            try:
                return datetime(year, int(month), int(day)).date()
            except:
                pass
        
        # Format: DD Month or DDth Month
        match = re.search(r'(\d{1,2})(st|nd|rd|th)?\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', text)
        if match:
            day = int(match.group(1))
            month_str = match.group(3)
            year = self.today.year
            try:
                parsed = dateutil_parser.parse(f"{day} {month_str} {year}")
                result_date = parsed.date()
                # If date is in the past, assume next year
                if result_date < self.today:
                    result_date = result_date.replace(year=year + 1)
                return result_date
            except:
                pass
        
        return None
    
    def parse_date_range(self, text):
        """
        Parse date range from text
        Returns (start_date, end_date) tuple or (None, None)
        """
        text = text.lower()
        
        # Pattern: "from X to Y" or "X to Y"
        from_to_pattern = r'(?:from\s+)?(.+?)\s+(?:to|until|till|-)\s+(.+?)(?:\s|$|,|\.)'
        match = re.search(from_to_pattern, text)
        if match:
            start_text, end_text = match.groups()
            start_date = self.parse_single_date(start_text)
            end_date = self.parse_single_date(end_text)
            if start_date and end_date:
                return start_date, end_date
        
        # Pattern: "on DATE" (single day)
        on_pattern = r'on\s+(.+?)(?:\s|$|,|\.)'
        match = re.search(on_pattern, text)
        if match:
            date = self.parse_single_date(match.group(1))
            if date:
                return date, date
        
        # Try to find two dates in the text
        dates = []
        words = text.split()
        for i in range(len(words)):
            for j in range(i+1, min(i+6, len(words)+1)):
                phrase = ' '.join(words[i:j])
                date = self.parse_single_date(phrase)
                if date and date not in dates:
                    dates.append(date)
                    if len(dates) == 2:
                        dates.sort()
                        return dates[0], dates[1]
        
        # If only one date found, assume single day
        if len(dates) == 1:
            return dates[0], dates[0]
        
        return None, None
    
    def _get_next_weekday(self, target_day):
        """Get the next occurrence of a weekday"""
        current_day = self.today.weekday()
        days_ahead = target_day - current_day
        if days_ahead <= 0:
            days_ahead += 7
        return self.today + timedelta(days=days_ahead)
    
    def _get_weekday_date(self, day_name, is_next_week):
        """Get date for 'this/next Monday' etc."""
        day_name = day_name.lower()
        if day_name not in self.weekdays:
            return None
        
        target_day = self.weekdays[day_name]
        current_day = self.today.weekday()
        days_ahead = target_day - current_day
        
        if is_next_week:
            if days_ahead <= 0:
                days_ahead += 7
            else:
                days_ahead += 7
        else:
            if days_ahead < 0:
                days_ahead += 7
        
        return self.today + timedelta(days=days_ahead)
    
    def calculate_business_days(self, start_date, end_date, include_weekends=False):
        """Calculate number of days between two dates"""
        if include_weekends:
            return (end_date - start_date).days + 1
        
        # Count business days only
        days = 0
        current = start_date
        while current <= end_date:
            if current.weekday() < 5:  # Monday = 0, Sunday = 6
                days += 1
            current += timedelta(days=1)
        return days
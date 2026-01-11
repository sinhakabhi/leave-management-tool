"""
Configuration settings for the Leave Management AI system
"""

# Database Configuration
DB_CONFIG = {
    'host': '<your_database_host>',
    'port': 5432,
    'database': '<your_database_name>',
    'user': '<your_database_user>',
    'password': '<your_database_password>'  # Change this to your PostgreSQL password
}

# Leave Types Configuration
LEAVE_TYPES = {
    'casual': 'Casual Leave',
    'sick': 'Sick Leave',
    'vacation': 'Vacation Leave',
    'general': 'General Leave'  # Default type
}

# Business Rules
BUSINESS_RULES = {
    'weekend_counts': False,  # Whether weekends count towards leave days
    'min_leave_balance': 0,   # Minimum leave balance allowed (can go negative)
    'max_consecutive_days': 30  # Maximum consecutive leave days
}

# NLP Configuration
NLP_CONFIG = {
    'spacy_model': 'en_core_web_sm',
    'confidence_threshold': 0.6  # Minimum confidence for intent classification
}

# Response Templates
RESPONSE_TEMPLATES = {
    'leave_request': (
        "📋 Leave Request Summary:\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Leave Type: {leave_type}\n"
        "Period: {start_date} to {end_date}\n"
        "Duration: {days} day(s)\n\n"
        "💼 Leave Balance:\n"
        "Current: {current_balance} days\n"
        "After deduction: {remaining_balance} days\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Type 'yes' or 'confirm' to approve this request."
    ),
    'leave_confirmed': (
        "✅ Leave Approved!\n\n"
        "Your leave from {start_date} to {end_date} has been granted.\n"
        "Remaining balance: {remaining_balance} days\n\n"
        "Have a great time off! 🌴"
    ),
    'insufficient_balance': (
        "❌ Insufficient Leave Balance\n\n"
        "Available: {current_balance} days\n"
        "Requested: {days} days\n"
        "Shortage: {shortage} days\n\n"
        "Please adjust your leave dates or choose a different leave type."
    ),
    'balance_query': (
        "💼 Your Leave Balance:\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "{balance_details}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
}
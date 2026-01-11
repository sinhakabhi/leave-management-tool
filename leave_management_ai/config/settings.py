"""
Configuration settings for the Leave Management AI system
"""

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'leave_management',
    'user': 'postgres',
    'password': 'your_password_here'  # Change this to your PostgreSQL password
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
        "Leave Request Summary:\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Leave Type: {leave_type}\n"
        "Period: {start_date} to {end_date}\n"
        "Duration: {days} day(s)\n\n"
        "Leave Balance:\n"
        "Current: {current_balance} days\n"
        "After deduction: {remaining_balance} days\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Type 'yes' or 'confirm' to approve this request."
    ),
    'leave_confirmed': (
        "Leave Approved!\n\n"
        "Your leave from {start_date} to {end_date} has been granted.\n"
        "Remaining balance: {remaining_balance} days\n\n"
        "Have a great time off! 🌴"
    ),
    'insufficient_balance': (
        "Insufficient Leave Balance\n\n"
        "Available: {current_balance} days\n"
        "Requested: {days} days\n"
        "Shortage: {shortage} days\n\n"
        "Please adjust your leave dates or choose a different leave type."
    ),
    'balance_query': (
        "Your Leave Balance:\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "{balance_details}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ),
    'eligibility_yes': (
        "Yes, you can take leave!\n\n"
        "Date: {date} ({day_name})\n"
        "Current Balance: {balance} days\n"
        "After Leave: {after_balance} days\n\n"
        "To proceed, just say 'I want to take leave {date_phrase}'"
    ),
    'eligibility_no_weekend': (
        "Not a Working Day\n\n"
        "{date} ({day_name}) is a weekend.\n\n"
        "Weekends don't count as working days in our system.\n"
        "You can request leave for a weekday instead!"
    ),
    'eligibility_no_balance': (
        "Insufficient Leave Balance\n\n"
        "Date: {date} ({day_name})\n"
        "Current Balance: {balance} days\n"
        "Required: {required} day(s)\n\n"
        "You don't have enough leave balance for this request."
    ),
    'overlapping_leaves': (
        "Overlapping Leave Detected\n\n"
        "You already have approved leave(s) for these dates:\n\n"
        "{overlap_details}\n\n"
        "To apply for new leave on these dates, you must first cancel the existing leave.\n"
        "Say 'cancel my leave from {start_date} to {end_date}' to cancel."
    ),
    'leaves_cancelled': (
        "Leave(s) Cancelled Successfully!\n\n"
        "{cancelled_details}\n\n"
        "Total restored: {total_restored} days\n\n"
        "Your leave balance has been updated."
    ),
    'cancel_past_leave_error': (
        "Cannot Cancel Past Leave\n\n"
        "You can only cancel future leaves.\n"
        "Past or current leaves cannot be cancelled."
    ),
    'no_leaves_to_cancel': (
        "No Leaves Found\n\n"
        "No approved leaves found for the specified dates.\n"
        "Check your leave history to see your approved leaves."
    )
}
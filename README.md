# Leave Management AI System

An intelligent leave management system that uses Natural Language Processing (NLP) to process employee leave requests through natural language queries.

## Features

✨ **Natural Language Understanding**
- Process leave requests in plain English
- Extract dates, employee IDs, and leave types automatically
- Support for various date formats (relative dates, specific dates, date ranges)

🤖 **Intent Classification**
- Apply for leave
- Confirm pending requests
- Cancel requests
- Check leave balance
- View leave history

📊 **Leave Management**
- Multiple leave types (Casual, Sick, Vacation, General)
- Automatic balance calculation
- Two-step confirmation process
- Transaction logging
- Business rules enforcement

🗄️ **PostgreSQL Database**
- Robust data persistence
- Transaction support
- Complete audit trail

## Project Structure

```
leave_management_ai/
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration settings
├── database/
│   ├── __init__.py
│   ├── connection.py            # Database connection pool
│   ├── models.py                # Database schema
│   └── operations.py            # CRUD operations
├── nlp/
│   ├── __init__.py
│   ├── intent_classifier.py     # Intent classification
│   ├── entity_extractor.py      # Entity extraction
│   └── date_parser.py           # Date parsing
├── services/
│   ├── __init__.py
│   └── leave_service.py         # Business logic
├── utils/
│   ├── __init__.py
│   └── response_generator.py   # Response formatting
├── main.py                      # Main application
├── setup_db.py                  # Database setup script
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+

### Step 1: Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Download and install from [postgresql.org](https://www.postgresql.org/download/)

### Step 2: Create Database

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database
CREATE DATABASE leave_management;

# Create user (optional)
CREATE USER leave_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE leave_management TO leave_user;

# Exit
\q
```

### Step 3: Clone and Setup Project

```bash
# Create project directory
mkdir leave_management_ai
cd leave_management_ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Step 4: Configure Database

Edit `config/settings.py` and update database credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'leave_management',
    'user': 'postgres',  # or your created user
    'password': 'your_password_here'
}
```

### Step 5: Initialize Database

```bash
python setup_db.py
```

This will:
- Create all necessary tables
- Create indexes
- Insert sample employee data
- Insert sample leave balances

## Usage

### Start the Application

```bash
python main.py
```

### Example Queries

**Apply for Leave:**
```
You: I need leave from 20th Jan to 25th Jan, EMP123
Assistant: Leave Request Summary:
Employee ID: EMP123
Leave Type: General Leave
From: 2026-01-20
To: 2026-01-25
Days: 4
Current Balance: 20.0
Balance After: 16.0

Reply 'confirm' or 'yes' to approve this leave request.

You: confirm
Assistant: ✓ Leave Approved!
Your leave from 2026-01-20 to 2026-01-25 has been granted.
Remaining Balance: 16.0 days
```

**Check Balance:**
```
You: What's my leave balance? EMP123
Assistant: Leave Balance for Employee EMP123:
Casual Leave: 12.0 days
General Leave: 16.0 days
Sick Leave: 8.0 days
Vacation Leave: 15.0 days
```

**View History:**
```
You: Show my leave history, EMP123
Assistant: Leave History for Employee EMP123:
1. General Leave
   From: 2026-01-20 To: 2026-01-25
   Days: 4.0 | Status: APPROVED
   Requested: 2026-01-10 14:30
```

### Supported Date Formats

- **Relative:** "tomorrow", "next Monday", "this Friday"
- **Specific:** "20th Jan", "January 25", "25/01/2026"
- **Ranges:** "from 20th to 25th", "20-25 Jan", "Jan 20 to Jan 25"

### Sample Employee IDs

- `EMP123` - John Doe (Engineering)
- `EMP124` - Jane Smith (Marketing)
- `EMP125` - Bob Johnson (Sales)
- `E001` - Alice Williams (HR)
- `E002` - Charlie Brown (Finance)

## Configuration

### Leave Types

Edit `config/settings.py` to add/modify leave types:

```python
LEAVE_TYPES = {
    'casual': 'Casual Leave',
    'sick': 'Sick Leave',
    'vacation': 'Vacation Leave',
    'general': 'General Leave'
}
```

### Business Rules

```python
BUSINESS_RULES = {
    'weekend_counts': False,  # Weekends don't count
    'min_leave_balance': 0,   # Can go to 0
    'max_consecutive_days': 30
}
```

## Database Schema

### Tables

1. **employees** - Employee information
2. **leave_balance** - Current leave balances
3. **leave_requests** - Leave request records
4. **leave_transactions** - Balance change audit trail
5. **pending_confirmations** - Temporary confirmation storage

## Architecture

### NLP Pipeline

1. **Intent Classification** - Identifies what the user wants to do
2. **Entity Extraction** - Extracts employee ID, dates, leave type
3. **Date Parsing** - Converts natural language dates to date objects
4. **Business Logic** - Validates and processes the request
5. **Response Generation** - Creates user-friendly responses

### Flow Diagram

```
User Input
    ↓
Intent Classification
    ↓
Entity Extraction
    ↓
Business Validation
    ↓
Database Operation
    ↓
Response Generation
    ↓
User Output
```

## Troubleshooting

### spaCy Model Not Found
```bash
python -m spacy download en_core_web_sm
```

### Database Connection Error
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify credentials in `config/settings.py`
- Ensure database exists: `psql -l`

### Module Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## Extending the System

### Add New Intent

1. Add pattern to `nlp/intent_classifier.py`
2. Create handler in `main.py`
3. Add response template in `config/settings.py`

### Add New Leave Type

1. Update `LEAVE_TYPES` in `config/settings.py`
2. Add keyword mapping in `nlp/entity_extractor.py`
3. Update sample data in `setup_db.py`

### Add Email Notifications

Create `utils/email_sender.py` and integrate with `services/leave_service.py`

## License

MIT License - Feel free to use and modify for your needs.

## Support

For issues or questions, please create an issue in the repository or contact the development team.

---

**Built with ❤️ using Python, spaCy, and PostgreSQL**

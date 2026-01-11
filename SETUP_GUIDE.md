# Complete Setup Guide - Leave Management AI

Follow these steps to set up and run the Leave Management AI system.

## Quick Start (5 Minutes)

### 1. Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Windows:**
- Download from https://www.postgresql.org/download/windows/
- Run installer and remember the password you set for 'postgres' user

### 2. Create Database

```bash
# Access PostgreSQL
sudo -u postgres psql

# Or on Windows/Mac, just:
psql -U postgres
```

Inside PostgreSQL prompt:
```sql
CREATE DATABASE leave_management;
\q
```

### 3. Setup Project

```bash
# Create project folder
mkdir leave_management_ai
cd leave_management_ai

# Create folder structure
mkdir -p config database nlp services utils

# Create __init__.py files
touch config/__init__.py
touch database/__init__.py
touch nlp/__init__.py
touch services/__init__.py
touch utils/__init__.py

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

### 4. Install Dependencies

Create `requirements.txt` with this content:
```
psycopg2-binary==2.9.9
spacy==3.7.2
python-dateutil==2.8.2
regex==2023.10.3
```

Then install:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 5. Copy All Python Files

Copy the following files from the artifacts into your project:

**Configuration:**
- `config/settings.py`

**Database:**
- `database/connection.py`
- `database/models.py`
- `database/operations.py`

**NLP:**
- `nlp/date_parser.py`
- `nlp/entity_extractor.py`
- `nlp/intent_classifier.py`

**Services:**
- `services/leave_service.py`

**Utils:**
- `utils/response_generator.py`

**Main files:**
- `main.py`
- `setup_db.py`

### 6. Configure Database Connection

Edit `config/settings.py` and update the password:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'leave_management',
    'user': 'postgres',
    'password': 'YOUR_PASSWORD_HERE'  # Change this!
}
```

### 7. Initialize Database

```bash
python setup_db.py
```

You should see:
```
✓ Table created successfully (5 times)
✓ Employee EMP123 added
✓ Leave balance added...
✓ Database setup completed successfully!
```

### 8. Run the Application

```bash
python main.py
```

### 9. Test It!

Try these commands:

```
You: I need leave from tomorrow to next Friday, EMP123

You: confirm

You: What's my leave balance? EMP123

You: Show my leave history, EMP123
```

## Complete File Structure

After setup, your directory should look like this:

```
leave_management_ai/
├── venv/                        # Virtual environment
├── config/
│   ├── __init__.py
│   └── settings.py
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── models.py
│   └── operations.py
├── nlp/
│   ├── __init__.py
│   ├── date_parser.py
│   ├── entity_extractor.py
│   └── intent_classifier.py
├── services/
│   ├── __init__.py
│   └── leave_service.py
├── utils/
│   ├── __init__.py
│   └── response_generator.py
├── main.py
├── setup_db.py
├── requirements.txt
└── README.md
```

## Troubleshooting

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "Can't connect to PostgreSQL"
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list               # Mac

# Start if not running
sudo systemctl start postgresql  # Linux
brew services start postgresql   # Mac
```

### Error: "FATAL: database 'leave_management' does not exist"
```bash
sudo -u postgres psql
CREATE DATABASE leave_management;
\q
```

### Error: "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

### Error: Module import errors
Make sure you're in the project root directory and virtual environment is activated:
```bash
cd leave_management_ai
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

## Testing Different Scenarios

### 1. Apply for Leave
```
I will be on leave from 25th January to 30th January, EMP123
```

### 2. With Leave Type
```
I need sick leave from tomorrow to next Monday, EMP124
I want casual leave on 15th Feb, E001
```

### 3. Different Date Formats
```
Leave from 1st to 5th March, EMP125
I'll be away from 10/02/2026 to 15/02/2026, E002
On leave next Friday, EMP123
```

### 4. Check Balance
```
What's my leave balance? EMP123
How many leaves do I have? EMP124
Show my balance, E001
```

### 5. View History
```
Show my leave history, EMP123
Display my past leaves, EMP124
```

### 6. Confirmation Flow
```
User: Leave from 20th to 25th, EMP123
AI: [Shows summary] Reply 'confirm' or 'yes'...
User: yes
AI: ✓ Leave Approved!
```

### 7. Cancellation
```
User: Leave from 20th to 25th, EMP123
AI: [Shows summary]
User: no
AI: Your pending leave request has been cancelled.
```

## Adding Your Own Employees

### Method 1: Via PostgreSQL
```bash
sudo -u postgres psql leave_management
```

```sql
INSERT INTO employees (employee_id, name, email, department, join_date)
VALUES ('EMP999', 'Your Name', 'your.email@company.com', 'IT', '2024-01-01');

INSERT INTO leave_balance (employee_id, leave_type, balance)
VALUES 
    ('EMP999', 'casual', 12),
    ('EMP999', 'sick', 10),
    ('EMP999', 'vacation', 15),
    ('EMP999', 'general', 20);
```

### Method 2: Modify setup_db.py
Edit the `employees` list and run `python setup_db.py` again.

## Production Deployment Tips

1. **Use Environment Variables** for database credentials
2. **Add Authentication** layer for multi-user access
3. **Implement Logging** for audit trails
4. **Add Email Notifications** for leave approvals
5. **Create Web Interface** using Flask/Django
6. **Add Manager Approval** workflow
7. **Implement Rate Limiting** for API protection

## Next Steps

1. ✅ Basic setup complete
2. 🔧 Customize leave types and business rules
3. 📧 Add email notifications
4. 🌐 Build web interface
5. 👥 Add manager approval workflow
6. 📊 Create analytics dashboard
7. 🔐 Implement authentication

## Need Help?

- Check PostgreSQL logs: `/var/log/postgresql/`
- Check Python errors: Run with `python -v main.py`
- Database issues: `psql -U postgres -d leave_management`

---

**You're all set! 🚀 Start managing leaves with AI!**
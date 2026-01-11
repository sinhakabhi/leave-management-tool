# Leave Management AI - Complete System Summary

## 📋 Table of Contents
1. [Valid User Messages](#valid-user-messages)
2. [System Response Patterns](#system-response-patterns)
3. [File Structure](#file-structure)
4. [Workflow Diagram](#workflow-diagram)

---

## 🎯 Valid User Messages

### 1. **Apply for Leave**

**Intent:** Request time off from work

**Valid Message Patterns:**
```
✅ I need leave from 20th to 25th
✅ I need leave from tomorrow to Friday
✅ I want leave on 20th January
✅ Apply for leave from 1st Feb to 5th Feb
✅ I'll be on leave next Monday to Wednesday
✅ Request sick leave from 15th to 20th
✅ I need casual leave on 25th
✅ Going on vacation from 1st to 10th March
✅ Will be away from tomorrow to next week
✅ Need time off from 10/01/2026 to 15/01/2026
```

**Supported Date Formats:**
- Relative: `tomorrow`, `next Monday`, `this Friday`
- Specific: `20th Jan`, `January 25`, `25th`
- Absolute: `20/01/2026`, `01-20-2026`
- Ranges: `from 20th to 25th`, `20-25 Jan`

**Supported Leave Types** (auto-detected):
- **Casual Leave:** Contains words: `casual`, `cl`
- **Sick Leave:** Contains words: `sick`, `medical`, `sl`, `health`
- **Vacation Leave:** Contains words: `vacation`, `holiday`, `vl`
- **General Leave:** Default if no type mentioned

**System Response:**
```
📋 Leave Request Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Leave Type: General Leave
Period: 2026-01-20 to 2026-01-25
Duration: 4 day(s)

💼 Leave Balance:
Current: 20 days
After deduction: 16 days
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type 'yes' or 'confirm' to approve this request.
```

**If Insufficient Balance:**
```
❌ Insufficient Leave Balance

Available: 5 days
Requested: 10 days
Shortage: 5 days

Please adjust your leave dates or choose a different leave type.
```

---

### 2. **Confirm Leave Request**

**Intent:** Approve a pending leave request

**Valid Message Patterns:**
```
✅ yes
✅ confirm
✅ ok
✅ okay
✅ sure
✅ approved
✅ accept
✅ proceed
✅ go ahead
```

**System Response (Success):**
```
✅ Leave Approved!

Your leave from 2026-01-20 to 2026-01-25 has been granted.
Remaining balance: 16 days

Have a great time off! 🌴
```

**System Response (No Pending Request):**
```
There is no pending leave request to confirm. 
Please create a new leave request first.
```

---

### 3. **Cancel Pending Request**

**Intent:** Cancel a leave request before confirmation

**Valid Message Patterns:**
```
✅ no
✅ cancel
✅ reject
✅ deny
✅ decline
✅ nevermind
✅ don't want
```

**System Response:**
```
Your pending leave request has been cancelled.
```

---

### 4. **Check Leave Balance**

**Intent:** View available leave days

**Valid Message Patterns:**
```
✅ What's my leave balance?
✅ How many leaves do I have?
✅ Show my balance
✅ Check my leave balance
✅ Tell me my balance
✅ How much leave do I have left?
✅ Show remaining leaves
✅ My balance
```

**System Response:**
```
💼 Your Leave Balance:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 Casual Leave: 12 days
🟢 General Leave: 20 days
🟡 Sick Leave: 8 days
🟢 Vacation Leave: 15 days
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Legend:
🟢 = 10+ days (Healthy)
🟡 = 5-9 days (Low)
🔴 = <5 days (Critical)
```

---

### 5. **View Leave History**

**Intent:** See past leave requests

**Valid Message Patterns:**
```
✅ Show my leave history
✅ View my history
✅ Display my past leaves
✅ My leave requests
✅ Check my history
✅ Show past leaves
✅ Leave history
✅ My requests
```

**System Response:**
```
📋 Your Leave History:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ✅ General Leave
   📅 2026-01-20 → 2026-01-25 (4 days)
   🕐 Requested on 2026-01-10 14:30

2. ✅ Sick Leave
   📅 2026-01-15 → 2026-01-16 (2 days)
   🕐 Requested on 2026-01-14 09:15

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If No History:**
```
📋 No leave history found.

You haven't taken any leaves yet.
```

---

### 6. **System Commands**

**Valid Commands:**
```
✅ logout / switch / change employee   → Switch to different employee
✅ quit / exit / bye                   → Exit the application
```

---

### 7. **Out of Scope Messages**

**Intent:** Anything the system doesn't understand

**Examples of Invalid Messages:**
```
❌ Book a flight
❌ Send email to manager
❌ Update my profile
❌ Random text without clear intent
```

**System Response:**
```
I'm not sure I understood that. I can help you with:

  • Applying for leave (e.g., 'I need leave from 20th to 25th')
  • Checking your leave balance (e.g., 'What's my balance?')
  • Viewing leave history (e.g., 'Show my leave history')

What would you like to do?
```

---

## 🔄 System Response Patterns

### Response Flow Chart

```
User Message
    ↓
[Login Check]
    ↓ (not logged in)
    → Request Employee ID → Validate → Welcome Message
    ↓ (logged in)
[Intent Classification]
    ↓
┌───────────────┬──────────────┬───────────────┬──────────────┬────────────┐
│  Apply Leave  │   Confirm    │    Cancel     │ Check Balance│  History   │
└───────┬───────┴──────┬───────┴───────┬───────┴──────┬───────┴─────┬──────┘
        ↓              ↓               ↓              ↓             ↓
  [Extract Dates] [Check Pending] [Clear Pending] [Get Balance] [Get Records]
        ↓              ↓               ↓              ↓             ↓
  [Validate Dates] [Deduct Balance] [Confirm] [Format Display] [Format List]
        ↓              ↓               ↓              ↓             ↓
  [Check Balance] [Log Transaction]    │              │             │
        ↓              ↓               ↓              ↓             ↓
  [Create Pending] [Success Msg] [Cancel Msg]  [Balance Msg]  [History Msg]
        ↓
  [Show Summary]
  [Wait for Confirm]
```

---

## 📁 File Structure

### Complete Directory Layout

```
leave_management_ai/
│
├── config/
│   ├── __init__.py                  # Package initializer
│   └── settings.py                  # Configuration settings
│       ├── DB_CONFIG               # Database credentials
│       ├── LEAVE_TYPES             # Leave type mappings
│       ├── BUSINESS_RULES          # Business logic rules
│       ├── NLP_CONFIG              # NLP settings
│       └── RESPONSE_TEMPLATES      # Response message templates
│
├── database/
│   ├── __init__.py                  # Package initializer
│   ├── connection.py                # PostgreSQL connection pool
│   │   ├── DatabaseConnection      # Singleton connection manager
│   │   ├── get_db_connection()     # Helper function
│   │   └── execute_query()         # Query execution helper
│   │
│   ├── models.py                    # Database schema definitions
│   │   ├── CREATE_EMPLOYEES_TABLE
│   │   ├── CREATE_LEAVE_BALANCE_TABLE
│   │   ├── CREATE_LEAVE_REQUESTS_TABLE
│   │   ├── CREATE_LEAVE_TRANSACTIONS_TABLE
│   │   ├── CREATE_PENDING_CONFIRMATIONS_TABLE
│   │   └── CREATE_INDEXES
│   │
│   └── operations.py                # CRUD operations
│       ├── EmployeeOperations      # Employee-related queries
│       ├── LeaveBalanceOperations  # Balance management
│       ├── LeaveRequestOperations  # Request handling
│       ├── LeaveTransactionOperations  # Transaction logging
│       └── PendingConfirmationOperations  # Pending requests
│
├── nlp/
│   ├── __init__.py                  # Package initializer
│   │
│   ├── intent_classifier.py        # Intent detection
│   │   └── IntentClassifier
│   │       ├── classify()          # Classify user intent
│   │       └── get_confidence()    # Get confidence score
│   │
│   ├── entity_extractor.py         # Entity extraction
│   │   └── EntityExtractor
│   │       ├── extract_employee_id()    # Extract employee ID
│   │       ├── extract_dates()          # Extract date range
│   │       ├── extract_leave_type()     # Extract leave type
│   │       └── extract_all_entities()   # Extract all entities
│   │
│   └── date_parser.py               # Natural language date parsing
│       └── DateParser
│           ├── parse_single_date()      # Parse single date
│           ├── parse_date_range()       # Parse date range
│           └── calculate_business_days()  # Calculate working days
│
├── services/
│   ├── __init__.py                  # Package initializer
│   └── leave_service.py             # Business logic
│       └── LeaveService
│           ├── validate_employee()          # Validate employee exists
│           ├── check_leave_eligibility()    # Check if enough balance
│           ├── create_leave_request()       # Create pending request
│           ├── confirm_leave_request()      # Confirm and apply leave
│           ├── get_leave_balance()          # Get all balances
│           ├── get_leave_history()          # Get leave history
│           └── cancel_pending_request()     # Cancel pending request
│
├── utils/
│   ├── __init__.py                  # Package initializer
│   └── response_generator.py       # Response formatting
│       └── ResponseGenerator
│           ├── generate_leave_request_response()
│           ├── generate_confirmation_response()
│           ├── generate_balance_response()
│           ├── generate_history_response()
│           ├── generate_error_response()
│           ├── generate_out_of_scope_response()
│           ├── generate_cancellation_response()
│           └── generate_no_pending_response()
│
├── main.py                          # Main application entry point
│   └── LeaveManagementAI
│       ├── set_employee_id()        # Login employee
│       ├── process_query()          # Main query processor
│       ├── _handle_leave_application()
│       ├── _handle_leave_confirmation()
│       ├── _handle_cancellation()
│       ├── _handle_balance_check()
│       └── _handle_leave_history()
│
├── setup_db.py                      # Database initialization
│   ├── create_tables()              # Create all tables
│   ├── create_indexes()             # Create indexes
│   ├── insert_sample_data()         # Insert sample employees
│   └── verify_setup()               # Verify database setup
│
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
├── SETUP_GUIDE.md                  # Installation guide
├── EXAMPLE_SESSIONS.md             # Example conversations
└── SYSTEM_SUMMARY.md               # This file
```

---

## 🗄️ Database Schema

### Tables Overview

#### 1. **employees**
```sql
employee_id   VARCHAR(20)   PRIMARY KEY
name          VARCHAR(100)  NOT NULL
email         VARCHAR(100)
department    VARCHAR(50)
join_date     DATE
created_at    TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
```

#### 2. **leave_balance**
```sql
id            SERIAL        PRIMARY KEY
employee_id   VARCHAR(20)   REFERENCES employees(employee_id)
leave_type    VARCHAR(20)   NOT NULL
balance       DECIMAL(5,2)  NOT NULL DEFAULT 0
updated_at    TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
UNIQUE(employee_id, leave_type)
```

#### 3. **leave_requests**
```sql
id            SERIAL        PRIMARY KEY
employee_id   VARCHAR(20)   REFERENCES employees(employee_id)
leave_type    VARCHAR(20)   NOT NULL
start_date    DATE          NOT NULL
end_date      DATE          NOT NULL
days_count    DECIMAL(5,2)  NOT NULL
status        VARCHAR(20)   DEFAULT 'pending'
reason        TEXT
requested_at  TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
approved_at   TIMESTAMP
```

#### 4. **leave_transactions**
```sql
id               SERIAL        PRIMARY KEY
employee_id      VARCHAR(20)   REFERENCES employees(employee_id)
leave_type       VARCHAR(20)   NOT NULL
transaction_type VARCHAR(20)   NOT NULL
amount           DECIMAL(5,2)  NOT NULL
balance_before   DECIMAL(5,2)  NOT NULL
balance_after    DECIMAL(5,2)  NOT NULL
description      TEXT
transaction_date TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
```

#### 5. **pending_confirmations**
```sql
id            SERIAL        PRIMARY KEY
employee_id   VARCHAR(20)   REFERENCES employees(employee_id)
leave_type    VARCHAR(20)   NOT NULL
start_date    DATE          NOT NULL
end_date      DATE          NOT NULL
days_count    DECIMAL(5,2)  NOT NULL
created_at    TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
expires_at    TIMESTAMP     NOT NULL
```

---

## 🎬 Workflow Diagram

### Complete User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                    START APPLICATION                            │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
                    ┌────────────────┐
                    │  Enter EMP ID  │
                    └────────┬───────┘
                             ↓
                    ┌────────────────┐
                    │  Validate ID   │
                    └────┬───────┬───┘
                         │       │
                    Valid│       │Invalid
                         ↓       ↓
                ┌──────────┐  ┌──────────┐
                │ Welcome! │  │  Error   │
                │ Login    │  │  Retry   │
                └────┬─────┘  └────┬─────┘
                     │             │
                     │             └──────┐
                     ↓                    ↓
            ┌────────────────┐    ┌────────────┐
            │  User Message  │←───│  Re-enter  │
            └────────┬───────┘    └────────────┘
                     ↓
        ┌────────────────────────┐
        │  Classify Intent (NLP) │
        └────────┬───────────────┘
                 ↓
    ┌────────────┴────────────┐
    │  Extract Entities (NLP) │
    │  - Dates                │
    │  - Leave Type           │
    │  - Employee ID          │
    └────────────┬────────────┘
                 ↓
┌────────────────┴────────────────┐
│      Route to Handler           │
└─┬──────┬──────┬──────┬──────┬──┘
  │      │      │      │      │
  ↓      ↓      ↓      ↓      ↓
Apply  Confirm Cancel Balance History
Leave          
  │
  ↓
┌──────────────────┐
│ Extract Dates    │
│ from NLP         │
└────────┬─────────┘
         ↓
    Valid Dates?
         ├─No──→ Error: "Specify dates clearly"
         │
        Yes
         ↓
┌──────────────────┐
│ Check Balance    │
│ Eligibility      │
└────────┬─────────┘
         ↓
   Enough Balance?
         ├─No──→ Error: "Insufficient balance"
         │
        Yes
         ↓
┌──────────────────┐
│ Create Pending   │
│ Request          │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Show Summary     │
│ Wait Confirmation│
└────────┬─────────┘
         ↓
    User Confirms?
         ├─No──→ Cancel Request
         │
        Yes
         ↓
┌──────────────────┐
│ Apply Leave:     │
│ 1. Create Record │
│ 2. Deduct Balance│
│ 3. Log Trans.    │
│ 4. Clear Pending │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Success Message  │
│ Show New Balance │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Back to Input    │
│ (Session Active) │
└──────────────────┘
```

---

## 🔐 Session Management

### Login Flow
1. User enters Employee ID
2. System validates against `employees` table
3. If valid: Store in session, show welcome message
4. If invalid: Show error, ask to re-enter
5. Session persists until `logout` or `quit`

### Session Features
- **Persistent ID:** No need to repeat in messages
- **Logout:** Switch to different employee
- **Quit:** Exit application

---

## 🎨 Response Design Principles

### Visual Elements Used
- **Emojis:** 📋 ✅ ❌ 💼 🟢 🟡 🔴 📅 🕐 🌴
- **Unicode Boxes:** `━` for separators
- **Status Indicators:** 
  - ✅ Approved
  - ⏳ Pending
  - 🟢 Healthy balance (10+)
  - 🟡 Low balance (5-9)
  - 🔴 Critical balance (<5)

### Formatting Standards
- Clear sections with separators
- Consistent spacing
- Color-coded information
- Friendly, professional tone

---

## 🚀 Quick Reference

### User Intent → System Action

| User Intent | Keywords | System Action |
|------------|----------|---------------|
| Apply Leave | need, want, apply, take, book, going, will be | Extract dates → Check balance → Create pending |
| Confirm | yes, confirm, ok, approve, accept | Apply leave → Deduct balance → Log transaction |
| Cancel | no, cancel, reject, deny | Clear pending request |
| Check Balance | balance, how many, how much, remaining | Query balance → Format display |
| View History | history, past, previous, requests | Query records → Format list |
| Logout | logout, switch, change | Clear session → Return to login |
| Quit | quit, exit, bye | Close application |

---

## 📊 Sample Data Included

### Employees
- **EMP123** - John Doe (Engineering) - 20 general leaves
- **EMP124** - Jane Smith (Marketing) - 18 general leaves
- **EMP125** - Bob Johnson (Sales) - 15 general leaves
- **E001** - Alice Williams (HR) - 25 general leaves
- **E002** - Charlie Brown (Finance) - 22 general leaves

### Leave Types Per Employee
Each employee has:
- Casual Leave
- Sick Leave
- Vacation Leave
- General Leave

---

## 🎯 Key Features Summary

1. ✅ **Session-Based Login** - Login once, chat naturally
2. ✅ **Natural Language Processing** - Understands conversational queries
3. ✅ **Smart Date Parsing** - Handles multiple date formats
4. ✅ **Two-Step Confirmation** - Prevents accidental requests
5. ✅ **Visual Balance Indicators** - Color-coded balance levels
6. ✅ **Complete Audit Trail** - All transactions logged
7. ✅ **Multiple Leave Types** - Casual, Sick, Vacation, General
8. ✅ **Business Rules** - Weekend handling, max days
9. ✅ **Error Handling** - Clear, helpful error messages
10. ✅ **Beautiful Formatting** - Professional, easy-to-read responses

---

**That's the complete system! 🎉**
"""
Database schema definitions and table creation
"""

# SQL Schema for the database tables

CREATE_EMPLOYEES_TABLE = """
CREATE TABLE IF NOT EXISTS employees (
    employee_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    department VARCHAR(50),
    join_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_LEAVE_BALANCE_TABLE = """
CREATE TABLE IF NOT EXISTS leave_balance (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(20) REFERENCES employees(employee_id) ON DELETE CASCADE,
    leave_type VARCHAR(20) NOT NULL,
    balance DECIMAL(5, 2) NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(employee_id, leave_type)
);
"""

CREATE_LEAVE_REQUESTS_TABLE = """
CREATE TABLE IF NOT EXISTS leave_requests (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(20) REFERENCES employees(employee_id) ON DELETE CASCADE,
    leave_type VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    days_count DECIMAL(5, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    reason TEXT,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP
);
"""

CREATE_LEAVE_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS leave_transactions (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(20) REFERENCES employees(employee_id) ON DELETE CASCADE,
    leave_type VARCHAR(20) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount DECIMAL(5, 2) NOT NULL,
    balance_before DECIMAL(5, 2) NOT NULL,
    balance_after DECIMAL(5, 2) NOT NULL,
    description TEXT,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_PENDING_CONFIRMATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS pending_confirmations (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(20) REFERENCES employees(employee_id) ON DELETE CASCADE,
    leave_type VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    days_count DECIMAL(5, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);
"""

# Index creation for better performance
CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_leave_requests_employee ON leave_requests(employee_id);",
    "CREATE INDEX IF NOT EXISTS idx_leave_requests_status ON leave_requests(status);",
    "CREATE INDEX IF NOT EXISTS idx_leave_balance_employee ON leave_balance(employee_id);",
    "CREATE INDEX IF NOT EXISTS idx_leave_transactions_employee ON leave_transactions(employee_id);",
    "CREATE INDEX IF NOT EXISTS idx_pending_confirmations_employee ON pending_confirmations(employee_id);"
]

# Sample data insertion queries
INSERT_SAMPLE_EMPLOYEE = """
INSERT INTO employees (employee_id, name, email, department, join_date)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (employee_id) DO NOTHING;
"""

INSERT_LEAVE_BALANCE = """
INSERT INTO leave_balance (employee_id, leave_type, balance)
VALUES (%s, %s, %s)
ON CONFLICT (employee_id, leave_type) 
DO UPDATE SET balance = EXCLUDED.balance;
"""

# All table creation queries in order
ALL_TABLES = [
    CREATE_EMPLOYEES_TABLE,
    CREATE_LEAVE_BALANCE_TABLE,
    CREATE_LEAVE_REQUESTS_TABLE,
    CREATE_LEAVE_TRANSACTIONS_TABLE,
    CREATE_PENDING_CONFIRMATIONS_TABLE
]
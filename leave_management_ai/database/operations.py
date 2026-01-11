"""
Database CRUD operations
"""
from datetime import datetime, timedelta
from leave_management_ai.database.connection import execute_query, get_db_connection, DatabaseConnection


class EmployeeOperations:
    """Employee-related database operations"""
    
    @staticmethod
    def get_employee(employee_id):
        """Get employee details by ID"""
        query = "SELECT * FROM employees WHERE employee_id = %s;"
        results = execute_query(query, (employee_id,), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def employee_exists(employee_id):
        """Check if employee exists"""
        employee = EmployeeOperations.get_employee(employee_id)
        return employee is not None


class LeaveBalanceOperations:
    """Leave balance operations"""
    
    @staticmethod
    def get_balance(employee_id, leave_type='general'):
        """Get leave balance for specific type"""
        query = """
        SELECT balance FROM leave_balance 
        WHERE employee_id = %s AND leave_type = %s;
        """
        results = execute_query(query, (employee_id, leave_type), fetch=True)
        return float(results[0][0]) if results else 0.0
    
    @staticmethod
    def get_all_balances(employee_id):
        """Get all leave balances for an employee"""
        query = """
        SELECT leave_type, balance FROM leave_balance 
        WHERE employee_id = %s ORDER BY leave_type;
        """
        results = execute_query(query, (employee_id,), fetch=True)
        return {row[0]: float(row[1]) for row in results}
    
    @staticmethod
    def update_balance(employee_id, leave_type, new_balance):
        """Update leave balance"""
        query = """
        INSERT INTO leave_balance (employee_id, leave_type, balance, updated_at)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (employee_id, leave_type) 
        DO UPDATE SET balance = EXCLUDED.balance, updated_at = CURRENT_TIMESTAMP;
        """
        execute_query(query, (employee_id, leave_type, new_balance))
    
    @staticmethod
    def deduct_balance(employee_id, leave_type, days):
        """Deduct days from leave balance"""
        current = LeaveBalanceOperations.get_balance(employee_id, leave_type)
        new_balance = current - days
        LeaveBalanceOperations.update_balance(employee_id, leave_type, new_balance)
        return new_balance


class LeaveRequestOperations:
    """Leave request operations"""
    
    @staticmethod
    def create_request(employee_id, leave_type, start_date, end_date, days_count, reason=None):
        """Create a new leave request"""
        query = """
        INSERT INTO leave_requests 
        (employee_id, leave_type, start_date, end_date, days_count, reason, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'approved')
        RETURNING id;
        """
        db = DatabaseConnection()
        conn = db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (employee_id, leave_type, start_date, end_date, days_count, reason))
            request_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return request_id
        finally:
            db.return_connection(conn)
    
    @staticmethod
    def get_employee_requests(employee_id, limit=10):
        """Get recent leave requests for an employee"""
        query = """
        SELECT id, leave_type, start_date, end_date, days_count, status, requested_at
        FROM leave_requests 
        WHERE employee_id = %s 
        ORDER BY requested_at DESC 
        LIMIT %s;
        """
        results = execute_query(query, (employee_id, limit), fetch=True)
        return results
    
    @staticmethod
    def check_overlapping_leaves(employee_id, start_date, end_date):
        """Check if there are existing approved leaves overlapping with the date range"""
        query = """
        SELECT id, leave_type, start_date, end_date, days_count
        FROM leave_requests
        WHERE employee_id = %s 
        AND status = 'approved'
        AND (
            (start_date <= %s AND end_date >= %s) OR
            (start_date <= %s AND end_date >= %s) OR
            (start_date >= %s AND end_date <= %s)
        );
        """
        results = execute_query(query, (employee_id, end_date, end_date, start_date, start_date, start_date, end_date), fetch=True)
        return results
    
    @staticmethod
    def get_future_leaves(employee_id, from_date):
        """Get future approved leaves after a specific date"""
        query = """
        SELECT id, leave_type, start_date, end_date, days_count, requested_at
        FROM leave_requests
        WHERE employee_id = %s 
        AND status = 'approved'
        AND start_date > %s
        ORDER BY start_date ASC;
        """
        results = execute_query(query, (employee_id, from_date), fetch=True)
        return results
    
    @staticmethod
    def get_leaves_in_range(employee_id, start_date, end_date):
        """Get approved leaves in a specific date range"""
        query = """
        SELECT id, leave_type, start_date, end_date, days_count
        FROM leave_requests
        WHERE employee_id = %s 
        AND status = 'approved'
        AND start_date >= %s 
        AND end_date <= %s
        ORDER BY start_date ASC;
        """
        results = execute_query(query, (employee_id, start_date, end_date), fetch=True)
        return results
    
    @staticmethod
    def cancel_leave_request(request_id):
        """Cancel an approved leave request"""
        query = """
        UPDATE leave_requests 
        SET status = 'cancelled'
        WHERE id = %s AND status = 'approved'
        RETURNING id, employee_id, leave_type, start_date, end_date, days_count;
        """
        db = DatabaseConnection()
        conn = db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (request_id,))
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
            return result
        finally:
            db.return_connection(conn)


class LeaveTransactionOperations:
    """Leave transaction logging"""
    
    @staticmethod
    def log_transaction(employee_id, leave_type, transaction_type, amount, 
                       balance_before, balance_after, description=None):
        """Log a leave balance transaction"""
        query = """
        INSERT INTO leave_transactions 
        (employee_id, leave_type, transaction_type, amount, balance_before, balance_after, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        execute_query(query, (employee_id, leave_type, transaction_type, amount, 
                             balance_before, balance_after, description))


class PendingConfirmationOperations:
    """Operations for pending leave confirmations"""
    
    @staticmethod
    def create_pending(employee_id, leave_type, start_date, end_date, days_count):
        """Create a pending confirmation"""
        # Clear any existing pending confirmations for this employee
        PendingConfirmationOperations.clear_pending(employee_id)
        
        query = """
        INSERT INTO pending_confirmations 
        (employee_id, leave_type, start_date, end_date, days_count, expires_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        expires_at = datetime.now() + timedelta(minutes=15)  # 15 minute expiry
        
        db = DatabaseConnection()
        conn = db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (employee_id, leave_type, start_date, end_date, 
                                  days_count, expires_at))
            pending_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return pending_id
        finally:
            db.return_connection(conn)
    
    @staticmethod
    def get_pending(employee_id):
        """Get pending confirmation for employee"""
        query = """
        SELECT leave_type, start_date, end_date, days_count 
        FROM pending_confirmations 
        WHERE employee_id = %s AND expires_at > CURRENT_TIMESTAMP
        ORDER BY created_at DESC LIMIT 1;
        """
        results = execute_query(query, (employee_id,), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def clear_pending(employee_id):
        """Clear pending confirmations for employee"""
        query = "DELETE FROM pending_confirmations WHERE employee_id = %s;"
        execute_query(query, (employee_id,))
"""
Database setup and initialization script
Run this script to create tables and populate sample data
"""
from datetime import datetime, timedelta

from leave_management_ai.database.connection import DatabaseConnection, execute_query
from leave_management_ai.database.models import ALL_TABLES, CREATE_INDEXES, INSERT_LEAVE_BALANCE, INSERT_SAMPLE_EMPLOYEE


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    
    for table_sql in ALL_TABLES:
        try:
            execute_query(table_sql)
            print("✓ Table created successfully")
        except Exception as e:
            print(f"✗ Error creating table: {e}")
            return False
    
    return True


def create_indexes():
    """Create database indexes"""
    print("\nCreating indexes...")
    
    for index_sql in CREATE_INDEXES:
        try:
            execute_query(index_sql)
            print("✓ Index created successfully")
        except Exception as e:
            print(f"⚠ Warning creating index: {e}")
    
    return True


def insert_sample_data():
    """Insert sample employees and leave balances"""
    print("\nInserting sample data...")
    
    # Sample employees
    employees = [
        ('EMP101', 'John Doe', 'john.doe@company.com', 'Engineering', '2022-01-15'),
        ('EMP102', 'Jane Smith', 'jane.smith@company.com', 'Marketing', '2021-06-20'),
        ('EMP103', 'Bob Johnson', 'bob.johnson@company.com', 'Sales', '2023-03-10'),
        ('EMP104', 'Alice Williams', 'alice.w@company.com', 'HR', '2020-09-01'),
        ('EMP105', 'Charlie Brown', 'charlie.b@company.com', 'Finance', '2022-11-15'),
    ]
    
    for emp in employees:
        try:
            execute_query(INSERT_SAMPLE_EMPLOYEE, emp)
            print(f"✓ Employee {emp[0]} added")
        except Exception as e:
            print(f"⚠ Warning: {e}")
    
    # Sample leave balances
    leave_balances = [
        # EMP101
        ('EMP101', 'casual', 12),
        ('EMP101', 'sick', 8),
        ('EMP101', 'vacation', 15),
        ('EMP101', 'general', 20),
        # EMP102
        ('EMP102', 'casual', 10),
        ('EMP102', 'sick', 10),
        ('EMP102', 'vacation', 12),
        ('EMP102', 'general', 18),
        # EMP103
        ('EMP103', 'casual', 8),
        ('EMP103', 'sick', 6),
        ('EMP103', 'vacation', 10),
        ('EMP103', 'general', 15),
        # EMP104
        ('EMP104', 'casual', 15),
        ('EMP104', 'sick', 12),
        ('EMP104', 'vacation', 20),
        ('EMP104', 'general', 25),
        # EMP105
        ('EMP105', 'casual', 11),
        ('EMP105', 'sick', 9),
        ('EMP105', 'vacation', 14),
        ('EMP105', 'general', 22),
    ]
    
    for balance in leave_balances:
        try:
            execute_query(INSERT_LEAVE_BALANCE, balance)
            print(f"✓ Leave balance added for {balance[0]} - {balance[1]}: {balance[2]} days")
        except Exception as e:
            print(f"⚠ Warning: {e}")
    
    return True


def verify_setup():
    """Verify database setup"""
    print("\nVerifying setup...")
    
    try:
        # Check employees
        result = execute_query("SELECT COUNT(*) FROM employees;", fetch=True)
        emp_count = result[0][0] if result else 0
        print(f"✓ Employees in database: {emp_count}")
        
        # Check leave balances
        result = execute_query("SELECT COUNT(*) FROM leave_balance;", fetch=True)
        balance_count = result[0][0] if result else 0
        print(f"✓ Leave balance records: {balance_count}")
        
        return True
    except Exception as e:
        print(f"✗ Verification error: {e}")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("     LEAVE MANAGEMENT AI - DATABASE SETUP")
    print("=" * 60)
    print()
    
    try:
        # Create tables
        if not create_tables():
            print("\n❌ Failed to create tables. Please check your database connection.")
            return
        
        # Create indexes
        create_indexes()
        
        # Insert sample data
        insert_sample_data()
        
        # Verify setup
        verify_setup()
        
        print("\n" + "=" * 60)
        print("✓ Database setup completed successfully!")
        print("=" * 60)
        print("\nYou can now run the main application:")
        print("  python main.py")
        print("\nSample Employee IDs you can use:")
        print("  - EMP101 (John Doe)")
        print("  - EMP102 (Jane Smith)")
        print("  - EMP103 (Bob Johnson)")
        print("  - EMP104 (Alice Williams)")
        print("  - EMP105 (Charlie Brown)")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("\nPlease check:")
        print("1. PostgreSQL is running")
        print("2. Database credentials in config/settings.py are correct")
        print("3. Database 'leave_management' exists (create it if needed)")
    finally:
        # Close connections
        db = DatabaseConnection()
        db.close_all_connections()


if __name__ == "__main__":
    main()
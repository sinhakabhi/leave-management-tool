"""
PostgreSQL database connection handler
"""
import psycopg2
from psycopg2 import pool
from leave_management_ai.config.settings import DB_CONFIG


class DatabaseConnection:
    """Singleton database connection pool manager"""
    
    _instance = None
    _connection_pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize_pool()
        return cls._instance
    
    def _initialize_pool(self):
        """Initialize connection pool"""
        try:
            self._connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,  # min and max connections
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                database=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            print("✓ Database connection pool created successfully")
        except Exception as e:
            print(f"✗ Error creating connection pool: {e}")
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        try:
            return self._connection_pool.getconn()
        except Exception as e:
            print(f"✗ Error getting connection: {e}")
            raise
    
    def return_connection(self, connection):
        """Return connection to the pool"""
        self._connection_pool.putconn(connection)
    
    def close_all_connections(self):
        """Close all connections in the pool"""
        if self._connection_pool:
            self._connection_pool.closeall()
            print("✓ All database connections closed")


def get_db_connection():
    """Helper function to get database connection"""
    db = DatabaseConnection()
    return db.get_connection()


def execute_query(query, params=None, fetch=False):
    """
    Execute a database query with automatic connection management
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or dict)
        fetch: Whether to fetch results (True for SELECT)
    
    Returns:
        Query results if fetch=True, else None
    """
    db = DatabaseConnection()
    connection = None
    
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(query, params)
        
        if fetch:
            results = cursor.fetchall()
            cursor.close()
            return results
        else:
            connection.commit()
            cursor.close()
            return None
            
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"✗ Database error: {e}")
        raise
    finally:
        if connection:
            db.return_connection(connection)
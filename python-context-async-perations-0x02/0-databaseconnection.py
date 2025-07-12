import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv   

load_dotenv()   # reads .env into process env 

class DatabaseConnection:
    """
    Custom context manager to handle MySQL database connections.
    Opens connection on __enter__, commits/rolls back and closes on __exit__.
    """


    def __init__(self):
        # pull credentials from environment
        self.config = {
            "host":     os.getenv("DB_HOST"),
            "user":     os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
        }
        self.conn   = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn   = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor                      
        except Error as e:
            print("  MySQL connection error:", e)
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:          # an exception happened
                self.conn.rollback()
            else:                 # success, commit writes
                self.conn.commit()
            self.cursor.close()
            self.conn.close()
        return False              # propagate exceptions if any


# Example usage

if __name__ == "__main__":
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("Query results:")
        for row in rows:
            print(row)

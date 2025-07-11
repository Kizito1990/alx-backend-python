import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    """
    Custom context manager to handle MySQL database connections.
    Opens connection on __enter__, commits/rolls back and closes on __exit__.
    """

    def __init__(self, host, user, password, database):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except Error as e:
            print("Error connecting to MySQL:", e)
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.cursor.close()
            self.conn.close()
        return False  # Don't suppress exceptions


# Replace these with your actual MySQL credentials
HOST = "localhost"
USER = "root"
PASSWORD = "mypass"
DATABASE = "mypass"

with DatabaseConnection(HOST, USER, PASSWORD, DATABASE) as cursor:
    # Run SELECT query
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()

    # Print the results
    print("Query Results:")
    for row in results:
        print(row)

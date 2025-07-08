import sqlite3
import functools

# Decorator that opens and closes the DB connection
def with_db_connection(my_func):
    @functools.wraps(my_func)
    def wrapper(*args, **kwargs):
        # Open connection to the database
        my_connection = sqlite3.connect('users.db')
        try:
            # Call the decorated function and pass the connection as first argument
            return my_func(my_connection, *args, **kwargs)
        finally:
            # Ensure the connection is always closed after the function runs
            my_connection.close()
    return wrapper

# Function that fetches a user by ID using the decorator
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user with ID 1
user = get_user_by_id(user_id=1)
print(user)

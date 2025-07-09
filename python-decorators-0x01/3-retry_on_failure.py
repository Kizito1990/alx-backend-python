import time
import sqlite3
import functools

# Decorator to open and close database connection
def with_db_connection(my_function):
    @functools.wraps(my_function)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return my_function(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Decorator to retry function on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(my_function):
        @functools.wraps(my_function)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return my_function(*args, **kwargs)
                except Exception as e:
                    print(f"[ERROR] Attempt {attempt+1} failed: {e}")
                    attempt += 1
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("All retry attempts failed.")
                        raise
        return wrapper
    return decorator

# Function to fetch users from DB with retry mechanism
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # may raise error if table doesn't exist
    return cursor.fetchall()

#  Try to fetch users with automatic retry
users = fetch_users_with_retry()
print(users)

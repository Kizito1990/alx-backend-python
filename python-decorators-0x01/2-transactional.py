import sqlite3
import functools

# Decorator that handles opening and closing DB connections
def with_db_connection(my_func):
    @functools.wraps(my_func)
    def wrapper(*args, **kwargs):
        my_connection = sqlite3.connect('users.db')
        try:
            return my_func(my_connection, *args, **kwargs)
        finally:
            my_connection.close()
    return wrapper

#  Decorator to handle transactions (commit or rollback)
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit if successful
            return result
        except Exception as e:
            conn.rollback()  # Rollback if error occurs
            print(f"[ERROR] Transaction failed: {e}")
            raise  # Re-raise the exception for visibility
    return wrapper

# Function that updates user email, wrapped with both decorators
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update a user’s email
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')

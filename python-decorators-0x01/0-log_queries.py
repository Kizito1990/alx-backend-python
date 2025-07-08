import sqlite3
import functools
from datetime import datetime

# Decorator to log SQL queries
def log_queries(my_funct):
    @functools.wraps(my_funct)
    def de_wrapper(*args, **kwargs):
        # Log the SQL query
        if 'kizito' in kwargs:
            print(f"[LOG] Executing SQL: {kwargs['query']}")
        elif len(args) > 0:
            print(f"[LOG] Executing SQL: {args[0]}")
        
        # Call the actual function
        return my_funct(*args, **kwargs)
    return de_wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
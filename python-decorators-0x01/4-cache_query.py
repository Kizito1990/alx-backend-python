import time
import sqlite3
import functools

#  In-memory dictionary to store cached query results
query_cache = {}

#  Decorator to open and close DB connection
def with_db_connection(my_function):
    @functools.wraps(my_function)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return my_function(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

#  Decorator to cache query results
def cache_query(my_function):
    @functools.wraps(my_function)
    def wrapper(conn, *args, **kwargs):
        # Determine the SQL query string from args or kwargs
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None

        if query in query_cache:
            print("[CACHE HIT] Returning cached result for query")
            return query_cache[query]
        else:
            print("[CACHE MISS] Executing query and caching result")
            result = my_function(conn, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

# Function to fetch users from DB using caching
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#  First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

#  Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)

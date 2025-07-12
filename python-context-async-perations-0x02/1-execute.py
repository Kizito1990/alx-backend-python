

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv   

load_dotenv()   # reads .env into process env 


class ExecuteQuery:
    """
    Context‑manager that takes a query & params,
    pulls DB credentials from env vars, executes, returns rows.
    """

    def __init__(self, query: str, params: tuple = ()):
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # 🛈 fetch credentials from environment variables
        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        return False  # propagate any exception



# Example use
if __name__ == "__main__":
    sql = "SELECT * FROM users WHERE age > %s"
    with ExecuteQuery(sql, (25,)) as rows:
        print(rows)

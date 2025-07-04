#!/usr/bin/python3
import mysql.connector

def stream_users():
    """
    Generator that yields one user row at a time from the user_data table.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()

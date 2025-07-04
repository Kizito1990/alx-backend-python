#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields user records in batches of a given size.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",  # replace with your actual password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    # Yield remaining rows in the last batch if not empty
    if batch:
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes batches of users, printing those older than 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)

#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    """
    Generator function that yields user ages one by one from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    connection.close()


def compute_average_age():
    """
    Uses the generator to calculate average age of users without loading entire dataset.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    if count > 0:
        print(f"Average age of users: {total / count:.2f}")
    else:
        print("No users found.")

import mysql.connector
import csv
import uuid
from mysql.connector import Error

def connect_db():
    """Connects to MySQL database server"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists")
    except Error as e:
        print(f"Error: {e}")

def connect_to_prodev():
    """Connects to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_table(connection):
    """Creates user_data table with required fields"""
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )
        ''')
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error: {e}")

def insert_data(connection, filename):
    """Inserts data from CSV file into user_data table"""
    try:
        cursor = connection.cursor()
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cursor.execute("SELECT * FROM user_data WHERE email=%s", (row['email'],))
                if cursor.fetchone():
                    continue  # Skip existing entries
                cursor.execute('''
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                ''', (str(uuid.uuid4()), row['name'], row['email'], row['age']))
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error: {e}")

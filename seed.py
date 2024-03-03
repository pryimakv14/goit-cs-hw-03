import psycopg2
from faker import Faker
import random


def insert_users(connection, users):
    cursor = connection.cursor()
    try:
        insert_query = """
            INSERT INTO users (id, fullname, email)
            VALUES (%s, %s, %s)
        """
        cursor.executemany(insert_query, users)
        connection.commit()
        print("Users data inserted successfully.")
    except psycopg2.Error as e:
        print("Error inserting data into users table:", e)
        connection.rollback()
    finally:
        cursor.close()


def insert_tasks(connection, tasks):
    cursor = connection.cursor()
    try:
        insert_query = """
            INSERT INTO tasks (title, description, user_id, status_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(insert_query, tasks)
        
        connection.commit()
        print("Tasks data inserted successfully.")
    except psycopg2.Error as e:
        print("Error inserting data into tasks table:", e)
        connection.rollback()
    finally:
        cursor.close()


def insert_statuses(connection):
    cursor = connection.cursor()
    try:
        insert_query = """
            INSERT INTO status (id, name)
            VALUES (%s, %s)
        """
        cursor.executemany(insert_query, [(1, 'new'), (2, 'in progress'), (3, 'completed')])
        connection.commit()
        print("Status rows are inserted successfully.")
    except psycopg2.Error as e:
        print("Error inserting data into status table:", e)
        connection.rollback()
    finally:
        cursor.close()

def main():
    connection = None
    try:
        connection = psycopg2.connect(
            dbname="mydb",
            user="postgres",
            password="example",
            host="db",
            port="5432"
        )

        insert_statuses(connection)

        fake = Faker()
        users = []
        for i in range(20):
            fullname = fake.name()
            email = fake.email()
            users.append((i + 1, fullname, email))

        insert_users(connection, users)
            
        tasks = []
        for _ in range(25):
            title = fake.sentence()
            description = fake.paragraph()
            user_id = random.randint(1, len(users) - 1)
            status_id = random.randint(1, 3)
            tasks.append((title, description, user_id, status_id))

        insert_tasks(connection, tasks)

    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()

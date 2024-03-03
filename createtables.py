import psycopg2
from psycopg2 import sql


def create_tables(connection):
    cursor = connection.cursor()
    try:
        create_users_table_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(100),
                email VARCHAR(100) UNIQUE
            )
        """)

        create_table_status_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS status (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE
            )
        """)

        create_table_tasks_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100),              
                description TEXT,
                status_id INTEGER REFERENCES status(id),
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        for query in [create_users_table_query, create_table_status_query, create_table_tasks_query]:
            cursor.execute(query)
            connection.commit()
    except psycopg2.Error as e:
        print("Error creating table:", e)
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

        create_tables(connection)
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()

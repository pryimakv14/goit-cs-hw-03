import psycopg2
from psycopg2 import sql


def run_queries(connection):
    cursor = connection.cursor()

    print('\n', '#1') # 1
    try:
        select_query = """
            SELECT id, fullname, email
            FROM users
            WHERE id = %s
        """
        cursor.execute(select_query, (1,))
        user = cursor.fetchone()
        if user:
            print("User found: ", user)
        else:
            print("User with ID {} not found.".format(1))
    except psycopg2.Error as e:
        print("Error selecting user by id:", e)


    print('\n', '#2') # 2
    try:
        select_query = """
            SELECT title
            FROM tasks
            WHERE status_id = (
                SELECT status_id
                FROM status
                WHERE name = (%s) 
            )
        """
        cursor.execute(select_query, ('new',))
        tasks = cursor.fetchall()
        print("Tasks: ", tasks)
    except psycopg2.Error as e:
        print("Error selecting user by id:", e)


    print('\n', '#3') # 3
    try:
        status = 'in progress'
        select_query = """
            SELECT id
            FROM tasks
            WHERE status_id <> (
                SELECT id
                FROM status
                WHERE name = (%s) 
                LIMIT 1
            )
        """
        cursor.execute(select_query, (status,))
        task = cursor.fetchone()

        update_query = """
            UPDATE tasks 
            SET status_id = (
                SELECT id
                FROM status
                WHERE name = %s
            )
            WHERE id = %s
        """
        cursor.execute(update_query, (status,task[0]))
        connection.commit()
        print("Task with id ", task[0], "was updated to status", status)
    except psycopg2.Error as e:
        print("Error updating status_id for task by id:", e)


    print('\n', '#4') # 4
    try:
        status = 'in progress'
        select_query = """
            SELECT id, fullname
            FROM users
            WHERE id NOT IN (
                SELECT DISTINCT(user_id) 
                FROM tasks
            )
        """
        cursor.execute(select_query, (status,))
        users = cursor.fetchall()
        print("Users without taks: ", users)
    except psycopg2.Error as e:
        print("Error selecting users without tasks:", e)


    print('\n', '#5') #5
    try:
        status = 'in progress'
        insert_query = """
            INSERT INTO tasks (title, description, user_id, status_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, ("test task title", None, 5, 1))
        connection.commit()
        print("Task for specific user is added.")
    except psycopg2.Error as e:
        print("Error adding a task for specific user:", e)


    print('\n', '#6') #6
    try:
        select_query = """
            SELECT title
            FROM tasks
            WHERE status_id <> (
                SELECT id 
                FROM status
                WHERE name = %s
            )
        """
        cursor.execute(select_query, ("completed",))
        tasks = cursor.fetchall()
        print("Tasks that are not completed: ", tasks)
    except psycopg2.Error as e:
        print("Error se;ecting all non completed tasks:", e)

    
    print('\n', '#7') #7
    try:
        select_query = """
            SELECT id
            FROM tasks
            ORDER BY RANDOM()
            LIMIT 1
        """
        cursor.execute(select_query)
        task = cursor.fetchone()

        delete_query = """
            DELETE FROM tasks
            WHERE id = %s
        """
        cursor.execute(delete_query, (task[0],))
        connection.commit()
        
        print("Task with ID {} deleted successfully.".format(task[0]))
    except psycopg2.Error as e:
        print("Error deleting specific task:", e)
    
    
    print('\n', '#8') #8
    try:
        select_query = """
            SELECT email
            FROM users
            ORDER BY RANDOM()
            LIMIT 1
        """
        cursor.execute(select_query)
        user = cursor.fetchone()

        select_query = """
            SELECT fullname
            FROM users
            WHERE email LIKE %s
        """
        cursor.execute(select_query, (user[0],))
        found_user = cursor.fetchone()
        
        print("User with email {} is found: {} ".format(user[0], found_user[0]))
    except psycopg2.Error as e:
        print("Error searching user with specific email:", e)


    
    print('\n', '#9') #9
    try:
        select_query = """
            SELECT id
            FROM users
            ORDER BY RANDOM()
        """
        cursor.execute(select_query)
        user = cursor.fetchone()

        update_query = """
            UPDATE users
            SET fullname = %s
            WHERE id = %s
        """
        cursor.execute(update_query, ("Test Name", user[0]))
        connection.commit()
        print("User's fullname was updated for user id ", user[0])
    except psycopg2.Error as e:
        print("Error updating user:", e)    

    
    print('\n', '#10') #10
    try:
        select_query = """
            SELECT COUNT(*) AS task_count
            FROM tasks
            GROUP BY status_id
            ORDER BY status_id ASC
        """
        cursor.execute(select_query)
        tasks = cursor.fetchall()
        print("Tasks number for 'new', 'in progress', 'completed' accordingly: ", tasks)
    except psycopg2.Error as e:
        print("Error selecting number of tasks per status:", e)
    
    
    print('\n', '#11') #11
    try:
        select_query = """
            SELECT tasks.title
            FROM tasks
            JOIN users ON tasks.user_id = users.id 
            WHERE users.email LIKE '%@example.com'
        """
        cursor.execute(select_query)
        tasks = cursor.fetchall()
        print("Tasks for users with @example.com as a domain: ", tasks)
    except psycopg2.Error as e:
        print("Error selecting for users with specific domain:", e)
    
    
    
    print('\n', '#12') #12
    try:
        select_query = """
            SELECT title
            FROM tasks
            WHERE description = '' OR description IS NULL
        """
        cursor.execute(select_query)
        tasks = cursor.fetchall()
        print("Tasks with no description: ", tasks)
    except psycopg2.Error as e:
        print("Error selecting tasks with no description:", e)

    
    print('\n', '#13') #13
    try:
        select_query = """
            SELECT users.fullname, tasks.title
            FROM users
            INNER JOIN tasks ON users.id = tasks.user_id
            WHERE tasks.title <> %s
        """
        cursor.execute(select_query, ('in progress',))
        users_with_tasks = cursor.fetchall()
        print("Users with tasks: ", users_with_tasks)
    except psycopg2.Error as e:
        print("Error selecting user with tasks:", e)

    
    print('\n', '#14') #14
    try:
        select_query = """
            SELECT users.fullname, COUNT(*) as task_count
            FROM users
            LEFT JOIN tasks ON users.id = tasks.user_id
            GROUP BY users.fullname
        """
        cursor.execute(select_query)
        users_with_tasks = cursor.fetchall()
        print("Users with tasks count: ", users_with_tasks)
    except psycopg2.Error as e:
        print("Error selecting user with tasks count:", e)


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

        run_queries(connection)
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()

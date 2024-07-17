
import mysql.connector
from mysql.connector import Error


def create_connection(host_name, user_name, user_password, db_name, port):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=port,
            auth_plugin='caching_sha2_password'  
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_table(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Table created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"Error: '{e}' occurred")


def insert_into_table(connection, table, name, salary, status):
    query = "INSERT INTO " + table + " (Name, Salary, Status) VALUES (%s, %s, %s)"
    args = (name, salary, status)

    cursor = connection.cursor()
    try:
        cursor.execute(query, args)
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.rollback()
    finally:
        cursor.close()


def select_all_texans(connection):
    query = "SELECT Name, Position FROM Texans"
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print("Name:", row[0], "| Position:", row[1])
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

# Connection parameters
host_name = "db4free.net"
user_name = "pinkmuffin"  # Replace with your db4free username
user_password = "bellucci12"  # Replace with your db4free password
db_name = "bryantestdb"  # Replace with your database name on db4free
port = 3306

# SQL query to create a table
create_table_query = """
CREATE TABLE IF NOT EXISTS Contract (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    salary VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL

);
"""


# Create a database connection
connection = create_connection(host_name, user_name, user_password, db_name, port)

"""
# Create a table
if connection:
    create_table(connection, create_table_query)
    connection.close()
else:
    print("Connection failed")
"""


""""
# Example data insertion
if connection:
    insert_into_table(connection, "Contract", "Tank Dell", "12","active")
    insert_into_table(connection, "Contract", "Stefon Diggs", "140","active")
    insert_into_table(connection, "Contract", "JJ Watt", "999999","retired")
    insert_into_table(connection, "Contract", "Demeco Ryans", "1","active")
    connection.close()
else:
    print("Connection failed")
"""



# Retrieve and print all data from the Texans table
if connection:
    select_all_texans(connection)
    connection.close()
else:
    print("Connection failed")


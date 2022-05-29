import mysql.connector
from mysql.connector import Error


def connect(host, username, password, database):
    connection = None

    try:
        connection = mysql.connector.connect(host=host,
                                             user=username,
                                             passwd=password,
                                             database=database,
                                             auth_plugin='mysql_native_password')
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def readData(connection, query):
    cursor = connection.cursor()
    results = []
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def executeQuery(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        return True
    except Error as err:
        print(f"Error: {err}")

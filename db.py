import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        user='root',
        password='',
        host='127.0.0.1',
        database='diverDB'
    )
    return connection

def get_cursor():
    connection = get_db_connection()
    return connection, connection.cursor()

def get_mysql_connector_version():
    return mysql.connector.__version__
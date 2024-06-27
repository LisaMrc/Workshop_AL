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

def get_dives_data():
    connection, cursor = get_cursor()
    cursor.execute("SELECT * FROM Dive ORDER BY id")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def get_places():
    connection, cursor = get_cursor()
    cursor.execute("SELECT place_id, place_name FROM place")
    places = cursor.fetchall()
    connection.close()
    return places
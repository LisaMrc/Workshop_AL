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

def get_places():
    connection, cursor = get_cursor()
    cursor.execute("SELECT place_id, place_name FROM place")
    places = cursor.fetchall()
    connection.close()
    return places

def get_fishes():
    connection, cursor = get_cursor()
    cursor.execute("SELECT id, common_name FROM fish")
    fishes = cursor.fetchall()
    connection.close()
    return fishes
# -*- coding: utf-8 -*-
from flask import Flask,request,render_template,jsonify
from flask_cors import CORS
from db import get_mysql_connector_version, get_cursor
import db

app = Flask(__name__)
CORS(app)

@app.route("/sql_version")
def sqlVersion():
    version = get_mysql_connector_version()
    return f"MySQL Connector version: {version}"

@app.route('/viewDB', methods=['GET'])
def show_data():
    data = db.get_dives_data()
    return jsonify(data)

@app.route('/viewRecord/<int:id>', methods=['GET'])
def get_record(id):
    connection, cursor = get_cursor()
    cursor.execute("SELECT * FROM Dive WHERE id = %s", (id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    if row:
        return row
    else:
        return {'message': 'Record not found'}, 404
    
@app.route('/your_table/<int:id>', methods=['PUT'])
def update_record(id):
    data = request.get_json()
    new_name = data.get('name')
    connection, cursor = get_cursor()
    cursor.execute("UPDATE your_table SET name = %s WHERE id = %s", (new_name, id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Record updated successfully'})
    
@app.route("/")
def render_landingPage():
    return render_template('landingPage.html')

@app.route("/render_login")
def render_login():
    return render_template('login.html')

@app.route('/login_user', methods=['POST'])
def verify_user():
    username = request.form['username']
    password = request.form['password']

    connection, cursor = get_cursor()
    sql_query = "SELECT username FROM diver WHERE username = %s AND password = %s"
    cursor.execute(sql_query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result:
        return "USER FOUND"
    else:
        return "USER NOT FOUND"

@app.route("/render_signin")
def render_signin():
    return render_template('signin.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']

    connection, cursor = get_cursor()

    sql_query = "INSERT INTO diver (username, password) VALUES (%s, %s)"
    cursor.execute(sql_query, (username, password))
    connection.commit()
    cursor.close()
    connection.close()

    return "USER WAS ADDED SUCCESSFULLY"

@app.route("/dives")
def user_dives_list():
    data = db.get_dives_data()
    return render_template('userDives.html', user_dives=data)

@app.route('/add', methods=['POST'])
def add_dive():
    dive_mins = request.form['dive_mins']
    dive_secs = request.form['dive_secs']
    dive_depth = request.form['dive_depth']
    dive_date = request.form['dive_date']
    rating = request.form['rating']

    connection, cursor = get_cursor()

    sql_query = "INSERT INTO Dive (dive_mins, dive_secs, dive_depth, dive_date, rating) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql_query, (dive_mins, dive_secs, dive_depth, dive_date, rating))
    connection.commit()
    cursor.close()
    connection.close()

    data = db.get_dives_data()
    return render_template('userDives.html', user_dives=data)

@app.route('/delete_dive/<int:index>', methods=['GET', 'POST'])
def delete_item(index):
    connection, cursor = get_cursor()
    sql_query = "DELETE FROM dive WHERE id = %s"
    cursor.execute(sql_query, (index,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('show_dives'))

# @app.route('/show_dives')
# def show_dives():
#     connection, cursor = get_cursor()
#     # cursor.execute("SELECT * FROM dive WHERE username = %s", (current_user.username,))
#     user_dives = cursor.fetchall()
#     cursor.close()
#     connection.close()
    
#     return render_template('show_dives.html')
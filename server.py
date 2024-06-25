# -*- coding: utf-8 -*-
from flask import Flask,request,render_template,jsonify
from flask_cors import CORS
from db import get_mysql_connector_version, get_cursor

app = Flask(__name__)
CORS(app)

#les absences, c'est pour un dictionnaire qui pour un entier donne le nom et le nombre d'absences
# structure absences : { 1:{'nom':'toto', 'abs':3}, 2:{'nom':'bob', 'abs':3} }
cpt=0
absences={}

@app.route("/sql_version")
def sqlVersion():
    version = get_mysql_connector_version()
    return f"MySQL Connector version: {version}"

@app.route('/viewDB', methods=['GET'])
def get_data():
    connection, cursor = get_cursor()
    cursor.execute("SELECT * FROM Dive")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(rows)

@app.route('/viewRecord/<int:id>', methods=['GET'])
def get_record(id):
    connection, cursor = get_cursor()
    cursor.execute("SELECT * FROM Dive WHERE id = %s", (id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    if row:
        return jsonify(row)
    else:
        return jsonify({'message': 'Record not found'}), 404

@app.route('/add', methods=['POST'])
def add_record():
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
    return "SUCCESS"

@app.route('/your_table/<int:id>')
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
def index():
    return render_template('userDives.html')

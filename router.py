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
        return jsonify(row)
    else:
        return jsonify({'message': 'Record not found'}), 404
    
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
def landingPage():
    return render_template('landingPage.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signin")
def signin():
    return render_template('signin.html')

# @app.route('/add_user', methods=['POST'])
# def add_user():
#     dive_mins = request.form['dive_mins']
#     dive_secs = request.form['dive_secs']

#     connection, cursor = get_cursor()

#     sql_query = "INSERT INTO Dive (dive_mins, dive_secs, dive_depth, dive_date, rating) VALUES (%s, %s, %s, %s, %s)"
#     cursor.execute(sql_query, (dive_mins, dive_secs, dive_depth, dive_date, rating))
#     connection.commit()
#     cursor.close()
#     connection.close()

#     return "USER WAS ADDED SUCCESSFULLY"

@app.route("/dives")
def user_dives_list():
    data = db.get_dives_data()
    data_formated = jsonify(data)
    print(data_formated)
    return render_template('userDives.html', user_dives=data_formated)

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

    return "DIVE WAS ADDED SUCCESSFULLY"

# @app.route('/delete_dive/<int:dive_id>', methods=['DELETE'])
# def delete_item(dive_id):
#     dive = dive.query.get(dive_id)
#     if dive:
#         dive.session.delete(dive)
#         dive.session.commit()
#         return jsonify({'message': 'Dive deleted successfully'}), 200
#     else:
#         return jsonify({'message': 'Dive not found'}), 404

# if __name__ == '__main__':
#     app.run(debug=True)
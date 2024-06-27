# -*- coding: utf-8 -*-
from flask import Flask,request, render_template, jsonify, redirect, session
from flask_cors import CORS
from flask_session import Session
from db import get_mysql_connector_version, get_cursor
import db

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)

@app.route("/sql_version")
def sqlVersion():
    version = get_mysql_connector_version()
    return f"MySQL Connector version: {version}"

@app.route("/")
def render_landingPage():
    return render_template('landingPage.html')

@app.route("/render_login", methods=["POST", "GET"])
def render_login():
    return render_template('login.html')

@app.route('/login_user', methods=['POST'])
def verify_user():
    username = request.form['username']
    password = request.form['password']
    connection, cursor = get_cursor()
    sql_query = "SELECT * FROM diver WHERE username = %s AND password = %s"
    cursor.execute(sql_query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        session['id'] = result[0]
        session['username'] = username
        return redirect("/show_dives")
    else:
        return redirect("/render_login")

@app.route("/render_signin")
def render_signin():
    return render_template('signin.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    
    # Does the user exists ?
    connection, cursor = get_cursor()
    sql_query = "SELECT username FROM diver WHERE username = %s"
    cursor.execute(sql_query, (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result:
        return redirect("/render_login")
    else:
        # If user do not exist, create new user
        connection, cursor = get_cursor()
        sql_query = "INSERT INTO diver (username, password) VALUES (%s, %s)"
        cursor.execute(sql_query, (username, password))
        connection.commit()
        cursor.close()
        connection.close()

        # Redirect user towards their new dashboard
        connection, cursor = get_cursor()
        sql_query = "SELECT id, username FROM diver WHERE username = %s"
        cursor.execute(sql_query, (username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            session['id'] = result[0]
            session['username'] = result[1]
            return redirect("/show_dives")
        else:
            return "Error creating user", 500

@app.route('/show_dives')
def show_dives():
    try:
        connection, cursor = get_cursor()
        cursor.execute("SELECT * FROM dive WHERE diver_id = %s", (session['id'],))
        user_dives = cursor.fetchall()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "An error occurred while fetching dives", 500
    finally:
        cursor.close()
        connection.close()
    
    return render_template('userDives.html', user_dives=user_dives)

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
def delete_dive(index):
    connection, cursor = get_cursor()
    sql_query = "DELETE FROM dive WHERE id = %s"
    cursor.execute(sql_query, (index,))
    connection.commit()
    cursor.close()
    connection.close()

    data = db.get_dives_data()

    return render_template('userDives.html', user_dives=data)

@app.route("/render_one_dive/<int:index>", methods=['GET', 'POST'])
def render_edit(index):
    connection, cursor = get_cursor()
    sql_query = "SELECT * FROM dive WHERE id = %s"
    cursor.execute(sql_query, (index,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    return render_template('userDivesEdit.html', entry=row)

@app.route("/edit_dive/<int:index>", methods=['GET', 'POST'])
def edit_dive(index):
    dive_mins = request.form['dive_mins']
    dive_secs = request.form['dive_secs']
    dive_depth = request.form['dive_depth']
    dive_date = request.form['dive_date']
    rating = request.form['rating']

    connection, cursor = get_cursor()
    sql_query = "UPDATE dive SET dive_mins = %s, dive_secs = %s, dive_depth = %s, dive_date = %s, rating = %s WHERE id = %s"
    cursor.execute(sql_query, (dive_mins, dive_secs, dive_depth, dive_date, rating, index))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect("/show_dives", code=302)

@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/")
 
if __name__ == "__main__":
    app.run(debug=True)
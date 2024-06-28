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
        cursor.execute("SELECT dive.id, dive.dive_mins, dive.dive_secs, dive.dive_depth, dive.dive_date, dive.rating, place.country, place.place_name, place.type, fish.common_name FROM dive JOIN place ON dive.place_id = place.place_id JOIN fish ON dive.fish_id = fish.id WHERE dive.diver_id = %s", (session['id'],))
        user_dives = cursor.fetchall()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "An error occurred while fetching dives", 500
    finally:
        cursor.close()
        connection.close()

    places = db.get_places()
    average_mins = sum(dive[1] for dive in user_dives) / len(user_dives) if user_dives else 0
    average_secs = sum(dive[2] for dive in user_dives) / len(user_dives) if user_dives else 0
    average_depth = sum(dive[3] for dive in user_dives) / len(user_dives) if user_dives else 0

    return render_template('userDives.html', user_dives=user_dives, places=places, avg_depth=average_depth, avg_mins=average_mins, avg_secs=average_secs)

@app.route('/add', methods=['POST'])
def add_dive():
    dive_mins = request.form['dive_mins']
    dive_secs = request.form['dive_secs']
    dive_depth = request.form['dive_depth']
    dive_date = request.form['dive_date']
    rating = request.form['rating']
    place = request.form['place']
    fish = request.form['fish']

    connection, cursor = get_cursor()
    sql_query = "INSERT INTO dive (dive_mins, dive_secs, dive_depth, dive_date, rating, place_id, diver_id, fish_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql_query, (dive_mins, dive_secs, dive_depth, dive_date, rating, place, session['id'], fish))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect("/show_dives")

@app.route('/delete_dive/<int:index>', methods=['GET', 'POST'])
def delete_dive(index):
    connection, cursor = get_cursor()
    sql_query = "DELETE FROM dive WHERE id = %s"
    cursor.execute(sql_query, (index,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect("/show_dives")

@app.route("/render_one_dive/<int:index>", methods=['GET', 'POST'])
def render_edit(index):
    connection, cursor = get_cursor()
    sql_query = "SELECT * FROM dive WHERE id = %s"
    cursor.execute(sql_query, (index,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    places = db.get_places()
    return render_template('userDivesEdit.html', entry=row, places=places)

@app.route("/edit_dive/<int:index>", methods=['GET', 'POST'])
def edit_dive(index):
    dive_mins = request.form['dive_mins']
    dive_secs = request.form['dive_secs']
    dive_depth = request.form['dive_depth']
    dive_date = request.form['dive_date']
    rating = request.form['rating']
    place = request.form['place']

    connection, cursor = get_cursor()
    sql_query = "UPDATE dive SET dive_mins = %s, dive_secs = %s, dive_depth = %s, dive_date = %s, rating = %s, place_id=%s WHERE id = %s"
    cursor.execute(sql_query, (dive_mins, dive_secs, dive_depth, dive_date, rating, place, index))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect("/show_dives", code=302)

@app.route('/fishes')
def show_fishes():
    return render_template("allFishes.html")

@app.route('/api/fishes')
def get_fishes():
    conn = db.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM fish')
    fishes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(fishes)

@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/")
 
if __name__ == "__main__":
    app.run(debug=True)
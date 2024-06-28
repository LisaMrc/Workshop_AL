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

def get_biggest_fish():
    connection, cursor = get_cursor()
    cursor.execute("SELECT fish.common_name, fish.average_size FROM fish JOIN dive_fish ON dive_fish.fish_id = fish.id WHERE dive_fish.diver_id = %s AND fish.average_size  = (SELECT MAX(fish.average_size) FROM fish JOIN dive ON dive_fish.fish_id = fish.id WHERE dive_fish.diver_id = %s)", (session['id'], session['id']))
    biggest_fish = cursor.fetchone()
    connection.close()
    return biggest_fish

@app.route('/show_dives')
def show_dives():
    connection, cursor = get_cursor()
    query = """
    SELECT 
        d.id AS dive_id,
        d.dive_mins, 
        d.dive_secs, 
        d.dive_depth, 
        d.dive_date, 
        d.rating, 
        p.country, 
        p.place_name AS place_name, 
        p.type AS place_type, 
        GROUP_CONCAT(f.common_name SEPARATOR ', ') AS fishes_seen
    FROM 
        dive d
    JOIN 
        place p ON d.place_id = p.place_id
    LEFT JOIN 
        dive_fish df ON d.id = df.dive_id
    LEFT JOIN 
        fish f ON df.fish_id = f.id
    GROUP BY 
        d.id, d.dive_mins, d.dive_secs, d.dive_depth, d.dive_date, d.rating, p.country, p.place_name, p.type
    ORDER BY 
        d.dive_date DESC;
    """
    cursor.execute(query)
    user_dives = cursor.fetchall()
    cursor.close()
    connection.close()

    places = db.get_places()
    biggest_fish = get_biggest_fish()
    average_mins = sum(dive[1] for dive in user_dives) / len(user_dives) if user_dives else 0
    average_secs = sum(dive[2] for dive in user_dives) / len(user_dives) if user_dives else 0
    average_depth = sum(dive[3] for dive in user_dives) / len(user_dives) if user_dives else 0

    return render_template('userDives.html', user_dives=user_dives, places=places, avg_depth=average_depth, avg_mins=average_mins, avg_secs=average_secs, biggest_fish=biggest_fish)

@app.route('/add', methods=['POST'])
def add_dive():
    try:
        dive_mins = request.form['dive_mins']
        dive_secs = request.form['dive_secs']
        dive_depth = request.form['dive_depth']
        dive_date = request.form['dive_date']
        rating = request.form['rating']
        place = request.form['place']
        fish = request.form.getlist('fish')  # List of fish IDs

        connection, cursor = get_cursor()
        sql_query = """
            INSERT INTO dive (dive_mins, dive_secs, dive_depth, dive_date, rating, place_id, diver_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_query, (dive_mins, dive_secs, dive_depth, dive_date, rating, place, session['id']))

        dive_id = cursor.lastrowid  # Get the ID of the newly inserted dive

        # Insert the fish IDs and diver_id into the dive_fish table
        if fish:
            insert_dive_fish_query = "INSERT INTO dive_fish (dive_id, fish_id, diver_id) VALUES (%s, %s, %s)"
            dive_fish_values = [(dive_id, fish_id, session['id']) for fish_id in fish]
            cursor.executemany(insert_dive_fish_query, dive_fish_values)

        connection.commit()

        query = """
            SELECT 
                d.id AS dive_id,
                d.dive_mins, 
                d.dive_secs, 
                d.dive_depth, 
                d.dive_date, 
                d.rating, 
                p.country, 
                p.place_name AS place_name, 
                p.type AS place_type, 
                GROUP_CONCAT(f.common_name SEPARATOR ', ') AS fishes_seen
            FROM 
                dive d
            JOIN 
                place p ON d.place_id = p.place_id
            LEFT JOIN 
                dive_fish df ON d.id = df.dive_id
            LEFT JOIN 
                fish f ON df.fish_id = f.id
            GROUP BY 
                d.id, d.dive_mins, d.dive_secs, d.dive_depth, d.dive_date, d.rating, p.country, p.place_name, p.type
            ORDER BY 
                d.dive_date DESC;
            """
        cursor.execute(query)

    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect("/show_dives")

@app.route('/delete_dive/<int:index>', methods=['GET', 'POST'])
def delete_dive(index):
    connection, cursor = get_cursor()
    sql_query = "DELETE FROM dive WHERE id = %s"
    cursor.execute(sql_query, (index,))

    sql_query_two = "DELETE FROM dive_fish WHERE dive_id = %s"
    cursor.execute(sql_query_two, (index,))

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
    fish = request.form['fish']

    connection, cursor = get_cursor()
    sql_query = "UPDATE dive SET dive_mins = %s, dive_secs = %s, dive_depth = %s, dive_date = %s, rating = %s, place_id=%s, fish_id=%s WHERE id = %s"
    cursor.execute(sql_query, (dive_mins, dive_secs, dive_depth, dive_date, rating, place, fish, index))
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
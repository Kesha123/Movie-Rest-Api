import json
import datetime

from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import session
from flask import render_template

from DataBase.dbconfig import Connection
from DataBase.query import get_all_movies, get_movie_by_id, add_movie, update_movie, delete_movie_by_id, validate_user, \
    register_user

app = Flask(__name__)
app.secret_key = "12345"
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=2)

connection = Connection()
#connection.init()
connection.init_from_file()
connection.connect()


@app.route('/api.movies', methods=["GET", "POST"])
def all_movies():
    if request.method == "GET":
        return get_all_movies(connection.connection)
    elif request.method == "POST":
        return add_movie(connection.connection, request.json)
    else:
        return {"response": "Not valid http method for this route."}


@app.route('/api.movies/<int:id>', methods=["DELETE", "GET", "PUT"])
def movie_by_id(id):
    if request.method == "GET":
        return get_movie_by_id(connection.connection, id)
    elif request.method == "DELETE":
        return delete_movie_by_id(connection.connection, id)
    elif request.method == "PUT":
        return update_movie(connection.connection, id, request.json)
    else:
        return {"response": "Not valid http method for this route"}


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/movies',methods=["GET", "POST"])
@app.route('/movies/', methods=["GET", "POST"])
def movies():
    movies = json.loads(get_all_movies(connection.connection))["movies"]
    return render_template('movies.html', movies=movies)


@app.route('/movies/<int:id>', methods=["GET", "POST"])
@app.route('/movies/<int:id>/', methods=["GET", "POST"])
def movie(id):
    movies = [json.loads(get_movie_by_id(connection.connection, id))]
    return render_template('movies.html', movies=movies)


@app.route('/user/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = validate_user(connection.connection, email, password)

        if user is not None:
            session["User account"] = request.form["email"]
            return redirect(url_for('account'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/user/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = register_user(connection.connection, email, password)

        if user:
            print("User has been registered")
        else:
            print("User already exist")

        return redirect(url_for('login'))
    else:
        return render_template('signup.html')


@app.route('/user/account', methods=["POST", "GET"])
def account():
    if session.get("User account"):
        print(session)
        return render_template('account.html')
    else:
        return redirect(url_for('login'))


@app.route('/user/logout', methods=["POST"])
def logout():
    session.pop("User account", default=None)
    return redirect(url_for('movies'))


if __name__ == '__main__':
    app.run()


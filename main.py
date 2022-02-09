from flask import Flask
from flask import request

from DataBase.dbconfig import Connection
from DataBase.query import get_all_movies, get_movie_by_id, add_movie, update_movie, delete_movie_by_id

app = Flask(__name__)

connection = Connection()
connection.init("movie", "postgres", "tyshkanmc")
connection.connect()


@app.route('/movies', methods=["GET", "POST"])
def all_movies():
    if request.method == "GET":
        return get_all_movies(connection.connection)
    elif request.method == "POST":
        return add_movie(connection.connection, request.json)
    else:
        pass


@app.route('/movies/<int:id>', methods=["DELETE", "GET", "PUT"])
def movie_by_id(id):
    if request.method == "GET":
        return get_movie_by_id(connection.connection, id)
    elif request.method == "DELETE":
        return delete_movie_by_id(connection.connection, id)
    elif request.method == "PUT":
        return update_movie(connection.connection, id, request.json)
    else:
        pass


if __name__ == '__main__':
    app.run()


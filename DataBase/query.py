def movie(params):
    return f'{{"id":{params[0]}, "title":"{params[1]}", "director":"{params[2]}", "year":{params[3]}}}'


def get_all_movies(connection):
    query = "SELECT * FROM movies;"

    cursor = connection.cursor()
    cursor.execute(query)
    response = cursor.fetchall()

    body = ""
    for i, item in enumerate(response):
        if i != len(response)-1:
            body += movie(item) + ','
        else:
            body += movie(item)

    cursor.close()
    return '{"movies": [' + body + ']}'


def get_movie_by_id(connection, id):
    query = f"SELECT * FROM movies WHERE id={id};"

    cursor = connection.cursor()
    cursor.execute(query)
    response = cursor.fetchone()
    cursor.close()

    body = movie(response)
    return body


def add_movie(connection, body):
    query = f"INSERT INTO movies (title, director, year) VALUES ('{body['title']}', '{body['director']}', {body['year']});"

    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()

    return body


def update_movie(connection, id, body):
    query = f"UPDATE movies SET title = '{body['title']}', director = '{body['director']}', year = {body['year']} WHERE id={id};"

    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()

    return "Updated successfully"


def delete_movie_by_id(connection, id):
    query = f"DELETE FROM movies WHERE id={id}"

    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()

    return "Deleted successfully"

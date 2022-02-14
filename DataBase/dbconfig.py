import psycopg2
from configparser import ConfigParser


class Connection:

    def __init__(self):
        self.config = None
        self.connection = None
        self.cursor = None

    def init(self, database, user, password, port="5432", host='localhost'):
        self.config = dict(
            [("host", host), ("database", database), ("user", user), ("password", password), ("port", port)])

    def init_from_file(self, filename='database.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)

        if parser.has_section(section):
            parameters = parser.items(section)
            self.config = dict(parameters)
        else:
            print("No parameters")

    def return_config(self):
        return self.config

    def connect(self):
        configuration = self.return_config()
        self.connection = psycopg2.connect(**configuration)

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

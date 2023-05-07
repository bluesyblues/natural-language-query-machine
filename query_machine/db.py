import fdb
import pymysql
import sqlite3


class DB:
    def __init__(self):
        self.connection_info = {}

    def make_connection(self):
        raise NotImplementedError

    def send_query(self, query):
        con = self.make_connection(**self.connection_info)
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        result = cursor.fetchall()
        con.close()
        return result


class MariaDB(DB):
    def __init__(self, host, port, database, user, password):
        super().__init__()
        self.connection_info["host"] = host
        self.connection_info["port"] = port
        self.connection_info["database"] = database
        self.connection_info["user"] = user
        self.connection_info["password"] = password

    def make_connection(self, host, port, database, user, password):
        con = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )
        return con


class SqliteDB(DB):
    def __init__(self, database):
        super().__init__()
        self.connection_info["database"] = database

    def make_connection(self, database):
        con = sqlite3.connect(database)
        return con


class FireBirdDB(DB):
    def __init__(self, host, port, database, user, password):
        super().__init__()
        self.connection_info["host"] = host
        self.connection_info["port"] = port
        self.connection_info["database"] = database
        self.connection_info["user"] = user
        self.connection_info["password"] = password

    def make_connection(self, host, port, database, user, password):
        con = fdb.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            charset='UTF8'
        )
        return con

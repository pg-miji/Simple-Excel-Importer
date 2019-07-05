import mysql.connector

class Connector:

    def get(self):
        connect = mysql.connector.connect(
            host = 'localhost',
            port = 3306,
            db = 'database_name',
            user = 'user_name',
            passwd = 'password'
        )

        return connect

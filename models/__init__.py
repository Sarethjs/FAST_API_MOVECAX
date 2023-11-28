import mysql.connector

db_connect = None


def get_connection():
    global db_connect

    try:
        if db_connect is None:
            db_connect = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='movecax'
            )
            return db_connect

        else:
            if db_connect.is_closed():
                db_connect.connect()

            return db_connect

    except mysql.connector.Error:
        return None
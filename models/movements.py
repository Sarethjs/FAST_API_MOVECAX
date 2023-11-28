import mysql.connector.errors
import json
from models import get_connection
import models.errors as cax_errors


class Movement:

    def __init__(self, user_id: int, origin: str, dest: str, route_name: str):
        self.id = None
        self.user_id = user_id
        self.origin: str = origin
        self.dest: str = dest
        self.route_name: str = route_name
        self.date = None

    def to_json(self):
        data = {
            'id': self.id,
            'userId': self.user_id,
            'origin': self.origin,
            'dest': self.dest,
            'routeName': self.route_name,
            'date': self.date
        }

        return json.dumps(data)

    def to_dict(self):
        data = {
            'id': self.id,
            'userId': self.user_id,
            'origin': self.origin,
            'dest': self.dest,
            'routeName': self.route_name,
            'date': self.date
        }

        return data

    def save(self):

        cursor = None
        connection = get_connection()

        if connection is None:
            raise cax_errors.DataNotInsertedException("Can't connect to database")

        try:
            cursor = connection.cursor()

            query = f""" INSERT INTO movements (user_id, origin, dest, route_name)
                        VALUES ('{self.user_id}', '{self.origin}', '{self.dest}', '{self.route_name}')
                    """
            cursor.execute(query)
            connection.commit()

        except mysql.connector.errors.Error as err:
            connection.rollback()
            raise cax_errors.DataNotInsertedException(err)

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()

        return self.to_json()

    @staticmethod
    def find(user_id: int):

        cursor = None
        connection = get_connection()

        if connection is None:
            raise cax_errors.DataNotInsertedException("Can't connect to database")

        try:
            if not connection.is_connected():
                connection.connect()

            cursor = connection.cursor()
            query = f"""
                SELECT origin, dest, route_name, date FROM movements 
                WHERE user_id = {user_id}
            """
            cursor.execute(query)
            movements = cursor.fetchall()

            movements_response = []

            for movement in movements:
                origin = movement[0]
                dest = movement[1]
                route_name = movement[2]
                date = movement[3]

                move = Movement(user_id, origin, dest, route_name)
                json_date = date.strftime("%Y-%m-%dT%H:%M:%S")
                move.date = json_date
                movements_response.append(move.to_dict())

        except mysql.connector.errors.Error as err:
            raise cax_errors.DataNotInsertedException(err)

        except IndexError as e:
            raise cax_errors.CantParseDataToModel(f"movements: {e}")

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()

        return json.dumps(movements_response)
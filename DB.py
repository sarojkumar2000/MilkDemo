import psycopg2
from psycopg2 import Error

class Database:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connected to PostgreSQL database!")
        except Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection to PostgreSQL database closed.")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        except Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchone()
        else:
            return None

    def fetch_all(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

# # Example usage:
# db = Database('postgres', 'postgres', '1234')
# db.connect()
# # result = db.fetch_one("SELECT version()")
# # print(result)
# db.close()

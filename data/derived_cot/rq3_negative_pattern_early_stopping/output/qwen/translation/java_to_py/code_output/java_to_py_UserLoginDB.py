import sqlite3

class UserLoginDB:
    def __init__(self, db_name):
        self.connection = None
        try:
            self.connection = sqlite3.connect(db_name)
            self.create_table()
        except sqlite3.Error as e:
            print(e)

    def create_table(self):
        create_table_query = """CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password TEXT
        )"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(create_table_query)
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def insert_user(self, username, password):
        insert_query = "INSERT INTO users (username, password) VALUES (?, ?)"
        cursor = self.connection.cursor()
        try:
            cursor.execute(insert_query, (username, password))
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def search_user_by_username(self, username):
        search_query = "SELECT * FROM users WHERE username = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(search_query, (username,))
            result = cursor.fetchone()
            if result:
                return f"{result[0]},{result[1]}"
            return None
        except sqlite3.Error as e:
            print(e)
            return None

    def delete_user_by_username(self, username):
        delete_query = "DELETE FROM users WHERE username = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(delete_query, (username,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def validate_user_login(self, username, password):
        user = self.search_user_by_username(username)
        if user is not None:
            stored_password = user.split(',')[1]
            return stored_password == password
        return False

    def close(self):
        if self.connection is not None:
            self.connection.close()
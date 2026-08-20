import sqlite3
import traceback


class MovieTicketDB:
    class Ticket:
        def __init__(self, id, movie_name, theater_name, seat_number, customer_name):
            self._id = id
            self._movie_name = movie_name
            self._theater_name = theater_name
            self._seat_number = seat_number
            self._customer_name = customer_name

        def get_id(self):
            return self._id

        def get_movie_name(self):
            return self._movie_name

        def get_theater_name(self):
            return self._theater_name

        def get_seat_number(self):
            return self._seat_number

        def get_customer_name(self):
            return self._customer_name

    def __init__(self, db_name):
        self.connection = None
        try:
            # isolation_level=None -> autocommit mode, matching the JDBC default
            self.connection = sqlite3.connect(db_name, isolation_level=None)
            self.connection.row_factory = sqlite3.Row
            self._create_table()
        except sqlite3.Error:
            traceback.print_exc()

    def _create_table(self):
        sql = ("CREATE TABLE IF NOT EXISTS tickets ("
               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "movie_name TEXT, "
               "theater_name TEXT, "
               "seat_number TEXT, "
               "customer_name TEXT)")
        try:
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql)
            finally:
                cursor.close()
        except sqlite3.Error:
            traceback.print_exc()

    def insert_ticket(self, movie_name, theater_name, seat_number, customer_name):
        sql = "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) VALUES (?, ?, ?, ?)"
        try:
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql, (movie_name, theater_name, seat_number, customer_name))
            finally:
                cursor.close()
        except sqlite3.Error:
            traceback.print_exc()

    def search_tickets_by_customer(self, customer_name):
        sql = "SELECT * FROM tickets WHERE customer_name = ?"
        tickets = []
        try:
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql, (customer_name,))
                for row in cursor:
                    tickets.append(MovieTicketDB.Ticket(
                        row["id"],
                        row["movie_name"],
                        row["theater_name"],
                        row["seat_number"],
                        row["customer_name"]
                    ))
            finally:
                cursor.close()
        except sqlite3.Error:
            traceback.print_exc()
        return tickets

    def delete_ticket(self, ticket_id):
        sql = "DELETE FROM tickets WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql, (ticket_id,))
            finally:
                cursor.close()
        except sqlite3.Error:
            traceback.print_exc()

    def close(self):
        try:
            if self.connection is not None:
                self.connection.close()
        except sqlite3.Error:
            traceback.print_exc()
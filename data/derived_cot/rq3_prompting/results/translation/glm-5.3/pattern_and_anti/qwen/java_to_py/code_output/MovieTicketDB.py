import sqlite3
import traceback


class MovieTicketDB:
    class Ticket:
        def __init__(self, id, movie_name, theater_name, seat_number, customer_name):
            self.id = id
            self.movie_name = movie_name
            self.theater_name = theater_name
            self.seat_number = seat_number
            self.customer_name = customer_name

        def get_id(self):
            return self.id

        def get_movie_name(self):
            return self.movie_name

        def get_theater_name(self):
            return self.theater_name

        def get_seat_number(self):
            return self.seat_number

        def get_customer_name(self):
            return self.customer_name

    def __init__(self, db_name):
        self.connection = None
        try:
            # isolation_level=None -> autocommit, matching JDBC's default autocommit behavior
            self.connection = sqlite3.connect(db_name, isolation_level=None)
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
            self.connection.execute(sql)
        except sqlite3.Error:
            traceback.print_exc()

    def insert_ticket(self, movie_name, theater_name, seat_number, customer_name):
        sql = "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) VALUES (?, ?, ?, ?)"
        try:
            self.connection.execute(sql, (movie_name, theater_name, seat_number, customer_name))
        except sqlite3.Error:
            traceback.print_exc()

    def search_tickets_by_customer(self, customer_name):
        sql = "SELECT * FROM tickets WHERE customer_name = ?"
        tickets = []
        try:
            cursor = self.connection.execute(sql, (customer_name,))
            for row in cursor.fetchall():
                ticket = MovieTicketDB.Ticket(row[0], row[1], row[2], row[3], row[4])
                tickets.append(ticket)
        except sqlite3.Error:
            traceback.print_exc()
        return tickets

    def delete_ticket(self, ticket_id):
        sql = "DELETE FROM tickets WHERE id = ?"
        try:
            self.connection.execute(sql, (ticket_id,))
        except sqlite3.Error:
            traceback.print_exc()

    def close(self):
        try:
            if self.connection is not None:
                self.connection.close()
        except sqlite3.Error:
            traceback.print_exc()
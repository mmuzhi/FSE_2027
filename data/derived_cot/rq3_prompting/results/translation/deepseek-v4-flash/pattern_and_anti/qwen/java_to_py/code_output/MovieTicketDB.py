import sqlite3
import traceback
from contextlib import closing


class MovieTicketDB:
    def __init__(self, dbName):
        self._connection = None
        self._closed = False
        try:
            self._connection = sqlite3.connect(dbName)
            self._connection.row_factory = sqlite3.Row
            self._connection.isolation_level = None
            self._create_table()
        except sqlite3.Error:
            traceback.print_exc()

    def _create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name TEXT,
                theater_name TEXT,
                seat_number TEXT,
                customer_name TEXT
            )
        """
        try:
            with self._connection:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(sql)
        except sqlite3.Error:
            traceback.print_exc()

    def insertTicket(self, movieName, theaterName, seatNumber, customerName):
        sql = "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) VALUES (?, ?, ?, ?)"
        try:
            with self._connection:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(sql, (movieName, theaterName, seatNumber, customerName))
        except sqlite3.Error:
            traceback.print_exc()

    def searchTicketsByCustomer(self, customerName):
        sql = "SELECT * FROM tickets WHERE customer_name = ?"
        tickets = []
        try:
            with self._connection:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(sql, (customerName,))
                    rows = cursor.fetchall()
            for row in rows:
                tickets.append(MovieTicketDB.Ticket(
                    row["id"],
                    row["movie_name"],
                    row["theater_name"],
                    row["seat_number"],
                    row["customer_name"]
                ))
        except sqlite3.Error:
            traceback.print_exc()
        return tickets

    def deleteTicket(self, ticketId):
        sql = "DELETE FROM tickets WHERE id = ?"
        try:
            with self._connection:
                with closing(self._connection.cursor()) as cursor:
                    cursor.execute(sql, (ticketId,))
        except sqlite3.Error:
            traceback.print_exc()

    def close(self):
        if self._connection is not None and not self._closed:
            try:
                self._connection.close()
                self._closed = True
            except sqlite3.Error:
                traceback.print_exc()

    class Ticket:
        def __init__(self, id, movieName, theaterName, seatNumber, customerName):
            self._id = id
            self._movieName = movieName
            self._theaterName = theaterName
            self._seatNumber = seatNumber
            self._customerName = customerName

        def getId(self):
            return self._id

        def getMovieName(self):
            return self._movieName

        def getTheaterName(self):
            return self._theaterName

        def getSeatNumber(self):
            return self._seatNumber

        def getCustomerName(self):
            return self._customerName
import sqlite3

class MovieTicketDB:
    def __init__(self, dbName):
        self.dbName = dbName
        self._connection = None
        try:
            self._connection = sqlite3.connect(dbName)
        except sqlite3.Error:
            raise RuntimeError("Unable to open database")
        self.create_table()

    def __del__(self):
        self.close_connection()

    def create_table(self):
        if self._connection is None:
            raise RuntimeError("Failed to create table: ")
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY,
            movie_name TEXT,
            theater_name TEXT,
            seat_number TEXT,
            customer_name TEXT
        )
        """
        try:
            self._connection.execute(create_table_sql)
            self._connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to create table: {e}")

    def insert_ticket(self, movieName, theaterName, seatNumber, customerName):
        if self._connection is None:
            raise RuntimeError("Failed to prepare statement")
        insert_sql = """
        INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name)
        VALUES (?, ?, ?, ?)
        """
        try:
            self._connection.execute(insert_sql, (movieName, theaterName, seatNumber, customerName))
            self._connection.commit()
        except sqlite3.Error:
            raise RuntimeError("Failed to insert ticket")

    def search_tickets_by_customer(self, customerName):
        if self._connection is None:
            raise RuntimeError("Failed to prepare statement")
        search_sql = "SELECT * FROM tickets WHERE customer_name = ?"
        try:
            cursor = self._connection.execute(search_sql, (customerName,))
            rows = cursor.fetchall()
        except sqlite3.Error:
            raise RuntimeError("Failed to prepare statement")
        results = []
        for row in rows:
            results.append([str(value) for value in row])
        return results

    def delete_ticket(self, ticketId):
        if self._connection is None:
            raise RuntimeError("Failed to prepare statement")
        delete_sql = "DELETE FROM tickets WHERE id = ?"
        try:
            self._connection.execute(delete_sql, (ticketId,))
            self._connection.commit()
        except sqlite3.Error:
            raise RuntimeError("Failed to delete ticket")

    def close_connection(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None
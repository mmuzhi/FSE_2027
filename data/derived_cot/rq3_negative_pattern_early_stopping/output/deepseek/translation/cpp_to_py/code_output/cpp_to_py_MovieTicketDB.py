import sqlite3

class MovieTicketDB:
    def __init__(self, dbName: str):
        self.dbName = dbName
        self.db = None
        try:
            self.db = sqlite3.connect(dbName)
        except sqlite3.Error:
            raise RuntimeError("Unable to open database")
        self.create_table()

    def __del__(self):
        self.close_connection()

    def create_table(self):
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
            self.db.execute(create_table_sql)
        except sqlite3.Error as e:
            raise RuntimeError("Failed to create table: " + str(e))

    def insert_ticket(self, movieName: str, theaterName: str, seatNumber: str, customerName: str):
        insert_sql = """
        INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name)
        VALUES (?, ?, ?, ?)
        """
        try:
            self.db.execute(insert_sql, (movieName, theaterName, seatNumber, customerName))
        except sqlite3.Error:
            raise RuntimeError("Failed to insert ticket")

    def search_tickets_by_customer(self, customerName: str):
        search_sql = "SELECT * FROM tickets WHERE customer_name = ?"
        try:
            cursor = self.db.execute(search_sql, (customerName,))
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append([str(val) for val in row])
            return results
        except sqlite3.Error:
            raise RuntimeError("Failed to prepare statement")

    def delete_ticket(self, ticketId: str):
        delete_sql = "DELETE FROM tickets WHERE id = ?"
        try:
            self.db.execute(delete_sql, (ticketId,))
        except sqlite3.Error:
            raise RuntimeError("Failed to delete ticket")

    def close_connection(self):
        if self.db is not None:
            self.db.close()
            self.db = None
import sqlite3


class MovieTicketDB:
    def __init__(self, db_name: str):
        self._db_name = db_name
        try:
            self._db = sqlite3.connect(db_name, isolation_level=None)
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
            self._db.execute(create_table_sql)
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to create table: {e}")

    def insert_ticket(self, movie_name: str, theater_name: str,
                      seat_number: str, customer_name: str):
        insert_sql = """
            INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name)
            VALUES (?, ?, ?, ?)
        """
        try:
            self._db.execute(insert_sql, (movie_name, theater_name, seat_number, customer_name))
        except sqlite3.OperationalError:
            raise RuntimeError("Failed to prepare statement")
        except sqlite3.Error:
            raise RuntimeError("Failed to insert ticket")

    def search_tickets_by_customer(self, customer_name: str):
        search_sql = """
            SELECT * FROM tickets WHERE customer_name = ?
        """
        try:
            cursor = self._db.execute(search_sql, (customer_name,))
        except sqlite3.OperationalError:
            raise RuntimeError("Failed to prepare statement")

        results = []
        try:
            for row in cursor:
                str_row = [str(col) for col in row]
                results.append(str_row)
        except sqlite3.Error:
            pass
        return results

    def delete_ticket(self, ticket_id: str):
        delete_sql = """
            DELETE FROM tickets WHERE id = ?
        """
        try:
            self._db.execute(delete_sql, (ticket_id,))
        except sqlite3.OperationalError:
            raise RuntimeError("Failed to prepare statement")
        except sqlite3.Error:
            raise RuntimeError("Failed to delete ticket")

    def close_connection(self):
        if self._db is not None:
            self._db.close()
            self._db = None
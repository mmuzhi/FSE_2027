import sqlite3


class MovieTicketDB:
    def __init__(self, db_name: str):
        self.db_name = db_name
        try:
            # isolation_level=None -> autocommit, matching sqlite3 default C behavior
            self.db = sqlite3.connect(db_name, isolation_level=None)
        except sqlite3.Error:
            raise RuntimeError("Unable to open database")
        self.create_table()

    def __del__(self):
        try:
            self.close_connection()
        except Exception:
            pass

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
            raise RuntimeError(f"Failed to create table: {e}")

    def insert_ticket(self, movie_name: str, theater_name: str,
                      seat_number: str, customer_name: str):
        insert_sql = """
        INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name)
        VALUES (?, ?, ?, ?)
    """
        try:
            self.db.execute(insert_sql,
                            (movie_name, theater_name, seat_number, customer_name))
        except sqlite3.Error:
            raise RuntimeError("Failed to insert ticket")

    def search_tickets_by_customer(self, customer_name: str):
        search_sql = """
        SELECT * FROM tickets WHERE customer_name = ?
    """
        try:
            cursor = self.db.execute(search_sql, (customer_name,))
        except sqlite3.Error:
            raise RuntimeError("Failed to prepare statement")

        results = []
        try:
            for row in cursor.fetchall():
                # C++ reads every column as text; mirror that with str()
                results.append([str(value) for value in row])
        except sqlite3.Error:
            raise RuntimeError("Failed to prepare statement")
        return results

    def delete_ticket(self, ticket_id: str):
        delete_sql = """
        DELETE FROM tickets WHERE id = ?
    """
        try:
            self.db.execute(delete_sql, (ticket_id,))
        except sqlite3.Error:
            raise RuntimeError("Failed to delete ticket")

    def close_connection(self):
        if self.db is not None:
            self.db.close()
            self.db = None
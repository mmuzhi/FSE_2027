import sqlite3


class MovieTicketDB:
    def __init__(self, db_name):
        self.db = None
        self.db_name = db_name
        try:
            # isolation_level=None keeps the connection in autocommit mode,
            # matching the default behavior of the SQLite C API used in the
            # original code (every statement commits immediately).
            self.db = sqlite3.connect(db_name, isolation_level=None)
        except sqlite3.Error:
            raise RuntimeError("Unable to open database")
        self.create_table()

    def __del__(self):
        # Destructor equivalent.
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
        except sqlite3.Error as err_msg:
            raise RuntimeError("Failed to create table: " + str(err_msg))

    def insert_ticket(self, movie_name, theater_name, seat_number, customer_name):
        insert_sql = """
        INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name)
        VALUES (?, ?, ?, ?)
    """
        try:
            self.db.execute(insert_sql, (movie_name, theater_name, seat_number, customer_name))
        except sqlite3.Error:
            raise RuntimeError("Failed to insert ticket")

    def search_tickets_by_customer(self, customer_name):
        search_sql = """
        SELECT * FROM tickets WHERE customer_name = ?
    """
        try:
            cursor = self.db.execute(search_sql, (customer_name,))
        except sqlite3.Error:
            raise RuntimeError("Failed to prepare statement")

        results = []
        # Mirrors the C++ loop: any step result other than SQLITE_ROW
        # (including errors) simply ends iteration, keeping the rows
        # gathered so far.
        while True:
            try:
                row = cursor.fetchone()
            except sqlite3.Error:
                break
            if row is None:
                break
            # sqlite3_column_text converted every column (including the
            # integer id) to its text representation; str() does the same.
            results.append([str(column) for column in row])
        return results

    def delete_ticket(self, ticket_id):
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
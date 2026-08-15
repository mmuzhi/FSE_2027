import sqlite3


def _c_str(value):
    """Mimic C++ c_str() semantics: truncate at the first null character."""
    if value is None:
        return ""
    s = str(value)
    idx = s.find("\0")
    if idx != -1:
        return s[:idx]
    return s


class MovieTicketDB:
    def __init__(self, dbName):
        self.db = None
        self.dbName = dbName
        try:
            self.db = sqlite3.connect(
                _c_str(dbName),
                isolation_level=None,
                timeout=0.0,
                check_same_thread=False,
            )
        except sqlite3.Error:
            raise RuntimeError("Unable to open database") from None
        self.create_table()

    def __del__(self):
        try:
            self.close_connection()
        except Exception:
            pass

    def create_table(self):
        if self.db is None:
            raise RuntimeError("Failed to create table: bad parameter or other API misuse")
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY,
            movie_name TEXT,
            theater_name TEXT,
            seat_number TEXT,
            customer_name TEXT
        )
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(create_table_sql)
        except sqlite3.Error as e:
            raise RuntimeError("Failed to create table: " + str(e)) from None
        finally:
            if cursor is not None:
                cursor.close()

    def insert_ticket(self, movieName, theaterName, seatNumber, customerName):
        if self.db is None:
            raise RuntimeError("Failed to prepare statement")
        insert_sql = """
        INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name)
        VALUES (?, ?, ?, ?)
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(
                insert_sql,
                (
                    _c_str(movieName),
                    _c_str(theaterName),
                    _c_str(seatNumber),
                    _c_str(customerName),
                ),
            )
        except sqlite3.Error:
            raise RuntimeError("Failed to insert ticket") from None
        finally:
            if cursor is not None:
                cursor.close()

    def search_tickets_by_customer(self, customerName):
        if self.db is None:
            raise RuntimeError("Failed to prepare statement")
        search_sql = """
        SELECT * FROM tickets WHERE customer_name = ?
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            try:
                cursor.execute(search_sql, (_c_str(customerName),))
            except sqlite3.Error:
                return []
            results = []
            while True:
                try:
                    row = cursor.fetchone()
                except sqlite3.Error:
                    break
                if row is None:
                    break
                results.append([_c_str(v) for v in row])
            return results
        finally:
            if cursor is not None:
                cursor.close()

    def delete_ticket(self, ticketId):
        if self.db is None:
            raise RuntimeError("Failed to prepare statement")
        delete_sql = """
        DELETE FROM tickets WHERE id = ?
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(delete_sql, (_c_str(ticketId),))
        except sqlite3.Error:
            raise RuntimeError("Failed to delete ticket") from None
        finally:
            if cursor is not None:
                cursor.close()

    def close_connection(self):
        if self.db is not None:
            try:
                self.db.close()
            except Exception:
                pass
            self.db = None
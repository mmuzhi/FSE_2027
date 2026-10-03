import sqlite3
from typing import List

class MovieTicketDB:
    def __init__(self, db_name: str):
        self.connection = None
        try:
            self.connection = sqlite3.connect(db_name)
            self.create_table()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_table(self):
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
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            raise  # Re-raise to allow the caller to handle if needed

    def insert_ticket(self, movie_name: str, theater_name: str, seat_number: str, customer_name: str):
        sql = """
        INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name)
        VALUES (?, ?, ?, ?)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (movie_name, theater_name, seat_number, customer_name))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error inserting ticket: {e}")
            raise

    def search_tickets_by_customer(self, customer_name: str) -> List['Ticket']:
        sql = "SELECT * FROM tickets WHERE customer_name = ?"
        tickets = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (customer_name,))
            rows = cursor.fetchall()
            for row in rows:
                ticket = Ticket(
                    id=row[0],
                    movie_name=row[1],
                    theater_name=row[2],
                    seat_number=row[3],
                    customer_name=row[4]
                )
                tickets.append(ticket)
        except sqlite3.Error as e:
            print(f"Error searching tickets: {e}")
            raise
        return tickets

    def delete_ticket(self, ticket_id: int):
        sql = "DELETE FROM tickets WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (ticket_id,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting ticket: {e}")
            raise

    def close(self):
        if self.connection is not None:
            try:
                self.connection.close()
            except sqlite3.Error as e:
                print(f"Error closing connection: {e}")

    class Ticket:
        def __init__(self, id: int, movie_name: str, theater_name: str, seat_number: str, customer_name: str):
            self.id = id
            self.movie_name = movie_name
            self.theater_name = theater_name
            self.seat_number = seat_number
            self.customer_name = customer_name

        def __repr__(self):
            return (f"Ticket(id={self.id}, movie_name='{self.movie_name}', "
                    f"theater_name='{self.theater_name}', seat_number='{self.seat_number}', "
                    f"customer_name='{self.customer_name}')")

        def __eq__(self, other):
            if not isinstance(other, MovieTicketDB.Ticket):
                return False
            return (self.id == other.id and
                    self.movie_name == other.movie_name and
                    self.theater_name == other.theater_name and
                    self.seat_number == other.seat_number and
                    self.customer_name == other.customer_name)

        def __hash__(self):
            return hash((self.id, self.movie_name, self.theater_name, self.seat_number, self.customer_name))

# Example usage (for testing purposes only)
if __name__ == "__main__":
    db = MovieTicketDB("tickets.db")
    db.insert_ticket("Inception", "Regal", "A1", "John Doe")
    tickets = db.search_tickets_by_customer("John Doe")
    print(tickets)
    db.delete_ticket(1)
    db.close()
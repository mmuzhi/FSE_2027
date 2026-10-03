import sqlite3
from typing import List, Any

class MovieTicketDB:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
        self.create_connection()
    
    def __del__(self):
        self.close_connection()
    
    def create_connection(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.create_table()
        except sqlite3.Error as e:
            raise RuntimeError(f"Unable to open database: {e}")
    
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
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to create table: {e}")
    
    def insert_ticket(self, movie_name: str, theater_name: str, seat_number: str, customer_name: str):
        insert_sql = """
        INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name)
        VALUES (?, ?, ?, ?)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_sql, (movie_name, theater_name, seat_number, customer_name))
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to insert ticket: {e}")
    
    def search_tickets_by_customer(self, customer_name: str) -> List[List[str]]:
        search_sql = "SELECT * FROM tickets WHERE customer_name = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(search_sql, (customer_name,))
            rows = cursor.fetchall()
            return [list(row) for row in rows]
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to search tickets: {e}")
    
    def delete_ticket(self, ticket_id: str):
        delete_sql = "DELETE FROM tickets WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(delete_sql, (ticket_id,))
            self.connection.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to delete ticket: {e}")
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
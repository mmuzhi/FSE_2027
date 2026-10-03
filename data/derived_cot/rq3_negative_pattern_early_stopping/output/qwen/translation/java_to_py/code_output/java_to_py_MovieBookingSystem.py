import datetime
from typing import List, Dict, Any

class MovieBookingSystem:
    def __init__(self):
        self.movies: List[Dict[str, Any]] = []

    def add_movie(self, name: str, price: float, start_time_str: str, end_time_str: str, n: int) -> None:
        try:
            start_time = datetime.time.fromisoformat(start_time_str)
            end_time = datetime.time.fromisoformat(end_time_str)
        except ValueError:
            raise ValueError("Invalid time format. Use 'HH:MM'.")
        
        movie = {
            "name": name,
            "price": price,
            "start_time": start_time,
            "end_time": end_time,
            "seats": [[0] * n for _ in range(n)]
        }
        self.movies.append(movie)

    def book_ticket(self, name: str, seats_to_book: List[List[int]]) -> str:
        for movie in self.movies:
            if movie["name"] == name:
                seats = movie["seats"]
                for row, col in seats_to_book:
                    if seats[row][col] == 0:
                        seats[row][col] = 1
                    else:
                        return "Booking failed."
                return "Booking success."
        return "Movie not found."

    def available_movies(self, start_time_str: str, end_time_str: str) -> List[str]:
        try:
            start_time = datetime.time.fromisoformat(start_time_str)
            end_time = datetime.time.fromisoformat(end_time_str)
        except ValueError:
            raise ValueError("Invalid time format. Use 'HH:MM'.")
        
        return [
            movie["name"]
            for movie in self.movies
            if not movie["start_time"].replace(microsecond=0) < start_time and
               not movie["end_time"].replace(microsecond=0) > end_time
        ]
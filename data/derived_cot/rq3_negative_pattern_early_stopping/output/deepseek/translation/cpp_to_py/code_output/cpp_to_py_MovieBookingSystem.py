from typing import List, Tuple

class MovieBookingSystem:
    class Movie:
        def __init__(self, name: str, price: float, start_minutes: int, end_minutes: int, n: int):
            self.name = name
            self.price = price
            self.start_minutes = start_minutes
            self.end_minutes = end_minutes
            self.seats = [[0] * n for _ in range(n)]

    def __init__(self):
        self.movies: List[MovieBookingSystem.Movie] = []

    def _parse_time(self, time_str: str) -> int:
        """Convert 'HH:MM' string to minutes since midnight. Raises ValueError on failure."""
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                raise ValueError
            hour = int(parts[0])
            minute = int(parts[1])
            if not (0 <= hour < 24 and 0 <= minute < 60):
                raise ValueError
            return hour * 60 + minute
        except (ValueError, IndexError):
            raise ValueError("Failed to parse time")

    def _is_time_in_range(self, start: int, end: int, check: int) -> bool:
        """Return True if start <= check <= end (inclusive)."""
        return start <= check <= end

    def add_movie(self, name: str, price: float, start_time: str, end_time: str, n: int) -> None:
        """Add a movie with given details. n is the side length of the square seating arrangement."""
        start = self._parse_time(start_time)
        end = self._parse_time(end_time)
        movie = self.Movie(name, price, start, end, n)
        self.movies.append(movie)

    def book_ticket(self, name: str, seats: List[Tuple[int, int]]) -> str:
        """
        Book the given seats for the movie named 'name'.
        Returns "Booking success." on success, "Booking failed." if any seat is
        already booked or out of bounds, and "Movie not found." if the movie doesn't exist.
        """
        for movie in self.movies:
            if movie.name == name:
                for row, col in seats:
                    if not (0 <= row < len(movie.seats) and 0 <= col < len(movie.seats[row])):
                        return "Booking failed."
                    if movie.seats[row][col] != 0:
                        return "Booking failed."
                for row, col in seats:
                    movie.seats[row][col] = 1
                return "Booking success."
        return "Movie not found."

    def available_movies(self, start_time: str, end_time: str) -> List[str]:
        """
        Return list of movie names whose entire showtime is within the given time range.
        Both start and end inclusive.
        """
        start = self._parse_time(start_time)
        end = self._parse_time(end_time)
        result = []
        for movie in self.movies:
            if self._is_time_in_range(start, end, movie.start_minutes) and \
               self._is_time_in_range(start, end, movie.end_minutes):
                result.append(movie.name)
        return result
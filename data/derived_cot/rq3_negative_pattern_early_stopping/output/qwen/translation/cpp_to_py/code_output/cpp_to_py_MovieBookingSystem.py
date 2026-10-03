from datetime import datetime, time

class MovieBookingSystem:
    class Movie:
        def __init__(self, name, price, start_time, end_time, seats):
            self.name = name
            self.price = price
            self.start_time = start_time
            self.end_time = end_time
            self.seats = seats

    def __init__(self):
        self.movies = []

    def parse_time(self, time_str):
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise RuntimeError("Failed to parse time")

    def is_time_in_range(self, start, end, check):
        def to_seconds(t):
            return t.hour * 3600 + t.minute * 60
        return to_seconds(start) <= to_seconds(check) <= to_seconds(end)

    def add_movie(self, name, price, start_time, end_time, n):
        start_time_parsed = self.parse_time(start_time)
        end_time_parsed = self.parse_time(end_time)
        seats = [[0] * n for _ in range(n)]
        movie = self.Movie(name, price, start_time_parsed, end_time_parsed, seats)
        self.movies.append(movie)

    def book_ticket(self, name, seats_to_book):
        for movie in self.movies:
            if movie.name == name:
                for seat in seats_to_book:
                    row, col = seat
                    if not (0 <= row < len(movie.seats) and 0 <= col < len(movie.seats[row])):
                        return "Booking failed."
                    if movie.seats[row][col] == 1:
                        return "Booking failed."
                    movie.seats[row][col] = 1
                return "Booking success."
        return "Movie not found."

    def available_movies(self, start_time, end_time):
        start_parsed = self.parse_time(start_time)
        end_parsed = self.parse_time(end_time)
        available = []
        for movie in self.movies:
            if (self.is_time_in_range(start_parsed, end_parsed, movie.start_time) and
                self.is_time_in_range(start_parsed, end_parsed, movie.end_time)):
                available.append(movie.name)
        return available
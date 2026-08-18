import re


class MovieBookingSystem:

    class Movie:
        def __init__(self, name, price, start_time, end_time, seats):
            self.name = name
            self.price = price
            self.start_time = start_time
            self.end_time = end_time
            self.seats = seats

    _TIME_RE = re.compile(r"\s*(\d{1,2}):(\d{1,2})")

    def __init__(self):
        self.movies = []

    def parse_time(self, time_str):
        m = self._TIME_RE.match(time_str)
        if not m:
            raise RuntimeError("Failed to parse time")
        hour = int(m.group(1))
        minute = int(m.group(2))
        if hour > 23 or minute > 59:
            raise RuntimeError("Failed to parse time")
        return (hour, minute)

    @staticmethod
    def _time_to_seconds(tm):
        return tm[0] * 3600 + tm[1] * 60

    def is_time_in_range(self, start, end, check):
        return (self._time_to_seconds(start) <= self._time_to_seconds(check)
                and self._time_to_seconds(check) <= self._time_to_seconds(end))

    def add_movie(self, name, price, start_time, end_time, n):
        movie = self.Movie(
            name=name,
            price=price,
            start_time=self.parse_time(start_time),
            end_time=self.parse_time(end_time),
            seats=[[0] * n for _ in range(n)],
        )
        self.movies.append(movie)

    def book_ticket(self, name, seats_to_book):
        for movie in self.movies:
            if movie.name == name:
                for row, col in seats_to_book:
                    if 0 <= row < len(movie.seats) and 0 <= col < len(movie.seats[row]):
                        if movie.seats[row][col] == 0:
                            movie.seats[row][col] = 1
                        else:
                            return "Booking failed."
                    else:
                        return "Booking failed."
                return "Booking success."
        return "Movie not found."

    def available_movies(self, start_time, end_time):
        start = self.parse_time(start_time)
        end = self.parse_time(end_time)

        available = []
        for movie in self.movies:
            if (self.is_time_in_range(start, end, movie.start_time)
                    and self.is_time_in_range(start, end, movie.end_time)):
                available.append(movie.name)
        return available
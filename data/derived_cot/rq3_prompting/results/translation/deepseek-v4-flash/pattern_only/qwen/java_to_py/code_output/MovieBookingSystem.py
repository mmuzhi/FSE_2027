import datetime


def _parse_time(value):
    try:
        return datetime.time.fromisoformat(value)
    except ValueError:
        # Fallback for Python versions that don't accept "HH:MM" and for
        # fractional seconds with more than 6 digits (Java accepts up to 9).
        parts = value.split(":")
        if len(parts) == 2:
            return datetime.time.fromisoformat(value + ":00")
        if len(parts) == 3:
            sec_part = parts[2]
            if "." in sec_part:
                sec, frac = sec_part.split(".", 1)
                if sec.isdigit() and frac.isdigit() and 0 < len(frac) <= 9:
                    # Truncate to microseconds (Python's time resolution)
                    return datetime.time.fromisoformat(
                        f"{parts[0]}:{parts[1]}:{sec}.{frac[:6]}"
                    )
        raise


class MovieBookingSystem:
    def __init__(self):
        self.movies = []

    def addMovie(self, name, price, startTime, endTime, n):
        movie = {
            "name": name,
            "price": price,
            "start_time": _parse_time(startTime),
            "end_time": _parse_time(endTime),
            "seats": [[0] * n for _ in range(n)],
        }
        self.movies.append(movie)

    def bookTicket(self, name, seatsToBook):
        for movie in self.movies:
            if movie["name"] == name:
                seats = movie["seats"]
                for seat in seatsToBook:
                    row, col = seat[0], seat[1]
                    if seats[row][col] == 0:
                        seats[row][col] = 1
                    else:
                        return "Booking failed."
                return "Booking success."
        return "Movie not found."

    def availableMovies(self, startTime, endTime):
        start = _parse_time(startTime)
        end = _parse_time(endTime)
        result = []
        for movie in self.movies:
            movie_start = movie["start_time"]
            movie_end = movie["end_time"]
            if not movie_start < start and not movie_end > end:
                result.append(movie["name"])
        return result

    def getMovies(self):
        return self.movies
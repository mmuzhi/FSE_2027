from datetime import time


class MovieBookingSystem:

    def __init__(self):
        self.movies = []

    def addMovie(self, name, price, startTime, endTime, n):
        movie = {
            "name": name,
            "price": price,
            "start_time": time.fromisoformat(startTime),
            "end_time": time.fromisoformat(endTime),
            "seats": [[0] * n for _ in range(n)],
        }
        self.movies.append(movie)

    def bookTicket(self, name, seatsToBook):
        for movie in self.movies:
            if movie["name"] == name:
                seats = movie["seats"]
                for seat in seatsToBook:
                    row = seat[0]
                    col = seat[1]
                    # Mimic Java ArrayIndexOutOfBoundsException (Python would
                    # silently wrap around on negative indices otherwise).
                    if not (0 <= row < len(seats) and 0 <= col < len(seats[row])):
                        raise IndexError(
                            f"Index [{row}][{col}] out of bounds for seat grid of size {len(seats)}"
                        )
                    if seats[row][col] == 0:
                        seats[row][col] = 1
                    else:
                        return "Booking failed."
                return "Booking success."
        return "Movie not found."

    def availableMovies(self, startTime, endTime):
        start = time.fromisoformat(startTime)
        end = time.fromisoformat(endTime)

        return [
            movie["name"]
            for movie in self.movies
            if not movie["start_time"] < start and not movie["end_time"] > end
        ]

    def getMovies(self):
        return self.movies
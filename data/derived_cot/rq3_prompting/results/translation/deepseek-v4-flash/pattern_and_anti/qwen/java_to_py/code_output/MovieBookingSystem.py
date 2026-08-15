from datetime import time

class MovieBookingSystem:
    def __init__(self):
        self.movies = []

    def addMovie(self, name, price, startTime, endTime, n):
        if n < 0:
            raise ValueError("NegativeArraySizeException")
        movie = {
            "name": name,
            "price": float(price),
            "start_time": time.fromisoformat(startTime),
            "end_time": time.fromisoformat(endTime),
            "seats": [[0] * n for _ in range(n)]
        }
        self.movies.append(movie)

    def bookTicket(self, name, seatsToBook):
        for movie in self.movies:
            if movie["name"] == name:
                seats = movie["seats"]
                for seat in seatsToBook:
                    row, col = seat[0], seat[1]
                    if row < 0 or row >= len(seats) or col < 0 or col >= len(seats[row]):
                        raise IndexError("Index out of bounds")
                    if seats[row][col] == 0:
                        seats[row][col] = 1
                    else:
                        return "Booking failed."
                return "Booking success."
        return "Movie not found."

    def availableMovies(self, startTime, endTime):
        start = time.fromisoformat(startTime)
        end = time.fromisoformat(endTime)
        result = []
        for movie in self.movies:
            movieStart = movie["start_time"]
            movieEnd = movie["end_time"]
            if movieStart >= start and movieEnd <= end:
                result.append(movie["name"])
        return result

    def getMovies(self):
        return self.movies
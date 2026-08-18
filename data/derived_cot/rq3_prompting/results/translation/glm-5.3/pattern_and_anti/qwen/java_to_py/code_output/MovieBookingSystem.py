import time


class MovieBookingSystem:

    def __init__(self):
        self.movies = []

    def addMovie(self, name, price, startTime, endTime, n):
        movie = {
            "name": name,
            "price": price,
            "start_time": time.strptime(startTime, "%H:%M:%S"),
            "end_time": time.strptime(endTime, "%H:%M:%S"),
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
                    if seats[row][col] == 0:
                        seats[row][col] = 1
                    else:
                        return "Booking failed."
                return "Booking success."
        return "Movie not found."

    def availableMovies(self, startTime, endTime):
        start = time.strptime(startTime, "%H:%M:%S")
        end = time.strptime(endTime, "%H:%M:%S")

        return [
            movie["name"]
            for movie in self.movies
            if not (movie["start_time"] < start) and not (movie["end_time"] > end)
        ]

    def getMovies(self):
        return self.movies
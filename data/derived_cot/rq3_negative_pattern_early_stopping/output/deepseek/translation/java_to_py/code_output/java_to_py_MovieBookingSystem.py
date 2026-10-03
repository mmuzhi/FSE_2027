import datetime

class MovieBookingSystem:
    def __init__(self):
        self.movies = []

    def add_movie(self, name, price, start_time, end_time, n):
        movie = {
            "name": name,
            "price": price,
            "start_time": datetime.datetime.strptime(start_time, "%H:%M").time(),
            "end_time": datetime.datetime.strptime(end_time, "%H:%M").time(),
            "seats": [[0] * n for _ in range(n)]
        }
        self.movies.append(movie)

    def book_ticket(self, name, seats_to_book):
        for movie in self.movies:
            if movie["name"] == name:
                seats = movie["seats"]
                for seat in seats_to_book:
                    row, col = seat[0], seat[1]
                    if seats[row][col] == 0:
                        seats[row][col] = 1
                    else:
                        return "Booking failed."
                return "Booking success."
        return "Movie not found."

    def available_movies(self, start_time, end_time):
        start = datetime.datetime.strptime(start_time, "%H:%M").time()
        end = datetime.datetime.strptime(end_time, "%H:%M").time()
        result = []
        for movie in self.movies:
            movie_start = movie["start_time"]
            movie_end = movie["end_time"]
            if movie_start >= start and movie_end <= end:
                result.append(movie["name"])
        return result

    def get_movies(self):
        return self.movies
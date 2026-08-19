#include <cstdio>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class MovieBookingSystem {
public:
    MovieBookingSystem() = default;

    // Add a new movie into movies_
    void add_movie(const std::string& name, double price,
                   const std::string& start_time, const std::string& end_time, int n) {
        if (n < 0) {
            throw std::invalid_argument("negative dimensions are not allowed");
        }
        Movie movie;
        movie.name = name;
        movie.price = price;
        movie.start_time = parse_time(start_time);
        movie.end_time = parse_time(end_time);
        movie.seats.assign(static_cast<std::size_t>(n),
                           std::vector<double>(static_cast<std::size_t>(n), 0.0));
        movies_.push_back(std::move(movie));
    }

    // Book tickets; mutates seats incrementally, mirroring Python's partial
    // mutation before a potential "Booking failed."
    std::string book_ticket(const std::string& name,
                            const std::vector<std::pair<int, int>>& seats_to_book) {
        for (auto& movie : movies_) {
            if (movie.name == name) {
                for (const auto& seat : seats_to_book) {
                    std::size_t r = py_index(seat.first, movie.seats.size());
                    std::size_t c = py_index(seat.second, movie.seats[r].size());
                    if (movie.seats[r][c] == 0) {
                        movie.seats[r][c] = 1;
                    } else {
                        return "Booking failed.";
                    }
                }
                return "Booking success.";
            }
        }
        return "Movie not found.";
    }

    // Names of movies fully contained within [start_time, end_time]
    std::vector<std::string> available_movies(const std::string& start_time,
                                              const std::string& end_time) {
        int start = parse_time(start_time);
        int end = parse_time(end_time);

        std::vector<std::string> result;
        for (const auto& movie : movies_) {
            if (start <= movie.start_time && movie.end_time <= end) {
                result.push_back(movie.name);
            }
        }
        return result;
    }

private:
    struct Movie {
        std::string name;
        double price;
        int start_time;  // minutes since midnight
        int end_time;    // minutes since midnight
        std::vector<std::vector<double>> seats;
    };

    // Mimics datetime.strptime(s, "%H:%M") -> minutes since midnight.
    // Rejects trailing garbage and out-of-range values like Python does.
    static int parse_time(const std::string& t) {
        int h = 0, m = 0, consumed = 0;
        if (std::sscanf(t.c_str(), "%d:%d%n", &h, &m, &consumed) != 2 ||
            consumed != static_cast<int>(t.size()) ||
            h < 0 || h > 23 || m < 0 || m > 59) {
            throw std::invalid_argument(
                "time data '" + t + "' does not match format '%H:%M'");
        }
        return h * 60 + m;
    }

    // Mimics Python indexing: negative indices wrap, out of range throws.
    static std::size_t py_index(int i, std::size_t size) {
        int s = static_cast<int>(size);
        int j = (i < 0) ? i + s : i;
        if (j < 0 || j >= s) {
            throw std::out_of_range("index out of range");
        }
        return static_cast<std::size_t>(j);
    }

    std::vector<Movie> movies_;
};
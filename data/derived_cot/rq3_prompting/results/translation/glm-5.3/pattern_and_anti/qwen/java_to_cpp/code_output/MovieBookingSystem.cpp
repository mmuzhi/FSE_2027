#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class MovieBookingSystem {
public:
    struct Movie {
        std::string name;
        double price;
        long long start_time;  // seconds since midnight (parsed LocalTime)
        long long end_time;    // seconds since midnight (parsed LocalTime)
        std::vector<std::vector<int>> seats;
    };

    MovieBookingSystem() = default;

    void addMovie(const std::string& name, double price,
                  const std::string& startTime, const std::string& endTime, int n) {
        Movie movie;
        movie.name = name;
        movie.price = price;
        movie.start_time = parseTime(startTime);
        movie.end_time = parseTime(endTime);
        movie.seats.assign(static_cast<size_t>(n), std::vector<int>(static_cast<size_t>(n), 0));
        movies.push_back(std::move(movie));
    }

    std::string bookTicket(const std::string& name,
                           const std::vector<std::vector<int>>& seatsToBook) {
        for (auto& movie : movies) {
            if (movie.name == name) {
                auto& seats = movie.seats;
                for (const auto& seat : seatsToBook) {
                    int row = seat[0];
                    int col = seat[1];
                    if (row < 0 || row >= static_cast<int>(seats.size()) ||
                        col < 0 || col >= static_cast<int>(seats[row].size())) {
                        throw std::out_of_range("seat index out of range");
                    }
                    if (seats[row][col] == 0) {
                        seats[row][col] = 1;
                    } else {
                        return "Booking failed.";
                    }
                }
                return "Booking success.";
            }
        }
        return "Movie not found.";
    }

    std::vector<std::string> availableMovies(const std::string& startTime,
                                             const std::string& endTime) {
        long long start = parseTime(startTime);
        long long end = parseTime(endTime);

        std::vector<std::string> result;
        for (const auto& movie : movies) {
            if (movie.start_time >= start && movie.end_time <= end) {
                result.push_back(movie.name);
            }
        }
        return result;
    }

    std::vector<Movie>& getMovies() {
        return movies;
    }

private:
    std::vector<Movie> movies;

    // Parses ISO local time ("HH:mm" or "HH:mm:ss[.fff]") to seconds since midnight,
    // mirroring LocalTime.parse comparison semantics.
    static long long parseTime(const std::string& s) {
        std::istringstream iss(s);
        std::string token;
        long long h = 0, m = 0, sec = 0;
        if (std::getline(iss, token, ':')) {
            h = std::stoll(token);
            if (std::getline(iss, token, ':')) {
                m = std::stoll(token);
                if (std::getline(iss, token, ':')) {
                    auto dot = token.find('.');
                    if (dot != std::string::npos) {
                        token = token.substr(0, dot);
                    }
                    sec = std::stoll(token);
                }
            }
        }
        return h * 3600 + m * 60 + sec;
    }
};
#include <string>
#include <vector>
#include <stdexcept>
#include <sstream>
#include <algorithm>
#include <chrono>
#include <iomanip>

// Simple time representation (hours:minutes) for compatibility with LocalTime parsing
struct Time {
    int hours;
    int minutes;

    // Parse "HH:mm" format; throws std::invalid_argument on failure
    static Time parse(const std::string& str) {
        std::istringstream ss(str);
        char colon;
        int h, m;
        if (!(ss >> h >> colon >> m) || colon != ':' || ss.fail() || !ss.eof()) {
            throw std::invalid_argument("Invalid time format: " + str + " (expected HH:mm)");
        }
        if (h < 0 || h > 23 || m < 0 || m > 59) {
            throw std::invalid_argument("Time out of range: " + str);
        }
        return {h, m};
    }

    // Comparison operators for availableMovies filter
    bool operator<(const Time& other) const {
        return (hours < other.hours) || (hours == other.hours && minutes < other.minutes);
    }
    bool operator>=(const Time& other) const { return !(*this < other); }
    bool operator<=(const Time& other) const { return !(other < *this); }
    bool operator>(const Time& other) const { return other < *this; }
};

// Movie data structure
struct Movie {
    std::string name;
    double price;
    Time start_time;
    Time end_time;
    std::vector<std::vector<int>> seats;  // n x n matrix (0=free, 1=booked)

    Movie(const std::string& name, double price, const Time& start, const Time& end, int n)
        : name(name), price(price), start_time(start), end_time(end), seats(n, std::vector<int>(n, 0)) {}
};

class MovieBookingSystem {
private:
    std::vector<Movie> movies;

public:
    MovieBookingSystem() = default;

    void addMovie(const std::string& name, double price,
                  const std::string& startTime, const std::string& endTime, int n) {
        Time start = Time::parse(startTime);
        Time end = Time::parse(endTime);
        movies.emplace_back(name, price, start, end, n);
    }

    std::string bookTicket(const std::string& name, const std::vector<std::vector<int>>& seatsToBook) {
        for (auto& movie : movies) {
            if (movie.name == name) {
                // Check each seat and book if free
                for (const auto& seat : seatsToBook) {
                    if (seat.size() != 2) {
                        throw std::invalid_argument("Each seat coordinate must have exactly two elements");
                    }
                    int row = seat[0];
                    int col = seat[1];
                    // Use at() to get bounds checking (similar to Java ArrayIndexOutOfBounds)
                    if (movie.seats.at(row).at(col) == 0) {
                        movie.seats[row][col] = 1;
                    } else {
                        return "Booking failed.";
                    }
                }
                return "Booking success.";
            }
        }
        return "Movie not found.";
    }

    std::vector<std::string> availableMovies(const std::string& startTime, const std::string& endTime) {
        Time start = Time::parse(startTime);
        Time end = Time::parse(endTime);
        std::vector<std::string> result;
        for (const auto& movie : movies) {
            // Condition: movie.start_time >= start && movie.end_time <= end
            if (!(movie.start_time < start) && !(movie.end_time > end)) {
                result.push_back(movie.name);
            }
        }
        return result;
    }

    // Returns non-const reference to internal vector (mimics Java's mutable list)
    std::vector<Movie>& getMovies() {
        return movies;
    }

    // Const version for read-only access (optional, but good practice)
    const std::vector<Movie>& getMovies() const {
        return movies;
    }
};
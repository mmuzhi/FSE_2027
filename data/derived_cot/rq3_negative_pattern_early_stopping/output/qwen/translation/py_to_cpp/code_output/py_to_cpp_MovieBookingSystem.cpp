#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <sstream>
#include <ctime>
#include <chrono>

namespace {

std::chrono::system_clock::time_point string_to_time_point(const std::string& time_str) {
    std::tm t = {};
    std::istringstream ss(time_str);
    ss >> std::get_time(&t, "%H:%M");
    std::time_t tt = std::mktime(&t);
    return std::chrono::system_clock::from_time_t(tt);
}

}

struct Movie {
    std::string name;
    double price;
    std::chrono::system_clock::time_point start_time;
    std::chrono::system_clock::time_point end_time;
    std::vector<std::vector<int>> seats;
};

class MovieBookingSystem {
private:
    std::vector<Movie> movies;

public:
    MovieBookingSystem() {}

    void add_movie(const std::string& name, double price, const std::string& start_time_str, const std::string& end_time_str, int n) {
        auto start_time = string_to_time_point(start_time_str);
        auto end_time = string_to_time_point(end_time_str);

        // Create a 2D vector of zeros
        std::vector<std::vector<int>> seats(n, std::vector<int>(n, 0));

        Movie movie = {name, price, start_time, end_time, seats};
        movies.push_back(movie);
    }

    std::string book_ticket(const std::string& name, const std::vector<std::pair<int, int>>& seats_to_book) {
        for (auto& movie : movies) {
            if (movie.name == name) {
                for (const auto& seat : seats_to_book) {
                    int row = seat.first;
                    int col = seat.second;
                    if (row < 0 || row >= movie.seats.size() || col < 0 || col >= movie.seats[0].size()) {
                        // This seat is out of bounds, booking fails.
                        return "Booking failed.";
                    }
                    if (movie.seats[row][col] == 0) {
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

    std::vector<std::string> available_movies(const std::string& start_time_str, const std::string& end_time_str) {
        auto start_time = string_to_time_point(start_time_str);
        auto end_time = string_to_time_point(end_time_str);

        std::vector<std::string> available;
        for (const auto& movie : movies) {
            if (start_time <= movie.start_time && movie.end_time <= end_time) {
                available.push_back(movie.name);
            }
        }
        return available;
    }
};
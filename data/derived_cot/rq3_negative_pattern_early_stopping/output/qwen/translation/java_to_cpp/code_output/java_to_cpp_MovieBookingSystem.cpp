#include <vector>
#include <string>
#include <stdexcept>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <algorithm>

struct Movie {
    std::string name;
    double price;
    int startMinutes;
    int endMinutes;
    std::vector<std::vector<int>> seats;
};

class MovieBookingSystem {
private:
    std::vector<Movie> movies;

    int parseTime(const std::string& timeStr) {
        std::istringstream ss(timeStr);
        int hours, minutes;
        char colon;
        if (!(ss >> hours >> std::ws >> colon >> minutes)) {
            throw std::invalid_argument("Invalid time format");
        }
        if (hours < 0 || hours > 23 || minutes < 0 || minutes > 59) {
            throw std::invalid_argument("Invalid time value");
        }
        return hours * 60 + minutes;
    }

public:
    MovieBookingSystem() = default;

    void addMovie(const std::string& name, double price, const std::string& startTime, const std::string& endTime, int n) {
        int startMinutes = parseTime(startTime);
        int endMinutes = parseTime(endTime);
        Movie movie;
        movie.name = name;
        movie.price = price;
        movie.startMinutes = startMinutes;
        movie.endMinutes = endMinutes;
        movie.seats = std::vector<std::vector<int>>(n, std::vector<int>(n, 0));
        movies.push_back(movie);
    }

    std::string bookTicket(const std::string& name, const std::vector<std::vector<int>>& seatsToBook) {
        for (const auto& movie : movies) {
            if (movie.name == name) {
                const auto& seats = movie.seats;
                for (const auto& row : seatsToBook) {
                    int rowIdx = row[0];
                    int colIdx = row[1];
                    if (rowIdx < 0 || rowIdx >= seats.size() || colIdx < 0 || colIdx >= seats[rowIdx].size()) {
                        return "Invalid seat coordinates.";
                    }
                    if (seats[rowIdx][colIdx] == 0) {
                        seats[rowIdx][colIdx] = 1;
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
        int startMinutes = parseTime(startTime);
        int endMinutes = parseTime(endTime);

        std::vector<std::string> result;
        for (const auto& movie : movies) {
            if (movie.startMinutes >= startMinutes && movie.endMinutes <= endMinutes) {
                result.push_back(movie.name);
            }
        }
        return result;
    }
};
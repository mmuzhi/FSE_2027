#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <utility>
#include <stdexcept>

class MovieBookingSystem {
private:
    struct Movie {
        std::string name;
        double price;
        int start_hour;
        int start_min;
        int end_hour;
        int end_min;
        std::vector<std::vector<double>> seats;
    };

    std::vector<Movie> movies;

    // Helper: convert hour+minute to total minutes
    static int toMinutes(int hour, int min) {
        return hour * 60 + min;
    }

    // Helper: parse "HH:MM" string to hour and minute
    static void parseTime(const std::string& timeStr, int& hour, int& min) {
        std::istringstream ss(timeStr);
        char colon;
        ss >> hour >> colon >> min;
        if (ss.fail() || colon != ':') {
            throw std::invalid_argument("Invalid time format: " + timeStr);
        }
    }

public:
    MovieBookingSystem() = default;

    void add_movie(const std::string& name, double price,
                   const std::string& start_time, const std::string& end_time,
                   int n) {
        int sh, sm, eh, em;
        parseTime(start_time, sh, sm);
        parseTime(end_time, eh, em);

        Movie movie;
        movie.name = name;
        movie.price = price;
        movie.start_hour = sh;
        movie.start_min = sm;
        movie.end_hour = eh;
        movie.end_min = em;
        movie.seats.assign(n, std::vector<double>(n, 0.0));

        movies.push_back(std::move(movie));
    }

    std::string book_ticket(const std::string& name,
                            const std::vector<std::pair<int, int>>& seats_to_book) {
        for (auto& movie : movies) {
            if (movie.name == name) {
                for (const auto& seat : seats_to_book) {
                    int row = seat.first;
                    int col = seat.second;
                    // Use .at() to raise out_of_range for invalid indices (like Python's IndexError)
                    if (movie.seats.at(row).at(col) == 0.0) {
                        movie.seats[row][col] = 1.0;
                    } else {
                        return "Booking failed.";
                    }
                }
                return "Booking success.";
            }
        }
        return "Movie not found.";
    }

    std::vector<std::string> available_movies(const std::string& start_time,
                                              const std::string& end_time) {
        int sh, sm, eh, em;
        parseTime(start_time, sh, sm);
        parseTime(end_time, eh, em);

        int start_minutes = toMinutes(sh, sm);
        int end_minutes = toMinutes(eh, em);

        std::vector<std::string> result;
        for (const auto& movie : movies) {
            int movie_start = toMinutes(movie.start_hour, movie.start_min);
            int movie_end = toMinutes(movie.end_hour, movie.end_min);
            if (start_minutes <= movie_start && movie_end <= end_minutes) {
                result.push_back(movie.name);
            }
        }
        return result;
    }
};
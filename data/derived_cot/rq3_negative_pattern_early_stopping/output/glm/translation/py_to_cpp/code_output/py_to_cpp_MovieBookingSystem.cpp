#include <string>
#include <vector>
#include <ctime>
#include <sstream>
#include <iomanip>
#include <utility>

class MovieBookingSystem {
public:
    struct Movie {
        std::string name;
        double price;
        std::tm start_time;
        std::tm end_time;
        std::vector<std::vector<double>> seats;
    };

private:
    std::vector<Movie> movies;

    static std::tm parse_time(const std::string& time_str) {
        std::tm tm = {};
        tm.tm_year = 0;
        tm.tm_mon = 0;
        tm.tm_mday = 1;
        std::istringstream iss(time_str);
        iss >> std::get_time(&tm, "%H:%M");
        return tm;
    }

    static int compare_time(const std::tm& a, const std::tm& b) {
        if (a.tm_hour != b.tm_hour) return a.tm_hour - b.tm_hour;
        return a.tm_min - b.tm_min;
    }

public:
    MovieBookingSystem() = default;

    void add_movie(const std::string& name, double price,
                   const std::string& start_time, const std::string& end_time, int n) {
        Movie movie;
        movie.name = name;
        movie.price = price;
        movie.start_time = parse_time(start_time);
        movie.end_time = parse_time(end_time);
        movie.seats = std::vector<std::vector<double>>(n, std::vector<double>(n, 0.0));
        movies.push_back(movie);
    }

    std::string book_ticket(const std::string& name,
                            const std::vector<std::pair<int, int>>& seats_to_book) {
        for (auto& movie : movies) {
            if (movie.name == name) {
                for (const auto& seat : seats_to_book) {
                    if (movie.seats[seat.first][seat.second] == 0) {
                        movie.seats[seat.first][seat.second] = 1;
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
        std::tm start = parse_time(start_time);
        std::tm end = parse_time(end_time);

        std::vector<std::string> available;
        for (const auto& movie : movies) {
            if (compare_time(start, movie.start_time) <= 0 &&
                compare_time(movie.end_time, end) <= 0) {
                available.push_back(movie.name);
            }
        }
        return available;
    }
};
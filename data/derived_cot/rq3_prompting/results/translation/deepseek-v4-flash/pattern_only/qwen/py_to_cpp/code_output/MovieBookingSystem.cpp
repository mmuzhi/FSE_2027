#include <string>
#include <vector>
#include <utility>
#include <stdexcept>

struct Movie {
    std::string name;
    double price;
    int start_time;  // minutes from midnight
    int end_time;    // minutes from midnight
    std::vector<std::vector<double>> seats;
};

class MovieBookingSystem {
public:
    std::vector<Movie> movies;

    void add_movie(const std::string& name, double price,
                   const std::string& start_time, const std::string& end_time, int n) {
        Movie movie;
        movie.name = name;
        movie.price = price;
        movie.start_time = parse_time(start_time);
        movie.end_time = parse_time(end_time);
        movie.seats.assign(n, std::vector<double>(n, 0.0));
        movies.push_back(movie);
    }

    std::string book_ticket(const std::string& name,
                            const std::vector<std::pair<int, int>>& seats_to_book) {
        for (auto& movie : movies) {
            if (movie.name == name) {
                for (const auto& seat : seats_to_book) {
                    double& seat_value = movie.seats.at(seat.first).at(seat.second);
                    if (seat_value == 0.0) {
                        seat_value = 1.0;
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
        int start = parse_time(start_time);
        int end = parse_time(end_time);

        std::vector<std::string> result;
        for (const auto& movie : movies) {
            if (start <= movie.start_time && movie.end_time <= end) {
                result.push_back(movie.name);
            }
        }
        return result;
    }

private:
    static int parse_time(const std::string& time_str) {
        size_t colon = time_str.find(':');
        if (colon == std::string::npos) {
            throw std::invalid_argument("Invalid time format");
        }
        int hour = std::stoi(time_str.substr(0, colon));
        int minute = std::stoi(time_str.substr(colon + 1));
        return hour * 60 + minute;
    }
};
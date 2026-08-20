#include <cctype>
#include <cstddef>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

// C++ translation of the Python MovieBookingSystem.
//
// datetime.strptime(s, "%H:%M") always yields a datetime on 1900-01-01, so a
// time is stored as "minutes since midnight"; ordering/equality is preserved.
class MovieBookingSystem {
public:
    struct Movie {
        std::string name;
        double price;
        int start_time;  // minutes since midnight (datetime(1900, 1, 1, HH, MM))
        int end_time;    // minutes since midnight
        std::vector<std::vector<double>> seats;  // n x n grid of 0.0 / 1.0 (np.zeros)
    };

    // Public, mirroring the directly accessible Python attribute `self.movies`.
    std::vector<Movie> movies;

    MovieBookingSystem() = default;

    void add_movie(const std::string& name, double price,
                   const std::string& start_time, const std::string& end_time, int n) {
        // Parse first: Python raises ValueError (and appends nothing) on bad input.
        const int start_minutes = parse_time(start_time);
        const int end_minutes = parse_time(end_time);

        if (n < 0) {
            // numpy raises ValueError("negative dimensions are not allowed")
            throw std::invalid_argument("negative dimensions are not allowed");
        }

        Movie movie;
        movie.name = name;
        movie.price = price;
        movie.start_time = start_minutes;
        movie.end_time = end_minutes;
        movie.seats.assign(static_cast<std::size_t>(n),
                           std::vector<double>(static_cast<std::size_t>(n), 0.0));
        movies.push_back(std::move(movie));
    }

    std::string book_ticket(const std::string& name,
                            const std::vector<std::pair<int, int>>& seats_to_book) {
        for (Movie& movie : movies) {
            if (movie.name == name) {
                for (const std::pair<int, int>& seat : seats_to_book) {
                    const std::size_t row =
                        normalize_index(seat.first, static_cast<int>(movie.seats.size()));
                    std::vector<double>& row_seats = movie.seats[row];
                    const std::size_t col =
                        normalize_index(seat.second, static_cast<int>(row_seats.size()));
                    if (row_seats[col] == 0.0) {
                        // Seats booked before a later failure stay booked (as in Python).
                        row_seats[col] = 1.0;
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
        const int start_minutes = parse_time(start_time);
        const int end_minutes = parse_time(end_time);

        std::vector<std::string> available;
        for (const Movie& movie : movies) {
            if (start_minutes <= movie.start_time && movie.end_time <= end_minutes) {
                available.push_back(movie.name);
            }
        }
        return available;
    }

private:
    // Equivalent of datetime.strptime(s, "%H:%M").
    // Mirrors Python's strptime rules: 1-2 digit hour (<= 23), ':',
    // 1-2 digit minute (<= 59), nothing else. Throws std::invalid_argument
    // where Python raises ValueError.
    static int parse_time(const std::string& time_str) {
        const std::string mismatch =
            "time data '" + time_str + "' does not match format '%H:%M'";

        std::size_t i = 0;
        auto read_field = [&](int max_digits, int max_value) -> int {
            int value = 0;
            int digits = 0;
            while (i < time_str.size() && digits < max_digits &&
                   std::isdigit(static_cast<unsigned char>(time_str[i]))) {
                value = value * 10 + (time_str[i] - '0');
                ++i;
                ++digits;
            }
            if (digits == 0 || (digits == max_digits && value > max_value)) {
                throw std::invalid_argument(mismatch);
            }
            return value;
        };

        const int hour = read_field(2, 23);
        if (i >= time_str.size() || time_str[i] != ':') {
            throw std::invalid_argument(mismatch);
        }
        ++i;  // consume ':'
        const int minute = read_field(2, 59);
        if (i != time_str.size()) {
            throw std::invalid_argument("unconverted data remains: '" +
                                        time_str.substr(i) + "'");
        }
        return hour * 60 + minute;
    }

    // Python/numpy indexing: negative indices count from the end; anything
    // still out of range raises (Python raises IndexError).
    static std::size_t normalize_index(int index, int size) {
        int i = index;
        if (i < 0) {
            i += size;
        }
        if (i < 0 || i >= size) {
            throw std::out_of_range("index " + std::to_string(index) +
                                    " is out of bounds for axis 0 with size " +
                                    std::to_string(size));
        }
        return static_cast<std::size_t>(i);
    }
};
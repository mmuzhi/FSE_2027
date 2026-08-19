#include <cctype>
#include <cstddef>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace org {
namespace example {

// Minimal equivalent of java.time.LocalTime, ISO format "HH:mm[:ss[.fraction]]".
struct LocalTime {
    int hour = 0;
    int minute = 0;
    int second = 0;
    long long nano = 0;

    static LocalTime parse(const std::string& text) {
        const std::string msg = "Text '" + text + "' could not be parsed";
        LocalTime t;
        int fields[3] = {0, 0, 0};
        int count = 0;
        std::size_t i = 0;

        while (true) {
            if (i + 2 > text.size() ||
                !std::isdigit(static_cast<unsigned char>(text[i])) ||
                !std::isdigit(static_cast<unsigned char>(text[i + 1]))) {
                throw std::invalid_argument(msg);  // ~ DateTimeParseException
            }
            fields[count++] = (text[i] - '0') * 10 + (text[i + 1] - '0');
            i += 2;

            if (i == text.size()) break;

            if (text[i] == ':' && count < 3) {
                ++i;
                continue;
            }
            if (text[i] == '.' && count == 3) {
                ++i;
                if (i >= text.size() ||
                    !std::isdigit(static_cast<unsigned char>(text[i]))) {
                    throw std::invalid_argument(msg);
                }
                long long scale = 100000000LL;
                while (i < text.size() &&
                       std::isdigit(static_cast<unsigned char>(text[i]))) {
                    if (scale == 0) throw std::invalid_argument(msg);  // >9 fraction digits
                    t.nano += static_cast<long long>(text[i] - '0') * scale;
                    scale /= 10;
                    ++i;
                }
                if (i != text.size()) throw std::invalid_argument(msg);
                break;
            }
            throw std::invalid_argument(msg);
        }

        if (count < 2) throw std::invalid_argument(msg);  // "HH:mm" minimum
        if (fields[0] > 23 || fields[1] > 59 || (count == 3 && fields[2] > 59)) {
            throw std::invalid_argument(msg);
        }

        t.hour = fields[0];
        t.minute = fields[1];
        t.second = (count == 3) ? fields[2] : 0;
        return t;
    }

    bool operator<(const LocalTime& o) const {
        return std::tie(hour, minute, second, nano) <
               std::tie(o.hour, o.minute, o.second, o.nano);
    }
};

// Equivalent of the Map<String, Object> movie record.
struct Movie {
    std::string name;
    double price;
    LocalTime start_time;
    LocalTime end_time;
    std::vector<std::vector<int>> seats;
};

class MovieBookingSystem {
private:
    std::vector<Movie> movies;

public:
    MovieBookingSystem() = default;

    void addMovie(const std::string& name, double price,
                  const std::string& startTime, const std::string& endTime, int n) {
        Movie movie;
        movie.name = name;
        movie.price = price;
        movie.start_time = LocalTime::parse(startTime);
        movie.end_time = LocalTime::parse(endTime);
        movie.seats.assign(static_cast<std::size_t>(n),
                           std::vector<int>(static_cast<std::size_t>(n), 0));
        movies.push_back(std::move(movie));
    }

    std::string bookTicket(const std::string& name,
                           const std::vector<std::vector<int>>& seatsToBook) {
        for (Movie& movie : movies) {
            if (movie.name == name) {
                for (const std::vector<int>& seat : seatsToBook) {
                    int row = seat.at(0);   // .at(): ~ArrayIndexOutOfBounds on bad input
                    int col = seat.at(1);
                    if (movie.seats.at(row).at(col) == 0) {
                        movie.seats[row][col] = 1;
                    } else {
                        return "Booking failed.";  // earlier seats stay booked
                    }
                }
                return "Booking success.";
            }
        }
        return "Movie not found.";
    }

    std::vector<std::string> availableMovies(const std::string& startTime,
                                             const std::string& endTime) {
        LocalTime start = LocalTime::parse(startTime);
        LocalTime end = LocalTime::parse(endTime);

        std::vector<std::string> result;
        for (const Movie& movie : movies) {
            // !movieStart.isBefore(start) && !movieEnd.isAfter(end)
            if (!(movie.start_time < start) && !(end < movie.end_time)) {
                result.push_back(movie.name);
            }
        }
        return result;
    }

    // Returns the live list (Java returns the internal reference).
    std::vector<Movie>& getMovies() { return movies; }
};

} // namespace example
} // namespace org
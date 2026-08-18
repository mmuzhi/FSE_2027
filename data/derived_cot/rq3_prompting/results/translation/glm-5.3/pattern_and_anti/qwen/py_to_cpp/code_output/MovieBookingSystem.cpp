#include <cctype>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

// Mirrors datetime.strptime(s, "%H:%M") -> time-of-day (year/month/day are irrelevant here)
struct TimeHM {
    int hour;
    int minute;
};

int toIntStrict(const std::string& s) {
    if (s.empty() || !std::isdigit(static_cast<unsigned char>(s[0])))
        throw std::invalid_argument("time data does not match format '%H:%M'");
    std::size_t pos = 0;
    int v = std::stoi(s, &pos);
    if (pos != s.size())
        throw std::invalid_argument("time data does not match format '%H:%M'");
    return v;
}

TimeHM parseHM(const std::string& s) {
    std::size_t colon = s.find(':');
    if (colon == std::string::npos)
        throw std::invalid_argument("time data '" + s + "' does not match format '%H:%M'");
    int h, m;
    try {
        h = toIntStrict(s.substr(0, colon));
        m = toIntStrict(s.substr(colon + 1));
    } catch (const std::invalid_argument&) {
        throw std::invalid_argument("time data '" + s + "' does not match format '%H:%M'");
    } catch (const std::out_of_range&) {
        throw std::invalid_argument("time data '" + s + "' does not match format '%H:%M'");
    }
    if (h < 0 || h > 23 || m < 0 || m > 59)
        throw std::invalid_argument("unconverted data remains / value out of range: '" + s + "'");
    return TimeHM{h, m};
}

bool lessEq(const TimeHM& a, const TimeHM& b) {
    return a.hour * 60 + a.minute <= b.hour * 60 + b.minute;
}

// Python-style index normalization (negative indices count from the end)
std::size_t normIndex(int i, std::size_t n) {
    if (i < 0) i += static_cast<int>(n);
    if (i < 0 || i >= static_cast<int>(n))
        throw std::out_of_range("seat index out of range");
    return static_cast<std::size_t>(i);
}

}  // namespace

struct Movie {
    std::string name;
    double price;
    TimeHM start_time;
    TimeHM end_time;
    std::vector<std::vector<int>> seats;  // 0 = free, 1 = booked (numpy zeros equivalent)
};

class MovieBookingSystem {
public:
    std::vector<Movie> movies;

    void add_movie(const std::string& name, double price,
                   const std::string& start_time, const std::string& end_time, int n) {
        Movie movie;
        movie.name = name;
        movie.price = price;
        movie.start_time = parseHM(start_time);
        movie.end_time = parseHM(end_time);
        movie.seats.assign(static_cast<std::size_t>(n),
                           std::vector<int>(static_cast<std::size_t>(n), 0));
        movies.push_back(std::move(movie));
    }

    std::string book_ticket(const std::string& name,
                            const std::vector<std::pair<int, int>>& seats_to_book) {
        for (auto& movie : movies) {
            if (movie.name == name) {
                for (const auto& seat : seats_to_book) {
                    std::size_t r = normIndex(seat.first, movie.seats.size());
                    std::size_t c = normIndex(seat.second, movie.seats[r].size());
                    if (movie.seats[r][c] == 0) {
                        movie.seats[r][c] = 1;  // partial bookings kept on later failure (Python parity)
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
        TimeHM start = parseHM(start_time);
        TimeHM end = parseHM(end_time);

        std::vector<std::string> result;
        for (const auto& movie : movies) {
            if (lessEq(start, movie.start_time) && lessEq(movie.end_time, end)) {
                result.push_back(movie.name);
            }
        }
        return result;
    }
};
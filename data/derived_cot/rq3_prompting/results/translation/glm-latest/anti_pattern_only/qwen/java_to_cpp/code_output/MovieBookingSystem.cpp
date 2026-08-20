#include <any>
#include <cctype>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace org::example {

// Minimal equivalent of java.time.LocalTime with ISO-8601 local-time parsing
// ("HH:mm" or "HH:mm:ss"; optional fractional seconds are ignored).
class LocalTime {
public:
    int hour;
    int minute;
    int second;

    LocalTime(int hour, int minute, int second)
        : hour(hour), minute(minute), second(second) {}

    static LocalTime parse(const std::string& text) {
        std::vector<std::string> tokens;
        std::string current;
        for (char c : text) {
            if (c == ':') {
                tokens.push_back(current);
                current.clear();
            } else {
                current.push_back(c);
            }
        }
        tokens.push_back(current);

        if (tokens.size() < 2 || tokens.size() > 3)
            throw parseError(text);

        int hour = parseField(tokens[0], text);
        int minute = parseField(tokens[1], text);
        int second = 0;
        if (tokens.size() == 3) {
            std::string sec = tokens[2];
            std::string::size_type dot = sec.find('.');
            if (dot != std::string::npos)
                sec = sec.substr(0, dot);
            second = parseField(sec, text);
            if (second > 59)
                throw parseError(text);
        }
        if (hour > 23 || minute > 59)
            throw parseError(text);

        return LocalTime(hour, minute, second);
    }

    int compareTo(const LocalTime& other) const {
        if (hour != other.hour) return hour < other.hour ? -1 : 1;
        if (minute != other.minute) return minute < other.minute ? -1 : 1;
        if (second != other.second) return second < other.second ? -1 : 1;
        return 0;
    }

    bool isBefore(const LocalTime& other) const { return compareTo(other) < 0; }
    bool isAfter(const LocalTime& other) const { return compareTo(other) > 0; }

private:
    static std::runtime_error parseError(const std::string& text) {
        return std::runtime_error("DateTimeParseException: Text '" + text + "' could not be parsed");
    }

    static int parseField(const std::string& token, const std::string& text) {
        if (token.size() != 2 ||
            !std::isdigit(static_cast<unsigned char>(token[0])) ||
            !std::isdigit(static_cast<unsigned char>(token[1])))
            throw parseError(text);
        return (token[0] - '0') * 10 + (token[1] - '0');
    }
};

class MovieBookingSystem {
private:
    std::vector<std::map<std::string, std::any>> movies;

public:
    MovieBookingSystem() = default;

    void addMovie(const std::string& name, double price,
                  const std::string& startTime, const std::string& endTime, int n) {
        std::map<std::string, std::any> movie;
        movie.emplace("name", name);
        movie.emplace("price", price);
        movie.emplace("start_time", LocalTime::parse(startTime));
        movie.emplace("end_time", LocalTime::parse(endTime));
        movie.emplace("seats", std::vector<std::vector<int>>(n, std::vector<int>(n, 0)));
        movies.push_back(std::move(movie));
    }

    std::string bookTicket(const std::string& name,
                           const std::vector<std::vector<int>>& seatsToBook) {
        for (std::map<std::string, std::any>& movie : movies) {
            if (std::any_cast<const std::string&>(movie.at("name")) == name) {
                std::vector<std::vector<int>>& seats =
                    std::any_cast<std::vector<std::vector<int>>&>(movie.at("seats"));
                for (const std::vector<int>& seat : seatsToBook) {
                    int row = seat.at(0);
                    int col = seat.at(1);
                    if (seats.at(row).at(col) == 0) {
                        seats.at(row).at(col) = 1;
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
                                             const std::string& endTime) const {
        LocalTime start = LocalTime::parse(startTime);
        LocalTime end = LocalTime::parse(endTime);

        std::vector<std::string> result;
        for (const std::map<std::string, std::any>& movie : movies) {
            const LocalTime& movieStart = std::any_cast<const LocalTime&>(movie.at("start_time"));
            const LocalTime& movieEnd = std::any_cast<const LocalTime&>(movie.at("end_time"));
            if (!movieStart.isBefore(start) && !movieEnd.isAfter(end)) {
                result.push_back(std::any_cast<const std::string&>(movie.at("name")));
            }
        }
        return result;
    }

    const std::vector<std::map<std::string, std::any>>& getMovies() const {
        return movies;
    }

    std::vector<std::map<std::string, std::any>>& getMovies() {
        return movies;
    }
};

}  // namespace org::example
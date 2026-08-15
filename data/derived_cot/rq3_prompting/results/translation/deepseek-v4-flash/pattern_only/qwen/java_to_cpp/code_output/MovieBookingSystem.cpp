#include <string>
#include <vector>
#include <stdexcept>
#include <cctype>
#include <utility>

using namespace std;

struct Time {
    long long nanos;
    bool operator>=(const Time& other) const { return nanos >= other.nanos; }
    bool operator<=(const Time& other) const { return nanos <= other.nanos; }
};

Time parseTime(const string& s) {
    size_t i = 0;
    auto readNDigits = [&](int n) -> int {
        if (i + n > s.size()) throw invalid_argument("Invalid time");
        int val = 0;
        for (int j = 0; j < n; ++j) {
            if (!isdigit(static_cast<unsigned char>(s[i]))) throw invalid_argument("Invalid time");
            val = val * 10 + (s[i] - '0');
            ++i;
        }
        return val;
    };

    int hours = readNDigits(2);
    if (i >= s.size() || s[i] != ':') throw invalid_argument("Invalid time");
    ++i;
    int minutes = readNDigits(2);
    int seconds = 0;
    long long fraction = 0;

    if (i < s.size() && s[i] == ':') {
        ++i;
        seconds = readNDigits(2);
        if (i < s.size() && s[i] == '.') {
            ++i;
            if (i >= s.size() || !isdigit(static_cast<unsigned char>(s[i]))) throw invalid_argument("Invalid time");
            long long frac = 0;
            int digits = 0;
            while (i < s.size() && isdigit(static_cast<unsigned char>(s[i]))) {
                if (digits >= 9) throw invalid_argument("Invalid time");
                frac = frac * 10 + (s[i] - '0');
                ++digits;
                ++i;
            }
            while (digits < 9) {
                frac *= 10;
                ++digits;
            }
            fraction = frac;
        }
    }

    if (i != s.size()) throw invalid_argument("Invalid time");
    if (hours > 23 || minutes > 59 || seconds > 59) throw invalid_argument("Invalid time");

    long long total = (hours * 3600LL + minutes * 60LL + seconds) * 1000000000LL + fraction;
    return Time{total};
}

struct Movie {
    string name;
    double price;
    Time start_time;
    Time end_time;
    vector<vector<int>> seats;
};

class MovieBookingSystem {
private:
    vector<Movie> movies;

public:
    MovieBookingSystem() {}

    void addMovie(const string& name, double price, const string& startTime, const string& endTime, int n) {
        Movie m;
        m.name = name;
        m.price = price;
        m.start_time = parseTime(startTime);
        m.end_time = parseTime(endTime);
        if (n < 0) throw invalid_argument("Negative array size");
        m.seats.assign(n, vector<int>(n, 0));
        movies.push_back(move(m));
    }

    string bookTicket(const string& name, const vector<vector<int>>& seatsToBook) {
        for (auto& movie : movies) {
            if (movie.name == name) {
                for (const auto& seat : seatsToBook) {
                    int row = seat.at(0);
                    int col = seat.at(1);
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

    vector<string> availableMovies(const string& startTime, const string& endTime) {
        Time start = parseTime(startTime);
        Time end = parseTime(endTime);
        vector<string> result;
        for (const auto& movie : movies) {
            if (movie.start_time >= start && movie.end_time <= end) {
                result.push_back(movie.name);
            }
        }
        return result;
    }

    vector<Movie>& getMovies() {
        return movies;
    }
};
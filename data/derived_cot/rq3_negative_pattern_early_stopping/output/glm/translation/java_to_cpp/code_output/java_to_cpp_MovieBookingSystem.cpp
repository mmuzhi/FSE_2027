#ifndef MOVIE_BOOKING_SYSTEM_H
#define MOVIE_BOOKING_SYSTEM_H

#include <string>
#include <vector>
#include <map>
#include <any>
#include <algorithm>

class LocalTime {
private:
    int hour;
    int minute;

public:
    LocalTime() : hour(0), minute(0) {}
    LocalTime(int h, int m) : hour(h), minute(m) {}

    static LocalTime parse(const std::string& timeStr) {
        size_t colonPos = timeStr.find(':');
        int h = std::stoi(timeStr.substr(0, colonPos));
        int m = std::stoi(timeStr.substr(colonPos + 1));
        return LocalTime(h, m);
    }

    bool isBefore(const LocalTime& other) const {
        if (hour < other.hour) return true;
        if (hour > other.hour) return false;
        return minute < other.minute;
    }

    bool isAfter(const LocalTime& other) const {
        return other.isBefore(*this);
    }
};

class MovieBookingSystem {
private:
    std::vector<std::map<std::string, std::any>> movies;

public:
    MovieBookingSystem() = default;

    void addMovie(const std::string& name, double price, const std::string& startTime, const std::string& endTime, int n) {
        std::map<std::string, std::any> movie;
        movie["name"] = name;
        movie["price"] = price;
        movie["start_time"] = LocalTime::parse(startTime);
        movie["end_time"] = LocalTime::parse(endTime);
        movie["seats"] = std::vector<std::vector<int>>(n, std::vector<int>(n, 0));
        movies.push_back(movie);
    }

    std::string bookTicket(const std::string& name, const std::vector<std::vector<int>>& seatsToBook) {
        for (auto& movie : movies) {
            if (std::any_cast<const std::string&>(movie.at("name")) == name) {
                auto& seats = std::any_cast<std::vector<std::vector<int>>&>(movie.at("seats"));
                for (const auto& seat : seatsToBook) {
                    int row = seat[0];
                    int col = seat[1];
                    if (seats[row][col] == 0) {
                        seats[row][col] = 1;
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
        LocalTime start = LocalTime::parse(startTime);
        LocalTime end = LocalTime::parse(endTime);

        std::vector<std::string> result;
        for (const auto& movie : movies) {
            LocalTime movieStart = std::any_cast<LocalTime>(movie.at("start_time"));
            LocalTime movieEnd = std::any_cast<LocalTime>(movie.at("end_time"));
            if (!movieStart.isBefore(start) && !movieEnd.isAfter(end)) {
                result.push_back(std::any_cast<const std::string&>(movie.at("name")));
            }
        }
        return result;
    }

    std::vector<std::map<std::string, std::any>>& getMovies() {
        return movies;
    }
};

#endif
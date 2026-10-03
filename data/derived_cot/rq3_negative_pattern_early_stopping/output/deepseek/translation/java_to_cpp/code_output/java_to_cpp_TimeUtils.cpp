#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <string>
#include <stdexcept>

class TimeUtils {
private:
    std::chrono::system_clock::time_point datetime;

    // Convert a time_point to a local std::tm structure (thread-unsafe, but acceptable for single-threaded use)
    std::tm to_tm(const std::chrono::system_clock::time_point& tp) const {
        std::time_t tt = std::chrono::system_clock::to_time_t(tp);
        std::tm* tm_ptr = std::localtime(&tt);
        if (!tm_ptr) {
            throw std::runtime_error("Failed to convert time_point to local time");
        }
        return *tm_ptr;
    }

    // Convert a std::tm (treated as local time) back to a time_point
    std::chrono::system_clock::time_point from_tm(const std::tm& tm) const {
        std::time_t tt = std::mktime(const_cast<std::tm*>(&tm));
        if (tt == -1) {
            throw std::runtime_error("Failed to convert tm to time_t");
        }
        return std::chrono::system_clock::from_time_t(tt);
    }

public:
    TimeUtils() : datetime(std::chrono::system_clock::now()) {}

    std::string getCurrentTime() const {
        std::tm tm = to_tm(datetime);
        std::ostringstream oss;
        oss << std::put_time(&tm, "%H:%M:%S");
        return oss.str();
    }

    std::string getCurrentDate() const {
        std::tm tm = to_tm(datetime);
        std::ostringstream oss;
        oss << std::put_time(&tm, "%Y-%m-%d");
        return oss.str();
    }

    std::string addSeconds(int seconds) {
        datetime += std::chrono::seconds(seconds);
        std::tm tm = to_tm(datetime);
        std::ostringstream oss;
        oss << std::put_time(&tm, "%H:%M:%S");
        return oss.str();
    }

    // Parses a string in format "yyyy-MM-dd HH:mm:ss" (Java's "yyyy-M-d H:m:s" but with zero-padded fields)
    std::chrono::system_clock::time_point stringToDatetime(const std::string& str) {
        std::tm tm = {};
        std::istringstream iss(str);
        iss >> std::get_time(&tm, "%Y-%m-%d %H:%M:%S");
        if (iss.fail()) {
            throw std::invalid_argument("Invalid datetime format: " + str);
        }
        return from_tm(tm);
    }

    std::string datetimeToString(std::chrono::system_clock::time_point dt) {
        std::tm tm = to_tm(dt);
        std::ostringstream oss;
        oss << std::put_time(&tm, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }

    int getMinutes(const std::string& stringTime1, const std::string& stringTime2) {
        auto time1 = stringToDatetime(stringTime1);
        auto time2 = stringToDatetime(stringTime2);
        auto diff = time2 - time1;
        auto minutes = std::chrono::duration_cast<std::chrono::minutes>(diff).count();
        // Mimic Java's Math.toIntExact(Math.round(minutes))
        // minutes is already an integer, round does nothing. toIntExact would throw on overflow.
        // For simplicity, we static_cast; overflow would be undefined behavior.
        return static_cast<int>(minutes);
    }

    std::string getFormatTime(int year, int month, int day, int hour, int minute, int second) {
        std::tm tm = {};
        tm.tm_year = year - 1900;
        tm.tm_mon = month - 1;   // 0-based
        tm.tm_mday = day;
        tm.tm_hour = hour;
        tm.tm_min = minute;
        tm.tm_sec = second;
        tm.tm_isdst = -1;        // Let mktime determine DST
        auto tp = from_tm(tm);
        return datetimeToString(tp);
    }
};
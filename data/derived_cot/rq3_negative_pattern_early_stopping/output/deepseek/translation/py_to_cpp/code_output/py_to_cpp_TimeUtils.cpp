#include <iostream>
#include <iomanip>
#include <sstream>
#include <ctime>
#include <cmath>

class TimeUtils {
private:
    std::tm datetime;

public:
    TimeUtils() {
        std::time_t t = std::time(nullptr);
        datetime = *std::localtime(&t);
    }

    std::string get_current_time() {
        std::ostringstream oss;
        oss << std::put_time(&datetime, "%H:%M:%S");
        return oss.str();
    }

    std::string get_current_date() {
        std::ostringstream oss;
        oss << std::put_time(&datetime, "%Y-%m-%d");
        return oss.str();
    }

    std::string add_seconds(int seconds) {
        std::time_t t = std::mktime(&datetime);
        t += seconds;
        std::tm new_tm = *std::localtime(&t);
        std::ostringstream oss;
        oss << std::put_time(&new_tm, "%H:%M:%S");
        return oss.str();
    }

    std::tm string_to_datetime(const std::string& str) {
        std::tm tm = {};
        std::istringstream iss(str);
        iss >> std::get_time(&tm, "%Y-%m-%d %H:%M:%S");
        if (iss.fail()) {
            throw std::runtime_error("Failed to parse time string");
        }
        return tm;
    }

    std::string datetime_to_string(const std::tm& dt) {
        std::ostringstream oss;
        oss << std::put_time(&dt, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }

    int get_minutes(const std::string& string_time1, const std::string& string_time2) {
        std::tm tm1 = string_to_datetime(string_time1);
        std::tm tm2 = string_to_datetime(string_time2);
        std::time_t t1 = std::mktime(&tm1);
        std::time_t t2 = std::mktime(&tm2);
        double diff_seconds = std::difftime(t2, t1);
        // Python's timedelta.seconds returns seconds component (0-86399), ignoring days.
        // But here we use total seconds diff; to replicate weird behaviour we mod with 86400.
        int seconds_component = static_cast<int>(diff_seconds) % 86400;
        if (seconds_component < 0) seconds_component += 86400;
        return static_cast<int>(std::round(seconds_component / 60.0));
    }

    std::string get_format_time(int year, int month, int day, int hour, int minute, int second) {
        std::tm tm = {};
        tm.tm_year = year - 1900;
        tm.tm_mon = month - 1;
        tm.tm_mday = day;
        tm.tm_hour = hour;
        tm.tm_min = minute;
        tm.tm_sec = second;
        std::mktime(&tm);
        std::ostringstream oss;
        oss << std::put_time(&tm, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }
};
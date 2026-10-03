#include <chrono>
#include <ctime>
#include <string>
#include <sstream>
#include <iomanip>
#include <cmath>

class TimeUtils {
public:
    std::tm datetime;

    TimeUtils() {
        auto now = std::chrono::system_clock::now();
        std::time_t now_time = std::chrono::system_clock::to_time_t(now);
        datetime = *std::localtime(&now_time);
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
        std::tm new_tm = datetime;
        new_tm.tm_sec += seconds;
        std::mktime(&new_tm);
        std::ostringstream oss;
        oss << std::put_time(&new_tm, "%H:%M:%S");
        return oss.str();
    }

    std::tm string_to_datetime(const std::string& str) {
        std::tm tm = {};
        int year, month, day, hour, minute, second;
        char sep;
        std::istringstream iss(str);
        iss >> year >> sep >> month >> sep >> day >> hour >> sep >> minute >> sep >> second;
        tm.tm_year = year - 1900;
        tm.tm_mon = month - 1;
        tm.tm_mday = day;
        tm.tm_hour = hour;
        tm.tm_min = minute;
        tm.tm_sec = second;
        tm.tm_isdst = -1;
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
        std::time_t time1 = std::mktime(&tm1);
        std::time_t time2 = std::mktime(&tm2);
        double diff = std::difftime(time2, time1);
        long total_seconds = static_cast<long>(diff);
        long py_seconds = total_seconds % 86400;
        if (py_seconds < 0) py_seconds += 86400;
        return static_cast<int>(std::round(py_seconds / 60.0));
    }

    std::string get_format_time(int year, int month, int day, int hour, int minute, int second) {
        std::tm tm = {};
        tm.tm_year = year - 1900;
        tm.tm_mon = month - 1;
        tm.tm_mday = day;
        tm.tm_hour = hour;
        tm.tm_min = minute;
        tm.tm_sec = second;
        tm.tm_isdst = -1;
        std::mktime(&tm);
        std::ostringstream oss;
        oss << std::put_time(&tm, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }
};
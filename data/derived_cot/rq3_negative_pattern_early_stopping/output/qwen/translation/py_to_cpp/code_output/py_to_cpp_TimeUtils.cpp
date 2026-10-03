#include <iostream>
#include <string>
#include <iomanip>
#include <sstream>
#include <chrono>
#include <ctime>
#include <cmath>

class TimeUtils {
private:
    std::chrono::system_clock::time_point m_currentTime;

public:
    TimeUtils() {
        m_currentTime = std::chrono::system_clock::now();
    }

    std::string get_current_time() {
        std::time_t now_c = std::chrono::system_clock::to_time_t(m_currentTime);
        std::tm tm = {};
        localtime_r(&now_c, &tm);
        char buffer[100];
        std::strftime(buffer, sizeof(buffer), "%H:%M:%S", &tm);
        return std::string(buffer);
    }

    std::string get_current_date() {
        std::time_t now_c = std::chrono::system_clock::to_time_t(m_currentTime);
        std::tm tm = {};
        localtime_r(&now_c, &tm);
        char buffer[100];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d", &tm);
        return std::string(buffer);
    }

    std::string add_seconds(int seconds) {
        auto duration = std::chrono::seconds(seconds);
        std::chrono::system_clock::time_point new_time = m_currentTime + duration;
        std::time_t new_time_c = std::chrono::system_clock::to_time_t(new_time);
        std::tm tm = {};
        localtime_r(&new_time_c, &tm);
        char buffer[100];
        std::strftime(buffer, sizeof(buffer), "%H:%M:%S", &tm);
        return std::string(buffer);
    }

    std::chrono::system_clock::time_point string_to_datetime(const std::string& str) {
        std::tm tm = {};
        std::istringstream iss(str);
        iss >> std::get_time(&tm, "%Y-%m-%d %H:%M:%S");
        std::time_t tt = mktime(&tm);
        return std::chrono::system_clock::from_time_t(tt);
    }

    std::string datetime_to_string(const std::chrono::system_clock::time_point& tp) {
        std::time_t tt = std::chrono::system_clock::to_time_t(tp);
        std::tm tm = {};
        localtime_r(&tt, &tm);
        char buffer[100];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &tm);
        return std::string(buffer);
    }

    int get_minutes(const std::string& str1, const std::string& str2) {
        auto time1 = string_to_datetime(str1);
        auto time2 = string_to_datetime(str2);
        auto duration = time2 - time1;
        auto seconds = std::chrono::duration_cast<std::chrono::seconds>(duration).count();
        return static_cast<int>(std::round(seconds / 60.0));
    }

    std::string get_format_time(int year, int month, int day, int hour, int minute, int second) {
        std::tm tm = {};
        tm.tm_year = year - 1900;
        tm.tm_mon = month - 1;
        tm.tm_mday = day;
        tm.tm_hour = hour;
        tm.tm_min = minute;
        tm.tm_sec = second;
        char buffer[100];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &tm);
        return std::string(buffer);
    }
};

int main() {
    TimeUtils timeutils;
    std::cout << "Current Time: " << timeutils.get_current_time() << std::endl;
    std::cout << "Current Date: " << timeutils.get_current_date() << std::endl;
    std::cout << "Time after adding 600 seconds: " << timeutils.add_seconds(600) << std::endl;
    auto dt = timeutils.string_to_datetime("2001-7-18 1:1:1");
    std::cout << "Converted datetime: " << timeutils.datetime_to_string(dt) << std::endl;
    std::cout << "Minutes between times: " << timeutils.get_minutes("2001-7-18 1:1:1", "2001-7-18 2:1:1") << std::endl;
    std::cout << "Formatted time: " << timeutils.get_format_time(2001, 7, 18, 1, 1, 1) << std::endl;
    return 0;
}
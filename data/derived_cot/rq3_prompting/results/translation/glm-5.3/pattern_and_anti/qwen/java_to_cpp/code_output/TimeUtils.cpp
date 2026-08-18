// Requires C++20
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <ctime>
#include <stdexcept>
#include <string>

class TimeUtils {
public:
    // Analog of java.time.LocalDateTime: wall-clock date-time with second precision.
    using LocalDateTime = std::chrono::time_point<std::chrono::system_clock, std::chrono::seconds>;

    TimeUtils() : datetime(nowLocal()) {}

    std::string getCurrentTime() {
        return formatTimeOnly(datetime);
    }

    std::string getCurrentDate() {
        return formatDateOnly(datetime);
    }

    std::string addSeconds(int seconds) {
        LocalDateTime newDatetime = datetime + std::chrono::seconds(seconds);
        return formatTimeOnly(newDatetime);
    }

    LocalDateTime stringToDatetime(const std::string& str) {
        int y, mo, d, h, mi, s, pos = 0;
        if (std::sscanf(str.c_str(), "%d-%d-%d %d:%d:%d%n",
                        &y, &mo, &d, &h, &mi, &s, &pos) != 6 ||
            pos != static_cast<int>(str.size())) {
            throw std::runtime_error("DateTimeParseException: " + str);
        }
        return of(y, mo, d, h, mi, s);
    }

    std::string datetimeToString(const LocalDateTime& dt) {
        return formatDateOnly(dt) + " " + formatTimeOnly(dt);
    }

    int getMinutes(const std::string& stringTime1, const std::string& stringTime2) {
        LocalDateTime time1 = stringToDatetime(stringTime1);
        LocalDateTime time2 = stringToDatetime(stringTime2);
        long long minutes =
            std::chrono::duration_cast<std::chrono::minutes>(time2 - time1).count();
        if (minutes > INT32_MAX || minutes < INT32_MIN) {
            // Math.toIntExact throws ArithmeticException on overflow
            throw std::runtime_error("ArithmeticException: integer overflow");
        }
        return static_cast<int>(minutes);
    }

    std::string getFormatTime(int year, int month, int day, int hour, int minute, int second) {
        LocalDateTime timeItem = of(year, month, day, hour, minute, second);
        return formatDateOnly(timeItem) + " " + formatTimeOnly(timeItem);
    }

private:
    LocalDateTime datetime;

    static void checkTimeFields(int hour, int minute, int second) {
        if (hour < 0 || hour > 23 || minute < 0 || minute > 59 ||
            second < 0 || second > 59) {
            throw std::runtime_error("DateTimeException: invalid time fields");
        }
    }

    static LocalDateTime of(int y, int mo, int d, int h, int mi, int s) {
        checkTimeFields(h, mi, s);
        const std::chrono::year_month_day ymd(
            std::chrono::year{y},
            std::chrono::month{static_cast<unsigned>(mo)},
            std::chrono::day{static_cast<unsigned>(d)});
        if (!ymd.ok()) {
            throw std::runtime_error("DateTimeException: invalid date");
        }
        return std::chrono::sys_days(ymd) + std::chrono::hours(h) +
               std::chrono::minutes(mi) + std::chrono::seconds(s);
    }

    static LocalDateTime nowLocal() {
        std::time_t now = std::time(nullptr);
        std::tm lt{};
#ifdef _WIN32
        localtime_s(&lt, &now);
#else
        localtime_r(&now, &lt);
#endif
        return of(lt.tm_year + 1900, lt.tm_mon + 1, lt.tm_mday,
                  lt.tm_hour, lt.tm_min, lt.tm_sec);
    }

    static std::string formatDateOnly(const LocalDateTime& tp) {
        const std::chrono::year_month_day ymd(
            std::chrono::floor<std::chrono::days>(tp));
        char buf[32];
        std::snprintf(buf, sizeof buf, "%04d-%02d-%02d",
                      static_cast<int>(ymd.year()),
                      static_cast<unsigned>(ymd.month()),
                      static_cast<unsigned>(ymd.day()));
        return buf;
    }

    static std::string formatTimeOnly(const LocalDateTime& tp) {
        const auto dayPart = std::chrono::floor<std::chrono::days>(tp);
        const std::chrono::hh_mm_ss hms(tp - dayPart);
        char buf[16];
        std::snprintf(buf, sizeof buf, "%02d:%02d:%02d",
                      static_cast<int>(hms.hours().count()),
                      static_cast<int>(hms.minutes().count()),
                      static_cast<int>(hms.seconds().count()));
        return buf;
    }
};
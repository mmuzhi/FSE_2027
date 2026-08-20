// TimeUtils.hpp — C++20 translation of org.example.TimeUtils
// Requires compiler support for <chrono> parsing and <format> (e.g. GCC 13+, MSVC 19.30+)

#pragma once

#include <chrono>
#include <format>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>

namespace org::example {

class TimeUtils {
public:
    // Naive wall-clock date-time (no zone offset): equivalent of java.time.LocalDateTime
    using LocalDateTime = std::chrono::local_seconds;

    TimeUtils()
        : datetime(std::chrono::floor<std::chrono::seconds>(
              std::chrono::zoned_time{std::chrono::current_zone(),
                                      std::chrono::system_clock::now()}
                  .get_local_time())) {}

    std::string getCurrentTime() {
        return std::format("{:%H:%M:%S}", datetime);
    }

    std::string getCurrentDate() {
        return std::format("{:%Y-%m-%d}", datetime);
    }

    std::string addSeconds(int seconds) {
        LocalDateTime newDatetime = datetime + std::chrono::seconds{seconds};
        return std::format("{:%H:%M:%S}", newDatetime);
    }

    LocalDateTime stringToDatetime(const std::string& string) {
        std::istringstream is{string};
        is >> std::noskipws;  // DateTimeFormatter.parse does not skip leading whitespace
        LocalDateTime result{};
        // "yyyy-M-d H:m:s": numeric fields accept 1..n digits, like the lenient Java pattern
        if (!std::chrono::from_stream(is, "%Y-%m-%d %H:%M:%S", result) ||
            is.peek() != std::char_traits<char>::eof()) {
            // LocalDateTime.parse must consume the entire input
            throw std::runtime_error(
                "DateTimeParseException: Text '" + string + "' could not be parsed");
        }
        return result;
    }

    std::string datetimeToString(const LocalDateTime& datetime) {
        return std::format("{:%Y-%m-%d %H:%M:%S}", datetime);
    }

    int getMinutes(const std::string& stringTime1, const std::string& stringTime2) {
        LocalDateTime time1 = stringToDatetime(stringTime1);
        LocalDateTime time2 = stringToDatetime(stringTime2);
        // ChronoUnit.MINUTES.between truncates toward zero; Math.round on a long is identity
        const long long minutes =
            std::chrono::duration_cast<std::chrono::minutes>(time2 - time1).count();
        if (minutes < static_cast<long long>(std::numeric_limits<int>::min()) ||
            minutes > static_cast<long long>(std::numeric_limits<int>::max())) {
            throw std::overflow_error("integer overflow");  // Math.toIntExact
        }
        return static_cast<int>(minutes);
    }

    std::string getFormatTime(int year, int month, int day, int hour, int minute, int second) {
        const std::chrono::year_month_day ymd{
            std::chrono::year{year},
            std::chrono::month{static_cast<unsigned>(month)},
            std::chrono::day{static_cast<unsigned>(day)}};
        if (!ymd.ok() || hour < 0 || hour > 23 || minute < 0 || minute > 59 ||
            second < 0 || second > 59) {
            // LocalDateTime.of throws DateTimeException on out-of-range/invalid fields
            throw std::runtime_error("DateTimeException: Invalid value for field");
        }
        const LocalDateTime timeItem = std::chrono::local_days{ymd} +
                                       std::chrono::hours{hour} +
                                       std::chrono::minutes{minute} +
                                       std::chrono::seconds{second};
        return std::format("{:%Y-%m-%d %H:%M:%S}", timeItem);
    }

private:
    LocalDateTime datetime;
};

}  // namespace org::example
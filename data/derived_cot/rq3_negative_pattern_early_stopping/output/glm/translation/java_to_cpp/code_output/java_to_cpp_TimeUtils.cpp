#include <iostream>
#include <string>
#include <ctime>
#include <chrono>
#include <sstream>
#include <iomanip>
#include <cmath>
#include <limits>
#include <stdexcept>
#include <cstdio>

class TimeUtils {
private:
    std::tm datetime;

    std::string formatTime(const std::tm& t, const std::string& format) const {
        char buffer[80];
        std::strftime(buffer, sizeof(buffer), format.c_str(), &t);
        return std::string(buffer);
    }

    bool isValidDate(int y, int m, int d, int h, int mi, int s) const {
        if (m < 1 || m > 12 || d < 1 || h < 0 || h > 23 || mi < 0 || mi > 59 || s < 0 || s > 59) return false;
        static const int daysInMonth[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        int maxDays = daysInMonth[m];
        if (m == 2) {
            bool isLeap = (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
            if (isLeap) maxDays = 29;
        }
        if (d > maxDays) return false;
        return true;
    }

    long long daysFromCivil(int y, int m, int d) const {
        if (m <= 2) { y--; m += 12; }
        long long era = (y >= 0 ? y : y - 399) / 400;
        long long yoe = y - era * 400;
        long long doy = (153 * (m - 3) + 2) / 5 + d - 1;
        long long doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
        return era * 146097 + doe - 719468;
    }

    long long toEpochSecond(int y, int m, int d, int h, int mi, int s) const {
        return daysFromCivil(y, m, d) * 86400LL + h * 3600LL + mi * 60LL + s;
    }

    std::tm fromEpochSecond(long long epochSeconds) const {
        long long days = epochSeconds / 86400LL;
        long long secondsOfDay = epochSeconds % 86400LL;
        if (secondsOfDay < 0) {
            secondsOfDay += 86400LL;
            days--;
        }
        
        days += 719468;
        long long era = (days >= 0 ? days : days - 146096) / 146097;
        unsigned long long doe = static_cast<unsigned long long>(days - era * 146097);
        unsigned long long yoe = (doe - doe/1460 + doe/36524 - doe/146096) / 365;
        long long y = static_cast<long long>(yoe) + era * 400;
        unsigned long long doy = doe - (365*yoe + yoe/4 - yoe/100);
        unsigned long long mp = (5*doy + 2)/153;
        unsigned long long d = doy - (153*mp+2)/5 + 1;
        unsigned long long m = mp + (mp < 10 ? 3 : -9);
        y += (m <= 2);

        std::tm t = {};
        t.tm_year = static_cast<int>(y - 1900);
        t.tm_mon = static_cast<int>(m - 1);
        t.tm_mday = static_cast<int>(d);
        t.tm_hour = static_cast<int>(secondsOfDay / 3600);
        t.tm_min = static_cast<int>((secondsOfDay % 3600) / 60);
        t.tm_sec = static_cast<int>(secondsOfDay % 60);
        t.tm_isdst = 0;
        return t;
    }

public:
    TimeUtils() {
        auto now = std::chrono::system_clock::now();
        std::time_t now_time = std::chrono::system_clock::to_time_t(now);
        datetime = *std::localtime(&now_time);
    }

    std::string getCurrentTime() {
        return formatTime(datetime, "%H:%M:%S");
    }

    std::string getCurrentDate() {
        return formatTime(datetime, "%Y-%m-%d");
    }

    std::string addSeconds(int seconds) {
        long long epoch = toEpochSecond(datetime.tm_year + 1900, datetime.tm_mon + 1, datetime.tm_mday, 
                                        datetime.tm_hour, datetime.tm_min, datetime.tm_sec);
        epoch += seconds;
        std::tm newDatetime = fromEpochSecond(epoch);
        return formatTime(newDatetime, "%H:%M:%S");
    }

    std::tm stringToDatetime(const std::string& string) const {
        std::tm t = {};
        int year, month, day, hour, minute, second;
        char trailing = '\0';
        int matched = sscanf(string.c_str(), "%d-%d-%d %d:%d:%d%c", &year, &month, &day, &hour, &minute, &second, &trailing);
        if (matched != 6) {
            throw std::invalid_argument("Invalid datetime format");
        }
        if (!isValidDate(year, month, day, hour, minute, second)) {
            throw std::invalid_argument("Invalid date or time value");
        }
        t.tm_year = year - 1900;
        t.tm_mon = month - 1;
        t.tm_mday = day;
        t.tm_hour = hour;
        t.tm_min = minute;
        t.tm_sec = second;
        t.tm_isdst = 0;
        return t;
    }

    std::string datetimeToString(const std::tm& datetime) const {
        return formatTime(datetime, "%Y-%m-%d %H:%M:%S");
    }

    int getMinutes(const std::string& stringTime1, const std::string& stringTime2) {
        std::tm t1 = stringToDatetime(stringTime1);
        std::tm t2 = stringToDatetime(stringTime2);
        long long s1 = toEpochSecond(t1.tm_year + 1900, t1.tm_mon + 1, t1.tm_mday, t1.tm_hour, t1.tm_min, t1.tm_sec);
        long long s2 = toEpochSecond(t2.tm_year + 1900, t2.tm_mon + 1, t2.tm_mday, t2.tm_hour, t2.tm_min, t2.tm_sec);
        long long diff = s2 - s1;
        long long minutes = diff / 60;
        if (minutes > std::numeric_limits<int>::max() || minutes < std::numeric_limits<int>::min()) {
            throw std::overflow_error("integer overflow");
        }
        return static_cast<int>(minutes
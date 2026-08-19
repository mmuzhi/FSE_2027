#include <cmath>
#include <cstdint>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <stdexcept>
#include <string>

class TimeUtils {
public:
    // Naive (field-based) local datetime captured at construction, like datetime.datetime.now()
    std::tm datetime;

    TimeUtils()
    {
        const std::time_t now = std::time(nullptr);
        datetime = *std::localtime(&now);
    }

    std::string get_current_time()
    {
        return format(datetime, "%H:%M:%S");
    }

    std::string get_current_date()
    {
        return format(datetime, "%Y-%m-%d");
    }

    std::string add_seconds(long long seconds)
    {
        const std::int64_t total = tm_to_seconds(datetime) + seconds;
        return format(seconds_to_tm(total), "%H:%M:%S");
    }

    std::tm string_to_datetime(const std::string& string)
    {
        std::tm t{};
        std::istringstream ss(string);
        ss >> std::noskipws >> std::get_time(&t, "%Y-%m-%d %H:%M:%S");
        if (ss.fail() || ss.peek() != std::char_traits<char>::eof())
            throw std::invalid_argument(
                "time data '" + string +
                "' does not match format '%Y-%m-%d %H:%M:%S'");
        validate_ymdhms(t.tm_year + 1900, t.tm_mon + 1, t.tm_mday,
                        t.tm_hour, t.tm_min, t.tm_sec);
        return t;
    }

    std::string datetime_to_string(const std::tm& datetime)
    {
        return format(datetime, "%Y-%m-%d %H:%M:%S");
    }

    long long get_minutes(const std::string& string_time1, const std::string& string_time2)
    {
        const std::tm time1 = string_to_datetime(string_time1);
        const std::tm time2 = string_to_datetime(string_time2);
        const std::int64_t diff = tm_to_seconds(time2) - tm_to_seconds(time1);
        // Python's timedelta.seconds only exposes the in-day component (0..86399);
        // whole days are dropped, and negative deltas wrap as days=-1, seconds=...
        const std::int64_t seconds_field = ((diff % 86400) + 86400) % 86400;
        // Python round(): half-to-even on the float division
        return static_cast<long long>(
            std::nearbyint(static_cast<double>(seconds_field) / 60.0));
    }

    std::string get_format_time(int year, int month, int day, int hour, int minute, int second)
    {
        validate_ymdhms(year, month, day, hour, minute, second);
        std::tm t{};
        t.tm_year = year - 1900;
        t.tm_mon = month - 1;
        t.tm_mday = day;
        t.tm_hour = hour;
        t.tm_min = minute;
        t.tm_sec = second;
        return format(t, "%Y-%m-%d %H:%M:%S");
    }

private:
    static std::string format(const std::tm& t, const char* fmt)
    {
        std::tm copy = t;
        std::ostringstream os;
        os << std::put_time(&copy, fmt);
        return os.str();
    }

    static void validate_ymdhms(int year, int month, int day, int hour, int minute, int second)
    {
        if (year < 1 || year > 9999)
            throw std::invalid_argument("year " + std::to_string(year) + " is out of range");
        if (month < 1 || month > 12)
            throw std::invalid_argument("month must be in 1..12");
        if (day < 1 || day > days_in_month(year, month))
            throw std::invalid_argument("day is out of range for month");
        if (hour < 0 || hour > 23)
            throw std::invalid_argument("hour must be in 0..23");
        if (minute < 0 || minute > 59)
            throw std::invalid_argument("minute must be in 0..59");
        if (second < 0 || second > 59)
            throw std::invalid_argument("second must be in 0..59");
    }

    static bool is_leap(int year)
    {
        return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
    }

    static int days_in_month(int year, int month)
    {
        static const int table[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        return (month == 2 && is_leap(year)) ? 29 : table[month - 1];
    }

    // Days since 1970-01-01 (Howard Hinnant's civil-date algorithms, proleptic Gregorian)
    static std::int64_t days_from_civil(int y, int m, int d)
    {
        y -= m <= 2;
        const std::int64_t era = (y >= 0 ? y : y - 399) / 400;
        const unsigned yoe = static_cast<unsigned>(y - era * 400);
        const unsigned doy = (153u * static_cast<unsigned>(m + (m > 2 ? -3 : 9)) + 2u) / 5u
                           + static_cast<unsigned>(d) - 1u;
        const unsigned doe = yoe * 365u + yoe / 4u - yoe / 100u + doy;
        return era * 146097 + static_cast<std::int64_t>(doe) - 719468;
    }

    static void civil_from_days(std::int64_t z, int& y, int& m, int& d)
    {
        z += 719468;
        const std::int64_t era = (z >= 0 ? z : z - 146096) / 146097;
        const unsigned doe = static_cast<unsigned>(z - era * 146097);
        const unsigned yoe = (doe - doe / 1460u + doe / 36524u - doe / 146096u) / 365u;
        const std::int64_t yr = static_cast<std::int64_t>(yoe) + era * 400;
        const unsigned doy = doe - (365u * yoe + yoe / 4u - yoe / 100u);
        const unsigned mp = (5u * doy + 2u) / 153u;
        d = static_cast<int>(doy - (153u * mp + 2u) / 5u + 1u);
        m = static_cast<int>(mp) + (mp < 10 ? 3 : -9);
        y = static_cast<int>(yr + (m <= 2));
    }

    static std::int64_t tm_to_seconds(const std::tm& t)
    {
        return days_from_civil(t.tm_year + 1900, t.tm_mon + 1, t.tm_mday) * 86400
             + t.tm_hour * 3600 + t.tm_min * 60 + t.tm_sec;
    }

    static std::tm seconds_to_tm(std::int64_t sec)
    {
        const std::int64_t days = floor_div(sec, 86400);
        const int rem = static_cast<int>(sec - days * 86400); // 0..86399
        int y, m, d;
        civil_from_days(days, y, m, d);
        std::tm t{};
        t.tm_year = y - 1900;
        t.tm_mon = m - 1;
        t.tm_mday = d;
        t.tm_hour = rem / 3600;
        t.tm_min = (rem % 3600) / 60;
        t.tm_sec = rem % 60;
        return t;
    }

    static std::int64_t floor_div(std::int64_t a, std::int64_t b)
    {
        const std::int64_t q = a / b;
        const std::int64_t r = a % b;
        return (r != 0 && ((r < 0) != (b < 0))) ? q - 1 : q;
    }
};
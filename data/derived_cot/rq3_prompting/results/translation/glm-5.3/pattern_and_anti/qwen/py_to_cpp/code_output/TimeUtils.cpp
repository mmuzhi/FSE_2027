#include <cctype>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <ctime>
#include <stdexcept>
#include <string>

class TimeUtils {
public:
    // Python: self.datetime = datetime.datetime.now()  (public attribute)
    std::tm datetime;

    TimeUtils() {
        std::time_t now = std::chrono::system_clock::to_time_t(
            std::chrono::system_clock::now());
#ifdef _WIN32
        localtime_s(&datetime, &now);
#else
        localtime_r(&now, &datetime);
#endif
    }

    std::string get_current_time() const {
        return format(datetime, "%H:%M:%S");
    }

    std::string get_current_date() const {
        return format(datetime, "%Y-%m-%d");
    }

    std::string add_seconds(int seconds) const {
        std::tm nd = from_seconds(to_seconds(datetime) + seconds);
        return format(nd, "%H:%M:%S");
    }

    static std::tm string_to_datetime(const std::string& string) {
        std::tm t{};
        const char* p = string.c_str();
        int Y, M, D, h, m, s;
        // Mirrors strptime("%Y-%m-%d %H:%M:%S") leniency (non-zero-padded
        // fields accepted) and raises on any trailing/extra data.
        if (!parse_int(p, Y) || *p++ != '-' ||
            !parse_int(p, M) || *p++ != '-' ||
            !parse_int(p, D) || *p++ != ' ' ||
            !parse_int(p, h) || *p++ != ':' ||
            !parse_int(p, m) || *p++ != ':' ||
            !parse_int(p, s) || *p != '\0') {
            throw std::invalid_argument(
                "time data '" + string +
                "' does not match format '%Y-%m-%d %H:%M:%S'");
        }
        validate(Y, M, D, h, m, s);
        t.tm_year = Y - 1900;
        t.tm_mon = M - 1;
        t.tm_mday = D;
        t.tm_hour = h;
        t.tm_min = m;
        t.tm_sec = s;
        t.tm_isdst = -1;
        return t;
    }

    static std::string datetime_to_string(const std::tm& datetime) {
        return format(datetime, "%Y-%m-%d %H:%M:%S");
    }

    static long long get_minutes(const std::string& string_time1,
                                 const std::string& string_time2) {
        std::tm t1 = string_to_datetime(string_time1);
        std::tm t2 = string_to_datetime(string_time2);
        long long diff = to_seconds(t2) - to_seconds(t1);
        // Python timedelta.seconds is the normalized component in [0, 86399]
        long long secs = ((diff % 86400) + 86400) % 86400;
        // Python round(): round-half-to-even
        return round_half_even(static_cast<double>(secs) / 60.0);
    }

    static std::string get_format_time(int year, int month, int day,
                                       int hour, int minute, int second) {
        validate(year, month, day, hour, minute, second);
        std::tm t{};
        t.tm_year = year - 1900;
        t.tm_mon = month - 1;
        t.tm_mday = day;
        t.tm_hour = hour;
        t.tm_min = minute;
        t.tm_sec = second;
        t.tm_isdst = -1;
        return format(t, "%Y-%m-%d %H:%M:%S");
    }

private:
    static bool parse_int(const char*& p, int& v) {
        if (!std::isdigit(static_cast<unsigned char>(*p))) return false;
        long long val = 0;
        while (std::isdigit(static_cast<unsigned char>(*p))) {
            val = val * 10 + (*p - '0');
            ++p;
        }
        v = static_cast<int>(val);
        return true;
    }

    static bool is_leap(int y) {
        return (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
    }

    static int days_in_month(int y, int m) {
        static const int d[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        if (m == 2 && is_leap(y)) return 29;
        return d[m - 1];
    }

    // Mirrors datetime(...) constructor range checks (raises ValueError)
    static void validate(int Y, int M, int D, int h, int m, int s) {
        bool ok = Y >= 1 && Y <= 9999 && M >= 1 && M <= 12 &&
                  D >= 1 && D <= days_in_month(Y, M) &&
                  h >= 0 && h <= 23 && m >= 0 && m <= 59 && s >= 0 && s <= 59;
        if (!ok)
            throw std::invalid_argument("invalid date/time components");
    }

    static std::string format(const std::tm& t, const char* fmt) {
        char buf[64];
        std::size_t n = std::strftime(buf, sizeof buf, fmt, &t);
        return std::string(buf, n);
    }

    // Howard Hinnant's civil-date algorithms (no timezone dependence)
    static long long days_from_civil(int y, int m, int d) {
        y -= m <= 2;
        const int era = (y >= 0 ? y : y - 399) / 400;
        const unsigned yoe = static_cast<unsigned>(y - era * 400);
        const unsigned doy = (153u * static_cast<unsigned>(m + (m > 2 ? -3 : 9)) + 2u) / 5u + static_cast<unsigned>(d) - 1u;
        const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
        return static_cast<long long>(era) * 146097 + static_cast<long long>(doe) - 719468;
    }

    static void civil_from_days(long long z, int& y, int& m, int& d) {
        z += 719468;
        const long long era = (z >= 0 ? z : z - 146096) / 146097;
        const unsigned doe = static_cast<unsigned>(z - era * 146097);
        const unsigned yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
        y = static_cast<int>(yoe) + static_cast<int>(era) * 400;
        const unsigned doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
        const unsigned mp = (5 * doy + 2) / 153;
        d = static_cast<int>(doy - (153 * mp + 2) / 5 + 1);
        m = static_cast<int>(mp) + (mp < 10 ? 3 : -9);
        y += (m <= 2);
    }

    static long long to_seconds(const std::tm& t) {
        return days_from_civil(t.tm_year + 1900, t.tm_mon + 1, t.tm_mday) * 86400
             + t.tm_hour * 3600 + t.tm_min * 60 + t.tm_sec;
    }

    static std::tm from_seconds(long long total) {
        long long days = total / 86400;
        if (total < 0 && total % 86400 != 0) --days;  // floor division
        long long rem = total - days * 86400;
        int y, m, d;
        civil_from_days(days, y, m, d);
        std::tm t{};
        t.tm_year = y - 1900;
        t.tm_mon = m - 1;
        t.tm_mday = d;
        t.tm_hour = static_cast<int>(rem / 3600);
        t.tm_min = static_cast<int>((rem % 3600) / 60);
        t.tm_sec = static_cast<int>(rem % 60);
        return t;
    }

    static long long round_half_even(double x) {
        double f = std::floor(x);
        double diff = x - f;
        long long r = static_cast<long long>(f);
        if (diff > 0.5) ++r;
        else if (diff == 0.5 && (r % 2 != 0)) ++r;
        return r;
    }
};
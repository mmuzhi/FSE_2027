#include <ctime>
#include <string>
#include <sstream>
#include <iomanip>
#include <stdexcept>
#include <cctype>
#include <cmath>
#include <cstddef>

struct DateTime {
    int year;
    int month;
    int day;
    int hour;
    int minute;
    int second;
};

bool is_leap_year(int y) {
    return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
}

int days_in_month(int y, int m) {
    static const int days[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (m == 2 && is_leap_year(y)) return 29;
    return days[m - 1];
}

// Howard Hinnant's civil date algorithms
int days_from_civil(int y, int m, int d) {
    y -= m <= 2;
    const int era = (y >= 0 ? y : y - 399) / 400;
    const unsigned yoe = static_cast<unsigned>(y - era * 400);
    const int doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
    const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return era * 146097 + static_cast<int>(doe) - 719468;
}

void civil_from_days(int z, int& y, int& m, int& d) {
    z += 719468;
    const int era = (z >= 0 ? z : z - 146096) / 146097;
    const unsigned doe = static_cast<unsigned>(z - era * 146097);
    const unsigned yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    y = static_cast<int>(yoe) + era * 400;
    const unsigned doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    const unsigned mp = (5 * doy + 2) / 153;
    d = static_cast<int>(doy - (153 * mp + 2) / 5 + 1);
    m = static_cast<int>(mp) + (mp < 10 ? 3 : -9);
    y += (m <= 2);
}

long long datetime_to_seconds(const DateTime& dt) {
    long long days = days_from_civil(dt.year, dt.month, dt.day);
    return days * 86400LL + dt.hour * 3600LL + dt.minute * 60LL + dt.second;
}

DateTime seconds_to_datetime(long long total_seconds) {
    long long days = total_seconds / 86400;
    long long rem = total_seconds % 86400;
    if (rem < 0) {
        rem += 86400;
        days -= 1;
    }
    int hour = static_cast<int>(rem / 3600);
    rem %= 3600;
    int minute = static_cast<int>(rem / 60);
    int second = static_cast<int>(rem % 60);

    int y, m, d;
    civil_from_days(static_cast<int>(days), y, m, d);
    DateTime result{y, m, d, hour, minute, second};
    if (result.year < 1 || result.year > 9999) {
        throw std::out_of_range("datetime out of range");
    }
    return result;
}

std::string format_two_digits(int x) {
    std::ostringstream oss;
    oss << std::setw(2) << std::setfill('0') << x;
    return oss.str();
}

std::string format_date(const DateTime& dt) {
    std::ostringstream oss;
    oss << std::setw(4) << std::setfill('0') << dt.year << '-'
        << format_two_digits(dt.month) << '-'
        << format_two_digits(dt.day);
    return oss.str();
}

std::string format_time(const DateTime& dt) {
    return format_two_digits(dt.hour) + ":" +
           format_two_digits(dt.minute) + ":" +
           format_two_digits(dt.second);
}

std::string format_datetime(const DateTime& dt) {
    return format_date(dt) + " " + format_time(dt);
}

bool read_int(const std::string& s, size_t& pos, int& out, size_t max_digits) {
    if (pos >= s.size() || !std::isdigit(static_cast<unsigned char>(s[pos]))) {
        return false;
    }
    int val = 0;
    size_t count = 0;
    while (pos < s.size() && count < max_digits &&
           std::isdigit(static_cast<unsigned char>(s[pos]))) {
        val = val * 10 + (s[pos] - '0');
        ++pos;
        ++count;
    }
    out = val;
    return true;
}

bool read_char(const std::string& s, size_t& pos, char c) {
    if (pos < s.size() && s[pos] == c) {
        ++pos;
        return true;
    }
    return false;
}

void validate_datetime(int year, int month, int day, int hour, int minute, int second) {
    if (year < 1 || year > 9999) throw std::invalid_argument("Year out of range");
    if (month < 1 || month > 12) throw std::invalid_argument("Month out of range");
    if (day < 1 || day > days_in_month(year, month)) throw std::invalid_argument("Day out of range");
    if (hour < 0 || hour > 23) throw std::invalid_argument("Hour out of range");
    if (minute < 0 || minute > 59) throw std::invalid_argument("Minute out of range");
    if (second < 0 || second > 59) throw std::invalid_argument("Second out of range");
}

DateTime parse_datetime(const std::string& s) {
    size_t pos = 0;
    int year, month, day, hour, minute, second;

    if (!read_int(s, pos, year, 4)) throw std::invalid_argument("Invalid datetime string");
    if (!read_char(s, pos, '-')) throw std::invalid_argument("Invalid datetime string");
    if (!read_int(s, pos, month, 2)) throw std::invalid_argument("Invalid datetime string");
    if (!read_char(s, pos, '-')) throw std::invalid_argument("Invalid datetime string");
    if (!read_int(s, pos, day, 2)) throw std::invalid_argument("Invalid datetime string");
    if (!read_char(s, pos, ' ')) throw std::invalid_argument("Invalid datetime string");
    if (!read_int(s, pos, hour, 2)) throw std::invalid_argument("Invalid datetime string");
    if (!read_char(s, pos, ':')) throw std::invalid_argument("Invalid datetime string");
    if (!read_int(s, pos, minute, 2)) throw std::invalid_argument("Invalid datetime string");
    if (!read_char(s, pos, ':')) throw std::invalid_argument("Invalid datetime string");
    if (!read_int(s, pos, second, 2)) throw std::invalid_argument("Invalid datetime string");

    if (pos != s.size()) throw std::invalid_argument("Invalid datetime string");

    validate_datetime(year, month, day, hour, minute, second);
    return DateTime{year, month, day, hour, minute, second};
}

long long round_half_even(double x) {
    double floor_x = std::floor(x);
    double diff = x - floor_x;
    long long result = static_cast<long long>(floor_x);
    if (diff > 0.5) {
        result += 1;
    } else if (diff == 0.5) {
        if (result % 2 != 0) result += 1;
    }
    return result;
}

class TimeUtils {
public:
    TimeUtils() {
        std::time_t t = std::time(nullptr);
        std::tm* now = std::localtime(&t);
        if (now == nullptr) {
            throw std::runtime_error("Failed to get current time");
        }
        datetime = DateTime{now->tm_year + 1900, now->tm_mon + 1, now->tm_mday,
                            now->tm_hour, now->tm_min, now->tm_sec};
    }

    std::string get_current_time() const {
        return format_time(datetime);
    }

    std::string get_current_date() const {
        return format_date(datetime);
    }

    std::string add_seconds(int seconds) const {
        long long total = datetime_to_seconds(datetime) + seconds;
        DateTime new_dt = seconds_to_datetime(total);
        return format_time(new_dt);
    }

    DateTime string_to_datetime(const std::string& s) const {
        return parse_datetime(s);
    }

    std::string datetime_to_string(const DateTime& dt) const {
        return format_datetime(dt);
    }

    int get_minutes(const std::string& string_time1, const std::string& string_time2) const {
        DateTime t1 = parse_datetime(string_time1);
        DateTime t2 = parse_datetime(string_time2);
        long long total_seconds = datetime_to_seconds(t2) - datetime_to_seconds(t1);
        long long seconds_component = (total_seconds % 86400 + 86400) % 86400;
        double minutes = static_cast<double>(seconds_component) / 60.0;
        return static_cast<int>(round_half_even(minutes));
    }

    std::string get_format_time(int year, int month, int day, int hour, int minute, int second) const {
        validate_datetime(year, month, day, hour, minute, second);
        DateTime dt{year, month, day, hour, minute, second};
        return format_datetime(dt);
    }

    DateTime datetime;
};
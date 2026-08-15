#include <vector>
#include <string>
#include <algorithm>
#include <utility>
#include <ctime>
#include <chrono>
#include <stdexcept>
#include <functional>

struct DateTime {
    int year;
    int month;
    int day;
    int hour;
    int minute;
    int second;
    int nano;

    DateTime(int year, int month, int day, int hour, int minute, int second, int nano)
        : year(year), month(month), day(day), hour(hour), minute(minute), second(second), nano(nano) {}

    static DateTime now() {
        auto now = std::chrono::system_clock::now();
        std::time_t t = std::chrono::system_clock::to_time_t(now);
        std::tm tm_struct = *std::localtime(&t);
        auto dur = now.time_since_epoch();
        auto nanos_since_epoch = std::chrono::duration_cast<std::chrono::nanoseconds>(dur).count();
        long long nanos = nanos_since_epoch % 1000000000LL;
        if (nanos < 0) nanos += 1000000000LL;
        return DateTime(
            tm_struct.tm_year + 1900,
            tm_struct.tm_mon + 1,
            tm_struct.tm_mday,
            tm_struct.tm_hour,
            tm_struct.tm_min,
            tm_struct.tm_sec,
            (int)nanos
        );
    }

    DateTime withHour(int h) const {
        DateTime dt = *this;
        dt.hour = h;
        return dt;
    }

    DateTime withMinute(int m) const {
        DateTime dt = *this;
        dt.minute = m;
        return dt;
    }

    DateTime plusHours(long long hours) const {
        DateTime dt = *this;
        long long total_hours = (long long)dt.hour + hours;
        dt.hour = (int)(total_hours % 24);
        long long extra_days = total_hours / 24;
        if (dt.hour < 0) {
            dt.hour += 24;
            extra_days--;
        }
        dt.day += (int)extra_days;

        while (dt.day > daysInMonth(dt.year, dt.month)) {
            dt.day -= daysInMonth(dt.year, dt.month);
            dt.month++;
            if (dt.month > 12) {
                dt.month = 1;
                dt.year++;
            }
        }
        while (dt.day < 1) {
            dt.month--;
            if (dt.month < 1) {
                dt.month = 12;
                dt.year--;
            }
            dt.day += daysInMonth(dt.year, dt.month);
        }
        return dt;
    }

    bool isBefore(const DateTime& other) const {
        return *this < other;
    }

    bool isAfter(const DateTime& other) const {
        return other < *this;
    }

    bool operator==(const DateTime& other) const {
        return year == other.year && month == other.month && day == other.day &&
               hour == other.hour && minute == other.minute && second == other.second &&
               nano == other.nano;
    }

    bool operator!=(const DateTime& other) const {
        return !(*this == other);
    }

    bool operator<(const DateTime& other) const {
        if (year != other.year) return year < other.year;
        if (month != other.month) return month < other.month;
        if (day != other.day) return day < other.day;
        if (hour != other.hour) return hour < other.hour;
        if (minute != other.minute) return minute < other.minute;
        if (second != other.second) return second < other.second;
        return nano < other.nano;
    }

    static bool isLeapYear(int y) {
        return (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
    }

    static int daysInMonth(int y, int m) {
        static const int days[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        if (m == 2 && isLeapYear(y)) return 29;
        return days[m - 1];
    }
};

class Event {
public:
    DateTime date;
    DateTime start_time;
    DateTime end_time;
    std::string description;

    Event(DateTime date, DateTime start_time, DateTime end_time, std::string description)
        : date(date), start_time(start_time), end_time(end_time), description(std::move(description)) {}

    bool operator==(const Event& other) const {
        return date == other.date &&
               start_time == other.start_time &&
               end_time == other.end_time &&
               description == other.description;
    }

    bool operator!=(const Event& other) const {
        return !(*this == other);
    }
};

namespace std {
    template<> struct hash<DateTime> {
        size_t operator()(const DateTime& dt) const noexcept {
            size_t h = std::hash<int>()(dt.year);
            h = h * 31 + std::hash<int>()(dt.month);
            h = h * 31 + std::hash<int>()(dt.day);
            h = h * 31 + std::hash<int>()(dt.hour);
            h = h * 31 + std::hash<int>()(dt.minute);
            h = h * 31 + std::hash<int>()(dt.second);
            h = h * 31 + std::hash<int>()(dt.nano);
            return h;
        }
    };

    template<> struct hash<Event> {
        size_t operator()(const Event& e) const noexcept {
            size_t h = std::hash<DateTime>()(e.date);
            h = h * 31 + std::hash<DateTime>()(e.start_time);
            h = h * 31 + std::hash<DateTime>()(e.end_time);
            h = h * 31 + std::hash<std::string>()(e.description);
            return h;
        }
    };
}

class CalendarUtil {
public:
    std::vector<Event> events;

    void addEvent(const Event& event) {
        events.push_back(event);
    }

    void removeEvent(const Event& event) {
        auto it = std::find(events.begin(), events.end(), event);
        if (it != events.end()) {
            events.erase(it);
        }
    }

    std::vector<Event> getEvents(const DateTime& date) const {
        std::vector<Event> result;
        for (const auto& e : events) {
            if (e.date.year == date.year && e.date.month == date.month && e.date.day == date.day) {
                result.push_back(e);
            }
        }
        return result;
    }

    bool isAvailable(const DateTime& start_time, const DateTime& end_time) const {
        for (const auto& e : events) {
            if (start_time.isBefore(e.end_time) && end_time.isAfter(e.start_time)) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::pair<DateTime, DateTime>> getAvailableSlots(const DateTime& date) const {
        std::vector<std::pair<DateTime, DateTime>> availableSlots;
        DateTime start_time = date.withHour(0).withMinute(0);
        DateTime end_time = date.withHour(23).withMinute(59);

        while (start_time.isBefore(end_time)) {
            DateTime slot_end_time = start_time.plusHours(1);
            if (isAvailable(start_time, slot_end_time)) {
                availableSlots.emplace_back(start_time, slot_end_time);
            }
            start_time = slot_end_time;
        }

        return availableSlots;
    }

    std::vector<Event> getUpcomingEvents(int num_events) const {
        if (num_events < 0) {
            throw std::invalid_argument("limit is negative");
        }

        DateTime now = DateTime::now();
        std::vector<Event> result;

        for (const auto& e : events) {
            if (e.start_time.isAfter(now)) {
                if ((int)result.size() < num_events) {
                    result.push_back(e);
                } else {
                    break;
                }
            }
        }

        return result;
    }
};
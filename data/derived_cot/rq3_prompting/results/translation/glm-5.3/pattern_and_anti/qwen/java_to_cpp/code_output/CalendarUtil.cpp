#include <algorithm>
#include <cstddef>
#include <ctime>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

struct LocalDateTime {
    int year;
    int month;
    int day;
    int hour;
    int minute;
    int second;

    bool operator==(const LocalDateTime& o) const {
        return std::tie(year, month, day, hour, minute, second) ==
               std::tie(o.year, o.month, o.day, o.hour, o.minute, o.second);
    }
    bool operator!=(const LocalDateTime& o) const { return !(*this == o); }
    bool operator<(const LocalDateTime& o) const {
        return std::tie(year, month, day, hour, minute, second) <
               std::tie(o.year, o.month, o.day, o.hour, o.minute, o.second);
    }
    bool operator>(const LocalDateTime& o) const { return o < *this; }

    static bool isLeap(int y) { return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0); }
    static int daysInMonth(int y, int m) {
        static const int d[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        if (m == 2 && isLeap(y)) return 29;
        return d[m - 1];
    }

    LocalDateTime plusHours(int h) const {
        LocalDateTime r = *this;
        r.hour += h;
        while (r.hour >= 24) {
            r.hour -= 24;
            r.day += 1;
            if (r.day > daysInMonth(r.year, r.month)) {
                r.day = 1;
                r.month += 1;
                if (r.month > 12) {
                    r.month = 1;
                    r.year += 1;
                }
            }
        }
        return r;
    }

    LocalDateTime withHour(int h) const { LocalDateTime r = *this; r.hour = h; return r; }
    LocalDateTime withMinute(int m) const { LocalDateTime r = *this; r.minute = m; return r; }

    static LocalDateTime now() {
        std::time_t t = std::time(nullptr);
        std::tm lt{};
#ifdef _WIN32
        localtime_s(&lt, &t);
#else
        localtime_r(&t, &lt);
#endif
        return {lt.tm_year + 1900, lt.tm_mon + 1, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec};
    }
};

class Event {
public:
    LocalDateTime date;
    LocalDateTime start_time;
    LocalDateTime end_time;
    std::string description;

    Event(LocalDateTime date_, LocalDateTime start_time_, LocalDateTime end_time_, std::string description_)
        : date(date_), start_time(start_time_), end_time(end_time_), description(std::move(description_)) {}

    bool operator==(const Event& o) const {
        return date == o.date &&
               start_time == o.start_time &&
               end_time == o.end_time &&
               description == o.description;
    }
    bool operator!=(const Event& o) const { return !(*this == o); }
};

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

    std::vector<Event> getEvents(const LocalDateTime& date) const {
        std::vector<Event> result;
        for (const auto& event : events) {
            if (event.date.year == date.year && event.date.month == date.month && event.date.day == date.day) {
                result.push_back(event);
            }
        }
        return result;
    }

    bool isAvailable(const LocalDateTime& start_time, const LocalDateTime& end_time) const {
        for (const auto& event : events) {
            if (start_time < event.end_time && end_time > event.start_time) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::pair<LocalDateTime, LocalDateTime>> getAvailableSlots(const LocalDateTime& date) const {
        std::vector<std::pair<LocalDateTime, LocalDateTime>> availableSlots;
        LocalDateTime start_time = date.withHour(0).withMinute(0);
        LocalDateTime end_time = date.withHour(23).withMinute(59);

        while (start_time < end_time) {
            LocalDateTime slot_end_time = start_time.plusHours(1);
            if (isAvailable(start_time, slot_end_time)) {
                availableSlots.emplace_back(start_time, slot_end_time);
            }
            start_time = slot_end_time;
        }

        return availableSlots;
    }

    std::vector<Event> getUpcomingEvents(int num_events) const {
        LocalDateTime now = LocalDateTime::now();
        if (num_events < 0) {
            throw std::invalid_argument("Cannot limit negative number of elements");
        }
        std::vector<Event> result;
        for (const auto& event : events) {
            if (static_cast<int>(result.size()) >= num_events) break;
            if (event.start_time > now) {
                result.push_back(event);
            }
        }
        return result;
    }
};
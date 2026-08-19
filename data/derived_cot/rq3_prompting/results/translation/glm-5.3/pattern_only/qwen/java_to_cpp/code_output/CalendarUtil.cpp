#include <algorithm>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <ctime>
#include <functional>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace org {
namespace example {

// Minimal LocalDateTime equivalent: wall-clock date-time with no time zone
// (like java.time.LocalDateTime), supporting exactly the operations used
// by the original code. Pure civil-calendar arithmetic => no DST effects.
class LocalDateTime {
public:
    int year = 0;
    int month = 1;
    int day = 1;
    int hour = 0;
    int minute = 0;
    int second = 0;
    int nanosecond = 0;

    LocalDateTime() = default;

    LocalDateTime(int year_, int month_, int day_, int hour_, int minute_,
                  int second_ = 0, int nanosecond_ = 0)
        : year(year_), month(month_), day(day_), hour(hour_), minute(minute_),
          second(second_), nanosecond(nanosecond_) {}

    static LocalDateTime now() {
        std::time_t t = std::chrono::system_clock::to_time_t(
            std::chrono::system_clock::now());
        std::tm tmv{};
#ifdef _WIN32
        localtime_s(&tmv, &t);
#else
        localtime_r(&t, &tmv);
#endif
        return LocalDateTime(tmv.tm_year + 1900, tmv.tm_mon + 1, tmv.tm_mday,
                             tmv.tm_hour, tmv.tm_min, tmv.tm_sec, 0);
    }

    LocalDateTime withHour(int h) const {
        LocalDateTime r(*this);
        r.hour = h;
        return r;
    }

    LocalDateTime withMinute(int m) const {
        LocalDateTime r(*this);
        r.minute = m;
        return r;
    }

    // Equivalent of plus(n, ChronoUnit.HOURS): fixed 60-minute hour steps.
    LocalDateTime plusHours(long long h) const {
        long long total = days_from_civil(year, month, day) * 24 + hour + h;
        long long d = floor_div(total, 24);
        int hh = static_cast<int>(total - d * 24); // in [0, 23]
        int y; unsigned mo, dd;
        civil_from_days(d, y, mo, dd);
        LocalDateTime r(*this);
        r.year = y;
        r.month = static_cast<int>(mo);
        r.day = static_cast<int>(dd);
        r.hour = hh;
        return r;
    }

    bool isBefore(const LocalDateTime& o) const { return *this < o; }
    bool isAfter(const LocalDateTime& o) const { return o < *this; }

    bool operator==(const LocalDateTime& o) const {
        return std::tie(year, month, day, hour, minute, second, nanosecond) ==
               std::tie(o.year, o.month, o.day, o.hour, o.minute, o.second, o.nanosecond);
    }
    bool operator!=(const LocalDateTime& o) const { return !(*this == o); }
    bool operator<(const LocalDateTime& o) const {
        return std::tie(year, month, day, hour, minute, second, nanosecond) <
               std::tie(o.year, o.month, o.day, o.hour, o.minute, o.second, o.nanosecond);
    }

private:
    static long long floor_div(long long a, long long b) {
        long long q = a / b, r = a % b;
        return (r != 0 && ((r < 0) != (b < 0))) ? q - 1 : q;
    }
    // Howard Hinnant's civil-calendar algorithms (proleptic Gregorian).
    static long long days_from_civil(int y, int m, int d) {
        y -= m <= 2;
        const long long era = (y >= 0 ? y : y - 399) / 400;
        const unsigned yoe = static_cast<unsigned>(y - era * 400);
        const unsigned doy = (153u * (m + (m > 2 ? -3 : 9)) + 2u) / 5u +
                             static_cast<unsigned>(d) - 1u;
        const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
        return era * 146097 + static_cast<long long>(doe) - 719468;
    }
    static void civil_from_days(long long z, int& y, unsigned& m, unsigned& d) {
        z += 719468;
        const long long era = (z >= 0 ? z : z - 146096) / 146097;
        const unsigned doe = static_cast<unsigned>(z - era * 146097);
        const unsigned yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
        const long long yy = static_cast<long long>(yoe) + era * 400;
        const unsigned doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
        const unsigned mp = (5 * doy + 2) / 153;
        d = doy - (153 * mp + 2) / 5 + 1;
        m = mp + (mp < 10 ? 3 : -9);
        y = static_cast<int>(yy + (m <= 2));
    }
};

class Event {
public:
    LocalDateTime date;
    LocalDateTime start_time;
    LocalDateTime end_time;
    std::string description;

    Event(const LocalDateTime& date_, const LocalDateTime& start_time_,
          const LocalDateTime& end_time_, std::string description_)
        : date(date_), start_time(start_time_), end_time(end_time_),
          description(std::move(description_)) {}

    bool operator==(const Event& o) const {
        return date == o.date && start_time == o.start_time &&
               end_time == o.end_time && description == o.description;
    }
    bool operator!=(const Event& o) const { return !(*this == o); }

    std::size_t hashCode() const {
        auto mix = [](std::size_t& h, long long v) {
            h ^= static_cast<std::size_t>(v) + 0x9e3779b97f4a7c15ULL +
                 (h << 6) + (h >> 2);
        };
        auto dtFields = [&mix](std::size_t& h, const LocalDateTime& t) {
            mix(h, t.year); mix(h, t.month); mix(h, t.day);
            mix(h, t.hour); mix(h, t.minute); mix(h, t.second); mix(h, t.nanosecond);
        };
        std::size_t h = 0;
        dtFields(h, date); dtFields(h, start_time); dtFields(h, end_time);
        mix(h, static_cast<long long>(std::hash<std::string>{}(description)));
        return h;
    }
};

class CalendarUtil {
public:
    std::vector<Event> events;

    void addEvent(const Event& event) {
        events.push_back(event);
    }

    void removeEvent(const Event& event) {
        // java.util.List#remove(Object): removes the first equal occurrence.
        auto it = std::find(events.begin(), events.end(), event);
        if (it != events.end()) {
            events.erase(it);
        }
    }

    std::vector<Event> getEvents(const LocalDateTime& date) const {
        std::vector<Event> result;
        for (const Event& event : events) {
            if (event.date.year == date.year && event.date.month == date.month &&
                event.date.day == date.day) {
                result.push_back(event);
            }
        }
        return result;
    }

    bool isAvailable(const LocalDateTime& start_time,
                     const LocalDateTime& end_time) const {
        for (const Event& event : events) {
            if (start_time.isBefore(event.end_time) &&
                end_time.isAfter(event.start_time)) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::pair<LocalDateTime, LocalDateTime>>
    getAvailableSlots(const LocalDateTime& date) const {
        std::vector<std::pair<LocalDateTime, LocalDateTime>> availableSlots;
        LocalDateTime start_time = date.withHour(0).withMinute(0);
        const LocalDateTime end_time = date.withHour(23).withMinute(59);

        while (start_time.isBefore(end_time)) {
            LocalDateTime slot_end_time = start_time.plusHours(1);
            if (isAvailable(start_time, slot_end_time)) {
                availableSlots.emplace_back(start_time, slot_end_time);
            }
            start_time = slot_end_time;
        }

        return availableSlots;
    }

    std::vector<Event> getUpcomingEvents(int num_events) const {
        // Stream.limit(n) throws IllegalArgumentException for negative n.
        if (num_events < 0) {
            throw std::invalid_argument("number of events must not be negative");
        }
        const LocalDateTime now = LocalDateTime::now();
        std::vector<Event> result;
        for (const Event& event : events) {
            if (static_cast<int>(result.size()) >= num_events) break;
            if (event.start_time.isAfter(now)) {
                result.push_back(event);
            }
        }
        return result;
    }
};

} // namespace example
} // namespace org

// Parity with Java's hashCode: usable in hashed containers.
namespace std {
template <>
struct hash<org::example::Event> {
    std::size_t operator()(const org::example::Event& e) const noexcept {
        return e.hashCode();
    }
};
} // namespace std
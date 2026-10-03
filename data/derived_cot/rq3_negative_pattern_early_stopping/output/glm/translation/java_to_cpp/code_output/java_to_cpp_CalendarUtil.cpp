#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include <ctime>
#include <utility>
#include <stdexcept>

class LocalDateTime {
private:
    std::chrono::system_clock::time_point tp;

    std::tm getTm() const {
        std::time_t t = std::chrono::system_clock::to_time_t(tp);
        std::tm tm_val = {};
        // Use thread-safe alternatives to std::localtime where available
#ifdef _WIN32
        localtime_s(&tm_val, &t);
#else
        localtime_r(&t, &tm_val);
#endif
        return tm_val;
    }

    static LocalDateTime fromTm(const std::tm& t) {
        std::tm copy = t;
        copy.tm_isdst = -1; // Let mktime determine daylight saving time
        std::time_t time = std::mktime(&copy);
        return LocalDateTime(std::chrono::system_clock::from_time_t(time));
    }

    explicit LocalDateTime(std::chrono::system_clock::time_point p) : tp(p) {}

public:
    LocalDateTime() : tp(std::chrono::system_clock::now()) {}

    LocalDateTime(int year, int month, int day, int hour, int min, int sec = 0) {
        std::tm t = {};
        t.tm_year = year - 1900;
        t.tm_mon = month - 1;
        t.tm_mday = day;
        t.tm_hour = hour;
        t.tm_min = min;
        t.tm_sec = sec;
        t.tm_isdst = -1;
        tp = std::chrono::system_clock::from_time_t(std::mktime(&t));
    }

    bool sameDate(const LocalDateTime& other) const {
        auto t1 = getTm();
        auto t2 = other.getTm();
        return t1.tm_year == t2.tm_year && t1.tm_mon == t2.tm_mon && t1.tm_mday == t2.tm_mday;
    }

    bool isBefore(const LocalDateTime& other) const {
        return tp < other.tp;
    }

    bool isAfter(const LocalDateTime& other) const {
        return tp > other.tp;
    }

    LocalDateTime withHour(int h) const {
        auto t = getTm();
        t.tm_hour = h;
        return fromTm(t);
    }

    LocalDateTime withMinute(int m) const {
        auto t = getTm();
        t.tm_min = m;
        return fromTm(t);
    }

    LocalDateTime plusHours(int h) const {
        auto t = getTm();
        t.tm_hour += h;
        return fromTm(t);
    }

    static LocalDateTime now() {
        return LocalDateTime(std::chrono::system_clock::now());
    }

    bool operator==(const LocalDateTime& other) const {
        return tp == other.tp;
    }
};

class Event {
public:
    LocalDateTime date;
    LocalDateTime start_time;
    LocalDateTime end_time;
    std::string description;

    Event(LocalDateTime date, LocalDateTime start_time, LocalDateTime end_time, std::string description)
        : date(date), start_time(start_time), end_time(end_time), description(std::move(description)) {}

    bool operator==(const Event& other) const {
        return date == other.date &&
               start_time == other.start_time &&
               end_time == other.end_time &&
               description == other.description;
    }
};

class CalendarUtil {
public:
    std::vector<Event> events;

    void addEvent(const Event& event) {
        events.push_back(event);
    }

    void removeEvent(const Event& event) {
        // Java's List.remove(Object) removes the first occurrence
        auto it = std::find(events.begin(), events.end(), event);
        if (it != events.end()) {
            events.erase(it);
        }
    }

    std::vector<Event> getEvents(const LocalDateTime& date) {
        std::vector<Event> result;
        std::copy_if(events.begin(), events.end(), std::back_inserter(result),
                     [&date](const Event& event) {
                         return event.date.sameDate(date);
                     });
        return result;
    }

    bool isAvailable(const LocalDateTime& start_time, const LocalDateTime& end_time) {
        return std::none_of(events.begin(), events.end(),
                            [&start_time, &end_time](const Event& event) {
                                return start_time.isBefore(event.end_time) && end_time.isAfter(event.start_time);
                            });
    }

    std::vector<std::pair<LocalDateTime, LocalDateTime>> getAvailableSlots(const LocalDateTime& date) {
        std::vector<std::pair<LocalDateTime, LocalDateTime>> availableSlots;
        LocalDateTime start_time = date.withHour(0).withMinute(0);
        LocalDateTime end_time = date.withHour(23).withMinute(59);

        while (start_time.isBefore(end_time)) {
            LocalDateTime slot_end_time = start_time.plusHours(1);
            if (isAvailable(start_time, slot_end_time)) {
                availableSlots.emplace_back(start_time, slot_end_time);
            }
            start_time = slot_end_time;
        }

        return availableSlots;
    }

    std::vector<Event> getUpcomingEvents(int num_events) {
        if (num_events < 0) {
            throw std::invalid_argument("num_events cannot be negative");
        }
        
        LocalDateTime now = LocalDateTime::now();
        std::vector<Event> result;
        int count = 0;
        for (const auto& event : events) {
            if (event.start_time.isAfter(now)) {
                result.push_back(event);
                count++;
                if (count == num_events) {
                    break;
                }
            }
        }
        return result;
    }
};
#include <vector>
#include <string>
#include <ctime>
#include <algorithm>
#include <utility>

struct Event {
    std::tm date;
    std::tm start_time;
    std::tm end_time;
    std::string description;

    bool operator==(const Event& other) const {
        auto tm_eq = [](const std::tm& a, const std::tm& b) {
            return a.tm_year == b.tm_year && a.tm_mon == b.tm_mon && a.tm_mday == b.tm_mday &&
                   a.tm_hour == b.tm_hour && a.tm_min == b.tm_min && a.tm_sec == b.tm_sec;
        };
        return tm_eq(date, other.date) && tm_eq(start_time, other.start_time) &&
               tm_eq(end_time, other.end_time) && description == other.description;
    }
};

class CalendarUtil {
public:
    CalendarUtil() = default;

    void add_event(const Event& event) {
        events.push_back(event);
    }

    void remove_event(const Event& event) {
        auto it = std::find(events.begin(), events.end(), event);
        if (it != events.end()) {
            events.erase(it);
        }
    }

    std::vector<Event> get_events(const std::tm& date) {
        std::vector<Event> events_on_date;
        for (const auto& event : events) {
            if (event.date.tm_year == date.tm_year &&
                event.date.tm_mon == date.tm_mon &&
                event.date.tm_mday == date.tm_mday) {
                events_on_date.push_back(event);
            }
        }
        return events_on_date;
    }

    bool is_available(const std::tm& start_time, const std::tm& end_time) {
        for (const auto& event : events) {
            if (to_time_t(start_time) < to_time_t(event.end_time) &&
                to_time_t(end_time) > to_time_t(event.start_time)) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::pair<std::tm, std::tm>> get_available_slots(const std::tm& date) {
        std::vector<std::pair<std::tm, std::tm>> available_slots;
        
        std::tm start_time = date;
        start_time.tm_hour = 0;
        start_time.tm_min = 0;
        start_time.tm_sec = 0;
        start_time.tm_isdst = -1;

        std::tm end_time = date;
        end_time.tm_hour = 23;
        end_time.tm_min = 59;
        end_time.tm_sec = 0;
        end_time.tm_isdst = -1;

        while (to_time_t(start_time) < to_time_t(end_time)) {
            std::tm slot_end_time = add_minutes(start_time, 60);
            if (is_available(start_time, slot_end_time)) {
                available_slots.push_back({start_time, slot_end_time});
            }
            start_time = add_minutes(start_time, 60);
        }
        return available_slots;
    }

    std::vector<Event> get_upcoming_events(int num_events) {
        std::time_t now_time = std::time(nullptr);
        std::vector<Event> upcoming_events;
        for (const auto& event : events) {
            if (to_time_t(event.start_time) >= now_time) {
                upcoming_events.push_back(event);
            }
            if (static_cast<int>(upcoming_events.size()) == num_events) {
                break;
            }
        }
        return upcoming_events;
    }

private:
    std::vector<Event> events;

    static std::time_t to_time_t(const std::tm& t) {
        std::tm copy = t;
        copy.tm_isdst = -1;
        return std::mktime(&copy);
    }

    static std::tm add_minutes(std::tm t, int minutes) {
        std::time_t time = to_time_t(t);
        time += minutes * 60;
        return *std::localtime(&time);
    }
};
#include <vector>
#include <string>
#include <chrono>
#include <ctime>
#include <algorithm>

using namespace std::chrono;

struct Event {
    system_clock::time_point date;
    system_clock::time_point start_time;
    system_clock::time_point end_time;
    std::string description;

    bool operator==(const Event& other) const {
        return date == other.date && start_time == other.start_time && end_time == other.end_time && description == other.description;
    }
};

class CalendarUtil {
public:
    std::vector<Event> events;

    void add_event(const Event& event) {
        events.push_back(event);
    }

    void remove_event(const Event& event) {
        auto it = std::find(events.begin(), events.end(), event);
        if (it != events.end()) {
            events.erase(it);
        }
    }

    std::vector<Event> get_events(const system_clock::time_point& date) {
        auto date_time = get_date_time(date);
        std::vector<Event> events_on_date;
        for (const auto& event : events) {
            if (get_date_time(event.date) == date_time) {
                events_on_date.push_back(event);
            }
        }
        return events_on_date;
    }

    bool is_available(const system_clock::time_point& start_time, const system_clock::time_point& end_time) {
        for (const auto& event : events) {
            if ((start_time < event.end_time) && (end_time > event.start_time)) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::pair<system_clock::time_point, system_clock::time_point>> get_available_slots(const system_clock::time_point& date) {
        auto start_time = get_date_time(date);
        auto end_time = start_time + days{1} - seconds{1};

        std::vector<std::pair<system_clock::time_point, system_clock::time_point>> available_slots;

        while (start_time < end_time) {
            system_clock::time_point slot_end_time = start_time + minutes{60};
            if (is_available(start_time, slot_end_time)) {
                available_slots.push_back({start_time, slot_end_time});
            }
            start_time += minutes{60};
        }

        return available_slots;
    }

    std::vector<Event> get_upcoming_events(int num_events) {
        auto now = system_clock::now();
        std::vector<Event> upcoming_events;
        for (const auto& event : events) {
            if (event.start_time >= now) {
                upcoming_events.push_back(event);
                if (upcoming_events.size() == static_cast<size_t>(num_events)) {
                    break;
                }
            }
        }
        return upcoming_events;
    }

private:
    system_clock::time_point get_date_time(const system_clock::time_point& tp) {
        auto tt = system_clock::to_time_t(tp);
        std::tm t = *localtime(&tt);
        t.tm_hour = 0;
        t.tm_min = 0;
        t.tm_sec = 0;
        auto new_tt = mktime(&t);
        return system_clock::from_time_t(new_tt);
    }
};
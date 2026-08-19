#include <algorithm>
#include <chrono>
#include <cstddef>
#include <string>
#include <utility>
#include <vector>

class CalendarUtil {
public:
    using Clock = std::chrono::system_clock;
    using TimePoint = Clock::time_point;
    using Minutes = std::chrono::minutes;

    struct Event {
        TimePoint date;
        TimePoint start_time;
        TimePoint end_time;
        std::string description;

        bool operator==(const Event&) const = default;
    };

    std::vector<Event> events;

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

    std::vector<Event> get_events(const TimePoint& date) const {
        std::vector<Event> events_on_date;
        auto day = std::chrono::floor<std::chrono::days>(date);
        for (const auto& event : events) {
            if (std::chrono::floor<std::chrono::days>(event.date) == day) {
                events_on_date.push_back(event);
            }
        }
        return events_on_date;
    }

    bool is_available(const TimePoint& start_time, const TimePoint& end_time) const {
        for (const auto& event : events) {
            if (start_time < event.end_time && end_time > event.start_time) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::pair<TimePoint, TimePoint>> get_available_slots(const TimePoint& date) const {
        std::vector<std::pair<TimePoint, TimePoint>> available_slots;
        auto day = std::chrono::floor<std::chrono::days>(date);
        TimePoint start_time(day);
        TimePoint end_time = start_time + std::chrono::hours(23) + Minutes(59);

        while (start_time < end_time) {
            TimePoint slot_end_time = start_time + Minutes(60);
            if (is_available(start_time, slot_end_time)) {
                available_slots.emplace_back(start_time, slot_end_time);
            }
            start_time += Minutes(60);
        }

        return available_slots;
    }

    std::vector<Event> get_upcoming_events(std::size_t num_events) const {
        TimePoint now = Clock::now();
        std::vector<Event> upcoming_events;
        for (const auto& event : events) {
            if (event.start_time >= now) {
                upcoming_events.push_back(event);
            }
            if (upcoming_events.size() == num_events) {
                break;
            }
        }
        return upcoming_events;
    }
};
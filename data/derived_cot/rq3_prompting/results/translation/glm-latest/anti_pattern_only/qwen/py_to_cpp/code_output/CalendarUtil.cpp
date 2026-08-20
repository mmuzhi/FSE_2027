#include <algorithm>
#include <chrono>
#include <cstddef>
#include <string>
#include <utility>
#include <vector>

class CalendarUtil {
public:
    // Analog of Python's datetime objects.
    using DateTime = std::chrono::system_clock::time_point;

    // Analog of Python's event dict:
    // {'date': ..., 'start_time': ..., 'end_time': ..., 'description': ...}
    struct Event {
        DateTime date;
        DateTime start_time;
        DateTime end_time;
        std::string description;

        bool operator==(const Event& other) const = default;
    };

    // Add an event to the calendar.
    void add_event(const Event& event) {
        events.push_back(event);
    }

    // Remove an event from the calendar (first occurrence, only if present).
    void remove_event(const Event& event) {
        auto it = std::find(events.begin(), events.end(), event);
        if (it != events.end()) {
            events.erase(it);
        }
    }

    // Get all events on a given date (compares calendar day, ignoring time of day).
    std::vector<Event> get_events(const DateTime& date) const {
        std::vector<Event> events_on_date;
        const auto day = std::chrono::floor<std::chrono::days>(date);
        for (const Event& event : events) {
            if (std::chrono::floor<std::chrono::days>(event.date) == day) {
                events_on_date.push_back(event);
            }
        }
        return events_on_date;
    }

    // Check if the calendar is available for a given time slot.
    bool is_available(const DateTime& start_time, const DateTime& end_time) const {
        for (const Event& event : events) {
            if (start_time < event.end_time && end_time > event.start_time) {
                return false;
            }
        }
        return true;
    }

    // Get all available time slots on a given date.
    std::vector<std::pair<DateTime, DateTime>> get_available_slots(const DateTime& date) const {
        std::vector<std::pair<DateTime, DateTime>> available_slots;
        // datetime(date.year, date.month, date.day, 0, 0) == midnight of that day.
        const DateTime day_start = std::chrono::floor<std::chrono::days>(date);
        // datetime(date.year, date.month, date.day, 23, 59)
        const DateTime end_time = day_start + std::chrono::hours(23) + std::chrono::minutes(59);

        DateTime start_time = day_start;
        while (start_time < end_time) {
            const DateTime slot_end_time = start_time + std::chrono::minutes(60);
            if (is_available(start_time, slot_end_time)) {
                available_slots.emplace_back(start_time, slot_end_time);
            }
            start_time += std::chrono::minutes(60);
        }

        return available_slots;
    }

    // Get the next n upcoming events from the current moment.
    std::vector<Event> get_upcoming_events(std::size_t num_events) const {
        const DateTime now = std::chrono::system_clock::now();
        std::vector<Event> upcoming_events;
        for (const Event& event : events) {
            if (event.start_time >= now) {
                upcoming_events.push_back(event);
            }
            if (upcoming_events.size() == num_events) {
                break;
            }
        }
        return upcoming_events;
    }

    // Public, mirroring Python's directly accessible `calendar.events` attribute.
    std::vector<Event> events;
};
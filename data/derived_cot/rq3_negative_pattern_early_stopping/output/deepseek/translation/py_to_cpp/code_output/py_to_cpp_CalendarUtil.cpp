#include <vector>
#include <string>
#include <chrono>
#include <algorithm>
#include <ctime>
#include <utility>

class CalendarUtil {
public:
    struct Event {
        std::chrono::system_clock::time_point date;
        std::chrono::system_clock::time_point start_time;
        std::chrono::system_clock::time_point end_time;
        std::string description;

        bool operator==(const Event& other) const {
            return date == other.date &&
                   start_time == other.start_time &&
                   end_time == other.end_time &&
                   description == other.description;
        }
    };

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

    std::vector<Event> get_events(const std::chrono::system_clock::time_point& date) const {
        std::vector<Event> result;
        for (const auto& ev : events) {
            if (date_only(ev.date) == date_only(date)) {
                result.push_back(ev);
            }
        }
        return result;
    }

    bool is_available(const std::chrono::system_clock::time_point& start_time,
                      const std::chrono::system_clock::time_point& end_time) const {
        for (const auto& ev : events) {
            if (start_time < ev.end_time && end_time > ev.start_time) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::pair<std::chrono::system_clock::time_point,
                          std::chrono::system_clock::time_point>>
    get_available_slots(const std::chrono::system_clock::time_point& date) const {
        auto day_start = date_only(date);
        auto day_end = day_start + std::chrono::hours(23) + std::chrono::minutes(59);

        std::vector<std::pair<time_point, time_point>> slots;
        auto current = day_start;
        const auto slot_duration = std::chrono::minutes(60);
        while (current < day_end) {
            auto slot_end = current + slot_duration;
            if (is_available(current, slot_end)) {
                slots.emplace_back(current, slot_end);
            }
            current = slot_end;
        }
        return slots;
    }

    std::vector<Event> get_upcoming_events(int num_events) const {
        // local time matching Python's datetime.now()
        auto now = local_now();
        std::vector<Event> result;
        for (const auto& ev : events) {
            if (ev.start_time >= now) {
                result.push_back(ev);
                if (static_cast<int>(result.size()) == num_events) {
                    break;
                }
            }
        }
        return result;
    }

private:
    std::vector<Event> events;

    // Returns a time_point representing the start of the UTC day (00:00:00)
    static std::chrono::system_clock::time_point date_only(
        const std::chrono::system_clock::time_point& tp) {
        auto tt = std::chrono::system_clock::to_time_t(tp);
        std::tm tm_buf;
        // Use gmtime to stay in UTC (matching Python's naive datetime)
#ifdef _WIN32
        gmtime_s(&tm_buf, &tt);
#else
        gmtime_r(&tt, &tm_buf);
#endif
        tm_buf.tm_hour = 0;
        tm_buf.tm_min = 0;
        tm_buf.tm_sec = 0;
        tm_buf.tm_isdst = -1;   // not needed for gmtime, but safe
        // timegm interprets tm as UTC and returns time_t
        auto utc_tt = timegm(&tm_buf);
        return std::chrono::system_clock::from_time_t(utc_tt);
    }

    // Returns a time_point representing the current local time
    static std::chrono::system_clock::time_point local_now() {
        auto now_utc = std::chrono::system_clock::now();
        std::time_t tt = std::chrono::system_clock::to_time_t(now_utc);
        std::tm tm_buf;
#ifdef _WIN32
        localtime_s(&tm_buf, &tt);
#else
        localtime_r(&tt, &tm_buf);
#endif
        std::time_t local_tt = std::mktime(&tm_buf);
        return std::chrono::system_clock::from_time_t(local_tt);
    }
};
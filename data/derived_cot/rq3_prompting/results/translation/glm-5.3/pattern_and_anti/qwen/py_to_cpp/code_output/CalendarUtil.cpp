#include <algorithm>
#include <chrono>
#include <cstdint>
#include <map>
#include <string>
#include <utility>
#include <variant>
#include <vector>

// Datetime analog: naive civil time with minute/second resolution,
// linear ordering, date truncation, minute arithmetic, and now().
class DateTime {
public:
    DateTime() : t_(0) {}
    DateTime(int year, int month, int day, int hour = 0, int minute = 0, int second = 0)
        : t_(days_from_civil(year, static_cast<unsigned>(month), static_cast<unsigned>(day)) * 86400
             + hour * 3600 + minute * 60 + second) {}

    static DateTime now() {
        DateTime dt;
        dt.t_ = std::chrono::duration_cast<std::chrono::seconds>(
                    std::chrono::system_clock::now().time_since_epoch()).count();
        return dt;
    }

    int year() const  { return civil().y; }
    int month() const { return civil().m; }
    int day() const   { return civil().d; }
    int hour() const   { return static_cast<int>(time_of_day() / 3600); }
    int minute() const { return static_cast<int>((time_of_day() % 3600) / 60); }

    DateTime date() const { DateTime dt; dt.t_ = t_ - time_of_day(); return dt; }
    DateTime add_minutes(std::int64_t minutes) const { DateTime dt; dt.t_ = t_ + minutes * 60; return dt; }

    friend bool operator==(const DateTime& a, const DateTime& b) { return a.t_ == b.t_; }
    friend bool operator!=(const DateTime& a, const DateTime& b) { return a.t_ != b.t_; }
    friend bool operator< (const DateTime& a, const DateTime& b) { return a.t_ <  b.t_; }
    friend bool operator<=(const DateTime& a, const DateTime& b) { return a.t_ <= b.t_; }
    friend bool operator> (const DateTime& a, const DateTime& b) { return a.t_ >  b.t_; }
    friend bool operator>=(const DateTime& a, const DateTime& b) { return a.t_ >= b.t_; }

private:
    std::int64_t t_;  // seconds since 1970-01-01T00:00:00

    std::int64_t time_of_day() const {
        std::int64_t days = floor_div(t_, 86400);
        return t_ - days * 86400;
    }

    struct Civil { int y, m, d; };
    Civil civil() const {
        std::int64_t days = floor_div(t_, 86400);
        int y; unsigned m, d;
        civil_from_days(days, y, m, d);
        return Civil{y, static_cast<int>(m), static_cast<int>(d)};
    }

    static std::int64_t floor_div(std::int64_t a, std::int64_t b) {
        return a >= 0 ? a / b : -((-a + b - 1) / b);
    }

    static std::int64_t days_from_civil(int y, unsigned m, unsigned d) {
        y -= m <= 2;
        const int era = (y >= 0 ? y : y - 399) / 400;
        const unsigned yoe = static_cast<unsigned>(y - era * 400);
        const unsigned doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
        const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
        return static_cast<std::int64_t>(era) * 146097 + doe - 719468;
    }

    static void civil_from_days(std::int64_t z, int& y, unsigned& m, unsigned& d) {
        z += 719468;
        const std::int64_t era = (z >= 0 ? z : z - 146096) / 146097;
        const unsigned doe = static_cast<unsigned>(z - era * 146097);
        const unsigned yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
        y = static_cast<int>(yoe) + static_cast<int>(era) * 400;
        const unsigned doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
        const unsigned mp = (5 * doy + 2) / 153;
        d = doy - (153 * mp + 2) / 5 + 1;
        m = mp + (mp < 10 ? 3 : -9);
        y += (m <= 2);
    }
};

// Event == Python dict with datetime/str values.
using EventValue = std::variant<DateTime, std::string>;
using Event = std::map<std::string, EventValue>;

class CalendarUtil {
public:
    CalendarUtil() = default;

    void add_event(const Event& event) {
        events.push_back(event);
    }

    void remove_event(const Event& event) {
        auto it = std::find(events.begin(), events.end(), event);
        if (it != events.end())
            events.erase(it);  // removes the first equal element, like list.remove
    }

    std::vector<Event> get_events(const DateTime& date) const {
        std::vector<Event> events_on_date;
        const DateTime target = date.date();
        for (const Event& event : events)
            if (get_datetime(event, "date").date() == target)
                events_on_date.push_back(event);
        return events_on_date;
    }

    bool is_available(const DateTime& start_time, const DateTime& end_time) const {
        for (const Event& event : events)
            if (start_time < get_datetime(event, "end_time") &&
                end_time > get_datetime(event, "start_time"))
                return false;
        return true;
    }

    std::vector<std::pair<DateTime, DateTime>> get_available_slots(const DateTime& date) const {
        std::vector<std::pair<DateTime, DateTime>> available_slots;
        DateTime start_time(date.year(), date.month(), date.day(), 0, 0);
        const DateTime end_time(date.year(), date.month(), date.day(), 23, 59);

        while (start_time < end_time) {
            DateTime slot_end_time = start_time.add_minutes(60);  // timedelta(minutes=60)
            if (is_available(start_time, slot_end_time))
                available_slots.emplace_back(start_time, slot_end_time);
            start_time = start_time.add_minutes(60);
        }

        return available_slots;
    }

    std::vector<Event> get_upcoming_events(int num_events) const {
        const DateTime now = DateTime::now();
        std::vector<Event> upcoming_events;
        for (const Event& event : events) {
            if (get_datetime(event, "start_time") >= now)
                upcoming_events.push_back(event);
            if (static_cast<int>(upcoming_events.size()) == num_events)
                break;
        }
        return upcoming_events;
    }

    std::vector<Event> events;

private:
    // .at() throws std::out_of_range for a missing key (KeyError analog);
    // std::get throws for a non-datetime value (type-error analog).
    static const DateTime& get_datetime(const Event& event, const std::string& key) {
        return std::get<DateTime>(event.at(key));
    }
};
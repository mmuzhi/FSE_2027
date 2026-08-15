#include <vector>
#include <string>
#include <algorithm>
#include <ctime>
#include <chrono>
#include <utility>

struct DateTime {
    int year;
    int month;
    int day;
    int hour;
    int minute;
    int second;
    int microsecond;

    DateTime(int y, int mo, int d, int h = 0, int mi = 0, int s = 0, int us = 0)
        : year(y), month(mo), day(d), hour(h), minute(mi), second(s), microsecond(us) {}

    DateTime() : year(0), month(0), day(0), hour(0), minute(0), second(0), microsecond(0) {}

    static bool isLeap(int y) {
        return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
    }

    static int daysInMonth(int y, int m) {
        static const int days[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        if (m == 2 && isLeap(y)) return 29;
        return days[m - 1];
    }

    void addMinutes(int minutes) {
        int total = minute + hour * 60 + minutes;
        minute = total % 60;
        hour = (total / 60) % 24;
        int extraDays = total / (60 * 24);
        day += extraDays;
        while (day > daysInMonth(year, month)) {
            day -= daysInMonth(year, month);
            month++;
            if (month > 12) {
                month = 1;
                year++;
            }
        }
    }

    DateTime date() const {
        return DateTime(year, month, day, 0, 0, 0, 0);
    }

    bool operator<(const DateTime& other) const {
        if (year != other.year) return year < other.year;
        if (month != other.month) return month < other.month;
        if (day != other.day) return day < other.day;
        if (hour != other.hour) return hour < other.hour;
        if (minute != other.minute) return minute < other.minute;
        if (second != other.second) return second < other.second;
        return microsecond < other.microsecond;
    }

    bool operator>(const DateTime& other) const {
        return other < *this;
    }

    bool operator<=(const DateTime& other) const {
        return !(other < *this);
    }

    bool operator>=(const DateTime& other) const {
        return !(*this < other);
    }

    bool operator==(const DateTime& other) const {
        return year == other.year && month == other.month && day == other.day &&
               hour == other.hour && minute == other.minute && second == other.second &&
               microsecond == other.microsecond;
    }

    bool operator!=(const DateTime& other) const {
        return !(*this == other);
    }

    static DateTime now() {
        auto now = std::chrono::system_clock::now();
        std::time_t t = std::chrono::system_clock::to_time_t(now);
        std::tm* tm = std::localtime(&t);
        auto since_epoch = now.time_since_epoch();
        auto secs = std::chrono::duration_cast<std::chrono::seconds>(since_epoch);
        auto micros = std::chrono::duration_cast<std::chrono::microseconds>(since_epoch - secs);
        return DateTime(tm->tm_year + 1900, tm->tm_mon + 1, tm->tm_mday,
                        tm->tm_hour, tm->tm_min, tm->tm_sec, micros.count());
    }
};

struct Event {
    DateTime date;
    DateTime start_time;
    DateTime end_time;
    std::string description;

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

    void add_event(const Event& event) {
        events.push_back(event);
    }

    void remove_event(const Event& event) {
        auto it = std::find(events.begin(), events.end(), event);
        if (it != events.end()) {
            events.erase(it);
        }
    }

    std::vector<Event> get_events(const DateTime& date) const {
        std::vector<Event> events_on_date;
        for (const auto& event : events) {
            if (event.date.date() == date.date()) {
                events_on_date.push_back(event);
            }
        }
        return events_on_date;
    }

    bool is_available(const DateTime& start_time, const DateTime& end_time) const {
        for (const auto& event : events) {
            if (start_time < event.end_time && end_time > event.start_time) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::pair<DateTime, DateTime>> get_available_slots(const DateTime& date) const {
        std::vector<std::pair<DateTime, DateTime>> available_slots;
        DateTime start_time(date.year, date.month, date.day, 0, 0);
        DateTime end_time(date.year, date.month, date.day, 23, 59);

        while (start_time < end_time) {
            DateTime slot_end_time = start_time;
            slot_end_time.addMinutes(60);
            if (is_available(start_time, slot_end_time)) {
                available_slots.push_back(std::make_pair(start_time, slot_end_time));
            }
            start_time.addMinutes(60);
        }
        return available_slots;
    }

    std::vector<Event> get_upcoming_events(int num_events) const {
        DateTime now = DateTime::now();
        std::vector<Event> upcoming_events;
        for (const auto& event : events) {
            if (event.start_time >= now) {
                upcoming_events.push_back(event);
                if (static_cast<int>(upcoming_events.size()) == num_events) {
                    break;
                }
            }
        }
        return upcoming_events;
    }
};
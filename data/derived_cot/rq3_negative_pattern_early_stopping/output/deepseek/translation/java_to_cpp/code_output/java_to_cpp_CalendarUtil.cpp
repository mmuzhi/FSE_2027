#include <vector>
#include <algorithm>
#include <chrono>
#include <ctime>
#include <utility>
#include <string>
#include <iterator>

class LocalDate {
public:
    int year;
    int month;
    int day;
    LocalDate(int y, int m, int d) : year(y), month(m), day(d) {}
    bool operator==(const LocalDate& other) const {
        return year == other.year && month == other.month && day == other.day;
    }
};

class LocalDateTime {
public:
    int year;
    int month;
    int day;
    int hour;
    int minute;
    int second;

    LocalDateTime(int y, int m, int d, int h, int min, int sec = 0)
        : year(y), month(m), day(d), hour(h), minute(min), second(sec) {}

    LocalDateTime() : year(0), month(0), day(0), hour(0), minute(0), second(0) {}

    static LocalDateTime now() {
        auto now = std::chrono::system_clock::now();
        std::time_t t = std::chrono::system_clock::to_time_t(now);
        std::tm* local = std::localtime(&t);
        return LocalDateTime(local->tm_year + 1900, local->tm_mon + 1, local->tm_mday,
                             local->tm_hour, local->tm_min, local->tm_sec);
    }

    LocalDate toLocalDate() const {
        return LocalDate(year, month, day);
    }

    LocalDateTime withHour(int h) const {
        return LocalDateTime(year, month, day, h, minute, second);
    }

    LocalDateTime withMinute(int m) const {
        return LocalDateTime(year, month, day, hour, m, second);
    }

    LocalDateTime plusHours(int h) const {
        int total_hours = hour + h;
        int new_day = day;
        int new_month = month;
        int new_year = year;
        while (total_hours >= 24) {
            total_hours -= 24;
            new_day++;
        }
        while (total_hours < 0) {
            total_hours += 24;
            new_day--;
        }
        auto daysInMonth = [](int y, int m) -> int {
            static const int days[] = {31,28,31,30,31,30,31,31,30,31,30,31};
            if (m == 2 && ((y % 4 == 0 && y % 100 != 0) || (y % 400 == 0)))
                return 29;
            return days[m-1];
        };
        while (new_day > daysInMonth(new_year, new_month)) {
            new_day -= daysInMonth(new_year, new_month);
            new_month++;
            if (new_month > 12) {
                new_month = 1;
                new_year++;
            }
        }
        while (new_day < 1) {
            new_month--;
            if (new_month < 1) {
                new_month = 12;
                new_year--;
            }
            new_day += daysInMonth(new_year, new_month);
        }
        return LocalDateTime(new_year, new_month, new_day, total_hours, minute, second);
    }

    bool isBefore(const LocalDateTime& other) const {
        if (year != other.year) return year < other.year;
        if (month != other.month) return month < other.month;
        if (day != other.day) return day < other.day;
        if (hour != other.hour) return hour < other.hour;
        if (minute != other.minute) return minute < other.minute;
        return second < other.second;
    }

    bool isAfter(const LocalDateTime& other) const {
        return other.isBefore(*this);
    }

    bool operator==(const LocalDateTime& other) const {
        return year == other.year && month == other.month && day == other.day &&
               hour == other.hour && minute == other.minute && second == other.second;
    }

    bool operator!=(const LocalDateTime& other) const {
        return !(*this == other);
    }

    bool operator<(const LocalDateTime& other) const {
        return isBefore(other);
    }

    bool operator>(const LocalDateTime& other) const {
        return other.isBefore(*this);
    }

    bool operator<=(const LocalDateTime& other) const {
        return !(other.isBefore(*this));
    }

    bool operator>=(const LocalDateTime& other) const {
        return !isBefore(other);
    }
};

class Event {
public:
    LocalDateTime date;
    LocalDateTime start_time;
    LocalDateTime end_time;
    std::string description;

    Event(const LocalDateTime& date, const LocalDateTime& start_time, const LocalDateTime& end_time, const std::string& description)
        : date(date), start_time(start_time), end_time(end_time), description(description) {}

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
        auto it = std::find(events.begin(), events.end(), event);
        if (it != events.end()) {
            events.erase(it);
        }
    }

    std::vector<Event> getEvents(const LocalDateTime& date) {
        std::vector<Event> result;
        std::copy_if(events.begin(), events.end(), std::back_inserter(result),
                     [&date](const Event& e) { return e.date.toLocalDate() == date.toLocalDate(); });
        return result;
    }

    bool isAvailable(const LocalDateTime& start_time, const LocalDateTime& end_time) {
        return std::none_of(events.begin(), events.end(),
                            [&start_time, &end_time](const Event& e) {
                                return start_time.isBefore(e.end_time) && end_time.isAfter(e.start_time);
                            });
    }

    std::vector<std::pair<LocalDateTime, LocalDateTime>> getAvailableSlots(const LocalDateTime& date) {
        std::vector<std::pair<LocalDateTime, LocalDateTime>> availableSlots;
        LocalDateTime start_time = date.withHour(0).withMinute(0);
        LocalDateTime end_time = date.withHour(23).withMinute(59);

        while (start_time.isBefore(end_time)) {
            LocalDateTime slot_end_time = start_time.plusHours(1);
            if (isAvailable(start_time, slot_end_time)) {
                availableSlots.push_back({start_time, slot_end_time});
            }
            start_time = slot_end_time;
        }

        return availableSlots;
    }

    std::vector<Event> getUpcomingEvents(int num_events) {
        LocalDateTime now = LocalDateTime::now();
        std::vector<Event> result;
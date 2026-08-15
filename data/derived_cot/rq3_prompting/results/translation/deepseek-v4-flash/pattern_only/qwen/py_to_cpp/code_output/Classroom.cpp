#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <cctype>

struct Course {
    std::string name;
    std::string start_time;
    std::string end_time;

    bool operator==(const Course& other) const {
        return name == other.name &&
               start_time == other.start_time &&
               end_time == other.end_time;
    }
};

class Classroom {
public:
    int id;
    std::vector<Course> courses;

    Classroom(int id) : id(id) {}

    void add_course(const Course& course) {
        if (std::find(courses.begin(), courses.end(), course) == courses.end()) {
            courses.push_back(course);
        }
    }

    void remove_course(const Course& course) {
        auto it = std::find(courses.begin(), courses.end(), course);
        if (it != courses.end()) {
            courses.erase(it);
        }
    }

    bool is_free_at(const std::string& check_time) const {
        int check = parse_time(check_time);
        for (const auto& course : courses) {
            int start = parse_time(course.start_time);
            int end = parse_time(course.end_time);
            if (start <= check && check <= end) {
                return false;
            }
        }
        return true;
    }

    bool check_course_conflict(const Course& new_course) const {
        int new_start = parse_time(new_course.start_time);
        int new_end = parse_time(new_course.end_time);

        for (const auto& course : courses) {
            int start = parse_time(course.start_time);
            int end = parse_time(course.end_time);

            if (start <= new_start && end >= new_start) {
                return false;
            }
            if (start <= new_end && end >= new_end) {
                return false;
            }
        }
        return true;
    }

private:
    static bool all_digits(const std::string& s) {
        if (s.empty()) return false;
        for (char c : s) {
            if (!std::isdigit(static_cast<unsigned char>(c))) {
                return false;
            }
        }
        return true;
    }

    static int parse_time(const std::string& time_str) {
        size_t colon = time_str.find(':');
        if (colon == std::string::npos) {
            throw std::invalid_argument("time data '" + time_str + "' does not match format '%H:%M'");
        }

        std::string hour_str = time_str.substr(0, colon);
        std::string minute_str = time_str.substr(colon + 1);

        if (!all_digits(hour_str) || !all_digits(minute_str)) {
            throw std::invalid_argument("time data '" + time_str + "' does not match format '%H:%M'");
        }

        int hour = std::stoi(hour_str);
        int minute = std::stoi(minute_str);

        if (hour < 0 || hour > 23 || minute < 0 || minute > 59) {
            throw std::invalid_argument("time data '" + time_str + "' does not match format '%H:%M'");
        }

        return hour * 60 + minute;
    }
};
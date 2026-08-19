#include <string>
#include <vector>
#include <cstdio>
#include <stdexcept>

class Classroom {
public:
    // Equivalent of the Python course dict: {'name', 'start_time', 'end_time'}
    struct Course {
        std::string name;
        std::string start_time;
        std::string end_time;

        // Value equality, mirroring Python dict comparison for `in`/`remove`
        bool operator==(const Course& other) const {
            return name == other.name &&
                   start_time == other.start_time &&
                   end_time == other.end_time;
        }
    };

    int id;
    std::vector<Course> courses;

    Classroom(int id) : id(id), courses() {}

    void add_course(const Course& course) {
        for (const auto& existing : courses) {
            if (existing == course) {
                return;
            }
        }
        courses.push_back(course);
    }

    void remove_course(const Course& course) {
        for (auto it = courses.begin(); it != courses.end(); ++it) {
            if (*it == course) {
                courses.erase(it);  // removes first occurrence, like list.remove
                return;
            }
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
        int new_start_time = parse_time(new_course.start_time);
        int new_end_time = parse_time(new_course.end_time);

        bool flag = true;
        for (const auto& course : courses) {
            int start_time = parse_time(course.start_time);
            int end_time = parse_time(course.end_time);
            if (start_time <= new_start_time && end_time >= new_start_time) {
                flag = false;
            }
            if (start_time <= new_end_time && end_time >= new_end_time) {
                flag = false;
            }
        }
        return flag;
    }

private:
    // Parses '%H:%M' (accepts non-zero-padded like '8:00') into minutes since midnight.
    // Throws on malformed input, mirroring datetime.strptime's ValueError.
    static int parse_time(const std::string& time_str) {
        int hour = 0, minute = 0;
        int consumed = 0;
        int count = std::sscanf(time_str.c_str(), "%d:%d%n", &hour, &minute, &consumed);
        if (count != 2 || consumed != static_cast<int>(time_str.size()) ||
            hour < 0 || hour > 23 || minute < 0 || minute > 59) {
            throw std::invalid_argument(
                "time data '" + time_str + "' does not match format '%H:%M'");
        }
        return hour * 60 + minute;
    }
};
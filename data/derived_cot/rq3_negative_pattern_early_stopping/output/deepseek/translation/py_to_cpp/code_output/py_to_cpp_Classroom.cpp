#include <string>
#include <vector>
#include <algorithm>
#include <sstream>
#include <iomanip>

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
            if ((start <= new_start && new_start <= end) ||
                (start <= new_end && new_end <= end)) {
                return false;
            }
        }
        return true;
    }

private:
    int id;
    std::vector<Course> courses;

    static int parse_time(const std::string& time_str) {
        int hours, minutes;
        char colon;
        std::istringstream ss(time_str);
        ss >> hours >> colon >> minutes;
        return hours * 60 + minutes;
    }
};
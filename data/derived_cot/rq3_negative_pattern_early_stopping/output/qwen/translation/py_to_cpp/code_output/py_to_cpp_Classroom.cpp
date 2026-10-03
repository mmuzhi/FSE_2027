#include <vector>
#include <string>
#include <iomanip>
#include <sstream>
#include <ctime>
#include <algorithm>

struct Course {
    std::string name;
    std::string start_time;
    std::string end_time;
};

class Classroom {
private:
    int id;
    std::vector<Course> courses;

    // Helper function to convert time string to time_t
    std::tm parse_time(const std::string& time_str) {
        std::tm time = {};
        std::istringstream ss(time_str);
        ss >> std::get_time(&time, "%H:%M");
        return time;
    }

public:
    Classroom(int id) : id(id) {}

    bool add_course(const Course& course) {
        for (const auto& c : courses) {
            if (c.name == course.name && c.start_time == course.start_time && c.end_time == course.end_time) {
                return false;
            }
        }
        courses.push_back(course);
        return true;
    }

    bool remove_course(const Course& course) {
        auto it = std::find(courses.begin(), courses.end(), course);
        if (it != courses.end()) {
            courses.erase(it);
            return true;
        }
        return false;
    }

    bool is_free_at(const std::string& check_time) {
        std::tm check_tm = parse_time(check_time);
        time_t check_time_t = mktime(&check_tm);

        for (const auto& course : courses) {
            std::tm start_tm = parse_time(course.start_time);
            std::tm end_tm = parse_time(course.end_time);
            time_t start_time_t = mktime(&start_tm);
            time_t end_time_t = mktime(&end_tm);

            if (check_time_t >= start_time_t && check_time_t <= end_time_t) {
                return false;
            }
        }
        return true;
    }

    bool check_course_conflict(const Course& new_course) {
        std::tm new_start_tm = parse_time(new_course.start_time);
        std::tm new_end_tm = parse_time(new_course.end_time);
        time_t new_start_time_t = mktime(&new_start_tm);
        time_t new_end_time_t = mktime(&new_end_tm);

        for (const auto& course : courses) {
            std::tm start_tm = parse_time(course.start_time);
            std::tm end_tm = parse_time(course.end_time);
            time_t start_time_t = mktime(&start_tm);
            time_t end_time_t = mktime(&end_tm);

            if ((start_time_t <= new_start_time_t && end_time_t >= new_start_time_t) ||
                (start_time_t <= new_end_time_t && end_time_t >= new_end_time_t)) {
                return false;
            }
        }
        return true;
    }
};
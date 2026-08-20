#include <algorithm>
#include <cctype>
#include <stdexcept>
#include <string>
#include <vector>

// Mirrors the Python course dict with keys 'name', 'start_time' and 'end_time'.
// Two courses are equal when all three fields are equal (dict equality).
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

namespace {

// Equivalent of datetime.strptime(time_str, "%H:%M"), expressed as minutes
// since midnight. Throws std::invalid_argument (the C++ analogue of Python's
// ValueError) when the string does not match the '%H:%M' format.
int parse_time_to_minutes(const std::string& time_str) {
    const std::string mismatch =
        "time data '" + time_str + "' does not match format '%H:%M'";

    std::size_t i = 0;

    // %H: one or two digits, hour in [0, 23].
    if (i >= time_str.size() ||
        !std::isdigit(static_cast<unsigned char>(time_str[i])))
        throw std::invalid_argument(mismatch);
    int hour = time_str[i++] - '0';
    if (i < time_str.size() &&
        std::isdigit(static_cast<unsigned char>(time_str[i])))
        hour = hour * 10 + (time_str[i++] - '0');
    if (hour > 23)
        throw std::invalid_argument(mismatch);

    // Literal ':'.
    if (i >= time_str.size() || time_str[i] != ':')
        throw std::invalid_argument(mismatch);
    ++i;

    // %M: one or two digits, minute in [0, 59].
    if (i >= time_str.size() ||
        !std::isdigit(static_cast<unsigned char>(time_str[i])))
        throw std::invalid_argument(mismatch);
    int minute = time_str[i++] - '0';
    if (i < time_str.size() &&
        std::isdigit(static_cast<unsigned char>(time_str[i])))
        minute = minute * 10 + (time_str[i++] - '0');
    if (minute > 59)
        throw std::invalid_argument(mismatch);

    // Python's strptime rejects any trailing characters.
    if (i != time_str.size())
        throw std::invalid_argument("unconverted data remains: " +
                                    time_str.substr(i));

    return hour * 60 + minute;
}

}  // namespace

// This is a class representing a classroom, capable of adding and removing
// courses, checking availability at a given time, and detecting conflicts
// when scheduling new courses.
class Classroom {
public:
    int id;
    std::vector<Course> courses;

    // Initialize the classroom management system.
    // :param id: int, the id of classroom
    explicit Classroom(int id) : id(id) {}

    // Add course to courses list if the course wasn't in it.
    void add_course(const Course& course) {
        if (std::find(courses.begin(), courses.end(), course) == courses.end()) {
            courses.push_back(course);
        }
    }

    // Remove course from courses list if the course was in it
    // (removes only the first matching occurrence, like Python's list.remove).
    void remove_course(const Course& course) {
        auto it = std::find(courses.begin(), courses.end(), course);
        if (it != courses.end()) {
            courses.erase(it);
        }
    }

    // Change the time format as '%H:%M' and check the time is free or not
    // in the classroom.
    // :param check_time: str, the time need to be checked
    // :return: true if the check_time does not conflict with every course
    //          time, or false otherwise.
    bool is_free_at(const std::string& check_time) const {
        int check = parse_time_to_minutes(check_time);

        for (const Course& course : courses) {
            int start = parse_time_to_minutes(course.start_time);
            int end = parse_time_to_minutes(course.end_time);
            if (start <= check && check <= end) {
                return false;
            }
        }
        return true;
    }

    // Before adding a new course, check if the new course time conflicts
    // with any other course.
    // :param new_course: course information with 'start_time', 'end_time'
    //                    and 'name'
    // :return: false if the new course time conflicts (including two courses
    //          having the same boundary time) with other courses, or true
    //          otherwise.
    bool check_course_conflict(const Course& new_course) const {
        int new_start = parse_time_to_minutes(new_course.start_time);
        int new_end = parse_time_to_minutes(new_course.end_time);

        bool flag = true;
        for (const Course& course : courses) {
            int start = parse_time_to_minutes(course.start_time);
            int end = parse_time_to_minutes(course.end_time);
            if (start <= new_start && end >= new_start) {
                flag = false;
            }
            if (start <= new_end && end >= new_end) {
                flag = false;
            }
        }
        return flag;
    }
};
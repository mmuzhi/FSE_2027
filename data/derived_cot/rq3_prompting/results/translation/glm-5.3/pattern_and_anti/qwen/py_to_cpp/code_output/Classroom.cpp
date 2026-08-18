#include <cctype>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

class Classroom {
public:
    int id;
    std::vector<std::map<std::string, std::string>> courses;

    // Initialize the classroom management system.
    // :param id: int, the id of classroom
    Classroom(int id) : id(id), courses() {}

    // Add course to courses list if the course wasn't in it.
    // :param course: dict-like map, information of the course, including 'start_time', 'end_time' and 'name'
    void add_course(const std::map<std::string, std::string>& course) {
        for (const auto& existing : courses) {
            if (existing == course) {
                return;
            }
        }
        courses.push_back(course);
    }

    // Remove course from courses list if the course was in it (first occurrence).
    // :param course: dict-like map, information of the course, including 'start_time', 'end_time' and 'name'
    void remove_course(const std::map<std::string, std::string>& course) {
        for (auto it = courses.begin(); it != courses.end(); ++it) {
            if (*it == course) {
                courses.erase(it);
                return;
            }
        }
    }

    // Check the time is free or not in the classroom.
    // :param check_time: str, the time need to be checked ('%H:%M')
    // :return: true if check_time does not conflict with every course time, false otherwise.
    bool is_free_at(const std::string& check_time) {
        int check = parse_time(check_time);

        for (const auto& course : courses) {
            if (parse_time(course.at("start_time")) <= check &&
                check <= parse_time(course.at("end_time"))) {
                return false;
            }
        }
        return true;
    }

    // Before adding a new course, check if the new course time conflicts with any other course.
    // :param new_course: dict-like map, information of the course, including 'start_time', 'end_time' and 'name'
    // :return: false if the new course time conflicts (including same boundary time) with other courses, true otherwise.
    bool check_course_conflict(const std::map<std::string, std::string>& new_course) {
        int new_start_time = parse_time(new_course.at("start_time"));
        int new_end_time = parse_time(new_course.at("end_time"));

        bool flag = true;
        for (const auto& course : courses) {
            int start_time = parse_time(course.at("start_time"));
            int end_time = parse_time(course.at("end_time"));
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
    // Parse a '%H:%M' time string into minutes since midnight.
    // Mirrors datetime.strptime(s, '%H:%M'): throws on malformed input or out-of-range values.
    static int parse_time(const std::string& s) {
        std::size_t colon = s.find(':');
        if (colon == std::string::npos || colon == 0 || colon > 2) {
            throw std::invalid_argument("time data '" + s + "' does not match format '%H:%M'");
        }
        std::string hh = s.substr(0, colon);
        std::string mm = s.substr(colon + 1);
        if (mm.empty() || mm.size() > 2) {
            throw std::invalid_argument("time data '" + s + "' does not match format '%H:%M'");
        }
        for (char c : hh) {
            if (std::isdigit(static_cast<unsigned char>(c)) == 0) {
                throw std::invalid_argument("time data '" + s + "' does not match format '%H:%M'");
            }
        }
        for (char c : mm) {
            if (std::isdigit(static_cast<unsigned char>(c)) == 0) {
                throw std::invalid_argument("time data '" + s + "' does not match format '%H:%M'");
            }
        }
        int h = std::stoi(hh);
        int m = std::stoi(mm);
        if (h > 23 || m > 59) {
            throw std::invalid_argument(
                "unconverted data remains: " + s);
        }
        return h * 60 + m;
    }
};
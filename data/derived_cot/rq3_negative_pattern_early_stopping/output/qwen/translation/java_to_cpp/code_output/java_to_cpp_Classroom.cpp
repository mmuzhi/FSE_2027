#include <vector>
#include <string>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <ctime>

class LocalTime {
private:
    int hour;
    int minute;
    int second;
    int nanosecond;

public:
    LocalTime() : hour(0), minute(0), second(0), nanosecond(0) {}

    LocalTime(int h, int m, int s, int ns) : hour(h), minute(m), second(s), nanosecond(ns) {}

    static LocalTime parse(const std::string& s) {
        LocalTime time;
        char colon1, colon2, dot;
        int h, m, s, ns;
        std::istringstream iss(s);
        if (s.find('.') != std::string::npos) {
            iss >> h >> colon1 >> m >> colon2 >> s >> dot >> ns;
        } else {
            iss >> h >> colon1 >> m >> colon2 >> s;
        }
        time = LocalTime(h, m, s, ns);
        return time;
    }

    bool isBefore(const LocalTime& other) const {
        if (hour < other.hour) return true;
        if (hour > other.hour) return false;
        if (minute < other.minute) return true;
        if (minute > other.minute) return false;
        if (second < other.second) return true;
        if (second > other.second) return false;
        return nanosecond < other.nanosecond;
    }

    bool isAfter(const LocalTime& other) const {
        if (hour > other.hour) return true;
        if (hour < other.hour) return false;
        if (minute > other.minute) return true;
        if (minute < other.minute) return false;
        if (second > other.second) return true;
        if (second < other.second) return false;
        return nanosecond > other.nanosecond;
    }
};

class Course {
public:
    LocalTime startTime;
    LocalTime endTime;
};

class Classroom {
private:
    int id;
    std::vector<Course> courses;

public:
    Classroom(int id) : id(id) {}

    void addCourse(const Course& course) {
        bool courseExists = false;
        for (const auto& existingCourse : courses) {
            if (existingCourse.startTime == course.startTime && existingCourse.endTime == course.endTime) {
                courseExists = true;
                break;
            }
        }
        if (!courseExists) {
            courses.push_back(course);
        }
    }

    void removeCourse(const Course& course) {
        courses.erase(std::remove(courses.begin(), courses.end(), course), courses.end());
    }

    bool isFreeAt(const std::string& checkTime) {
        LocalTime currentTime = LocalTime::parse(checkTime);
        for (const auto& course : courses) {
            if (!currentTime.isBefore(course.startTime) && !currentTime.isAfter(course.endTime)) {
                return false;
            }
        }
        return true;
    }

    bool checkCourseConflict(const Course& newCourse) {
        LocalTime newStartTime = newCourse.startTime;
        LocalTime newEndTime = newCourse.endTime;

        for (const auto& course : courses) {
            if (!(newEndTime.isBefore(course.startTime) || newStartTime.isAfter(course.endTime))) {
                return false;
            }
        }
        return true;
    }
};
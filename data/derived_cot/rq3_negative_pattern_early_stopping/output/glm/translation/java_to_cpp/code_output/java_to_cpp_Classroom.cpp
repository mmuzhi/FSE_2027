#ifndef CLASSROOM_H
#define CLASSROOM_H

#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>

struct LocalTime {
    int secondsSinceMidnight;

    static LocalTime parse(const std::string& timeStr) {
        int hours = 0, minutes = 0, seconds = 0;
        size_t pos = 0;

        size_t colonPos = timeStr.find(':');
        if (colonPos == std::string::npos) {
            throw std::invalid_argument("Invalid time format: " + timeStr);
        }
        hours = std::stoi(timeStr.substr(pos, colonPos - pos));
        pos = colonPos + 1;

        colonPos = timeStr.find(':', pos);
        if (colonPos == std::string::npos) {
            minutes = std::stoi(timeStr.substr(pos));
        } else {
            minutes = std::stoi(timeStr.substr(pos, colonPos - pos));
            pos = colonPos + 1;
            seconds = std::stoi(timeStr.substr(pos));
        }

        return LocalTime{hours * 3600 + minutes * 60 + seconds};
    }

    bool isBefore(const LocalTime& other) const {
        return secondsSinceMidnight < other.secondsSinceMidnight;
    }

    bool isAfter(const LocalTime& other) const {
        return secondsSinceMidnight > other.secondsSinceMidnight;
    }
};

struct Course {
    LocalTime startTime;
    LocalTime endTime;

    bool operator==(const Course& other) const {
        return startTime.secondsSinceMidnight == other.startTime.secondsSinceMidnight &&
               endTime.secondsSinceMidnight == other.endTime.secondsSinceMidnight;
    }
};

class Classroom {
private:
    int id;
    std::vector<Course> courses;

public:
    Classroom(int id) : id(id), courses() {}

    void addCourse(const Course& course) {
        if (std::find(courses.begin(), courses.end(), course) == courses.end()) {
            courses.push_back(course);
        }
    }

    void removeCourse(const Course& course) {
        auto it = std::find(courses.begin(), courses.end(), course);
        if (it != courses.end()) {
            courses.erase(it);
        }
    }

    bool isFreeAt(const std::string& checkTime) {
        LocalTime time = LocalTime::parse(checkTime);
        for (const Course& course : courses) {
            if (!time.isBefore(course.startTime) && !time.isAfter(course.endTime)) {
                return false;
            }
        }
        return true;
    }

    bool checkCourseConflict(const Course& newCourse) {
        LocalTime newStartTime = newCourse.startTime;
        LocalTime newEndTime = newCourse.endTime;

        for (const Course& course : courses) {
            if (!(newEndTime.isBefore(course.startTime) || newStartTime.isAfter(course.endTime))) {
                return false;
            }
        }
        return true;
    }
};

#endif
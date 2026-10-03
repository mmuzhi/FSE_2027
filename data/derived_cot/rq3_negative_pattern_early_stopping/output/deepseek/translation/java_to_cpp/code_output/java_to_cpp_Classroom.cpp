#include <vector>
#include <string>
#include <algorithm>
#include <sstream>
#include <stdexcept>
#include <iostream> // only for potential debugging, not required

// Forward declaration of Course, assumed to have startMinutes and endMinutes.
// In the original Java code, Course is defined inside ClassroomManagementTest.
// For this translation, we define it here with the necessary interface.
struct Course {
    int startMinutes; // minutes from midnight
    int endMinutes;   // minutes from midnight

    bool operator==(const Course& other) const {
        return startMinutes == other.startMinutes && endMinutes == other.endMinutes;
    }
};

// Helper function to convert time string "HH:MM" to minutes since midnight.
// This mimics Java's LocalTime.parse with the same default format.
int parseTimeToMinutes(const std::string& timeStr) {
    std::istringstream iss(timeStr);
    int hours, minutes;
    char colon;
    if (!(iss >> hours >> colon >> minutes) || colon != ':' ||
        hours < 0 || hours > 23 || minutes < 0 || minutes > 59) {
        throw std::invalid_argument("Invalid time format: " + timeStr);
    }
    return hours * 60 + minutes;
}

class Classroom {
private:
    int id;
    std::vector<Course> courses;

public:
    Classroom(int id) : id(id) {}

    void addCourse(const Course& course) {
        // Java behavior: only add if not already present (using equals -> operator==)
        if (std::find(courses.begin(), courses.end(), course) == courses.end()) {
            courses.push_back(course);
        }
    }

    void removeCourse(const Course& course) {
        // Java behavior: removes the first occurrence that equals the given course.
        // If not found, std::remove? Actually, List.remove returns true/false,
        // but we keep the same effect: do nothing if not present.
        auto it = std::find(courses.begin(), courses.end(), course);
        if (it != courses.end()) {
            courses.erase(it);
        }
    }

    bool isFreeAt(const std::string& checkTime) const {
        int checkMinutes = parseTimeToMinutes(checkTime);
        for (const auto& course : courses) {
            // Java: !time.isBefore(start) && !time.isAfter(end) → time >= start && time <= end
            if (checkMinutes >= course.startMinutes && checkMinutes <= course.endMinutes) {
                return false;
            }
        }
        return true;
    }

    bool checkCourseConflict(const Course& newCourse) const {
        int newStart = newCourse.startMinutes;
        int newEnd = newCourse.endMinutes;
        for (const auto& course : courses) {
            // Java: !(newEnd.isBefore(course.start) || newStart.isAfter(course.end))
            //     → not (end < start_other OR start > end_other)
            //     → intervals overlap if !(end < start_other || start > end_other)
            if (!(newEnd < course.startMinutes || newStart > course.endMinutes)) {
                return false; // conflict found
            }
        }
        return true; // no conflict
    }
};

// Example usage (not part of the original code, just for illustration)
// int main() {
//     Classroom room(101);
//     Course c1 = { 9*60, 10*60 };  // 09:00 - 10:00
//     Course c2 = { 10*60, 11*60 }; // 10:00 - 11:00
//     room.addCourse(c1);
//     room.addCourse(c2);
//     std::cout << std::boolalpha;
//     std::cout << "Free at 10:30? " << room.isFreeAt("10:30") << std::endl; // false
//     std::cout << "Free at 08:00? " << room.isFreeAt("08:00") << std::endl; // true
//     Course c3 = { 10*60, 11*60 };
//     std::cout << "Conflict with 10:00-11:00? " << room.checkCourseConflict(c3) << std::endl; // false (conflict)
//     Course c4 = { 11*60, 12*60 };
//     std::cout << "Conflict with 11:00-12:00? " << room.checkCourseConflict(c4) << std::endl; // true (no conflict)
//     return 0;
// }
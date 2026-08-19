#include <algorithm>
#include <cstddef>
#include <stdexcept>
#include <string>
#include <vector>

namespace org {
namespace example {

// Minimal counterpart of java.time.LocalTime covering the used surface:
// parse (strict ISO-8601 "HH:mm[:ss[.fraction]]", throws on invalid input,
// mirroring DateTimeParseException), isBefore, isAfter, value equality.
class LocalTime {
public:
    int hour = 0;
    int minute = 0;
    int second = 0;
    int nano = 0;

    LocalTime() = default;
    LocalTime(int h, int m, int s, int n = 0)
        : hour(h), minute(m), second(s), nano(n) {}

    static LocalTime parse(const std::string& text) {
        const std::size_t len = text.size();
        auto fail = [&text]() {
            throw std::runtime_error("Text '" + text + "' could not be parsed");
        };
        auto twoDigitsAt = [&](std::size_t i) -> int {
            if (i + 2 > len) fail();
            char a = text[i];
            char b = text[i + 1];
            if (a < '0' || a > '9' || b < '0' || b > '9') fail();
            return (a - '0') * 10 + (b - '0');
        };

        if (len < 5) fail();
        int h = twoDigitsAt(0);
        if (text[2] != ':') fail();
        int m = twoDigitsAt(3);
        int sec = 0;
        int nanos = 0;
        std::size_t idx = 5;
        if (idx < len) {
            if (text[idx] != ':') fail();
            ++idx;
            sec = twoDigitsAt(idx);
            idx += 2;
            if (idx < len) {
                if (text[idx] != '.') fail();
                ++idx;
                std::size_t start = idx;
                while (idx < len && text[idx] >= '0' && text[idx] <= '9') ++idx;
                std::size_t count = idx - start;
                if (count == 0 || count > 9) fail();
                int scale = 1;
                for (std::size_t k = 0; k < 9 - count; ++k) scale *= 10;
                for (std::size_t k = start; k < idx; ++k) {
                    nanos = nanos * 10 + (text[k] - '0');
                }
                nanos *= scale;
            }
        }
        if (h > 23 || m > 59 || sec > 59) fail();
        return LocalTime(h, m, sec, nanos);
    }

    bool isBefore(const LocalTime& other) const { return compare(other) < 0; }
    bool isAfter(const LocalTime& other) const { return compare(other) > 0; }

    bool operator==(const LocalTime& other) const {
        return hour == other.hour && minute == other.minute &&
               second == other.second && nano == other.nano;
    }
    bool operator!=(const LocalTime& other) const { return !(*this == other); }

private:
    int compare(const LocalTime& other) const {
        if (hour != other.hour) return hour < other.hour ? -1 : 1;
        if (minute != other.minute) return minute < other.minute ? -1 : 1;
        if (second != other.second) return second < other.second ? -1 : 1;
        if (nano != other.nano) return nano < other.nano ? -1 : 1;
        return 0;
    }
};

// Counterpart of ClassroomManagementTest.Course
class ClassroomManagementTest {
public:
    struct Course {
        LocalTime startTime;
        LocalTime endTime;

        bool operator==(const Course& other) const {
            return startTime == other.startTime && endTime == other.endTime;
        }
        bool operator!=(const Course& other) const { return !(*this == other); }
    };
};

class Classroom {
private:
    int id;

public:
    // package-private in Java; kept public so same-"package" code can access it
    std::vector<ClassroomManagementTest::Course> courses;

    explicit Classroom(int id_) : id(id_), courses() {}

    void addCourse(const ClassroomManagementTest::Course& course) {
        if (std::find(courses.begin(), courses.end(), course) == courses.end()) {
            courses.push_back(course);
        }
    }

    void removeCourse(const ClassroomManagementTest::Course& course) {
        // removes the first occurrence only, like java.util.List.remove(Object)
        auto it = std::find(courses.begin(), courses.end(), course);
        if (it != courses.end()) {
            courses.erase(it);
        }
    }

    bool isFreeAt(const std::string& checkTime) const {
        LocalTime time = LocalTime::parse(checkTime);
        for (const ClassroomManagementTest::Course& course : courses) {
            if (!time.isBefore(course.startTime) && !time.isAfter(course.endTime)) {
                return false;
            }
        }
        return true;
    }

    bool checkCourseConflict(const ClassroomManagementTest::Course& newCourse) const {
        LocalTime newStartTime = newCourse.startTime;
        LocalTime newEndTime = newCourse.endTime;

        for (const ClassroomManagementTest::Course& course : courses) {
            if (!(newEndTime.isBefore(course.startTime) || newStartTime.isAfter(course.endTime))) {
                return false;
            }
        }
        return true;
    }
};

} // namespace example
} // namespace org
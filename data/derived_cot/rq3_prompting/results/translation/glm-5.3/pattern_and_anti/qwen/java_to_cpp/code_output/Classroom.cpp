#pragma once
#include <algorithm>
#include <cctype>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

namespace org {
namespace example {

// Minimal LocalTime equivalent: stores nanoseconds since start of day.
// Ordering semantics match java.time.LocalTime (isBefore/isAfter).
class LocalTime {
public:
    int64_t nanosOfDay = 0;

    LocalTime() = default;

    LocalTime(int hour, int minute, int second)
        : nanosOfDay(((static_cast<int64_t>(hour) * 60 + minute) * 60 + second) * 1000000000LL) {}

    bool isBefore(const LocalTime& other) const { return nanosOfDay < other.nanosOfDay; }
    bool isAfter(const LocalTime& other) const { return nanosOfDay > other.nanosOfDay; }

    // Mirrors LocalTime.parse(String): ISO-8601 "HH:mm[:ss[.fraction]]";
    // throws std::invalid_argument where Java throws DateTimeParseException.
    static LocalTime parse(const std::string& text) {
        auto fail = [&text]() {
            throw std::invalid_argument("Text '" + text + "' could not be parsed");
        };
        auto digit = [](char c) { return std::isdigit(static_cast<unsigned char>(c)) != 0; };

        if (text.size() < 5) fail();
        std::size_t i = 0;
        auto twoDigits = [&](int maxValue) -> int {
            if (i + 1 >= text.size() || !digit(text[i]) || !digit(text[i + 1])) fail();
            int value = (text[i] - '0') * 10 + (text[i + 1] - '0');
            i += 2;
            if (value > maxValue) fail();
            return value;
        };

        int hour = twoDigits(23);
        if (i >= text.size() || text[i] != ':') fail();
        ++i;
        int minute = twoDigits(59);
        int second = 0;
        int64_t nanoAdjust = 0;
        if (i < text.size()) {
            if (text[i] != ':') fail();
            ++i;
            second = twoDigits(59);
            if (i < text.size()) {
                if (text[i] != '.') fail();
                ++i;
                std::size_t start = i;
                while (i < text.size() && digit(text[i])) ++i;
                if (i == start) fail();
                std::size_t count = std::min<std::size_t>(i - start, 9);
                int64_t frac = 0;
                for (std::size_t k = 0; k < count; ++k) {
                    frac = frac * 10 + (text[start + k] - '0');
                }
                for (std::size_t k = count; k < 9; ++k) frac *= 10;
                nanoAdjust = frac;
                if (i != text.size()) fail();
            }
        }
        if (i != text.size()) fail();

        LocalTime t(hour, minute, second);
        t.nanosOfDay += nanoAdjust;
        return t;
    }
};

// Mirrors the nested ClassroomManagementTest.Course type.
class ClassroomManagementTest {
public:
    struct Course {
        LocalTime startTime;
        LocalTime endTime;
    };
};

class Classroom {
private:
    int id;
    // shared_ptr models Java object references; contains/remove preserve
    // reference-identity semantics (Java default equals).
    std::vector<std::shared_ptr<ClassroomManagementTest::Course>> courses;

public:
    explicit Classroom(int id) : id(id), courses() {}

    void addCourse(const std::shared_ptr<ClassroomManagementTest::Course>& course) {
        if (std::find(courses.begin(), courses.end(), course) == courses.end()) {
            courses.push_back(course);
        }
    }

    void removeCourse(const std::shared_ptr<ClassroomManagementTest::Course>& course) {
        auto it = std::find(courses.begin(), courses.end(), course);
        if (it != courses.end()) {
            courses.erase(it);  // removes first occurrence, like java.util.List.remove
        }
    }

    bool isFreeAt(const std::string& checkTime) {
        LocalTime time = LocalTime::parse(checkTime);
        for (const auto& course : courses) {
            if (!time.isBefore(course->startTime) && !time.isAfter(course->endTime)) {
                return false;
            }
        }
        return true;
    }

    bool checkCourseConflict(const std::shared_ptr<ClassroomManagementTest::Course>& newCourse) {
        LocalTime newStartTime = newCourse->startTime;
        LocalTime newEndTime = newCourse->endTime;

        for (const auto& course : courses) {
            if (!(newEndTime.isBefore(course->startTime) || newStartTime.isAfter(course->endTime))) {
                return false;
            }
        }
        return true;
    }
};

} // namespace example
} // namespace org
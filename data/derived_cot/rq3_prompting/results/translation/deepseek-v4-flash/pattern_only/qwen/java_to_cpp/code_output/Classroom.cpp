#include <string>
#include <vector>
#include <stdexcept>

namespace org {
namespace example {

class LocalTime {
private:
    long long nanosSinceMidnight;
    explicit LocalTime(long long nanos) : nanosSinceMidnight(nanos) {}
public:
    static LocalTime parse(const std::string& s) {
        size_t i = 0;
        auto readDigits = [&](int count) -> int {
            if (i + count > s.size()) {
                throw std::invalid_argument("Text '" + s + "' could not be parsed");
            }
            int val = 0;
            for (int j = 0; j < count; ++j) {
                char c = s[i++];
                if (c < '0' || c > '9') {
                    throw std::invalid_argument("Text '" + s + "' could not be parsed");
                }
                val = val * 10 + (c - '0');
            }
            return val;
        };
        auto expect = [&](char c) {
            if (i >= s.size() || s[i] != c) {
                throw std::invalid_argument("Text '" + s + "' could not be parsed");
            }
            ++i;
        };
        int hour = readDigits(2);
        expect(':');
        int minute = readDigits(2);
        int second = 0;
        long long nanos = 0;
        if (i < s.size() && s[i] == ':') {
            ++i;
            second = readDigits(2);
            if (i < s.size() && s[i] == '.') {
                ++i;
                int fracDigits = 0;
                long long frac = 0;
                while (i < s.size() && s[i] >= '0' && s[i] <= '9') {
                    if (fracDigits < 9) {
                        frac = frac * 10 + (s[i] - '0');
                    } else {
                        throw std::invalid_argument("Text '" + s + "' could not be parsed");
                    }
                    ++fracDigits;
                    ++i;
                }
                if (fracDigits == 0) {
                    throw std::invalid_argument("Text '" + s + "' could not be parsed");
                }
                for (int j = fracDigits; j < 9; ++j) {
                    frac *= 10;
                }
                nanos = frac;
            }
        }
        if (i != s.size()) {
            throw std::invalid_argument("Text '" + s + "' could not be parsed");
        }
        if (hour > 23 || minute > 59 || second > 59) {
            throw std::invalid_argument("Text '" + s + "' could not be parsed");
        }
        long long total = ((long long)hour * 3600 + minute * 60 + second) * 1000000000LL + nanos;
        return LocalTime(total);
    }

    bool isBefore(const LocalTime& other) const {
        return nanosSinceMidnight < other.nanosSinceMidnight;
    }

    bool isAfter(const LocalTime& other) const {
        return nanosSinceMidnight > other.nanosSinceMidnight;
    }
};

class ClassroomManagementTest {
public:
    struct Course {
        LocalTime startTime;
        LocalTime endTime;
        Course(const LocalTime& start, const LocalTime& end) : startTime(start), endTime(end) {}
    };
};

class Classroom {
private:
    int id;
    std::vector<ClassroomManagementTest::Course*> courses;

    bool contains(ClassroomManagementTest::Course* course) const {
        for (auto c : courses) {
            if (c == course) return true;
        }
        return false;
    }

public:
    explicit Classroom(int id) : id(id) {}

    Classroom(const Classroom&) = delete;
    Classroom& operator=(const Classroom&) = delete;

    void addCourse(ClassroomManagementTest::Course* course) {
        if (!contains(course)) {
            courses.push_back(course);
        }
    }

    void removeCourse(ClassroomManagementTest::Course* course) {
        for (auto it = courses.begin(); it != courses.end(); ++it) {
            if (*it == course) {
                courses.erase(it);
                break;
            }
        }
    }

    bool isFreeAt(const std::string& checkTime) const {
        LocalTime time = LocalTime::parse(checkTime);
        for (auto course : courses) {
            if (!time.isBefore(course->startTime) && !time.isAfter(course->endTime)) {
                return false;
            }
        }
        return true;
    }

    bool checkCourseConflict(ClassroomManagementTest::Course* newCourse) const {
        LocalTime newStartTime = newCourse->startTime;
        LocalTime newEndTime = newCourse->endTime;
        for (auto course : courses) {
            if (!(newEndTime.isBefore(course->startTime) || newStartTime.isAfter(course->endTime))) {
                return false;
            }
        }
        return true;
    }
};

} // namespace example
} // namespace org
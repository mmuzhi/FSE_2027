#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <optional>
#include <sstream>
#include <iomanip>
#include <cmath>
#include <functional>

class AssessmentSystem {
public:
    class Student {
    public:
        Student(const std::string& name, int grade, const std::string& major)
            : name(name), grade(grade), major(major) {}

        const std::string& getName() const { return name; }

        void addCourseScore(const std::string& course, int score) {
            courses[course] = score;
        }

        std::optional<double> calculateGPA() const {
            if (courses.empty()) {
                return std::nullopt;
            }
            int totalScore = 0;
            for (const auto& pair : courses) {
                totalScore += pair.second;
            }
            return static_cast<double>(totalScore) / courses.size();
        }

        bool hasFailingCourse() const {
            for (const auto& pair : courses) {
                if (pair.second < 60) {
                    return true;
                }
            }
            return false;
        }

        std::optional<int> getCourseScore(const std::string& course) const {
            auto it = courses.find(course);
            if (it != courses.end()) {
                return it->second;
            }
            return std::nullopt;
        }

        bool operator==(const Student& other) const {
            return name == other.name &&
                   grade == other.grade &&
                   major == other.major &&
                   courses == other.courses;
        }

        bool operator!=(const Student& other) const {
            return !(*this == other);
        }

    private:
        friend struct std::hash<AssessmentSystem::Student>;

        std::string name;
        int grade;
        std::string major;
        std::unordered_map<std::string, int> courses;
    };

    AssessmentSystem() = default;

    void addStudent(const std::string& name, int grade, const std::string& major) {
        students.insert_or_assign(name, Student(name, grade, major));
    }

    void addCourseScore(const std::string& name, const std::string& course, int score) {
        auto it = students.find(name);
        if (it != students.end()) {
            it->second.addCourseScore(course, score);
        }
    }

    std::optional<double> getGPA(const std::string& name) const {
        auto it = students.find(name);
        if (it != students.end()) {
            return it->second.calculateGPA();
        }
        return std::nullopt;
    }

    std::vector<std::string> getAllStudentsWithFailCourse() const {
        std::vector<std::string> failingStudents;
        for (const auto& pair : students) {
            const Student& student = pair.second;
            if (student.hasFailingCourse()) {
                failingStudents.push_back(student.getName());
            }
        }
        return failingStudents;
    }

    std::optional<double> getCourseAverage(const std::string& course) const {
        int totalScore = 0;
        int count = 0;
        for (const auto& pair : students) {
            const Student& student = pair.second;
            auto score = student.getCourseScore(course);
            if (score.has_value()) {
                totalScore += score.value();
                count++;
            }
        }
        if (count > 0) {
            return static_cast<double>(totalScore) / count;
        }
        return std::nullopt;
    }

    std::optional<std::string> getTopStudent() const {
        std::optional<std::string> topStudent = std::nullopt;
        double topGPA = 0.0;
        for (const auto& pair : students) {
            const Student& student = pair.second;
            auto gpa = student.calculateGPA();
            if (gpa.has_value() && gpa.value() > topGPA) {
                topGPA = gpa.value();
                topStudent = student.getName();
            }
        }
        return topStudent;
    }

private:
    std::unordered_map<std::string, Student> students;
};

namespace std {
    template<>
    struct hash<AssessmentSystem::Student> {
        size_t operator()(const AssessmentSystem::Student& s) const noexcept {
            size_t h1 = std::hash<std::string>{}(s.name);
            size_t h2 = std::hash<int>{}(s.grade);
            size_t h3 = std::hash<std::string>{}(s.major);
            size_t h4 = 0;
            for (const auto& pair : s.courses) {
                h4 ^= std::hash<std::string>{}(pair.first) ^ (std::hash<int>{}(pair.second) << 1);
            }
            size_t h = h1;
            h = h * 31 + h2;
            h = h * 31 + h3;
            h = h * 31 + h4;
            return h;
        }
    };
}

static std::string formatDouble(double d) {
    std::ostringstream oss;
    if (d == std::floor(d)) {
        oss << std::fixed << std::setprecision(1) << d;
    } else {
        oss << std::setprecision(16) << d;
    }
    return oss.str();
}

static void printStringList(const std::vector<std::string>& v) {
    std::cout << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << v[i];
    }
    std::cout << "]" << std::endl;
}

int main() {
    AssessmentSystem system;
    system.addStudent("student 1", 3, "SE");
    system.addStudent("student 2", 2, "SE");
    system.addCourseScore("student 1", "course 1", 86);
    system.addCourseScore("student 2", "course 1", 59);
    system.addCourseScore("student 1", "course 2", 78);
    system.addCourseScore("student 2", "course 2", 90);

    printStringList(system.getAllStudentsWithFailCourse());

    auto avg1 = system.getCourseAverage("course 1");
    if (avg1.has_value()) {
        std::cout << formatDouble(avg1.value()) << std::endl;
    } else {
        std::cout << "null" << std::endl;
    }

    auto avg2 = system.getCourseAverage("course 2");
    if (avg2.has_value()) {
        std::cout << formatDouble(avg2.value()) << std::endl;
    } else {
        std::cout << "null" << std::endl;
    }

    auto gpa1 = system.getGPA("student 1");
    if (gpa1.has_value()) {
        std::cout << formatDouble(gpa1.value()) << std::endl;
    } else {
        std::cout << "null" << std::endl;
    }

    auto gpa2 = system.getGPA("student 2");
    if (gpa2.has_value()) {
        std::cout << formatDouble(gpa2.value()) << std::endl;
    } else {
        std::cout << "null" << std::endl;
    }

    auto top = system.getTopStudent();
    if (top.has_value()) {
        std::cout << top.value() << std::endl;
    } else {
        std::cout << "null" << std::endl;
    }

    return 0;
}
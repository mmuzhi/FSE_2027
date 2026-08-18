#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

// Mimics Java's Double.toString for the values produced by this program
// (shortest round-trip representation, always with a fractional part).
static std::string javaDoubleToString(double d) {
    if (std::isnan(d)) return "NaN";
    if (std::isinf(d)) return d > 0 ? "Infinity" : "-Infinity";
    char buf[64];
    for (int prec = 1; prec <= 17; ++prec) {
        std::snprintf(buf, sizeof buf, "%.*g", prec, d);
        if (std::strtod(buf, nullptr) == d) break;
    }
    std::string s(buf);
    if (s.find('.') == std::string::npos && s.find('e') == std::string::npos)
        s += ".0";
    return s;
}

// Mimics Java's List.toString
static std::string javaListToString(const std::vector<std::string>& v) {
    std::string s = "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i > 0) s += ", ";
        s += v[i];
    }
    return s + "]";
}

// Mimics Java's println on nullable Double / nullable String
static std::string javaToString(const std::optional<double>& d) {
    return d.has_value() ? javaDoubleToString(*d) : "null";
}
static std::string javaToString(const std::optional<std::string>& s) {
    return s.has_value() ? *s : "null";
}

class AssessmentSystem {
public:
    struct Student {
    private:
        std::string name;
        int grade;
        std::string major;
        std::unordered_map<std::string, int> courses;

    public:
        Student(std::string name, int grade, std::string major)
            : name(std::move(name)), grade(grade), major(std::move(major)) {}

        const std::string& getName() const { return name; }

        void addCourseScore(const std::string& course, int score) {
            courses.insert_or_assign(course, score);
        }

        std::optional<double> calculateGPA() const {
            if (courses.empty()) {
                return std::nullopt;
            }
            int totalScore = 0;
            for (const auto& kv : courses) {
                totalScore += kv.second;
            }
            return static_cast<double>(totalScore) / courses.size();
        }

        bool hasFailingCourse() const {
            for (const auto& kv : courses) {
                if (kv.second < 60) {
                    return true;
                }
            }
            return false;
        }

        std::optional<int> getCourseScore(const std::string& course) const {
            auto it = courses.find(course);
            if (it == courses.end()) {
                return std::nullopt;
            }
            return it->second;
        }
    };

private:
    std::unordered_map<std::string, Student> students;

public:
    void addStudent(const std::string& name, int grade, const std::string& major) {
        students.insert_or_assign(name, Student(name, grade, major));
    }

    void addCourseScore(const std::string& name, const std::string& course, int score) {
        auto it = students.find(name);
        if (it != students.end()) {
            it->second.addCourseScore(course, score);
        }
    }

    std::optional<double> getGPA(const std::string& name) {
        auto it = students.find(name);
        if (it != students.end()) {
            return it->second.calculateGPA();
        }
        return std::nullopt;
    }

    std::vector<std::string> getAllStudentsWithFailCourse() {
        std::vector<std::string> failingStudents;
        for (const auto& kv : students) {
            if (kv.second.hasFailingCourse()) {
                failingStudents.push_back(kv.second.getName());
            }
        }
        return failingStudents;
    }

    std::optional<double> getCourseAverage(const std::string& course) {
        int totalScore = 0;
        int count = 0;
        for (const auto& kv : students) {
            std::optional<int> score = kv.second.getCourseScore(course);
            if (score.has_value()) {
                totalScore += *score;
                count++;
            }
        }
        if (count > 0) {
            return static_cast<double>(totalScore) / count;
        }
        return std::nullopt;
    }

    std::optional<std::string> getTopStudent() {
        std::optional<std::string> topStudent;
        double topGPA = 0;
        for (const auto& kv : students) {
            std::optional<double> gpa = kv.second.calculateGPA();
            if (gpa.has_value() && *gpa > topGPA) {
                topGPA = *gpa;
                topStudent = kv.second.getName();
            }
        }
        return topStudent;
    }
};

int main() {
    AssessmentSystem system;
    system.addStudent("student 1", 3, "SE");
    system.addStudent("student 2", 2, "SE");
    system.addCourseScore("student 1", "course 1", 86);
    system.addCourseScore("student 2", "course 1", 59);
    system.addCourseScore("student 1", "course 2", 78);
    system.addCourseScore("student 2", "course 2", 90);

    std::cout << javaListToString(system.getAllStudentsWithFailCourse()) << std::endl;
    std::cout << javaToString(system.getCourseAverage("course 1")) << std::endl;
    std::cout << javaToString(system.getCourseAverage("course 2")) << std::endl;
    std::cout << javaToString(system.getGPA("student 1")) << std::endl;
    std::cout << javaToString(system.getGPA("student 2")) << std::endl;
    std::cout << javaToString(system.getTopStudent()) << std::endl;
    return 0;
}
// Translation of the Java AssessmentSystem program.
// Requires C++17 (std::optional, unordered_map::insert_or_assign).
// Nullable Java references (Double/String/Integer) are modeled with std::optional;
// Java's println output ("null", "[a, b]", "84.0") is reproduced exactly.

#include <cmath>
#include <cstddef>
#include <iostream>
#include <optional>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace org {
namespace example {

class AssessmentSystem {
public:
    // Equivalent of the Java static nested class Student.
    class Student {
    public:
        Student(std::string name, int grade, std::string major)
            : name(std::move(name)), grade(grade), major(std::move(major)) {}

        const std::string& getName() const {
            return name;
        }

        void addCourseScore(const std::string& course, int score) {
            courses.insert_or_assign(course, score); // Map.put semantics
        }

        std::optional<double> calculateGPA() const {
            if (courses.empty()) {
                return std::nullopt; // Java: null
            }
            int totalScore = 0;
            for (const auto& entry : courses) {
                totalScore += entry.second;
            }
            return static_cast<double>(totalScore) / courses.size();
        }

        bool hasFailingCourse() const {
            for (const auto& entry : courses) {
                if (entry.second < 60) {
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
            return std::nullopt; // Java: null when absent
        }

        bool operator==(const Student& other) const {
            return grade == other.grade && name == other.name &&
                   major == other.major && courses == other.courses;
        }
        // Java's hashCode() is not needed here: no code path hashes a Student.

    private:
        std::string name;
        int grade;
        std::string major;
        std::unordered_map<std::string, int> courses;
    };

    AssessmentSystem() = default;

    void addStudent(const std::string& name, int grade, const std::string& major) {
        students.insert_or_assign(name, Student(name, grade, major)); // Map.put
    }

    void addCourseScore(const std::string& name, const std::string& course, int score) {
        auto it = students.find(name);
        if (it != students.end()) { // containsKey
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
        for (const auto& entry : students) {
            if (entry.second.hasFailingCourse()) {
                failingStudents.push_back(entry.second.getName());
            }
        }
        return failingStudents;
    }

    std::optional<double> getCourseAverage(const std::string& course) const {
        int totalScore = 0;
        int count = 0;
        for (const auto& entry : students) {
            std::optional<int> score = entry.second.getCourseScore(course);
            if (score.has_value()) { // score != null
                totalScore += *score;
                ++count;
            }
        }
        if (count > 0) {
            return static_cast<double>(totalScore) / count;
        }
        return std::nullopt;
    }

    std::optional<std::string> getTopStudent() const {
        std::optional<std::string> topStudent; // Java: null
        double topGPA = 0;
        for (const auto& entry : students) {
            std::optional<double> gpa = entry.second.calculateGPA();
            if (gpa.has_value() && *gpa > topGPA) { // gpa != null && gpa > topGPA
                topGPA = *gpa;
                topStudent = entry.second.getName();
            }
        }
        return topStudent;
    }

private:
    std::unordered_map<std::string, Student> students;
};

} // namespace example
} // namespace org

// Formatting helpers that reproduce the exact textual output of
// System.out.println for the values printed by this program.
namespace {

// Java's Double.toString keeps at least one digit after the decimal point ("84.0").
std::string javaToString(double value) {
    if (std::isnan(value)) return "NaN";
    if (std::isinf(value)) return value > 0 ? "Infinity" : "-Infinity";
    std::ostringstream oss;
    oss << value;
    std::string result = oss.str();
    if (result.find('.') == std::string::npos &&
        result.find('e') == std::string::npos &&
        result.find('E') == std::string::npos) {
        result += ".0";
    }
    return result;
}

std::string javaToString(const std::string& value) {
    return value;
}

// Java's AbstractCollection.toString(): "[element1, element2]" or "[]".
std::string javaToString(const std::vector<std::string>& list) {
    std::string result = "[";
    for (std::size_t i = 0; i < list.size(); ++i) {
        if (i > 0) result += ", ";
        result += list[i];
    }
    result += "]";
    return result;
}

// Java prints the string "null" for null references.
template <typename T>
std::string javaToString(const std::optional<T>& value) {
    return value.has_value() ? javaToString(*value) : std::string("null");
}

} // namespace

int main() {
    org::example::AssessmentSystem system;
    system.addStudent("student 1", 3, "SE");
    system.addStudent("student 2", 2, "SE");
    system.addCourseScore("student 1", "course 1", 86);
    system.addCourseScore("student 2", "course 1", 59);
    system.addCourseScore("student 1", "course 2", 78);
    system.addCourseScore("student 2", "course 2", 90);

    std::cout << javaToString(system.getAllStudentsWithFailCourse()) << "\n";
    std::cout << javaToString(system.getCourseAverage("course 1")) << "\n";
    std::cout << javaToString(system.getCourseAverage("course 2")) << "\n";
    std::cout << javaToString(system.getGPA("student 1")) << "\n";
    std::cout << javaToString(system.getGPA("student 2")) << "\n";
    std::cout << javaToString(system.getTopStudent()) << "\n";
    return 0;
}
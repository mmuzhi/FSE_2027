#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <optional>
#include <utility>

namespace org::example {

class AssessmentSystem {
public:
    class Student {
    public:
        Student(std::string name, int grade, std::string major)
            : name_(std::move(name)), grade_(grade), major_(std::move(major)) {}

        std::string getName() const { return name_; }

        void addCourseScore(const std::string& course, int score) {
            courses_[course] = score;
        }

        std::optional<double> calculateGPA() const {
            if (courses_.empty()) {
                return std::nullopt;
            }
            int totalScore = 0;
            for (const auto& kv : courses_) {
                totalScore += kv.second;
            }
            return static_cast<double>(totalScore) / static_cast<double>(courses_.size());
        }

        bool hasFailingCourse() const {
            for (const auto& kv : courses_) {
                if (kv.second < 60) {
                    return true;
                }
            }
            return false;
        }

        std::optional<int> getCourseScore(const std::string& course) const {
            auto it = courses_.find(course);
            if (it != courses_.end()) {
                return it->second;
            }
            return std::nullopt;
        }

        bool operator==(const Student& other) const {
            return grade_ == other.grade_ &&
                   name_ == other.name_ &&
                   major_ == other.major_ &&
                   courses_ == other.courses_;
        }

        bool operator!=(const Student& other) const {
            return !(*this == other);
        }

    private:
        std::string name_;
        int grade_;
        std::string major_;
        std::unordered_map<std::string, int> courses_;
    };

    AssessmentSystem() = default;

    void addStudent(const std::string& name, int grade, const std::string& major) {
        students_.insert_or_assign(name, Student(name, grade, major));
    }

    void addCourseScore(const std::string& name, const std::string& course, int score) {
        auto it = students_.find(name);
        if (it != students_.end()) {
            it->second.addCourseScore(course, score);
        }
    }

    std::optional<double> getGPA(const std::string& name) const {
        auto it = students_.find(name);
        if (it != students_.end()) {
            return it->second.calculateGPA();
        }
        return std::nullopt;
    }

    std::vector<std::string> getAllStudentsWithFailCourse() const {
        std::vector<std::string> failingStudents;
        for (const auto& kv : students_) {
            if (kv.second.hasFailingCourse()) {
                failingStudents.push_back(kv.second.getName());
            }
        }
        return failingStudents;
    }

    std::optional<double> getCourseAverage(const std::string& course) const {
        int totalScore = 0;
        int count = 0;
        for (const auto& kv : students_) {
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

    std::optional<std::string> getTopStudent() const {
        std::optional<std::string> topStudent;
        double topGPA = 0;
        for (const auto& kv : students_) {
            std::optional<double> gpa = kv.second.calculateGPA();
            if (gpa.has_value() && *gpa > topGPA) {
                topGPA = *gpa;
                topStudent = kv.second.getName();
            }
        }
        return topStudent;
    }

private:
    std::unordered_map<std::string, Student> students_;
};

} // namespace org::example

namespace {

// Mimics Java's Double.toString: integral doubles print with a trailing ".0".
std::string javaDoubleToString(double d) {
    std::ostringstream oss;
    oss << d;
    std::string s = oss.str();
    if (s.find_first_of(".eE") == std::string::npos &&
        s.find("inf") == std::string::npos &&
        s.find("nan") == std::string::npos) {
        s += ".0";
    }
    return s;
}

// Mimics Java's List.toString: "[a, b, c]"
std::string javaListToString(const std::vector<std::string>& list) {
    std::ostringstream oss;
    oss << "[";
    for (std::size_t i = 0; i < list.size(); ++i) {
        if (i > 0) oss << ", ";
        oss << list[i];
    }
    oss << "]";
    return oss.str();
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

    std::cout << javaListToString(system.getAllStudentsWithFailCourse()) << "\n";

    std::optional<double> avg1 = system.getCourseAverage("course 1");
    std::cout << (avg1.has_value() ? javaDoubleToString(*avg1) : std::string("null")) << "\n";

    std::optional<double> avg2 = system.getCourseAverage("course 2");
    std::cout << (avg2.has_value() ? javaDoubleToString(*avg2) : std::string("null")) << "\n";

    std::optional<double> gpa1 = system.getGPA("student 1");
    std::cout << (gpa1.has_value() ? javaDoubleToString(*gpa1) : std::string("null")) << "\n";

    std::optional<double> gpa2 = system.getGPA("student 2");
    std::cout << (gpa2.has_value() ? javaDoubleToString(*gpa2) : std::string("null")) << "\n";

    std::optional<std::string> top = system.getTopStudent();
    std::cout << (top.has_value() ? *top : std::string("null")) << "\n";

    return 0;
}
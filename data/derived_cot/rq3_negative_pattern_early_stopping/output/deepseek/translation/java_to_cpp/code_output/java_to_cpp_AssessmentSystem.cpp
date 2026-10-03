cpp
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <optional>
#include <algorithm>

class AssessmentSystem {
private:
    struct Student {
        std::string name;
        int grade;
        std::string major;
        std::unordered_map<std::string, int> courses;

        Student(const std::string& name, int grade, const std::string& major)
            : name(name), grade(grade), major(major) {}

        void addCourseScore(const std::string& course, int score) {
            courses[course] = score;
        }

        std::optional<double> calculateGPA() const {
            if (courses.empty()) return std::nullopt;
            int total = 0;
            for (const auto& [course, score] : courses) {
                total += score;
            }
            return static_cast<double>(total) / courses.size();
        }

        bool hasFailingCourse() const {
            for (const auto& [course, score] : courses) {
                if (score < 60) return true;
            }
            return false;
        }

        std::optional<int> getCourseScore(const std::string& course) const {
            auto it = courses.find(course);
            if (it != courses.end()) return it->second;
            return std::nullopt;
        }

        bool operator==(const Student& other) const {
            return name == other.name && grade == other.grade && major == other.major && courses == other.courses;
        }
    };

    std::unordered_map<std::string, Student> students;

public:
    AssessmentSystem() = default;

    void addStudent(const std::string& name, int grade, const std::string& major) {
        students.emplace(name, Student(name, grade, major));
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
        std::vector<std::string> failing;
        for (const auto& [name, student] : students) {
            if (student.hasFailingCourse()) {
                failing.push_back(student.name);
            }
        }
        return failing;
    }

    std::optional<double> getCourseAverage(const std::string& course) const {
        int total = 0;
        int count = 0;
        for (const auto& [name, student] : students) {
            auto score = student.getCourseScore(course);
            if (score.has_value()) {
                total += score.value();
                ++count;
            }
        }
        if (count > 0) return static_cast<double>(total) / count;
        return std::nullopt;
    }

    // Returns empty string if no top student (like Java's null)
    std::string getTopStudent() const {
        std::string topStudent;
        double topGPA = 0.0;
        for (const auto& [name, student] : students) {
            auto gpa = student.calculateGPA();
            if (gpa.has_value() && gpa.value() > topGPA) {
                topGPA = gpa.value();
                topStudent = student.name;
            }
        }
        return topStudent;
    }
};

// Helper to print optional<double>
void printOptional(std::optional<double> val) {
    if (val.has_value()) {
        std::cout << val.value();
    } else {
        std::cout << "null";
    }
}

// Helper to print vector<string> like Java's list toString: [a, b]
void printVector(const std::vector<std::string>& vec) {
    std::cout << "[";
    for (size_t i = 0; i < vec.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << vec[i];
    }
    std::cout << "]";
}

int main() {
    AssessmentSystem system;
    system.addStudent("student 1", 3, "SE");
    system.addStudent("student 2", 2, "SE");
    system.addCourseScore("student 1", "course 1", 86);
    system.addCourseScore("student 2", "course 1", 59);
    system.addCourseScore("student 1", "course 2", 78);
    system.addCourseScore("student 2", "course 2", 90);

    printVector(system.getAllStudentsWithFailCourse());
    std::cout << std::endl;

    printOptional(system.getCourseAverage("course 1"));
    std::cout << std::endl;

    printOptional(system.getCourseAverage("course 2"));
    std::cout << std::endl;

    printOptional(system.getGPA("student 1"));
    std::cout << std::endl;

    printOptional(system.getGPA("student 2"));
    std::cout << std::endl;

    std::string top = system.getTopStudent();
    if (top.empty()) {
        std::cout << "null" << std::endl;
    } else {
        std::cout << top << std::endl;
    }

    return 0;
}
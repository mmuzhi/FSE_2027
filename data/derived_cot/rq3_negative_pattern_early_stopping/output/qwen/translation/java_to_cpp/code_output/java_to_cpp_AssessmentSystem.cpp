#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include <optional>
#include <cmath>
#include <algorithm>

// Define a hash function for the Student struct
struct StudentHash {
    size_t operator()(const Student& s) const {
        // We'll combine the hash of name, grade, major, and the hash of the courses map.
        // Since courses is a map, we can't directly hash it, so we'll use the hash of the entire student.
        // Alternatively, we can use the default hash for the fields we have.
        // But note: the Student struct has a map, which is not hashable by default.
        // We'll use a simpler approach: combine the hash of name, grade, major, and the hash of the courses map's keys and values.
        // However, this is complex. Alternatively, we can use a tuple of (name, grade, major) and then the courses map's hash?
        // But the original Java uses equals and hashCode for the entire object.

        // Since the problem requires identical behavior, we must ensure that two Student objects are considered equal if all their fields are equal.

        // We'll define a hash function that uses the fields: name, grade, major, and the courses map.
        // We can use boost hash_combine, but we don't want to include boost. Instead, we can use std::hash for the fields we have and then combine.

        // We'll use the fields: name, grade, major, and then the hash of the courses map.

        // First, hash the name, grade, major.
        std::hash<std::string> hasher;
        auto h1 = hasher(s.name);
        auto h2 = std::hash<int>{}(s.grade);
        auto h3 = hasher(s.major);

        // Now, hash the courses map. We can iterate over the map and combine the hashes.
        size_t seed = 0;
        for (const auto& kv : s.courses) {
            auto h4 = hasher(kv.first);
            auto h5 = std::hash<int>{}(kv.second);
            seed ^= h4() ^ h5() ^ 1;
        }

        // Combine the hashes.
        return h1 ^ h2 ^ h3 ^ seed;
    }
};

// Define the equality operator for Student
bool operator==(const Student& a, const Student& b) {
    return a.name == b.name &&
           a.grade == b.grade &&
           a.major == b.major &&
           a.courses == b.courses;
}

struct Student {
    std::string name;
    int grade;
    std::string major;
    std::unordered_map<std::string, int> courses;

    Student(std::string name, int grade, std::string major) : name(std::move(name)), grade(grade), major(std::move(major)) {}

    void addCourseScore(std::string course, int score) {
        courses[course] = score;
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
        if (it != courses.end()) {
            return it->second;
        }
        return std::nullopt;
    }
};

class AssessmentSystem {
public:
    std::unordered_map<std::string, Student, StudentHash> students;

    AssessmentSystem() {}

    void addStudent(std::string name, int grade, std::string major) {
        students[name] = Student(std::move(name), grade, std::move(major));
    }

    void addCourseScore(std::string name, std::string course, int score) {
        auto it = students.find(name);
        if (it != students.end()) {
            it->second.addCourseScore(std::move(course), score);
        }
    }

    std::optional<double> getGPA(std::string name) {
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
                failingStudents.push_back(kv.first);
            }
        }
        return failingStudents;
    }

    std::optional<double> getCourseAverage(std::string course) {
        int totalScore = 0;
        int count = 0;
        for (const auto& kv : students) {
            auto score = kv.second.getCourseScore(course);
            if (score.has_value()) {
                totalScore += score.value();
                count++;
            }
        }
        if (count == 0) {
            return std::nullopt;
        }
        return static_cast<double>(totalScore) / count;
    }

    std::string getTopStudent() {
        std::string topStudent;
        double topGPA = -1.0; // Start with a negative value, since GPA is between 0 and 100 (or average of scores)

        for (const auto& kv : students) {
            auto gpa = kv.second.calculateGPA();
            if (gpa.has_value()) {
                if (gpa.value() > topGPA) {
                    topGPA = gpa.value();
                    topStudent = kv.first;
                }
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

    // Output the list of failing students
    std::vector<std::string> failingStudents = system.getAllStudentsWithFailCourse();
    std::cout << "Failing students: ";
    for (const auto& student : failingStudents) {
        std::cout << student << " ";
    }
    std::cout << std::endl;

    // Output the average for course 1 and course 2
    auto avgCourse1 = system.getCourseAverage("course 1");
    auto avgCourse2 = system.getCourseAverage("course 2");

    if (avgCourse1.has_value()) {
        std::cout << "Average for course 1: " << avgCourse1.value() << std::endl;
    } else {
        std::cout << "Average for course 1: null" << std::endl;
    }

    if (avgCourse2.has_value()) {
        std::cout << "Average for course 2: " << avgCourse2.value() << std::endl;
    } else {
        std::cout << "Average for course 2: null" << std::endl;
    }

    // Output GPA for student 1 and student 2
    auto gpa1 = system.getGPA("student 1");
    auto gpa2 = system.getGPA("student 2");

    if (gpa1.has_value()) {
        std::cout << "GPA for student 1: " << gpa1.value() << std::endl;
    } else {
        std::cout << "GPA for student 1: null" << std::endl;
    }

    if (gpa2.has_value()) {
        std::cout << "GPA for student 2: " << gpa2.value() << std::endl;
    } else {
        std::cout << "GPA for student 2: null" << std::endl;
    }

    // Output the top student
    std::string top = system.getTopStudent();
    if (!top.empty()) {
        std::cout << "Top student: " << top << std::endl;
    } else {
        std::cout << "Top student: null" << std::endl;
    }

    return 0;
}
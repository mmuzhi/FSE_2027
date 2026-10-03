#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <stdexcept>

class ClassRegistrationSystem {
public:
    // Nested Student class
    class Student {
    public:
        Student() = default;
        Student(std::string name, std::string major)
            : name_(std::move(name)), major_(std::move(major)) {}

        const std::string& getName() const { return name_; }
        const std::string& getMajor() const { return major_; }

        bool operator==(const Student& other) const {
            return name_ == other.name_ && major_ == other.major_;
        }

    private:
        std::string name_;
        std::string major_;
    };

    ClassRegistrationSystem() = default;

    // Register a student. Returns 1 if added, 0 if already present.
    int registerStudent(const Student& student) {
        auto it = std::find(students_.begin(), students_.end(), student);
        if (it != students_.end()) {
            return 0;
        }
        students_.push_back(student);
        return 1;
    }

    // Register a class for a student.
    // If the student is not yet in the map, a new entry is created.
    // Returns a reference to the list of classes for that student.
    std::vector<std::string>& registerClass(const std::string& studentName, const std::string& className) {
        auto it = studentClasses_.find(studentName);
        if (it != studentClasses_.end()) {
            it->second.push_back(className);
            return it->second;
        } else {
            auto& vec = studentClasses_[studentName];
            vec.push_back(className);
            return vec;
        }
    }

    // Get all student names for a given major.
    std::vector<std::string> getStudentsByMajor(const std::string& major) const {
        std::vector<std::string> result;
        for (const auto& s : students_) {
            if (s.getMajor() == major) {
                result.push_back(s.getName());
            }
        }
        return result;
    }

    // Get all distinct majors.
    std::vector<std::string> getAllMajor() const {
        std::unordered_set<std::string> majorSet;
        for (const auto& s : students_) {
            majorSet.insert(s.getMajor());
        }
        return std::vector<std::string>(majorSet.begin(), majorSet.end());
    }

    // Get the most popular class (most registrations) among students of a given major.
    // Throws std::out_of_range if no class is found (mimics Java's NoSuchElementException).
    std::string getMostPopularClassInMajor(const std::string& major) const {
        std::unordered_map<std::string, int> classCount;
        for (const auto& s : students_) {
            if (s.getMajor() == major) {
                auto it = studentClasses_.find(s.getName());
                if (it != studentClasses_.end()) {
                    for (const auto& cls : it->second) {
                        classCount[cls]++;
                    }
                }
            }
        }
        if (classCount.empty()) {
            throw std::out_of_range("No classes found for this major");
        }
        auto maxIt = std::max_element(classCount.begin(), classCount.end(),
            [](const std::pair<const std::string, int>& a, const std::pair<const std::string, int>& b) {
                return a.second < b.second;
            });
        return maxIt->first;
    }

    // Setters for testing
    void setStudents(const std::vector<Student>& students) {
        students_ = students;
    }

    void setStudentClasses(const std::unordered_map<std::string, std::vector<std::string>>& studentClasses) {
        studentClasses_ = studentClasses;
    }

private:
    std::vector<Student> students_;
    std::unordered_map<std::string, std::vector<std::string>> studentClasses_;
};
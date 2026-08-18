#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <stdexcept>
#include <utility>

class ClassRegistrationSystem {
public:
    class Student {
    public:
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

    int registerStudent(Student student) {
        if (std::find(students.begin(), students.end(), student) != students.end()) {
            return 0;
        }
        students.push_back(std::move(student));
        return 1;
    }

    std::vector<std::string>& registerClass(const std::string& studentName, const std::string& className) {
        studentsRegistrationClasses[studentName].push_back(className);
        return studentsRegistrationClasses[studentName];
    }

    std::vector<std::string> getStudentsByMajor(const std::string& major) const {
        std::vector<std::string> studentList;
        for (const Student& student : students) {
            if (student.getMajor() == major) {
                studentList.push_back(student.getName());
            }
        }
        return studentList;
    }

    std::vector<std::string> getAllMajor() const {
        std::unordered_set<std::string> majorSet;
        for (const Student& student : students) {
            majorSet.insert(student.getMajor());
        }
        return std::vector<std::string>(majorSet.begin(), majorSet.end());
    }

    std::string getMostPopularClassInMajor(const std::string& major) const {
        std::unordered_map<std::string, int> classCount;
        for (const Student& student : students) {
            if (student.getMajor() == major) {
                auto it = studentsRegistrationClasses.find(student.getName());
                if (it != studentsRegistrationClasses.end()) {
                    for (const std::string& className : it->second) {
                        classCount[className] += 1;
                    }
                }
            }
        }
        if (classCount.empty()) {
            // Mirrors Collections.max throwing NoSuchElementException on an empty map
            throw std::runtime_error("NoSuchElementException");
        }
        auto best = std::max_element(
            classCount.begin(), classCount.end(),
            [](const std::pair<const std::string, int>& a,
               const std::pair<const std::string, int>& b) {
                return a.second < b.second;
            });
        return best->first;
    }

    // Setter methods for tests
    void setStudents(std::vector<Student> students) {
        this->students = std::move(students);
    }

    void setStudentClasses(std::unordered_map<std::string, std::vector<std::string>> studentClasses) {
        this->studentsRegistrationClasses = std::move(studentClasses);
    }

private:
    std::vector<Student> students;
    std::unordered_map<std::string, std::vector<std::string>> studentsRegistrationClasses;
};
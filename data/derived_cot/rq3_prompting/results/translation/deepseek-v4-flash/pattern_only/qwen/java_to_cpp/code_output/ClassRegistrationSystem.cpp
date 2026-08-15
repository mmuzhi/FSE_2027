#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <stdexcept>
#include <utility>
#include <functional>
#include <cstddef>

class ClassRegistrationSystem {
public:
    class Student {
    public:
        Student(std::string name, std::string major)
            : name(std::move(name)), major(std::move(major)) {}

        const std::string& getName() const { return name; }
        const std::string& getMajor() const { return major; }

        bool operator==(const Student& other) const {
            return name == other.name && major == other.major;
        }

    private:
        std::string name;
        std::string major;
    };

    ClassRegistrationSystem() = default;

    int registerStudent(const Student& student) {
        if (std::find(students.begin(), students.end(), student) != students.end()) {
            return 0;
        }
        students.push_back(student);
        return 1;
    }

    std::vector<std::string>& registerClass(const std::string& studentName, const std::string& className) {
        std::vector<std::string>& classes = studentsRegistrationClasses[studentName];
        classes.push_back(className);
        return classes;
    }

    std::vector<std::string> getStudentsByMajor(const std::string& major) const {
        std::vector<std::string> studentList;
        for (const auto& student : students) {
            if (student.getMajor() == major) {
                studentList.push_back(student.getName());
            }
        }
        return studentList;
    }

    std::vector<std::string> getAllMajor() const {
        std::unordered_set<std::string> majorSet;
        for (const auto& student : students) {
            majorSet.insert(student.getMajor());
        }
        return std::vector<std::string>(majorSet.begin(), majorSet.end());
    }

    std::string getMostPopularClassInMajor(const std::string& major) const {
        std::unordered_map<std::string, int> classCount;
        for (const auto& student : students) {
            if (student.getMajor() == major) {
                auto it = studentsRegistrationClasses.find(student.getName());
                if (it != studentsRegistrationClasses.end()) {
                    for (const auto& className : it->second) {
                        classCount[className]++;
                    }
                }
            }
        }
        if (classCount.empty()) {
            throw std::runtime_error("NoSuchElementException");
        }
        auto maxIt = std::max_element(
            classCount.begin(),
            classCount.end(),
            [](const std::pair<const std::string, int>& a, const std::pair<const std::string, int>& b) {
                return a.second < b.second;
            }
        );
        return maxIt->first;
    }

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

namespace std {
    template<>
    struct hash<ClassRegistrationSystem::Student> {
        size_t operator()(const ClassRegistrationSystem::Student& s) const {
            return std::hash<std::string>()(s.getName()) ^ (std::hash<std::string>()(s.getMajor()) << 1);
        }
    };
}
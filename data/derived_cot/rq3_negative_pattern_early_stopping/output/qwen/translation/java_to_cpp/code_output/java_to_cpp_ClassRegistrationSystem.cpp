#include <vector>
#include <string>
#include <unordered_map>
#include <set>
#include <algorithm>

class ClassRegistrationSystem {
private:
    std::vector<Student> students;
    std::unordered_map<std::string, std::vector<std::string>> studentsRegistrationClasses;

    struct Student {
        std::string name;
        std::string major;

        Student(std::string n, std::string m) : name(n), major(m) {}

        bool operator==(const Student& other) const {
            return name == other.name && major == other.major;
        }
    };

public:
    ClassRegistrationSystem() = default;

    int registerStudent(Student student) {
        for (const auto& s : students) {
            if (s == student) {
                return 0;
            }
        }
        students.push_back(student);
        return 1;
    }

    std::vector<std::string> registerClass(std::string studentName, std::string className) {
        auto& classes = studentsRegistrationClasses[studentName];
        classes.push_back(className);
        return classes;
    }

    std::vector<std::string> getStudentsByMajor(std::string major) {
        std::vector<std::string> studentList;
        for (const auto& student : students) {
            if (student.major == major) {
                studentList.push_back(student.name);
            }
        }
        return studentList;
    }

    std::vector<std::string> getAllMajor() {
        std::set<std::string> majorSet;
        for (const auto& student : students) {
            majorSet.insert(student.major);
        }
        return std::vector<std::string>(majorSet.begin(), majorSet.end());
    }

    std::string getMostPopularClassInMajor(std::string major) {
        std::unordered_map<std::string, int> classCount;
        for (const auto& student : students) {
            if (student.major == major) {
                const auto& classes = studentsRegistrationClasses.find(student.name);
                if (classes != studentsRegistrationClasses.end()) {
                    const auto& classesList = classes->second;
                    for (const auto& className : classesList) {
                        classCount[className]++;
                    }
                }
            }
        }
        // Find the entry with the maximum count
        auto max_entry = std::max_element(classCount.begin(), classCount.end(),
            [](const std::pair<std::string, int>& a, const std::pair<std::string, int>& b) {
                return a.second < b.second;
            });
        return max_entry->first;
    }

    // Setter methods for tests
    void setStudents(std::vector<Student> students) {
        this->students = std::move(students);
    }

    void setStudentClasses(std::unordered_map<std::string, std::vector<std::string>> studentClasses) {
        this->studentsRegistrationClasses = std::move(studentClasses);
    }
};
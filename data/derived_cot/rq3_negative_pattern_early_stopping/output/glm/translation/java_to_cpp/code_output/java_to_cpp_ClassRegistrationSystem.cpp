#ifndef CLASS_REGISTRATION_SYSTEM_H
#define CLASS_REGISTRATION_SYSTEM_H

#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <string>
#include <algorithm>
#include <functional>

class ClassRegistrationSystem {
public:
    class Student {
    private:
        std::string name;
        std::string major;

    public:
        Student(const std::string& name, const std::string& major)
            : name(name), major(major) {}

        const std::string& getName() const {
            return name;
        }

        const std::string& getMajor() const {
            return major;
        }

        bool operator==(const Student& other) const {
            return name == other.name && major == other.major;
        }

        bool operator!=(const Student& other) const {
            return !(*this == other);
        }
    };

private:
    std::vector<Student> students;
    std::unordered_map<std::string, std::vector<std::string>> studentsRegistrationClasses;

public:
    ClassRegistrationSystem() = default;

    int registerStudent(const Student& student) {
        if (std::find(students.begin(), students.end(), student) != students.end()) {
            return 0;
        } else {
            students.push_back(student);
            return 1;
        }
    }

    std::vector<std::string> registerClass(const std::string& studentName, const std::string& className) {
        auto it = studentsRegistrationClasses.find(studentName);
        if (it != studentsRegistrationClasses.end()) {
            it->second.push_back(className);
        } else {
            studentsRegistrationClasses[studentName] = std::vector<std::string>{className};
        }
        return studentsRegistrationClasses[studentName];
    }

    std::vector<std::string> getStudentsByMajor(const std::string& major) {
        std::vector<std::string> studentList;
        for (const auto& student : students) {
            if (student.getMajor() == major) {
                studentList.push_back(student.getName());
            }
        }
        return studentList;
    }

    std::vector<std::string> getAllMajor() {
        std::unordered_set<std::string> majorSet;
        for (const auto& student : students) {
            majorSet.insert(student.getMajor());
        }
        return std::vector<std::string>(majorSet.begin(), majorSet.end());
    }

    std::string getMostPopularClassInMajor(const std::string& major) {
        std::unordered_map<std::string, int> classCount;
        for (const auto& student : students) {
            if (student.getMajor() == major) {
                auto it = studentsRegistrationClasses.find(student.getName());
                std::vector<std::string> classes;
                if (it != studentsRegistrationClasses.end()) {
                    classes = it->second;
                }
                for (const auto& className : classes) {
                    classCount[className]++;
                }
            }
        }
        auto maxIt = std::max_element(classCount.begin(), classCount.end(),
            [](const std::pair<const std::string, int>& a, const std::pair<const std::string, int>& b) {
                return a.second < b.second;
            });
        return maxIt->first;
    }

    void setStudents(const std::vector<Student>& students) {
        this->students = students;
    }

    void setStudentClasses(const std::unordered_map<std::string, std::vector<std::string>>& studentClasses) {
        this->studentsRegistrationClasses = studentClasses;
    }
};

#endif
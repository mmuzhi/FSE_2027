#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <set>

struct Student {
    std::string name;
    std::string major;
};

class ClassRegistrationSystem {
private:
    std::vector<Student> students;
    std::map<std::string, std::vector<std::string>> students_registration_classes;

public:
    int register_student(const Student& student) {
        // Check if the student already exists by comparing the entire student record
        for (const auto& s : students) {
            if (s.name == student.name && s.major == student.major) {
                return 0;
            }
        }
        students.push_back(student);
        return 1;
    }

    std::vector<std::string> register_class(const std::string& student_name, const std::string& class_name) {
        // If the student has not been registered for any classes, we need to check if they exist in the system?
        // But note: the Python code does not check if the student exists in the system. It just uses the student_name as key.
        // However, the problem says to keep behavior identical. The Python code does not require the student to be registered before registering a class.
        // But note: the example usage in the docstring does not show any error handling for non-registered students.

        // Since the Python code does not check for the existence of the student in the system, we do the same.
        if (students_registration_classes.find(student_name) == students_registration_classes.end()) {
            students_registration_classes[student_name] = std::vector<std::string>();
        }
        students_registration_classes[student_name].push_back(class_name);
        return students_registration_classes[student_name];
    }

    std::vector<std::string> get_students_by_major(const std::string& major) {
        std::vector<std::string> student_list;
        for (const auto& student : students) {
            if (student.major == major) {
                student_list.push_back(student.name);
            }
        }
        return student_list;
    }

    std::vector<std::string> get_all_major() {
        std::vector<std::string> major_list;
        for (const auto& student : students) {
            if (std::find(major_list.begin(), major_list.end(), student.major) == major_list.end()) {
                major_list.push_back(student.major);
            }
        }
        return major_list;
    }

    std::string get_most_popular_class_in_major(const std::string& major) {
        // First, collect all classes from students in the given major
        std::vector<std::string> class_list;
        for (const auto& student : students) {
            if (student.major == major) {
                // For each student in the major, add their classes
                // But note: the student might not have registered any classes, so we check the map
                if (students_registration_classes.find(student.name) != students_registration_classes.end()) {
                    class_list.insert(class_list.end(), students_registration_classes[student.name].begin(), students_registration_classes[student.name].end());
                }
            }
        }

        // If there are no classes, return an empty string? But the problem doesn't specify. Let's assume we return an empty string.
        if (class_list.empty()) {
            return "";
        }

        // Find the most popular class: the one that appears the most in class_list
        std::string most_popular_class = "";
        int max_count = 0;

        // We can use a map to count occurrences
        std::map<std::string, int> class_count;
        for (const auto& cls : class_list) {
            class_count[cls]++;
        }

        // Find the class with the highest count
        for (const auto& entry : class_count) {
            if (entry.second > max_count) {
                max_count = entry.second;
                most_popular_class = entry.first;
            }
        }

        return most_popular_class;
    }
};
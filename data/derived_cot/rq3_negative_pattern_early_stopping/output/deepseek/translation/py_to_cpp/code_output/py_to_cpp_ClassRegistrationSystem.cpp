#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <stdexcept>

class ClassRegistrationSystem {
public:
    struct Student {
        std::string name;
        std::string major;

        bool operator==(const Student& other) const {
            return name == other.name && major == other.major;
        }

        bool operator!=(const Student& other) const {
            return !(*this == other);
        }
    };

    ClassRegistrationSystem() = default;

    int register_student(const Student& student) {
        auto it = std::find(students.begin(), students.end(), student);
        if (it != students.end()) {
            return 0;
        }
        students.push_back(student);
        return 1;
    }

    std::vector<std::string> register_class(const std::string& student_name, const std::string& class_name) {
        auto& classes = students_registration_classes[student_name];
        classes.push_back(class_name);
        return classes;
    }

    std::vector<std::string> get_students_by_major(const std::string& major) const {
        std::vector<std::string> student_list;
        for (const auto& student : students) {
            if (student.major == major) {
                student_list.push_back(student.name);
            }
        }
        return student_list;
    }

    std::vector<std::string> get_all_major() const {
        std::vector<std::string> major_list;
        for (const auto& student : students) {
            if (std::find(major_list.begin(), major_list.end(), student.major) == major_list.end()) {
                major_list.push_back(student.major);
            }
        }
        return major_list;
    }

    std::string get_most_popular_class_in_major(const std::string& major) const {
        std::vector<std::string> class_list;
        for (const auto& student : students) {
            if (student.major == major) {
                const auto& classes = students_registration_classes.at(student.name);
                class_list.insert(class_list.end(), classes.begin(), classes.end());
            }
        }

        if (class_list.empty()) {
            throw std::invalid_argument("No classes found for this major");
        }

        std::unordered_map<std::string, int> counts;
        int max_count = 0;
        for (const auto& c : class_list) {
            int cnt = ++counts[c];
            if (cnt > max_count) {
                max_count = cnt;
            }
        }

        for (const auto& pair : counts) {
            if (pair.second == max_count) {
                return pair.first;
            }
        }
        // Should never reach here
        return "";
    }

private:
    std::vector<Student> students;
    std::unordered_map<std::string, std::vector<std::string>> students_registration_classes;
};
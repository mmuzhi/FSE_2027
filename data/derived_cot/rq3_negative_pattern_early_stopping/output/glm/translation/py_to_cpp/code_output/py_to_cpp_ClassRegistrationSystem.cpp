#include <vector>
#include <map>
#include <string>
#include <algorithm>
#include <stdexcept>

class ClassRegistrationSystem {
private:
    struct Student {
        std::string name;
        std::string major;
        bool operator==(const Student& other) const {
            return name == other.name && major == other.major;
        }
    };

    std::vector<Student> students;
    std::map<std::string, std::vector<std::string>> students_registration_classes;

public:
    ClassRegistrationSystem() = default;

    int register_student(const std::map<std::string, std::string>& student) {
        Student s{student.at("name"), student.at("major")};
        for (const auto& existing : students) {
            if (existing == s) {
                return 0;
            }
        }
        students.push_back(s);
        return 1;
    }

    std::vector<std::string> register_class(const std::string& student_name, const std::string& class_name) {
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
        std::vector<std::string> class_list;
        for (const auto& student : students) {
            if (student.major == major) {
                const auto& classes = students_registration_classes.at(student.name);
                class_list.insert(class_list.end(), classes.begin(), classes.end());
            }
        }

        if (class_list.empty()) {
            throw std::runtime_error("max() arg is an empty sequence");
        }

        std::map<std::string, int> freq;
        for (const auto& cls : class_list) {
            freq[cls]++;
        }

        std::string most_popular;
        int max_count = -1;
        for (const auto& p : freq) {
            if (p.second > max_count) {
                max_count = p.second;
                most_popular = p.first;
            }
        }

        return most_popular;
    }
};
#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <stdexcept>

struct Student {
    std::string name;
    std::string major;

    bool operator==(const Student& other) const {
        return name == other.name && major == other.major;
    }
};

class ClassRegistrationSystem {
public:
    std::vector<Student> students;
    std::unordered_map<std::string, std::vector<std::string>> students_registration_classes;

    ClassRegistrationSystem() {}

    int register_student(const Student& student) {
        for (const auto& s : students) {
            if (s == student) {
                return 0;
            }
        }
        students.push_back(student);
        return 1;
    }

    std::vector<std::string>& register_class(const std::string& student_name, const std::string& class_name) {
        std::vector<std::string>& classes = students_registration_classes[student_name];
        classes.push_back(class_name);
        return classes;
    }

    std::vector<std::string> get_students_by_major(const std::string& major) const {
        std::vector<std::string> result;
        for (const auto& student : students) {
            if (student.major == major) {
                result.push_back(student.name);
            }
        }
        return result;
    }

    std::vector<std::string> get_all_major() const {
        std::vector<std::string> result;
        for (const auto& student : students) {
            if (std::find(result.begin(), result.end(), student.major) == result.end()) {
                result.push_back(student.major);
            }
        }
        return result;
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
            throw std::invalid_argument("max() arg is an empty sequence");
        }

        std::unordered_set<std::string> unique_classes(class_list.begin(), class_list.end());
        std::string most_popular;
        int max_count = -1;

        for (const auto& cls : unique_classes) {
            int cnt = static_cast<int>(std::count(class_list.begin(), class_list.end(), cls));
            if (cnt > max_count) {
                max_count = cnt;
                most_popular = cls;
            }
        }

        return most_popular;
    }
};
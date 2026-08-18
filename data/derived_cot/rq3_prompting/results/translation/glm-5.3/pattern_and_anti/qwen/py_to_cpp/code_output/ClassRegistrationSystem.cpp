#include <algorithm>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

class ClassRegistrationSystem {
public:
    // students is a list of student dictionaries, each with keys "name" and "major".
    std::vector<std::map<std::string, std::string>> students;
    // key is the student name, value is a list of class names
    std::map<std::string, std::vector<std::string>> students_registration_classes;

    ClassRegistrationSystem() = default;

    // register a student to the system, add the student to the students list,
    // if the student is already registered, return 0, else return 1
    int register_student(const std::map<std::string, std::string>& student) {
        if (std::find(students.begin(), students.end(), student) != students.end()) {
            return 0;
        } else {
            students.push_back(student);
            return 1;
        }
    }

    // register a class to the student; returns the student's list of registered classes
    std::vector<std::string>& register_class(const std::string& student_name, const std::string& class_name) {
        auto it = students_registration_classes.find(student_name);
        if (it != students_registration_classes.end()) {
            it->second.push_back(class_name);
        } else {
            students_registration_classes.emplace(student_name,
                                                  std::vector<std::string>{class_name});
        }
        return students_registration_classes[student_name];
    }

    // get all students in the major; returns a list of student names
    std::vector<std::string> get_students_by_major(const std::string& major) {
        std::vector<std::string> student_list;
        for (const auto& student : students) {
            if (student.at("major") == major) {
                student_list.push_back(student.at("name"));
            }
        }
        return student_list;
    }

    // get all majors in the system; returns a list of majors (first-appearance order)
    std::vector<std::string> get_all_major() {
        std::vector<std::string> major_list;
        for (const auto& student : students) {
            const std::string& m = student.at("major");
            if (std::find(major_list.begin(), major_list.end(), m) == major_list.end()) {
                major_list.push_back(m);
            }
        }
        return major_list;
    }

    // get the class with the highest enrollment in the major
    std::string get_most_popular_class_in_major(const std::string& major) {
        std::vector<std::string> class_list;
        for (const auto& student : students) {
            if (student.at("major") == major) {
                const std::vector<std::string>& registered =
                    students_registration_classes.at(student.at("name"));
                class_list.insert(class_list.end(), registered.begin(), registered.end());
            }
        }

        // max(set(class_list), key=class_list.count): raise on empty like Python's max()
        if (class_list.empty()) {
            throw std::invalid_argument("max() arg is an empty sequence");
        }

        std::vector<std::string> unique_classes;
        std::map<std::string, int> counts;
        for (const auto& cls : class_list) {
            if (counts.find(cls) == counts.end()) {
                unique_classes.push_back(cls);
            }
            counts[cls]++;
        }

        const std::string* most_popular_class = nullptr;
        int best_count = -1;
        for (const auto& cls : unique_classes) {
            if (counts[cls] > best_count) {
                best_count = counts[cls];
                most_popular_class = &cls;
            }
        }
        return *most_popular_class;
    }
};
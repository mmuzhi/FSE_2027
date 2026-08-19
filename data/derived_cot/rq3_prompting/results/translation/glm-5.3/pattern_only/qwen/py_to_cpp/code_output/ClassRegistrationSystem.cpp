#include <algorithm>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

class ClassRegistrationSystem {
public:
    // Each student is a dictionary with keys "name" and "major".
    using Student = std::map<std::string, std::string>;

    ClassRegistrationSystem() = default;

    // Register a student; return 0 if already registered, else 1.
    int register_student(const Student& student) {
        if (std::find(students.begin(), students.end(), student) != students.end()) {
            return 0;
        } else {
            students.push_back(student);
            return 1;
        }
    }

    // Register a class for the student; returns (a reference to) the student's class list.
    std::vector<std::string>& register_class(const std::string& student_name,
                                             const std::string& class_name) {
        auto it = students_registration_classes.find(student_name);
        if (it != students_registration_classes.end()) {
            it->second.push_back(class_name);
        } else {
            students_registration_classes.emplace(student_name,
                                                  std::vector<std::string>{class_name});
        }
        return students_registration_classes[student_name];
    }

    // Get all student names in the given major.
    std::vector<std::string> get_students_by_major(const std::string& major) const {
        std::vector<std::string> student_list;
        for (const auto& student : students) {
            if (student.at("major") == major) {  // at(): throws like KeyError on missing key
                student_list.push_back(student.at("name"));
            }
        }
        return student_list;
    }

    // Get all majors in order of first appearance.
    std::vector<std::string> get_all_major() const {
        std::vector<std::string> major_list;
        for (const auto& student : students) {
            const std::string& m = student.at("major");
            if (std::find(major_list.begin(), major_list.end(), m) == major_list.end()) {
                major_list.push_back(m);
            }
        }
        return major_list;
    }

    // Get the class with the highest enrollment in the major.
    std::string get_most_popular_class_in_major(const std::string& major) const {
        std::vector<std::string> class_list;
        for (const auto& student : students) {
            if (student.at("major") == major) {
                const std::vector<std::string>& regs =
                    students_registration_classes.at(student.at("name"));
                class_list.insert(class_list.end(), regs.begin(), regs.end());
            }
        }
        if (class_list.empty()) {
            // Python: max() on empty sequence raises ValueError
            throw std::invalid_argument("max() arg is an empty sequence");
        }

        // Unique classes in first-occurrence order (stable stand-in for Python's set).
        std::vector<std::string> unique_classes;
        for (const auto& c : class_list) {
            if (std::find(unique_classes.begin(), unique_classes.end(), c) ==
                unique_classes.end()) {
                unique_classes.push_back(c);
            }
        }

        const std::string* most_popular_class = nullptr;
        std::size_t best_count = 0;
        for (const auto& c : unique_classes) {
            std::size_t count =
                static_cast<std::size_t>(std::count(class_list.begin(), class_list.end(), c));
            if (most_popular_class == nullptr || count > best_count) {
                most_popular_class = &c;
                best_count = count;
            }
        }
        return *most_popular_class;
    }

private:
    std::vector<Student> students;
    std::map<std::string, std::vector<std::string>> students_registration_classes;
};
#include <algorithm>
#include <cstddef>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

/*
 * A class registration system: registers students, registers them for
 * classes, retrieves students by major, lists all majors, and determines
 * the most popular class within a specific major.
 */
class ClassRegistrationSystem {
public:
    // In the Python original every student is a dict with the keys
    // "name" and "major".
    struct Student {
        std::string name;
        std::string major;

        bool operator==(const Student& other) const {
            return name == other.name && major == other.major;
        }
    };

    // students: list of registered students.
    // students_registration_classes: student name -> list of class names.
    std::vector<Student> students;
    std::unordered_map<std::string, std::vector<std::string>> students_registration_classes;

    ClassRegistrationSystem() = default;

    // Register a student. Returns 0 if the student is already registered,
    // otherwise adds the student and returns 1.
    int register_student(const Student& student) {
        if (std::find(students.begin(), students.end(), student) != students.end()) {
            return 0;
        }
        students.push_back(student);
        return 1;
    }

    // Register a class for the student and return the student's (live) list
    // of registered class names.
    std::vector<std::string>& register_class(const std::string& student_name,
                                             const std::string& class_name) {
        std::vector<std::string>& classes = students_registration_classes[student_name];
        classes.push_back(class_name);
        return classes;
    }

    // Return the names of all students in the given major (registration order).
    std::vector<std::string> get_students_by_major(const std::string& major) const {
        std::vector<std::string> student_list;
        for (const Student& student : students) {
            if (student.major == major) {
                student_list.push_back(student.name);
            }
        }
        return student_list;
    }

    // Return all majors in the system (order of first appearance).
    std::vector<std::string> get_all_major() const {
        std::vector<std::string> major_list;
        for (const Student& student : students) {
            if (std::find(major_list.begin(), major_list.end(), student.major) ==
                major_list.end()) {
                major_list.push_back(student.major);
            }
        }
        return major_list;
    }

    // Return the class with the highest enrollment in the given major.
    // Mirrors Python behavior: throws std::out_of_range (Python: KeyError) if
    // a student of that major has no entry in students_registration_classes,
    // and std::invalid_argument (Python: ValueError from max()) if no classes
    // are registered in that major at all.
    std::string get_most_popular_class_in_major(const std::string& major) const {
        std::vector<std::string> class_list;
        for (const Student& student : students) {
            if (student.major == major) {
                const std::vector<std::string>& registered =
                    students_registration_classes.at(student.name);
                class_list.insert(class_list.end(), registered.begin(), registered.end());
            }
        }

        if (class_list.empty()) {
            throw std::invalid_argument("max() arg is an empty sequence");
        }

        // Equivalent of: max(set(class_list), key=class_list.count)
        // Ties resolve to the first occurrence in list order (Python's set
        // iteration order is arbitrary, so any deterministic tie-break is
        // consistent with the original's observable behavior).
        std::unordered_map<std::string, std::size_t> counts;
        for (const std::string& cls : class_list) {
            ++counts[cls];
        }

        std::string most_popular_class = class_list.front();
        std::size_t best_count = counts[most_popular_class];
        for (const std::string& cls : class_list) {
            const std::size_t count = counts[cls];
            if (count > best_count) {
                best_count = count;
                most_popular_class = cls;
            }
        }
        return most_popular_class;
    }
};
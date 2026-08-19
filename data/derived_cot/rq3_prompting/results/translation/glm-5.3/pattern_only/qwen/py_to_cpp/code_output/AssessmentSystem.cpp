#include <map>
#include <string>
#include <vector>
#include <optional>
#include <stdexcept>

class AssessmentSystem {
public:
    struct Student {
        std::string name;
        int grade;
        std::string major;
        std::map<std::string, std::optional<double>> courses; // course -> score (score may be "None")
    };

    std::map<std::string, Student> students;

    void add_student(const std::string& name, int grade, const std::string& major) {
        students[name] = Student{name, grade, major, {}};
    }

    void add_course_score(const std::string& name, const std::string& course,
                          std::optional<double> score) {
        auto it = students.find(name);
        if (it != students.end()) {
            it->second.courses[course] = score;
        }
    }

    // Returns average grade, or nullopt (None) if student missing or has no courses.
    std::optional<double> get_gpa(const std::string& name) {
        auto it = students.find(name);
        if (it != students.end() && !it->second.courses.empty()) {
            double total = 0;
            for (const auto& [course, score] : it->second.courses) {
                if (!score.has_value()) {
                    // Python: sum() over values containing None raises TypeError
                    throw std::runtime_error(
                        "TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'");
                }
                total += *score;
            }
            return total / static_cast<double>(it->second.courses.size());
        }
        return std::nullopt;
    }

    std::vector<std::string> get_all_students_with_fail_course() {
        std::vector<std::string> result;
        for (const auto& [name, student] : students) {
            for (const auto& [course, score] : student.courses) {
                if (!score.has_value()) {
                    // Python: None < 60 raises TypeError
                    throw std::runtime_error(
                        "TypeError: '<' not supported between instances of 'NoneType' and 'int'");
                }
                if (*score < 60) {
                    result.push_back(name);
                    break;
                }
            }
        }
        return result;
    }

    std::optional<double> get_course_average(const std::string& course) {
        double total = 0;
        int count = 0;
        for (const auto& [name, student] : students) {
            auto it = student.courses.find(course);
            if (it != student.courses.end()) {
                const std::optional<double>& score = it->second;
                if (score.has_value()) {
                    total += *score;
                    count += 1;
                }
            }
        }
        if (count > 0) {
            return total / count;
        }
        return std::nullopt;
    }

    std::optional<std::string> get_top_student() {
        std::optional<std::string> top_student;
        double top_gpa = 0;
        for (const auto& [name, student] : students) {
            std::optional<double> gpa = get_gpa(name);
            if (gpa.has_value() && *gpa > top_gpa) {
                top_gpa = *gpa;
                top_student = name;
            }
        }
        return top_student;
    }
};
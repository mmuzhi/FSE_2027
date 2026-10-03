#include <string>
#include <unordered_map>
#include <vector>
#include <optional>

class AssessmentSystem {
private:
    struct Student {
        std::string name;
        int grade;
        std::string major;
        std::unordered_map<std::string, int> courses;
    };

    std::unordered_map<std::string, Student> students;

public:
    AssessmentSystem() = default;

    void add_student(const std::string& name, int grade, const std::string& major) {
        students[name] = {name, grade, major, {}};
    }

    void add_course_score(const std::string& name, const std::string& course, int score) {
        auto it = students.find(name);
        if (it != students.end()) {
            it->second.courses[course] = score;
        }
    }

    std::optional<double> get_gpa(const std::string& name) const {
        auto it = students.find(name);
        if (it != students.end() && !it->second.courses.empty()) {
            double sum = 0.0;
            for (const auto& [course, score] : it->second.courses) {
                sum += score;
            }
            return sum / it->second.courses.size();
        }
        return std::nullopt;
    }

    std::vector<std::string> get_all_students_with_fail_course() const {
        std::vector<std::string> result;
        for (const auto& [name, student] : students) {
            for (const auto& [course, score] : student.courses) {
                if (score < 60) {
                    result.push_back(name);
                    break;
                }
            }
        }
        return result;
    }

    std::optional<double> get_course_average(const std::string& course) const {
        double total = 0.0;
        int count = 0;
        for (const auto& [name, student] : students) {
            auto it = student.courses.find(course);
            if (it != student.courses.end()) {
                total += it->second;
                ++count;
            }
        }
        if (count > 0) {
            return total / count;
        }
        return std::nullopt;
    }

    std::optional<std::string> get_top_student() {
        std::optional<std::string> top_student = std::nullopt;
        double top_gpa = 0.0;
        for (const auto& [name, student] : students) {
            auto gpa_opt = get_gpa(name);
            if (gpa_opt.has_value()) {
                double gpa = gpa_opt.value();
                if (!top_student.has_value() || gpa > top_gpa) {
                    top_gpa = gpa;
                    top_student = name;
                }
            }
        }
        return top_student;
    }
};
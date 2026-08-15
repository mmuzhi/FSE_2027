#include <vector>
#include <string>
#include <map>
#include <optional>
#include <utility>

class AssessmentSystem {
private:
    struct Student {
        std::string name;
        int grade;
        std::string major;
        std::map<std::string, int> courses;
    };

    std::vector<Student> students;

    Student* find_student(const std::string& name) {
        for (auto& s : students) {
            if (s.name == name) return &s;
        }
        return nullptr;
    }

    const Student* find_student(const std::string& name) const {
        for (const auto& s : students) {
            if (s.name == name) return &s;
        }
        return nullptr;
    }

public:
    void add_student(const std::string& name, int grade, const std::string& major) {
        if (auto* s = find_student(name)) {
            s->grade = grade;
            s->major = major;
            s->courses.clear();
            return;
        }
        Student s;
        s.name = name;
        s.grade = grade;
        s.major = major;
        students.push_back(std::move(s));
    }

    void add_course_score(const std::string& name, const std::string& course, int score) {
        if (auto* s = find_student(name)) {
            s->courses[course] = score;
        }
    }

    std::optional<double> get_gpa(const std::string& name) const {
        const auto* s = find_student(name);
        if (!s || s->courses.empty()) return std::nullopt;

        double total = 0.0;
        for (const auto& [course, score] : s->courses) {
            total += score;
        }
        return total / s->courses.size();
    }

    std::vector<std::string> get_all_students_with_fail_course() const {
        std::vector<std::string> result;
        for (const auto& s : students) {
            for (const auto& [course, score] : s.courses) {
                if (score < 60) {
                    result.push_back(s.name);
                    break;
                }
            }
        }
        return result;
    }

    std::optional<double> get_course_average(const std::string& course) const {
        double total = 0.0;
        int count = 0;

        for (const auto& s : students) {
            auto it = s.courses.find(course);
            if (it != s.courses.end()) {
                total += it->second;
                ++count;
            }
        }

        if (count == 0) return std::nullopt;
        return total / count;
    }

    std::optional<std::string> get_top_student() const {
        std::optional<std::string> top_student;
        double top_gpa = 0.0;

        for (const auto& s : students) {
            auto gpa = get_gpa(s.name);
            if (gpa.has_value() && *gpa > top_gpa) {
                top_gpa = *gpa;
                top_student = s.name;
            }
        }

        return top_student;
    }
};
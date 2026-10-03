#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include <optional>
#include <cmath>

struct Student {
    std::string name;
    int grade;
    std::string major;
    std::unordered_map<std::string, int> courses;
};

class AssessmentSystem {
private:
    std::unordered_map<std::string, Student> students;

    std::optional<double> calculate_gpa(const Student& student) const {
        if (student.courses.empty()) {
            return std::nullopt;
        }
        double total = 0.0;
        for (const auto& course_score : student.courses) {
            total += course_score.second;
        }
        return total / student.courses.size();
    }

public:
    void add_student(const std::string& name, int grade, const std::string& major) {
        students[name] = {name, grade, major, {}};
    }

    void add_course_score(const std::string& name, const std::string& course, int score) {
        if (students.find(name) != students.end()) {
            students[name].courses[course] = score;
        }
    }

    std::optional<double> get_gpa(const std::string& name) const {
        if (students.find(name) == students.end()) {
            return std::nullopt;
        }
        return calculate_gpa(students.at(name));
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
            if (student.courses.find(course) != student.courses.end()) {
                total += student.courses.at(course);
                count++;
            }
        }
        if (count == 0) {
            return std::nullopt;
        }
        return total / count;
    }

    std::optional<std::string> get_top_student() const {
        if (students.empty()) {
            return std::nullopt;
        }
        std::string top_student = "";
        double top_gpa = -1.0;
        for (const auto& [name, student] : students) {
            auto gpa = get_gpa(name);
            if (!gpa.has_value()) {
                continue;
            }
            if (*gpa > top_gpa) {
                top_gpa = *gpa;
                top_student = name;
            }
        }
        return top_student.empty() ? std::nullopt : std::make_optional(top_student);
    }
};
#include <string>
#include <vector>
#include <utility>
#include <optional>
#include <cstddef>

class AssessmentSystem {
public:
    AssessmentSystem() = default;

    void add_student(const std::string& name, int grade, const std::string& major) {
        // Python dict semantics: re-adding replaces the value but keeps insertion position,
        // resetting 'courses' to an empty dict.
        Student* s = find(name);
        if (s != nullptr) {
            *s = Student{name, grade, major, {}};
        } else {
            students_.push_back(Student{name, grade, major, {}});
        }
    }

    void add_course_score(const std::string& name, const std::string& course, int score) {
        Student* s = find(name);
        if (s != nullptr) {
            for (auto& [c, sc] : s->courses) {
                if (c == course) {
                    sc = score;  // overwrite existing course score, like dict assignment
                    return;
                }
            }
            s->courses.emplace_back(course, score);
        }
    }

    // Returns average grade (float) if the student exists and has courses, else "None".
    std::optional<double> get_gpa(const std::string& name) const {
        const Student* s = find(name);
        if (s != nullptr && !s->courses.empty()) {
            long long sum = 0;
            for (const auto& [course, score] : s->courses) {
                (void)course;
                sum += score;
            }
            return static_cast<double>(sum) / static_cast<double>(s->courses.size());
        }
        return std::nullopt;
    }

    // Returns names (in insertion order) of students with any score below 60.
    std::vector<std::string> get_all_students_with_fail_course() const {
        std::vector<std::string> result;
        for (const auto& s : students_) {
            for (const auto& [course, score] : s.courses) {
                (void)course;
                if (score < 60) {
                    result.push_back(s.name);
                    break;
                }
            }
        }
        return result;
    }

    // Returns average score of a course if anyone has a record, else "None".
    std::optional<double> get_course_average(const std::string& course) const {
        long long total = 0;
        std::size_t count = 0;
        for (const auto& s : students_) {
            for (const auto& [c, score] : s.courses) {
                if (c == course) {
                    // 'score is not None' check in Python is vacuous for int scores.
                    total += score;
                    ++count;
                    break;
                }
            }
        }
        if (count > 0) {
            return static_cast<double>(total) / static_cast<double>(count);
        }
        return std::nullopt;
    }

    // Returns the name of the student with the highest GPA, or "None" if no qualifying student.
    std::optional<std::string> get_top_student() const {
        std::optional<std::string> top_student;
        double top_gpa = 0;
        for (const auto& s : students_) {
            std::optional<double> gpa = get_gpa(s.name);
            if (gpa.has_value() && *gpa > top_gpa) {
                top_gpa = *gpa;
                top_student = s.name;
            }
        }
        return top_student;
    }

private:
    struct Student {
        std::string name;
        int grade;
        std::string major;
        std::vector<std::pair<std::string, int>> courses;  // insertion-ordered course -> score
    };

    std::vector<Student> students_;  // preserves Python dict insertion order

    Student* find(const std::string& name) {
        for (auto& s : students_) {
            if (s.name == name) return &s;
        }
        return nullptr;
    }

    const Student* find(const std::string& name) const {
        for (const auto& s : students_) {
            if (s.name == name) return &s;
        }
        return nullptr;
    }
};
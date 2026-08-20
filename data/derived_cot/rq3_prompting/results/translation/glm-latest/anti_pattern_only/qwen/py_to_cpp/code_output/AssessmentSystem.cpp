#include <cstddef>
#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

// This is a class as a student assessment system, which supports add student,
// add course score, calculate GPA, and other functions for students and courses.
class AssessmentSystem {
public:
    // A single course record; a score of None is represented by std::nullopt.
    struct CourseScore {
        std::string course;
        std::optional<int> score;
    };

    // Equivalent of the Python student dict:
    // {'name': ..., 'grade': ..., 'major': ..., 'courses': {...}}
    struct Student {
        std::string name;
        int grade;
        std::string major;
        std::vector<CourseScore> courses;  // insertion-ordered, like a Python dict
    };

    // Equivalent of the Python dict self.students (name -> student record),
    // kept in insertion order like a Python dict.
    std::vector<Student> students;

    // Initialize the students dict in assessment system.
    AssessmentSystem() = default;

    // Add a new student into students.
    void add_student(const std::string& name, int grade, const std::string& major) {
        for (Student& student : students) {
            if (student.name == name) {
                // Assigning to an existing key keeps its position in a Python dict.
                student.grade = grade;
                student.major = major;
                student.courses.clear();
                return;
            }
        }
        students.push_back(Student{name, grade, major, {}});
    }

    // Add score of a specific course for a student in students
    // (silently ignored if the student does not exist).
    void add_course_score(const std::string& name, const std::string& course,
                          std::optional<int> score) {
        Student* student = find_student(name);
        if (student == nullptr) {
            return;
        }
        for (CourseScore& cs : student->courses) {
            if (cs.course == course) {
                // Assigning to an existing key keeps its position in a Python dict.
                cs.score = score;
                return;
            }
        }
        student->courses.push_back(CourseScore{course, score});
    }

    // Get average grade of one student.
    // Returns the average (float) if the student exists and has course grades,
    // std::nullopt (None) otherwise.
    std::optional<double> get_gpa(const std::string& name) const {
        const Student* student = find_student(name);
        if (student == nullptr || student->courses.empty()) {
            return std::nullopt;
        }
        long long total = 0;
        for (const CourseScore& cs : student->courses) {
            if (!cs.score.has_value()) {
                // sum() over a None value raises TypeError in Python.
                throw std::runtime_error(
                    "TypeError: unsupported operand type(s) for +: "
                    "'int' and 'NoneType'");
            }
            total += *cs.score;
        }
        return static_cast<double>(total) /
               static_cast<double>(student->courses.size());
    }

    // Get all students who have any score below 60 (in insertion order).
    std::vector<std::string> get_all_students_with_fail_course() const {
        std::vector<std::string> failed;
        for (const Student& student : students) {
            for (const CourseScore& cs : student.courses) {
                if (!cs.score.has_value()) {
                    // None < 60 raises TypeError in Python.
                    throw std::runtime_error(
                        "TypeError: '<' not supported between instances of "
                        "'NoneType' and 'int'");
                }
                if (*cs.score < 60) {
                    failed.push_back(student.name);
                    break;
                }
            }
        }
        return failed;
    }

    // Get the average score of a specific course.
    // Returns the average if anyone has a (non-None) score for the course,
    // std::nullopt (None) if nobody has records.
    std::optional<double> get_course_average(const std::string& course) const {
        long long total = 0;
        std::size_t count = 0;
        for (const Student& student : students) {
            const std::optional<int>* score = find_course(student, course);
            if (score != nullptr && score->has_value()) {
                total += **score;
                ++count;
            }
        }
        if (count > 0) {
            return static_cast<double>(total) / static_cast<double>(count);
        }
        return std::nullopt;
    }

    // Calculate every student's GPA and find the student with the highest GPA
    // (first one in insertion order wins ties, since only strictly greater
    // GPAs replace the current top).
    // Returns std::nullopt (None) if no student has a GPA greater than 0.
    std::optional<std::string> get_top_student() const {
        std::optional<std::string> top_student;
        double top_gpa = 0;  // Python: top_gpa = 0
        for (const Student& student : students) {
            const std::optional<double> gpa = get_gpa(student.name);
            if (gpa.has_value() && *gpa > top_gpa) {
                top_gpa = *gpa;
                top_student = student.name;
            }
        }
        return top_student;
    }

private:
    Student* find_student(const std::string& name) {
        for (Student& student : students) {
            if (student.name == name) {
                return &student;
            }
        }
        return nullptr;
    }

    const Student* find_student(const std::string& name) const {
        for (const Student& student : students) {
            if (student.name == name) {
                return &student;
            }
        }
        return nullptr;
    }

    static const std::optional<int>* find_course(const Student& student,
                                                 const std::string& course) {
        for (const CourseScore& cs : student.courses) {
            if (cs.course == course) {
                return &cs.score;
            }
        }
        return nullptr;
    }
};
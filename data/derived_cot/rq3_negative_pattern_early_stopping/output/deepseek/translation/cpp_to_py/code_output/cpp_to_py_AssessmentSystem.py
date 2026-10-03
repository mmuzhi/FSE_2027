class AssessmentSystem:
    def __init__(self):
        self.students = {}   # name -> {"grade": int, "major": str, "courses": {course: int}}

    def add_student(self, name: str, grade: int, major: str) -> None:
        self.students[name] = {
            "grade": grade,
            "major": major,
            "courses": {}
        }

    def add_course_score(self, name: str, course: str, score: int) -> None:
        if name in self.students:
            self.students[name]["courses"][course] = score

    def get_gpa(self, name: str):
        student = self.students.get(name)
        if student is None:
            return None
        courses = student["courses"]
        if not courses:
            return None
        total = sum(courses.values())
        return total / len(courses)

    def get_all_students_with_fail_course(self):
        result = []
        for name, student in self.students.items():
            if any(score < 60 for score in student["courses"].values()):
                result.append(name)
        return result

    def get_course_average(self, course: str):
        total = 0.0
        count = 0
        for student in self.students.values():
            score = student["courses"].get(course)
            if score is not None:
                total += score
                count += 1
        return total / count if count > 0 else None

    def get_top_student(self):
        top_name = None
        top_gpa = None
        for name in self.students:
            gpa = self.get_gpa(name)
            if gpa is not None and (top_gpa is None or gpa > top_gpa):
                top_gpa = gpa
                top_name = name
        return top_name
class Student:
    def __init__(self, student_id: int, email: str, grade: int, first_name: str = None, last_name: str = None, interested_subjects: str = None):
        self.student_id = student_id
        self.email = email
        self.grade = grade
        self.first_name = first_name
        self.last_name = last_name
        self.interested_subjects = interested_subjects

    def __str__(self):
        return (f"Student(id={self.student_id}, email={self.email}, "
                f"grade={self.grade}, first_name={self.first_name}, "
                f"last_name={self.last_name}, interested={self.interested_subjects})")
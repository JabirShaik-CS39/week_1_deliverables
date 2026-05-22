# Hybrid Inheritance Example 

class SchoolMember:
    def sign_in(self):
        return "Signed into the campus directory."
class Teacher(SchoolMember):   # Hierarchical portion: Teacher and Student both inherit from SchoolMember
    def grade_papers(self):
        return "Grading exams."
class Student(SchoolMember):
    def study(self):
        return "Reviewing textbook material."
class Tutor(Teacher, Student):  # Multiple Inheritance portion: Tutor inherits from BOTH Teacher and Student
    def conduct_session(self):
        return "Explaining a tricky math problem."
campus_tutor = Tutor()
print(campus_tutor.sign_in())        # From SchoolMember
print(campus_tutor.grade_papers())   # From Teacher
print(campus_tutor.study())          # From Student
print(campus_tutor.conduct_session())# From Tutor
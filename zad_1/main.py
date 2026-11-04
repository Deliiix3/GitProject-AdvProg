from zad_1.student import Student

student_1 = Student("Jan Kowalski", [70, 65, 80])
student_2 = Student("Anna Nowak", [30, 45, 50])

print(student_1, "->", student_1.is_passed())
print(student_2, "->", student_2.is_passed())

from zad_1.student import Student

s1 = Student("Jan Kowalski", [70, 80, 65])
s2 = Student("Anna Nowak", [30, 45, 50])
print(s1, "->", s1.is_passed())  # True
print(s2, "->", s2.is_passed())  # False

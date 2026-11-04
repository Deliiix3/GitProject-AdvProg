class Student:
    def __init__(self, name: str, marks: list[int]):
        self.name = name
        self.marks = marks

    def is_passed(self) -> bool:
        if not self.marks:
            return False
        return sum(self.marks) / len(self.marks) > 50

    def __str__(self) -> str:
        return f"Student: {self.name}, oceny: {self.marks}"

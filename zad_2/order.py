from datetime import date

from zad_1.student import Student
from zad_2.book import Book
from zad_2.employee import Employee


class Order:
    def __init__(
        self,
        employee: Employee,
        student: Student,
        books: list[Book],
        order_date: date,
    ):
        self.employee = employee
        self.student = student
        self.books = books
        self.order_date = order_date

    def __str__(self) -> str:
        ksiazki = "\n".join(f"  - {b}" for b in self.books)
        return (
            f"Zamówienie z dnia {self.order_date}\n"
            f"  {self.employee}\n"
            f"  {self.student}\n"
            f"  Książki:\n{ksiazki}"
        )

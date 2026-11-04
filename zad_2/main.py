from datetime import date

from zad_1.student import Student
from zad_2.book import Book
from zad_2.employee import Employee
from zad_2.library import Library
from zad_2.order import Order

library_1 = Library(
    "Katowice", "ul. Książnicy 1", "40-001", "8:00-18:00", "32 111 22 33"
)
library_2 = Library(
    "Cieszyn", "ul. Głęboka 5", "43-400", "9:00-17:00", "33 444 55 66"
)

books = [
    Book(library_1, date(1999, 5, 12), "Adam", "Mickiewicz", 320),
    Book(library_1, date(2005, 3, 1), "Henryk", "Sienkiewicz", 540),
    Book(library_2, date(2012, 9, 20), "Olga", "Tokarczuk", 410),
    Book(library_2, date(2018, 11, 5), "Stanisław", "Lem", 280),
    Book(library_1, date(1985, 1, 30), "Bolesław", "Prus", 610),
]

employees = [
    Employee(
        "Piotr",
        "Zieliński",
        date(2015, 6, 1),
        date(1985, 4, 10),
        "Katowice",
        "ul. Długa 3",
        "40-002",
        "600 100 200",
    ),
    Employee(
        "Maria",
        "Lis",
        date(2018, 9, 15),
        date(1990, 8, 22),
        "Cieszyn",
        "ul. Krótka 7",
        "43-400",
        "601 200 300",
    ),
    Employee(
        "Tomasz",
        "Wójcik",
        date(2020, 2, 3),
        date(1995, 12, 5),
        "Gliwice",
        "ul. Leśna 12",
        "44-100",
        "602 300 400",
    ),
]

students = [
    Student("Jan Kowalski", [70, 65, 80]),
    Student("Anna Nowak", [30, 45, 50]),
    Student("Ewa Mazur", [90, 85, 95]),
]

order_1 = Order(employees[0], students[0], books[:2], date(2026, 10, 1))
order_2 = Order(employees[1], students[2], books[2:], date(2026, 10, 15))

print(order_1)
print()
print(order_2)

from datetime import date

from zad_1.student import Student
from zad_2.book import Book
from zad_2.employee import Employee
from zad_2.library import Library
from zad_2.order import Order

lib1 = Library(
    "Warszawa", "Marszałkowska 1", "00-001", "8:00-16:00", "111-222-333"
)
lib2 = Library("Katowice", "Rynek 5", "40-001", "9:00-17:00", "444-555-666")

books = [
    Book(lib1, date(2001, 5, 1), "Adam", "Mickiewicz", 300),
    Book(lib1, date(1999, 3, 12), "Henryk", "Sienkiewicz", 450),
    Book(lib2, date(2010, 8, 20), "Olga", "Tokarczuk", 520),
    Book(lib2, date(2015, 1, 9), "Stanisław", "Lem", 280),
    Book(lib1, date(1985, 11, 30), "Bolesław", "Prus", 600),
]

employees = [
    Employee(
        "Piotr",
        "Zieliński",
        date(2015, 4, 1),
        date(1985, 2, 14),
        "Warszawa",
        "Długa 3",
        "00-002",
        "500-100-100",
    ),
    Employee(
        "Maria",
        "Lis",
        date(2018, 9, 15),
        date(1990, 7, 3),
        "Katowice",
        "Krótka 7",
        "40-002",
        "500-200-200",
    ),
    Employee(
        "Tomasz",
        "Wójcik",
        date(2020, 1, 10),
        date(1995, 12, 25),
        "Warszawa",
        "Polna 9",
        "00-003",
        "500-300-300",
    ),
]

students = [
    Student("Jan Kowalski", [70, 80, 65]),
    Student("Anna Nowak", [30, 45, 50]),
    Student("Ewa Mazur", [90, 85, 95]),
]

order1 = Order(
    employees[0], students[0], [books[0], books[1]], date(2026, 10, 1)
)
order2 = Order(
    employees[1],
    students[2],
    [books[2], books[3], books[4]],
    date(2026, 10, 5),
)

print(order1)
print()
print(order2)

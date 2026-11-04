from datetime import date

from zad_2.library import Library


class Book:
    def __init__(
        self,
        library: Library,
        publication_date: date,
        author_name: str,
        author_surname: str,
        number_of_pages: int,
    ):
        self.library = library
        self.publication_date = publication_date
        self.author_name = author_name
        self.author_surname = author_surname
        self.number_of_pages = number_of_pages

    def __str__(self) -> str:
        return (
            f"Książka: {self.author_name} {self.author_surname}, "
            f"wydana {self.publication_date}, stron: {self.number_of_pages}\n"
            f"    {self.library}"
        )

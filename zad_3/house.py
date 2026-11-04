from zad_3.property import Property


class House(Property):
    def __init__(self, area, rooms, price, address, plot):
        super().__init__(area, rooms, price, address)
        self.plot = plot

    def __str__(self):
        return f"Dom, działka {self.plot} m2. {super().__str__()}"

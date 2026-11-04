class Property:
    def __init__(self, area, rooms, price, address):
        self.area = area
        self.rooms = rooms
        self.price = price
        self.address = address

    def __str__(self):
        return (
            f"Nieruchomość: {self.address}, {self.area} m2, "
            f"pokoje: {self.rooms}, cena: {self.price} zł"
        )

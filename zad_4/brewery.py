from typing import Optional


class Brewery:
    def __init__(
        self,
        id: str,
        name: str,
        brewery_type: Optional[str] = None,
        address_1: Optional[str] = None,
        address_2: Optional[str] = None,
        address_3: Optional[str] = None,
        city: Optional[str] = None,
        state_province: Optional[str] = None,
        postal_code: Optional[str] = None,
        country: Optional[str] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        phone: Optional[str] = None,
        website_url: Optional[str] = None,
        state: Optional[str] = None,
        street: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.brewery_type = brewery_type
        self.address_1 = address_1
        self.address_2 = address_2
        self.address_3 = address_3
        self.city = city
        self.state_province = state_province
        self.postal_code = postal_code
        self.country = country
        self.longitude = longitude
        self.latitude = latitude
        self.phone = phone
        self.website_url = website_url
        self.state = state
        self.street = street

    @classmethod
    def from_dict(cls, data: dict) -> "Brewery":
        longitude = data.get("longitude")
        latitude = data.get("latitude")
        return cls(
            id=data["id"],
            name=data["name"],
            brewery_type=data.get("brewery_type"),
            address_1=data.get("address_1"),
            address_2=data.get("address_2"),
            address_3=data.get("address_3"),
            city=data.get("city"),
            state_province=data.get("state_province"),
            postal_code=data.get("postal_code"),
            country=data.get("country"),
            longitude=float(longitude) if longitude else None,
            latitude=float(latitude) if latitude else None,
            phone=data.get("phone"),
            website_url=data.get("website_url"),
            state=data.get("state"),
            street=data.get("street"),
        )

    def __str__(self) -> str:
        return (
            f"Browar: {self.name} (id: {self.id})\n"
            f"  typ: {self.brewery_type}\n"
            f"  adres: {self.street}, {self.postal_code} {self.city}, "
            f"{self.state_province}, {self.country}\n"
            f"  współrzędne: {self.latitude}, {self.longitude}\n"
            f"  telefon: {self.phone}\n"
            f"  strona: {self.website_url}"
        )

from typing import List, Optional

import requests

from zad_4.brewery import Brewery

API_URL = "https://api.openbrewerydb.org/v1/breweries"


def fetch_breweries(
    limit: int = 20, city: Optional[str] = None
) -> List[Brewery]:
    params = {"per_page": limit}
    if city:
        params["by_city"] = city.replace(" ", "_")

    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()

    return [Brewery.from_dict(item) for item in response.json()]

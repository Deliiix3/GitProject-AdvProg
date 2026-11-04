from zad_4.api import fetch_breweries

breweries = fetch_breweries(20)

for brewery in breweries:
    print(brewery)
    print()

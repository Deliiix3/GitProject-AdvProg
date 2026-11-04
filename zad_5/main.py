import argparse

from zad_4.api import fetch_breweries


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lista browarów z API")
    parser.add_argument(
        "--city",
        default=None,
        help="miasto, do którego ograniczamy wyniki (np. --city=Berlin)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    breweries = fetch_breweries(20, args.city)

    if not breweries:
        print(f"Brak browarów dla miasta: {args.city}")
        return

    for brewery in breweries:
        print(brewery)
        print()


if __name__ == "__main__":
    main()

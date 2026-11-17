import argparse

from file_queue import add_job


def main() -> None:
    parser = argparse.ArgumentParser(description="Producer - dodaje prace")
    parser.add_argument(
        "--count", type=int, default=1, help="liczba prac (domyślnie 1)"
    )
    args = parser.parse_args()

    for _ in range(args.count):
        job = add_job("Rozmowa telefoniczna")
        print(f"Dodano pracę {job['id']} (status: {job['status']})")


if __name__ == "__main__":
    main()

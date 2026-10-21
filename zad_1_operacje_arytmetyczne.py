def greet(name: str, surname: str) -> str:
    return f'Cześć {name}, {surname}'

if __name__ == "__main__":
    out = greet("Jan", "Kowalski")
    print(out)
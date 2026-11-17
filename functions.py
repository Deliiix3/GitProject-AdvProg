import re
from collections import Counter
from math import isqrt

VOWELS = set("aąeęioóuy")


def is_palindrome(text: str) -> bool:
    cleaned = "".join(text.lower().split())
    return cleaned == cleaned[::-1]


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n nie może być ujemne")
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


def count_vowels(text: str) -> int:
    return sum(1 for char in text.lower() if char in VOWELS)


def calculate_discount(price: float, discount: float) -> float:
    if not 0 <= discount <= 1:
        raise ValueError("zniżka musi być w zakresie 0-1")
    return float(price * (1 - discount))


def flatten_list(nested_list: list) -> list:
    flat = []
    for item in nested_list:
        if isinstance(item, list):
            flat.extend(flatten_list(item))
        else:
            flat.append(item)
    return flat


def word_frequencies(text: str) -> dict:
    words = re.findall(r"\w+", text.lower())
    return dict(Counter(words))


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for divisor in range(2, isqrt(n) + 1):
        if n % divisor == 0:
            return False
    return True

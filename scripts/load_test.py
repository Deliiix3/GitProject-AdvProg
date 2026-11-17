import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

BASE_URL = "http://127.0.0.1:8000"


def call(url: str) -> float:
    started = time.time()
    requests.get(url, timeout=300)
    return time.time() - started


def main() -> None:
    path = sys.argv[1]  # np. "/analyze_img_sync?url=https://..."
    count = int(sys.argv[2])  # liczba równoczesnych zapytań
    with ThreadPoolExecutor(max_workers=count) as pool:
        times = list(pool.map(call, [BASE_URL + path] * count))
    print(f"zapytań: {count}")
    print(f"najkrótsze: {min(times):.2f}s")
    print(f"najdłuższe: {max(times):.2f}s")
    print(f"średnio:    {sum(times) / len(times):.2f}s")


if __name__ == "__main__":
    main()

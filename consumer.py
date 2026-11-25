import argparse
import os
import time
from rabbit_queue import consume_jobs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Consumer - wykonuje prace z RabbitMQ"
    )
    parser.add_argument("--name", default=f"consumer-{os.getpid()}")
    parser.add_argument(
        "--work-time", type=float, default=30, help="czas pracy w sekundach"
    )
    parser.add_argument(
        "--exit-when-empty",
        action="store_true",
        help="zakończ, gdy nie ma prac (do testów)",
    )
    args = parser.parse_args()

    def process_job(job: dict) -> None:
        print(
            f"[{args.name}] pobrano {job['id']} ({job['description']}) -> in_progress"
        )
        time.sleep(args.work_time)
        print(f"[{args.name}] zakończono {job['id']} -> done")

    print(f"[{args.name}] start i oczekiwanie na zadania...")
    consume_jobs(
        consumer_name=args.name,
        work_callback=process_job,
        exit_when_empty=args.exit_when_empty,
    )


if __name__ == "__main__":
    main()

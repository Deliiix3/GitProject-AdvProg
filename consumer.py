import argparse
import os
import time

from db_queue import claim_next_job, mark_done


def main() -> None:
    parser = argparse.ArgumentParser(description="Consumer - wykonuje prace")
    parser.add_argument("--name", default=f"consumer-{os.getpid()}")
    parser.add_argument(
        "--work-time", type=float, default=30, help="czas pracy w sekundach"
    )
    parser.add_argument(
        "--poll-interval", type=float, default=5, help="co ile sprawdzać bazę"
    )
    parser.add_argument(
        "--exit-when-empty",
        action="store_true",
        help="zakończ, gdy nie ma prac (do testów)",
    )
    args = parser.parse_args()

    print(f"[{args.name}] start")
    while True:
        job = claim_next_job(args.name)
        if job is None:
            if args.exit_when_empty:
                break
            time.sleep(args.poll_interval)
            continue

        print(f"[{args.name}] pobrano {job['id']} -> in_progress")
        time.sleep(args.work_time)
        mark_done(job["id"])
        print(f"[{args.name}] zakończono {job['id']} -> done")


if __name__ == "__main__":
    main()

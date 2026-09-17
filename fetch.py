# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

from pathlib import Path
from datetime import date, timedelta
import time
import requests


# --------------------------------------------------
# Settings
# --------------------------------------------------

START_DATE = date(2026, 7, 17)
END_DATE = date(2026, 9, 15)

STATIONS = [
    "KEV",
    "KIL",
    "IVA",
    "MUO",
    "RAN",
    "MEK",
]

BASE_URL = "https://lake.fmi.fi/r-index-archive"
BASE_URL = "https://lake.fmi.fi/r-index-archive"

HERE = Path(__file__).parent
DATA = HERE / "data" / "fmi-r-index"


# --------------------------------------------------
# Download
# --------------------------------------------------

def download_file(url, path):

    if path.exists():
        print(f"already exists: {path.name}")
        return True

    for attempt in range(3):

        try:

            print(
                f"downloading: {path.name} "
                f"(attempt {attempt + 1}/3)"
            )

            response = requests.get(
                url,
                timeout=60,
                headers={
                    "User-Agent": "SD5913 PolyU student"
                },
            )

            response.raise_for_status()

            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            path.write_bytes(
                response.content
            )

            print(
                f"saved: {path}"
            )

            return True

        except requests.RequestException as error:

            print(
                f"FAILED: {path.name}"
            )
            print(error)

            if attempt < 2:
                print("waiting 5 seconds...")
                time.sleep(5)

    return False


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    DATA.mkdir(
        parents=True,
        exist_ok=True
    )

    total = 0
    success = 0
    failed = 0

    current = START_DATE

    total_days = (
        END_DATE - START_DATE
    ).days + 1

    total_files = (
        total_days * len(STATIONS)
    )

    print()
    print("===================================")
    print("FMI R-index data download")
    print("===================================")
    print(f"Date range: {START_DATE} -> {END_DATE}")
    print(f"Days: {total_days}")
    print(f"Stations: {len(STATIONS)}")
    print(f"Expected files: {total_files}")
    print("===================================")
    print()

    while current <= END_DATE:

        date_text = current.strftime(
            "%Y%m%d"
        )

        print()
        print(
            f"===== {current} ====="
        )

        for station in STATIONS:

            filename = (
                f"{station}-R-index-"
                f"{date_text}.csv.gz"
            )

            url = f"{BASE_URL}/{filename}"

            path = DATA / filename

            total += 1

            if download_file(
                url,
                path
            ):
                success += 1
            else:
                failed += 1

            # Give FMI server a little break.
            time.sleep(1)

        current += timedelta(days=1)

    print()
    print("===================================")
    print("Download finished")
    print("===================================")
    print(f"Checked: {total}")
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print(f"Folder: {DATA}")
    print("===================================")


if __name__ == "__main__":
    main()
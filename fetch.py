# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

from pathlib import Path
from datetime import date, timedelta
import requests
import time


# --------------------------------------------------
# Settings
# --------------------------------------------------

START_DATE = date(2026, 6, 17)
END_DATE = date(2026, 9, 15)

STATIONS = [
    "KEV",  # Kevo
    "KIL",  # Kilpisjärvi
    "IVA",  # Ivalo
    "MUO",  # Muonio
    "PEL",  # Pello
    "RAN",  # Ranua
    "OUJ",  # Oulujärvi
    "MEK",  # Mekrijärvi
    "HAN",  # Hankasalmi
    "NUR",  # Nurmijärvi
    "TAR",  # Tartu
]

BASE_URL = "https://lake.fmi.fi/r-index-archive"

HERE = Path(__file__).parent
DATA = HERE / "data" / "fmi-r-index"


# --------------------------------------------------
# Download one file
# --------------------------------------------------

def download_file(url, path):
    if path.exists():
        print(f"already exists: {path}")
        return

    print(f"downloading: {url}")

    try:
        response = requests.get(
            url,
            timeout=60,
            headers={"User-Agent": "SD5913 PolyU student"}
        )
        response.raise_for_status()

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(response.content)

        print(f"saved: {path}")

    except requests.RequestException as error:
        print(f"FAILED: {url}")
        print(error)


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    DATA.mkdir(parents=True, exist_ok=True)

    current = START_DATE
    total = 0

    while current <= END_DATE:

        date_text = current.strftime("%Y%m%d")

        for station in STATIONS:

            filename = f"{station}-R-index-{date_text}.csv.gz"

            url = f"{BASE_URL}/{filename}"
            path = DATA / filename

            download_file(url, path)

            total += 1

        current += timedelta(days=1)

        # Avoid sending too many requests at once.
        time.sleep(0.2)

    print()
    print("Download finished.")
    print(f"Files checked: {total}")
    print(f"Data folder: {DATA}")


if __name__ == "__main__":
    main()
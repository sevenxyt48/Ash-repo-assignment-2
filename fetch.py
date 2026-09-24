# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

from pathlib import Path
import requests
import json
import time

URL = (
    "https://api.gbif.org/v1/occurrence/search"
    "?scientificName=Passer%20domesticus"
    "&country=GB"
    "&year=2026"
    "&occurrenceStatus=PRESENT"
    "&hasCoordinate=true"
)

FILE = "uk-house-sparrow-2026.json"

HERE = Path(__file__).parent
DATA = HERE / "data"


def fetch(url, path):
    if path.exists():
        print(f"data/{path.name} is already here.")
        return path

    DATA.mkdir(exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": "SD5913 PolyU student"})

    for attempt in range(5):
        try:
            response = session.get(url + "&limit=1", timeout=180)
            response.raise_for_status()
            total = response.json()["count"]
            break
        except requests.RequestException:
            print(f"Retry {attempt + 1}/5...")
            time.sleep(3)
    else:
        raise RuntimeError("Could not connect to GBIF.")

    print(f"GBIF records found: {total}")

    records = []

    for offset in range(0, total, 300):
        for attempt in range(5):
            try:
                response = session.get(
                    url + f"&limit=300&offset={offset}",
                    timeout=180
                )
                response.raise_for_status()
                records.extend(response.json()["results"])
                print(f"Downloaded {len(records)}/{total}")
                break
            except requests.RequestException:
                print(f"Retry {attempt + 1}/5...")
                time.sleep(3)
        else:
            raise RuntimeError("GBIF download failed.")

    path.write_text(
        json.dumps({"count": total, "results": records}, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"saved data/{path.name}")


if __name__ == "__main__":
    fetch(URL, DATA / FILE)
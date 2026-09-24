# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

import csv
import gzip
from pathlib import Path

import matplotlib.pyplot as plt


DATA = Path(__file__).parent / "data" / "fmi-r-index"
OUT = Path(__file__).parent / "out"

STATIONS = {
    "KEV": "Kevo",
    "KIL": "Kilpisjärvi",
    "IVA": "Ivalo",
    "MUO": "Muonio",
    "RAN": "Ranua",
    "MEK": "Mekrijärvi",
}


def rows(path):
    """Read time and R-index from one FMI .csv.gz file."""
    data = []

    with gzip.open(path, "rt", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                time = row["Time"]
                value = float(row["R-index"])
                data.append((time, value))
            except (ValueError, KeyError):
                continue

    return data


def main():
    # day -> station -> maximum R-index
    values = {}

    for path in sorted(DATA.glob("*-R-index-*.csv.gz")):
        station = path.name.split("-")[0]

        if station not in STATIONS:
            continue

        for time, value in rows(path):
            day = time[:10]

            if day not in values:
                values[day] = {}

            if station not in values[day]:
                values[day][station] = value
            else:
                values[day][station] = max(
                    values[day][station], value
                )

    days = sorted(values)

    stations = list(STATIONS)

    matrix = [
        [values.get(day, {}).get(station, 0) for day in days]
        for station in stations
    ]

    print(f"{len(days)} days, {len(stations)} stations")
    print(f"R-index range: {min(map(min, matrix))} to {max(map(max, matrix))}")

    fig, ax = plt.subplots(figsize=(10, 5))

    image = ax.imshow(
        matrix,
        aspect="auto",
        cmap="viridis",
        vmin=0,
        vmax=100,
    )

    ax.set_xticks(range(len(days)))
    ax.set_xticklabels(days, rotation=45)

    ax.set_yticks(range(len(stations)))
    ax.set_yticklabels(STATIONS.values())

    ax.set_xlabel("Date")
    ax.set_ylabel("Observation station")
    ax.set_title("Auroral Activity Across Northern Finland")

    colorbar = fig.colorbar(image, ax=ax)
    colorbar.set_label("Daily maximum R-index")

    fig.tight_layout()

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "aurora-heatmap.png", dpi=150)

    print("saved out/aurora-heatmap.png")

    plt.show()


if __name__ == "__main__":
    main()
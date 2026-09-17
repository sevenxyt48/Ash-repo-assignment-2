# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "pillow", "requests"]
# ///

from pathlib import Path
import csv
import gzip
import math
import re
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import requests


# --------------------------------------------------
# Settings
# --------------------------------------------------

HERE = Path(__file__).parent
DATA = HERE / "data" / "fmi-r-index"
OUT = HERE / "out"
MAP_CACHE = HERE / "data" / "map-finland.png"

STATIONS = {
    "KEV": ("Kevo", 69.76, 27.01),
    "KIL": ("Kilpisjärvi", 69.05, 20.79),
    "IVA": ("Ivalo", 68.56, 27.29),
    "MUO": ("Muonio", 68.02, 23.53),
    "PEL": ("Pello", 66.90, 24.08),
    "RAN": ("Ranua", 65.90, 26.41),
    "OUJ": ("Oulujärvi", 64.52, 27.23),
    "MEK": ("Mekrijärvi", 62.77, 30.97),
    "HAN": ("Hankasalmi", 62.25, 26.60),
    "NUR": ("Nurmijärvi", 60.50, 24.65),
    "TAR": ("Tartu", 58.26, 26.46),
}

# Finland + nearby northern Europe
LON_MIN = 18
LON_MAX = 34
LAT_MIN = 57
LAT_MAX = 71

# R-index display range
R_MIN = 0
R_MAX = 100


# --------------------------------------------------
# Read R-index from CSV
# --------------------------------------------------

def clean_name(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def find_column(fieldnames, keywords):
    """
    Find a column even if FMI changes spaces/capitalisation.
    """
    for field in fieldnames:
        name = clean_name(field)

        for keyword in keywords:
            if keyword in name:
                return field

    return None


def parse_csv_file(path):
    """
    Read one FMI .csv.gz file.

    Returns:
        list of (datetime, r_index)
    """

    results = []

    with gzip.open(path, "rt", encoding="utf-8-sig", errors="replace") as file:

        # Detect delimiter.
        sample = file.read(5000)
        file.seek(0)

        try:
            dialect = csv.Sniffer().sniff(sample)
            delimiter = dialect.delimiter
        except csv.Error:
            delimiter = ";"

        reader = csv.DictReader(file, delimiter=delimiter)

        if not reader.fieldnames:
            return results

        time_column = find_column(
            reader.fieldnames,
            ["time", "datetime", "date"]
        )

        r_column = find_column(
            reader.fieldnames,
            ["rindex", "r-index", "r index"]
        )

        if r_column is None:
            # Try a more relaxed search.
            for field in reader.fieldnames:
                if "r" in clean_name(field) and "index" in clean_name(field):
                    r_column = field
                    break

        if time_column is None or r_column is None:
            print(f"Could not find columns in {path.name}")
            print("Columns:", reader.fieldnames)
            return results

        for row in reader:

            time_text = str(row.get(time_column, "")).strip()
            value_text = str(row.get(r_column, "")).strip()

            if not time_text or not value_text:
                continue

            if value_text.lower() in {
                "",
                "nan",
                "null",
                "none",
                "missing",
                "na",
            }:
                continue

            try:
                value = float(value_text)
            except ValueError:
                continue

            # Try several common time formats.
            parsed_time = None

            time_formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S%z",
            ]

            for fmt in time_formats:
                try:
                    parsed_time = datetime.strptime(time_text, fmt)
                    break
                except ValueError:
                    pass

            if parsed_time is None:
                try:
                    parsed_time = datetime.fromisoformat(
                        time_text.replace("Z", "+00:00")
                    )
                except ValueError:
                    continue

            results.append((parsed_time, value))

    return results


# --------------------------------------------------
# Load all historical data
# --------------------------------------------------

def load_data():

    daily_data = {}

    files = sorted(DATA.glob("*-R-index-*.csv.gz"))

    print(f"Found {len(files)} data files.")

    for path in files:

        station_code = path.name.split("-")[0]

        if station_code not in STATIONS:
            continue

        records = parse_csv_file(path)

        for timestamp, value in records:

            day = timestamp.date()

            if day not in daily_data:
                daily_data[day] = {}

            if station_code not in daily_data[day]:
                daily_data[day][station_code] = []

            daily_data[day][station_code].append(value)

    # Convert each station to daily maximum.
    #
    # We use maximum R-index because it clearly shows
    # when auroral activity was strongest during the day.
    frames = []

    for day in sorted(daily_data):

        frame = {}

        for station, values in daily_data[day].items():

            if values:
                frame[station] = max(values)

        if frame:
            frames.append((day, frame))

    print(f"Created {len(frames)} daily frames.")

    return frames


# --------------------------------------------------
# Web Mercator
# --------------------------------------------------

def lon_to_x(lon, zoom):

    n = 2 ** zoom

    return (lon + 180) / 360 * n


def lat_to_y(lat, zoom):

    n = 2 ** zoom

    lat_rad = math.radians(lat)

    return (
        1
        - math.asinh(math.tan(lat_rad)) / math.pi
    ) / 2 * n


# --------------------------------------------------
# Download map tiles
# --------------------------------------------------

def download_basemap():

    if MAP_CACHE.exists():
        print(f"Using cached map: {MAP_CACHE}")
        return

    print("Downloading map tiles...")

    zoom = 5
    tile_size = 256

    x1 = int(lon_to_x(LON_MIN, zoom))
    x2 = int(lon_to_x(LON_MAX, zoom))

    y1 = int(lat_to_y(LAT_MAX, zoom))
    y2 = int(lat_to_y(LAT_MIN, zoom))

    width = (x2 - x1 + 1) * tile_size
    height = (y2 - y1 + 1) * tile_size

    from PIL import Image

    canvas = Image.new("RGB", (width, height))

    for x in range(x1, x2 + 1):

        for y in range(y1, y2 + 1):

            url = (
                "https://server.arcgisonline.com/"
                "ArcGIS/rest/services/Canvas/"
                "World_Light_Gray_Base/MapServer/"
                f"tile/{zoom}/{y}/{x}"
            )

            print(f"map tile {x}, {y}")

            response = requests.get(
                url,
                timeout=30,
                headers={
                    "User-Agent": "SD5913 PolyU student"
                },
            )

            response.raise_for_status()

            from io import BytesIO

            tile = Image.open(
                BytesIO(response.content)
            ).convert("RGB")

            px = (x - x1) * tile_size
            py = (y - y1) * tile_size

            canvas.paste(tile, (px, py))

    MAP_CACHE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    canvas.save(MAP_CACHE)

    print(f"Saved map: {MAP_CACHE}")


# --------------------------------------------------
# Map coordinate conversion
# --------------------------------------------------

def geographic_to_image(lon, lat, image_width, image_height):

    zoom = 5
    tile_size = 256

    x_min = lon_to_x(LON_MIN, zoom)
    x_max = lon_to_x(LON_MAX, zoom)

    y_min = lat_to_y(LAT_MAX, zoom)
    y_max = lat_to_y(LAT_MIN, zoom)

    x = (
        (lon_to_x(lon, zoom) - x_min)
        / (x_max - x_min)
        * image_width
    )

    y = (
        (lat_to_y(lat, zoom) - y_min)
        / (y_max - y_min)
        * image_height
    )

    return x, y


# --------------------------------------------------
# Main visualization
# --------------------------------------------------

def make_animation():

    OUT.mkdir(
        parents=True,
        exist_ok=True
    )

    download_basemap()

    frames = load_data()

    if not frames:
        raise RuntimeError(
            "No historical data found. "
            "Run fetch.py first."
        )

    from PIL import Image

    map_image = Image.open(
        MAP_CACHE
    ).convert("RGB")

    image_width, image_height = map_image.size

    fig, ax = plt.subplots(
        figsize=(10, 8)
    )

    ax.imshow(map_image)

    ax.set_xlim(0, image_width)
    ax.set_ylim(image_height, 0)

    ax.axis("off")

    # Station coordinates.
    station_positions = {}

    for code, (name, lat, lon) in STATIONS.items():

        x, y = geographic_to_image(
            lon,
            lat,
            image_width,
            image_height
        )

        station_positions[code] = (x, y)

    # Plot station locations.
    for code, (x, y) in station_positions.items():

        ax.scatter(
            x,
            y,
            s=10,
            c="white",
            edgecolors="black",
            linewidths=0.5,
            zorder=5,
        )

    title = ax.set_title(
        "",
        fontsize=16,
        pad=12
    )

    # Empty scatter.
    activity = ax.scatter(
        [],
        [],
        s=[],
        c=[],
        cmap="viridis",
        vmin=R_MIN,
        vmax=R_MAX,
        alpha=0.85,
        edgecolors="white",
        linewidths=0.5,
        zorder=10,
    )

    # Color bar.
    colorbar = fig.colorbar(
        activity,
        ax=ax,
        fraction=0.035,
        pad=0.02
    )

    colorbar.set_label(
        "R-index",
        fontsize=11
    )

    def update(frame_number):

        day, data = frames[frame_number]

        xs = []
        ys = []
        values = []
        sizes = []

        for station, value in data.items():

            if station not in station_positions:
                continue

            x, y = station_positions[station]

            xs.append(x)
            ys.append(y)

            value = max(0, min(R_MAX, value))

            values.append(value)

            # Stronger activity = larger point.
            sizes.append(
                30 + value * 4
            )

        activity.set_offsets(
            list(zip(xs, ys))
        )

        activity.set_sizes(
            sizes
        )

        activity.set_array(
            values
        )

        title.set_text(
            f"Auroral Activity\n"
            f"{day.strftime('%Y-%m-%d')}  |  "
            f"FMI R-index"
        )

        return activity, title

    animation = FuncAnimation(
        fig,
        update,
        frames=len(frames),
        interval=150,
        blit=False,
        repeat=True,
    )

    # First frame PNG.
    update(0)

    png_path = OUT / "aurora-map.png"

    fig.savefig(
        png_path,
        dpi=150,
        bbox_inches="tight"
    )

    print(f"Saved: {png_path}")

    # Animated GIF.
    gif_path = OUT / "aurora-animation.gif"

    print("Creating animation...")

    animation.save(
        gif_path,
        writer=PillowWriter(fps=5)
    )

    print(f"Saved: {gif_path}")

    plt.close(fig)


if __name__ == "__main__":
    make_animation()
# /// script
# requires-python = ">=3.10"
# dependencies = ["folium"]
# ///

from pathlib import Path
import json
import folium
from folium.plugins import HeatMap


HERE = Path(__file__).parent
DATA = HERE / "data" / "uk-house-sparrow-2026.json"
OUT = HERE / "out" / "plot.html"


data = json.loads(DATA.read_text(encoding="utf-8"))

points = [
    [r["decimalLatitude"], r["decimalLongitude"]]
    for r in data["results"]
    if "decimalLatitude" in r and "decimalLongitude" in r
]

print("First point:", points[0])
print("Type:", type(points[0]))

m = folium.Map(
    location=[54.5, -3],
    zoom_start=6,
    tiles="CartoDB positron"
)

HeatMap(
    points,
    radius=12,
    blur=10,
    min_opacity=0.3
).add_to(m)

m.save(OUT)

print(f"saved {OUT}")
# /// script
# requires-python = ">=3.10"
# dependencies = ["folium"]
# ///

from pathlib import Path
import json
import folium


HERE = Path(__file__).parent
DATA = HERE / "data" / "uk-house-sparrow-2026.json"
OUT = HERE / "out" / "plot.html"


data = json.loads(DATA.read_text(encoding="utf-8"))

points = [
    [r["decimalLatitude"], r["decimalLongitude"]]
    for r in data["results"]
    if "decimalLatitude" in r and "decimalLongitude" in r
]

# Use a UK-centered map view that allows regular zooming and clear point markers.
m = folium.Map(
    location=[54.5, -3.0],
    zoom_start=5,
    min_zoom=3,
    max_zoom=12,
    zoom_control=True,
    control_scale=True,
    prefer_canvas=True,
)
folium.TileLayer(
    tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    attr='&copy; OpenStreetMap contributors &copy; CARTO',
    name="CartoDB Light",
    max_zoom=20,
    subdomains="abcd",
).add_to(m)

for lat, lon in points:
    folium.CircleMarker(
        location=[lat, lon],
        radius=3,
        color="#d62728",
        fill=True,
        fill_color="#d62728",
        fill_opacity=0.8,
        weight=0.8,
    ).add_to(m)

m.save(OUT, close_file=True)

print(f"saved {OUT}")
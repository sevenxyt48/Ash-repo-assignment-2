# /// script
# requires-python = ">=3.10"
# dependencies = ["folium"]
# ///

from pathlib import Path
import json
import folium
from folium.plugins import MarkerCluster


HERE = Path(__file__).parent
DATA = HERE / "data" / "uk-house-sparrow-2026.json"
OUT = HERE / "out" / "plot.html"


data = json.loads(DATA.read_text(encoding="utf-8"))

points = [
    [r["decimalLatitude"], r["decimalLongitude"]]
    for r in data["results"]
    if "decimalLatitude" in r and "decimalLongitude" in r
]

m = folium.Map(
    location=[54.5, -3.0],
    zoom_start=5,
    min_zoom=3,
    max_zoom=14,
    zoom_control=True,
    control_scale=True,
    prefer_canvas=True,
    tiles=None,
)

folium.TileLayer(
    tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    attr='&copy; OpenStreetMap contributors &copy; CARTO',
    name="CartoDB Light",
    max_zoom=20,
    subdomains="abcd",
).add_to(m)

# The plugin re-clusters live as you zoom: many small clusters merge into
# fewer big ones zoomed out, and split apart as you zoom in — no Python
# rebinning needed. Below disableClusteringAtZoom, points show individually.
icon_create_function = """
function(cluster) {
    var count = cluster.getChildCount();
    var c = ' marker-cluster-';
    if (count < 10) { c += 'small'; }
    else if (count < 50) { c += 'medium'; }
    else { c += 'large'; }
    return new L.DivIcon({
        html: '<div><span>' + count + '</span></div>',
        className: 'marker-cluster' + c,
        iconSize: new L.Point(40, 40)
    });
}
"""

cluster = MarkerCluster(
    icon_create_function=icon_create_function,
    maxClusterRadius=45,       # how aggressively nearby points merge
    disableClusteringAtZoom=11,  # zoom in past this and see raw points
    spiderfyOnMaxZoom=True,
    showCoverageOnHover=False,
).add_to(m)

for lat, lon in points:
    folium.CircleMarker(
        location=[lat, lon],
        radius=4,
        color="#3d4d47",
        fill=True,
        fill_color="#64766a",
        fill_opacity=0.8,
        weight=0.6,
    ).add_to(cluster)

# Recolor the plugin's default blue/yellow/orange bubbles to match your
# muted green density palette.
m.get_root().html.add_child(folium.Element("""
<style>
.marker-cluster-small  { background-color: rgba(184, 197, 180, 0.75); }
.marker-cluster-small div  { background-color: rgba(142, 160, 143, 0.9); }
.marker-cluster-medium { background-color: rgba(100, 118, 106, 0.75); }
.marker-cluster-medium div { background-color: rgba(80, 98, 86, 0.9); }
.marker-cluster-large  { background-color: rgba(61, 77, 71, 0.8); }
.marker-cluster-large div  { background-color: rgba(45, 58, 53, 0.95); }
.marker-cluster div span { color: #fdfdfb; font-weight: 600; font-family: sans-serif; }
</style>
"""))

m.save(OUT, close_file=True)
print(f"saved {OUT} with {len(points)} points")
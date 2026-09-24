# The phenomenon

(out/plot.html) is the real picture — it's an interactive map, so GitHub can only show a screenshot above. Open the HTML file in a browser to zoom and watch the clusters split apart.
## The phenomenon

<!-- What goes up and down, and why you looked at it. -->
I looked at the distribution of House Sparrow observations in the United Kingdom in 2026. I chose this phenomenon because bird observations can show where a species is recorded more often in different parts of the country. I wanted to see whether the observations are spread evenly across the UK or concentrated in particular areas.

## The source

<!-- A link to the page or endpoint the file came from, and one line on what is in
the file: how many rows, what a row means, what the units are. -->
The data comes from the GBIF Occurrence Search API. The dataset contains 3,512 records for Passer domesticus (House Sparrow) in the United Kingdom in 2026. I filtered the records to include only observations marked as present and records with geographic coordinates. Each record represents one observation, with latitude and longitude showing where it was recorded.

Source: https://api.gbif.org/v1/occurrence/search

## What the picture shows

The map groups nearby sightings into clusters, each labelled with a count, so density is readable at a glance instead of getting lost under thousands of overlapping dots. Zooming in splits a cluster into smaller ones, and past a certain zoom level the individual sightings show up on their own.

The picture does not show the actual number of House Sparrows living in each area. It only shows recorded observations in GBIF, so areas with more records may partly reflect differences in observation effort and data collection, not just bird density.

## Run it

```
uv run fetch.py
uv run plot.py
```
plot.py builds the map and imports page.py to add the title, frame, and source footer around it — page.py doesn't run on its own.
# The phenomenon

<!-- This is the SD5913 assignment 2 template. Everything in this file is yours to
replace, and the check counts words: comments like this one are not words, so
delete each one as you write. Start with the heading: name the phenomenon.

Then, in this order, at least 150 words in total.

New to folders, paths, or the files here whose names start with a dot? Read
https://github.com/sd5913/pfad/blob/2026/reference/files.md first. Ten minutes. -->

![what the picture is](out/plot.png)

## The phenomenon

<!-- What goes up and down, and why you looked at it. -->
I looked at the distribution of House Sparrow observations in the United Kingdom in 2026. I chose this phenomenon because bird observations can show where a species is recorded more often in different parts of the country. I wanted to see whether the observations are spread evenly across the UK or concentrated in particular areas.

## The source

<!-- A link to the page or endpoint the file came from, and one line on what is in
the file: how many rows, what a row means, what the units are. -->
The data comes from the GBIF Occurrence Search API. The dataset contains 3,512 records for Passer domesticus (House Sparrow) in the United Kingdom in 2026. I filtered the records to include only observations marked as present and records with geographic coordinates. Each record represents one observation, with latitude and longitude showing where it was recorded.

Source: https://api.gbif.org/v1/occurrence/search

## What the picture shows

The map shows where House Sparrow observations were recorded across the UK. The points make it easier to see areas where observations are more concentrated.

The picture does not show the actual number of House Sparrows living in each area. It only shows recorded observations in GBIF, so areas with more records may partly reflect differences in observation and data collection.

## Run it

```
uv run fetch.py
uv run plot.py
```

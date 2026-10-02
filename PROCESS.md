# Process

## Tools

I used Gemini to talk through the assignment brief and clarify what was required. I used ChatGPT to search for data sources and to write and iterate on `fetch.py` and `plot.py` — picking the map API, shaping the request, and getting the first working version of the map. I used Claude to rework the map's UI once the layout and interaction were unusable: switching to clustering so the map stays readable and responsive at every zoom level, and adding the title/frame/footer around it.

## Kept

ChatGPT's suggestion to narrow the dataset down to a single species instead of the three most-recorded ones. The combined dataset was large enough that the map became cluttered and slow, and one species was still enough to show a real pattern. Cutting the scope was the right call — it's a better assignment 2 than a bigger, messier one would have been.

## Rejected

At the beginning of the project, I wanted to visualise where auroras occurred on a map. ChatGPT suggested several ways to approach the visualisation, but I could not find suitable data or a good way to present it, so I rejected this direction and looked for another dataset. I then found bird occurrence data on GBIF and asked ChatGPT whether it was suitable. It suggested using bird data from Southeast Asia, but GBIF did not have the regional data I needed, so I switched to UK bird data. Since the dataset was very large, I was concerned that downloading too many records would take too long. ChatGPT suggested using three species: House Sparrow, Blue Tit, and Starling, but I still felt that the amount of data would be too large, so I rejected this suggestion and used only House Sparrow, the most-recorded species. ChatGPT also initially suggested a map API that did not have permission to display the map, so I asked it to replace the API with another one that worked.
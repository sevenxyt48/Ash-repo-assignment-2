# Process

## Tools

I used Gemini to talk through the assignment brief and get my head around what was being asked. I used ChatGPT to search for data sources and to write and iterate on `fetch.py` and `plot.py` — picking the API, shaping the request, and getting the first working version of the map. I used Claude to rework the map's UI once the layout and interaction were unusable: switching to clustering so the map stays readable and responsive at every zoom level, and adding the title/frame/footer around it.

## Kept

ChatGPT's suggestion to narrow the dataset down to a single species instead of the three most-recorded ones. The combined dataset was large enough that the map became cluttered and slow, and one species was still enough to show a real pattern. Cutting the scope was the right call — it's a better assignment 2 than a bigger, messier one would have been.

## Rejected

ChatGPT's suggestion to use bird distribution data for Southeast Asian countries, and my own original idea of aurora sightings. Both looked promising on paper but neither had an actual file behind them: I could not find a working, accessible dataset for Southeast Asian bird distribution, and the aurora data I did find produced bad or empty output. Chasing them cost time before I switched to something with a real, working file — the UK's GBIF House Sparrow records — which is exactly the "change the phenomenon, not the amount of time" rule in the brief.
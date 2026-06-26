---
name: weather-info
description: Fetches real-time, live weather data, temperature, and wind speed for a given city. Use this whenever the user asks about current weather conditions.
---

# Weather Information Skill

You have access to a local Python script that fetches live weather data from the Open-Meteo API. 

## How to get the weather

When the user asks for the weather in a specific city, you must execute the provided script using your bash/terminal tool. 

Run this exact command:
`python ../default_workspace/skills/weather-info/scripts/fetch_weather.py "<city_name>"`

**Rules:**
1. Wait for the script to output the data.
2. Read the standard output from the terminal.
3. Reply to the user naturally using the exact temperature and wind speed provided by the script.

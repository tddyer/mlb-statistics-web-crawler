# MLB-Player-Rater
Ever wonder just how good your favorite baseball player is? Well now you can know thanks to this MLB player rater!

## What?
A web scraper that gathers lifetime statistics for every active MLB player and then uses those statistics to generate an accurate overall rating for that player

## Why?
I have begun to develop a passion for data analysis/web scraping and I figured what better way to explore it than with my favorite sport, baseball.

## How?
The project is written in python3 and uses both Beautiful Soup 4 and pandas to scrape information from two sites: (1) mlb.com for base statistics as well as team rosters and (2) baseballsavant.mlb.com for in-depth player statistics. 
  - Once the stats are gathered, they are sorted by positional category (position player or pitcher) as well as by team, and then stored in a json file (30 in total, one for each team).
  - From there, the stats can easily be accessed from the json files to be analyzed for player ratings.

## Current state:
- All statistics have been scraped, cleaned, and stored in json files.

## In progress:
- Currently working on generating the player rating algorithms which will use statistical analysis to form an overall rating for each individual player. 
  - Overall rating will be formed from multiple sub ratings in the following categories:
    - Contact
    - Power
    - Clutch
    - Plate Discipline
    - Plate Vision
    - Speed
    - Baserunning Ability
    - Baserunning Aggressivenes
    - Fielding
    - Durability
    
## Future updates:
- Move from json file to local database storage
- Optimize web scraper (I am aware it can most likely be greatly improved from current state)

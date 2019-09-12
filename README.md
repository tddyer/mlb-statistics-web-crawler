# MLB-Player-Rater
Ever wonder just how good your favorite baseball player is? Well now you can know thanks to this MLB player rater!

## What?
A web scraper that aggregates lifetime statistics for every active player in the MLB and then uses those statistics to generate an accurate overall rating for that player.

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

## Setup
Current state only allows for data scraping. I have provided a set of scraped statistics as of 09-12-2019, but these can be updated at any point by running the main.py file
  - NOTE: the web scraper takes quite a while to gather all of the statistics as it is gathering data for all 30 teams, each with over 30 players, each with 2 separate web pages to parse. That being said, if you don't have very reliable internet connection, the parser will most likely fail at some point during the process. This is a bug I intend to fix in the future by allowing for individual team or player parsing so you don't have to parse so much data at one time. Currently I have it split up by league, AL and NL. 
    
## Future updates:
- Move from json file to local database storage
- Optimize web scraper (I am aware it can most likely be greatly improved from current state)

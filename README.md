# MLB Statistics Web Crawler

A web crawler that gathers lifetime player hitting statistics for all active MLB players (500+ players).

## Directory Organization

- Code for the web crawler can be found in 'mlb_scraper/mlb_scraper/spiders/current-players-spider.py'
- The scraped player data is stored in the 'Data' directory, where there is a directory for each team containing that team's player .csv files

## Scraping Process

1. The web crawler starts by going through every MLB teams hitting statistics page on mlb.com (see "Data Sources" section for an example url), which lists the current active players on that team and their year-to-date hitting stats. Using the list of players, it grabs each player's unique player link, which contains the player's name and identification number, and compiles a list of these links for each team. 
    - NOTE: The unique player links are consistent across all of the MLB statistics pages and can be used to identify each player.
2. Using the list of player links, the crawler then navigates to each player's Baseball Savant statistic page, which provides more in-depth stats than the general stats that were listed on the MLB team page.
3. Once on the Baseball Savant page, the crawler finds the data tables that contain the both the player's lifetime standard hitting statistics (titled "Standard MLB Batting Statistics"), as well as the player's lifetime advanced hitting statistics (titled "Advanced MLB Batting Statistics").
4. After the tables are scraped, they are stored in a .csv file for that player. Each player gets their own .csv file and they are organized within a directory that contains only players on their team.

## Tools + Technologies

- Web crawling/data scraping -> Scrapy (Python)
- Data storage (current) -> .csv files

## Data Sources

- mlb.com team statistic pages (eg: https://www.mlb.com/stats/chicago-cubs?playerPool=ALL)
  - 30 total team pages, each with roughly 15-25 players listed
- mlb.com Baseball Savant player statistic pages (eg: https://baseballsavant.mlb.com/savant-player/mike-trout-545361?stats=career-r-hitting-mlb)
  - each player has a Baseball Savant page, amounting to over 500 pages
  
## Performance

Given Scrapy's asynchronous functionality, the web crawler performs pretty efficiently in its current state. 
- On my machine (HP Spectre x360, 4 processors, 16 GB RAM, running Ubuntu 18.04) it completes in about a minute on average.
- I'm not an expert in web scraping, but given that it scrapes data from 500+ web pages, it is more than efficient enough for my purposes. However, I'm sure it can still be improved and in the future I may consider optimizing its performance.

## Future Updates

- Improve data storage techniques
  - Having 500+ .csv files is not optimal
  - Potential options: Database storage (SQL or FireBase) or Google Sheets (use the Python Google Sheets API - https://developers.google.com/sheets/api/quickstart/python - to mimick a database)
- Optimize performance



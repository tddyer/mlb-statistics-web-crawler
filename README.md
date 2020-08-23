# MLB Stats Scraper

A web scraper that gathers lifetime player statistics for all active MLB players

## Current Status

Web crawler currently scrapes lifetime hitting statistics for all active players (active players being those who have had an at-bat in the current season) in the MLB.

## Tools + Technologies

- Data scraping -> Scrapy (Python)
- Data storage -> Database (MongoDB or PostgreSQL) OR file storage (Json) OR Google Sheets (mimicks a database)

## Data Sources

- mlb.com team statistic pages (eg: https://www.mlb.com/stats/chicago-cubs?playerPool=ALL)
  - scrapes links to all active players baseballsavant statistics page for each team
- mlb.com baseballsavant player statistic pages (eg: https://baseballsavant.mlb.com/savant-player/mike-trout-545361?stats=career-r-hitting-mlb)
  - scrapes players lifetime hitting statistics - both standard and advanced



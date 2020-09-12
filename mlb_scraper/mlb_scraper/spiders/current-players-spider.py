import multiprocessing
import pandas as pd
import scrapy
import os


class CurrentPlayersSpider(scrapy.Spider):
    name = "current-players"

    # starts the scraping process by navigating to each team's stats page, then recursively calls the parse method on each page
    def start_requests(self):
        teams = ['los-angeles-angels', 'houston-astros', 'oakland-athletics', 'toronto-blue-jays',
                 'atlanta-braves', 'milwaukee-brewers', 'st-louis-cardinals', 'chicago-cubs',
                 'arizona-diamondbacks', 'los-angeles-dodgers', 'san-francisco-giants', 'cleveland-indians',
                 'seattle-mariners', 'miami-marlins', 'new-york-mets', 'washington-nationals',
                 'baltimore-orioles', 'san-diego-padres', 'philadelphia-phillies', 'pittsburgh-pirates',
                 'texas-rangers', 'tampa-bay-rays', 'boston-red-sox', 'cincinnati-reds',
                 'colorado-rockies', 'kansas-city-royals', 'detroit-tigers', 'minnesota-twins',
                 'chicago-white-sox', 'new-york-yankees']

        # list of urls for all mlb teams
        urls = [
            'https://www.mlb.com/stats/' + team + '/at-bats?playerPool=ALL' for team in teams
        ]

        # recursive calls to parse method
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    # parses team stats pages to gather list of unique player links that will be used for gathering player stats, 
    # then recursively calls parse_player method for each player
    def parse(self, response):
        team_name = response.url.split("/")[-2]
        names = response.css('span.full-3fV3c9pF::text').getall()
        player_links = response.css('a.bui-link::attr(href)').getall()[4::]

        # check if team has existing directory in data directory
        if not os.path.exists('../data/%s' % team_name):
            os.makedirs('../data/%s' % team_name)

        i = 0
        url_start = 'https://baseballsavant.mlb.com/savant-player/'
        url_end = '?stats=career-r-hitting-mlb'
        while i < len(names) - 1:
            # generate player url to be scraped
            player_name = names[i].lower() + '-' + names[i + 1].lower()
            player_info = '-'.join([player_name, player_links[i // 2][-6::]])
            player_url = url_start + player_info + url_end
            i += 2
            # scrape player page
            yield scrapy.Request(url=player_url, callback=self.parse_player,
                                 meta={'player_name': player_name, 'team_name': team_name})


    # parses player Baseball Savant pages and scrapes their lifetime standard hitting stats + lifetime advanced hitting stats
    def parse_player(self, response):
        player_name = response.meta['player_name'].lower()
        team_name = response.meta['team_name'].lower()

        # getting player statistic tables
        hitting = response.css('#hittingStandard.standard-mlb')
        hitting_table = hitting.css('table')[0]
        rows = hitting_table.xpath('//tr')
        rows = [row for row in rows if 'hittingStandard-' in str(row)]
        
        all_table_rows = [] # will store data for rows from both data tables
        num_seasons = 1 # number of seasons played for this player

        # getting hitting table headers
        table_head = hitting_table.xpath('//thead')
        head = table_head[0]
        ths = head.xpath('//th')
        ths = [th for th in ths if 'hittingStandard_' in str(th)]

        table_headers = [] 
        for th in ths:
          header = th.xpath('text()').extract()
          if header and header[0] not in table_headers:
            table_headers.append(header[0])

        # getting clean format of data for each table
        for row in rows:
            text = row.xpath('td//text()').extract()
            text = [i for i in text if i != ' ']
            if '*' in text:
                text.remove('*')

            temp = []
            for item in text:
                temp.append(item)
                if 'Seasons' in item:
                    num_seasons = int(item[0:item.index(' ')])

            all_table_rows.append(temp)
        
        # combining clean data from tables into single table (standard + advanced)
        new_table = self.combine_tables(all_table_rows, num_seasons)

        # writing headers + cleaned data to file
        with open('../data/{}/{}-combined.csv'.format(team_name, player_name), 'w') as f:
            for ind in range(len(table_headers)):
                if ind == len(table_headers) - 1:
                    f.write(table_headers[ind] + '\n')
                else:
                    f.write(table_headers[ind] + ', ')
            
            for row in new_table:
                for ind in range(len(row)):
                    if ind == len(row) - 1:
                        f.write(row[ind] + '\n')
                    else:
                        f.write(row[ind] + ', ')
            f.close()


    # method for combining the standard and advanced data tables into one
    # NOTE: players who have had seasons in which they've played for more than one team have different tables that 
    # need to be handled differently: 
    #   - every season with multi-teams adds 2 extra rows to the table
    #   (i.e multi_team_years * 2 total additional rows that need to be accounted for)
    def combine_tables(self, all_table_rows, num_seasons): 
        total = len(all_table_rows)
        new_table = []

        # players who haven't had multi-team seasons
        if total == (num_seasons * 2 + 2): 
            for i in range(num_seasons + 1):
                # combining career total rows
                if i == num_seasons:
                    totals = all_table_rows[i]
                    totals.extend(all_table_rows[-1]) 
                    new_table.append(totals)
                    break

                # combine standard + advanced rows for each year
                standard = all_table_rows[i]
                advanced = all_table_rows[i + num_seasons + 1]
                combined = standard.copy()
                combined.extend(advanced[3::])
                new_table.append(combined)
        else: # players who have had multi-team seasons
            multi_team_years = str(all_table_rows).count('2 Teams') // 2 # total number of seasons with multi-teams
            to_skip = 'filler' # used to skip additional rows added from multi-team years

            for j in range((num_seasons + 1) + (multi_team_years * 2)):
                if to_skip in all_table_rows[j][0]:
                    continue

                # combines career total rows
                if 'Seasons' in all_table_rows[j][0]:
                    totals = all_table_rows[j]
                    totals.extend(all_table_rows[-1]) 
                    new_table.append(totals)
                    break

                # handles multi-team seasons
                if '2 Teams' in all_table_rows[j][1]:
                    to_skip = all_table_rows[j][0]
                    for n in range(j, j+3):
                        standard = all_table_rows[n]
                        advanced = all_table_rows[n + num_seasons + 1 + (multi_team_years * 2)]
                        combined = standard.copy()
                        combined.extend(advanced[3::])
                        new_table.append(combined)
                else:
                    standard = all_table_rows[j]
                    advanced = all_table_rows[j + num_seasons + 1 + (multi_team_years * 2)]
                    combined = standard.copy()
                    combined.extend(advanced[3::])
                    new_table.append(combined)
        
        return new_table
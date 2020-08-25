import pandas as pd
import scrapy
import os


class CurrentPlayersSpider(scrapy.Spider):
    name = "current-players"

    def start_requests(self):
        teams = ['los-angeles-angels', 'houston-astros', 'oakland-athletics', 'toronto-blue-jays', 
            'atlanta-braves', 'milwaukee-brewers', 'st-louis-cardinals', 'chicago-cubs',
            'arizona-diamondbacks', 'los-angeles-dodgers', 'san-francisco-giants', 'cleveland-indians',
            'seattle-mariners', 'miami-marlins', 'new-york-mets', 'washington-nationals', 
            'baltimore-orioles', 'san-diego-padres', 'philadelphia-phillies', 'pittsburg-pirates',
            'texas-rangers', 'tampa-bay-rays', 'boston-red-sox', 'cincinnati-reds',
            'colorado-rockies', 'kansas-city-royals', 'detroit-tigers', 'minnesota-twins',
            'chicago-white-sox', 'new-york-yankees']

        # list of urls for all mlb teams
        urls = [
            'https://www.mlb.com/stats/' + team + '/at-bats?playerPool=ALL' for team in teams
        ]

        # break urls into groups to prevent opening too many urls at once
        for url in urls[0:10]:
            yield scrapy.Request(url=url, callback=self.parse)
        
        for url in urls[10:20]:
            yield scrapy.Request(url=url, callback=self.parse)
        
        for url in urls[20::]:
            yield scrapy.Request(url=url, callback=self.parse)

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
                                    meta={'player_name': player_name, 'team_name':team_name})

    #TODO: grab row headers for csv files
    def parse_player(self, response):
        player_name = response.meta['player_name'].lower()
        team_name = response.meta['team_name'].lower()

        # getting player statistic tables
        hitting = response.css('#hittingStandard.standard-mlb')
        hitting_table = hitting.css('table')[0]
        rows = hitting_table.xpath('//tr')
        rows = [row for row in rows if 'hittingStandard-' in str(row)]

        # write stats to player .csv file
        with open('../data/{}/{}.csv'.format(team_name, player_name), 'w') as f:
            for row in rows:
                text = row.xpath('td//text()').extract()
                text = [i for i in text if i != ' ']
                if '*' in text:
                    text.remove('*')
                for item in text:
                    data = item + ', '
                    f.write(data)
                f.write('\n')
            f.close()
        
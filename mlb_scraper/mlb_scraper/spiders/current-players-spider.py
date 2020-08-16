import pandas as pd
import scrapy
import os


class CurrentPlayersSpider(scrapy.Spider):
    name = "current-players"


    def start_requests(self):
        teams = ['los-angeles-angels']#, 'houston-astros', 'oakland-athletics', 'toronto-blue-jays', 
            # 'atlanta-braves', 'milwaukee-brewers', 'st-louis-cardinals', 'chicago-cubs',
            # 'arizona-diamondbacks', 'los-angeles-dodgers', 'san-francisco-giants', 'cleveland-indians',
            # 'seattle-mariners', 'miami-marlins', 'new-york-mets', 'washington-nationals', 
            # 'baltimore-orioles', 'san-diego-padres', 'philadelphia-phillies', 'pittsburg-pirates',
            # 'texas-rangers', 'tampa-bay-rays', 'boston-red-sox', 'cincinnati-reds',
            # 'colorado-rockies', 'kansas-city-royals', 'detroit-tigers', 'minnesota-twins',
            # 'chicago-white-sox', 'new-york-yankees']

        # list of urls for all mlb teams
        urls = [
            'https://www.mlb.com/stats/' + team + '/at-bats?playerPool=ALL' for team in teams
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        team_name = response.url.split("/")[-2]
        # filename = '%s.csv' % page
        names = response.css('span.full-3fV3c9pF::text').getall()
        playerLinks = response.css('a.bui-link::attr(href)').getall()[4::]

        # check if team has existing directory in data directory
        if not os.path.exists('../data/%s' % team_name):
            os.makedirs('../data/%s' % team_name)

        i = 0
        j = 0
        # with open('../data/{}/{}'.format(page, filename), 'w') as f:
            #f.write('name, url\n')
        print(names)
        while i < len(names) - 1:
            player_url = response.urljoin(playerLinks[j])
            player_name = names[i] + '-' + names[i + 1]
            i += 2
            j += 1
            # scrape player page
            yield scrapy.Request(url=player_url, callback=self.parse_player, 
                                    meta={'player_name': player_name, 'team_name':team_name})


    def parse_player(self, response):
        player_name = response.meta['player_name'].lower()
        team_name = response.meta['team_name'].lower()
        # dfs = pd.read_html(response.url)
        with open('../data/{}/{}.csv'.format(team_name, player_name), 'w') as f:
            f.write(player_name + ', ' + team_name + '\n')
            f.close()
        
from bs4 import BeautifulSoup
#import rating_scripts
import pandas as pd
import urllib
import json
import re


TEAM_IDS = {'Arizona Diamondbacks':'109', 'Atlanta Braves':'144', 'Baltimore Orioles':'110', 'Boston Red Sox':'111', 'Chicago Cubs':'112', 'Chicago White Sox':'145',
            'Cincinnati Reds':'113', 'Cleveland Indians':'114', 'Colorado Rockies':'115', 'Detroit Tigers':'116', 'Houston Astros':'117', 'Kansas City Royals':'118',
            'Los Angeles Angels':'108', 'Los Angeles Dodgers':'119', 'Miami Marlins':'146', 'Milwaukee Brewers':'158', 'Minnesota Twins':'142', 'New York Mets':'121',
            'New York Yankees':'147', 'Oakland Athletics':'133', 'Philadelphia Phillies':'143', 'Pittsburg Pirates':'134', 'San Diego Padres':'135', 'San Francisco Giants':'137',
            'Seattle Mariners':'136', 'St. Louis Cardinals':'138', 'Tampa Bay Rays':'139', 'Texas Rangers':'140', 'Toronto Blue Jays':'141', 'Washington Nationals':'120'}

# generates BeautifulSoup soup object
def soup_gen(url):
    html_page = urllib.request.urlopen(url)
    return BeautifulSoup(html_page, features='lxml')

# generates pandas dataframes
def df_gen(url):
    return pd.read_html(url)

# saves dictionary to json file
def save_dict_to_json(filename, dict):
    with open(filename, 'w') as outfile:
        json.dump(dict, outfile)

# opens json file and returns dict from json object
def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
        return data

# retrieves every individual player's baseballsavant stat page link for the given team and returns them in a list
def get_player_pages(team_id):

    player_links = []

    # getting team url
    url_start = "http://m.mlb.com/stats/?stat_type=hitting&season=2019&team_option="
    url_end = "&game_type=R&sort_column=era&player_pool=ALL"
    url = url_start + team_id + url_end

    soup = soup_gen(url)

    for link in soup.findAll('a', attrs={'href': re.compile("/player/")}):
        temp_str = str(link)[str(link).find('"'):str(link).rfind('"')]
        name = temp_str[temp_str.rfind('/') + 1::]
        player_id = temp_str[9:temp_str.rfind('/')]
        player_links.append('https://baseballsavant.mlb.com/savant-player/' + name + '-' + player_id)

    return player_links

# retrieves and returns a list of player vitals (name, postion, bats/throws, height/weight, age, draft, hometown)
def get_vitals(player_link):
    soup = soup_gen(player_link)
    info = soup.find('div', attrs={'class': "info"})
    vitals = [text for text in info.stripped_strings]

    for i in vitals:
        if i == '|' or i == 'Show Random Video':
            vitals.remove(i)

    for j in range(len(vitals)):
        if vitals[j] == 'Draft:':
            vitals[j] += ' ' + vitals[j+1] + ' ' + vitals[j+2] + ' ' + vitals[j+3] + ' ' + vitals[j+4]
            vitals.remove(vitals[j+4])
            vitals.remove(vitals[j+3])
            vitals.remove(vitals[j+2])
            vitals.remove(vitals[j+1])
            break

    return vitals

# returns a list containing a dictionary of the given players lifetime stats for stat categories
# to be used in rating generation as well as a list of secondary positions for that player
def get_lifetime_hitter_data(player_link, position):
    dfs = df_gen(player_link)
    lifetime_data = {}
    secondary_pos = []

    # selecting relevant dataframes
    for df in dfs:
        # Latest Transactions chart for current player (gets time injured and number of injuries)
        if 'Transaction' in df.columns:
            lifetime_data['Days injured'] = 0
            lifetime_data['Number of injuries'] = 0
            for row in range(len(df.index)):
                if type(df.iloc[row][2]) == str and '-day' in df.iloc[row][2] and 'placed' in df.iloc[row][2]:
                    lifetime_data['Days injured'] += int(df.iloc[row][2][df.iloc[row][2][:df.iloc[row][2].rfind('-day')].rfind(' ') + 1:df.iloc[row][2].rfind('-day')])
                    lifetime_data['Number of injuries'] += 1
                elif type(df.iloc[row][2]) == str and 'transferred' in df.iloc[row][2] and '-day' in df.iloc[row][2]:
                    lifetime_data['Days injured'] -= int(df.iloc[row][2][df.iloc[row][2][:df.iloc[row][2].find('-day')].rfind(' ') + 1:df.iloc[row][2].find('-day')])
                    lifetime_data['Days injured'] += int(df.iloc[row][2][df.iloc[row][2][:df.iloc[row][2].rfind('-day')].rfind(' ') + 1:df.iloc[row][2].rfind('-day')])

        # Standard MLB Batting Statistics chart
        elif 'LG' in df.columns and 'L' not in df.columns and '3B' in df.columns:
            df.columns = df.columns.str.strip().str.replace('\n', '')
            df = df.drop(['Unnamed: 0', 'Tm', 'LG'], axis=1)
            for col in list(df):
                if col == 'Season':
                    lifetime_data['Seasons'] = int(df.ix[len(df.index)-1][col][:df.ix[len(df.index)-1][col].find(' ')])
                elif float(df.ix[len(df.index) - 1][col]) > 1 and float(df.ix[len(df.index) - 1][col]) / int(float(df.ix[len(df.index) - 1][col])) == 1:
                    lifetime_data[col] = int(df.ix[len(df.index) - 1][col])
                else:
                    lifetime_data[col] = round(float(df.ix[len(df.index) - 1][col]), 3)

        # Advanced MLB Batting Statistics chart
        elif 'LG' in df.columns and 'L' not in df.columns and 'BB/K' in df.columns:
            df.columns = df.columns.str.strip().str.replace('\n', '')
            df = df.drop(['Season', 'Tm', 'LG'], axis=1)
            for col in list(df):
                if float(df.ix[len(df.index) - 1][col]) > 1 and float(df.ix[len(df.index) - 1][col]) / int(float(df.ix[len(df.index) - 1][col])) == 1:
                    lifetime_data[col] = int(df.ix[len(df.index) - 1][col])
                else:
                    lifetime_data[col] = round(float(df.ix[len(df.index) - 1][col]), 3)

        # Statcast Batting chart
        elif 'Batted Balls' in df.columns:
            df.columns = df.columns.str.strip().str.replace('\n', '')
            df = df.drop('Season', axis=1)
            if 'Batted Balls' not in lifetime_data.keys():
                for col in list(df):
                    if float(df.ix[len(df.index) - 2][col]) > 1 and float(df.ix[len(df.index) - 2][col]) / int(float(df.ix[len(df.index) - 2][col])) == 1:
                        lifetime_data[col] = int(df.ix[len(df.index) - 2][col])
                    else:
                        lifetime_data[col] = round(float(df.ix[len(df.index) - 2][col]), 3)

        # Standard MLB Fielding Statistics chart
        elif 'LG' in df.columns and 'L' not in df.columns and 'FPCT%' in df.columns:
            df.columns = df.columns.str.strip().str.replace('\n', '')
            cutoff = len(df.index) - 1
            for i in range(len(df.index) - 1):
                if type(df.ix[i]['Season']) != float and 'Season' in df.ix[i]['Season']:
                    cutoff = i
            if cutoff == len(df.index) - 1:
                lifetime_data['FPCT %'] = float(df.ix[len(df.index)-1]['FPCT%'])
            else:
                df = df.iloc[cutoff:,]
                for r in range(len(df.index)):
                    if position in df.ix[r + cutoff].any():
                        lifetime_data['FPCT %'] = float(df.ix[r + cutoff]['FPCT%'])
                    if str(df.ix[r + cutoff]['LG']) == 'nan':
                        secondary_pos.append(df.ix[r + cutoff]['POS'])

        # Statcast Running Statistics chart
        elif 'Sprint Speed (ft/s)' in df.columns:
            df.columns = df.columns.str.strip().str.replace('\n', '')
            if str(df.ix[len(df.index)-1]['% Rank']) != 'nan':
                lifetime_data['% Rank'] = float(df.ix[len(df.index)-1]['% Rank'])
            else:
                lifetime_data['% Rank'] = float(df.ix[len(df.index)-2]['% Rank'])

        # Statcast Plate Discipline chart
        elif 'Chase %' in df.columns:
            df.columns = df.columns.str.strip().str.replace('\n', '')
            df = df.drop(['Season', 'Pitches'], axis=1)
            for col in list(df):
                if float(df.ix[len(df.index) - 2][col]) > 1 and float(df.ix[len(df.index) - 2][col]) / int(float(df.ix[len(df.index) - 2][col])) == 1:
                    lifetime_data[col] = int(df.ix[len(df.index) - 2][col])
                else:
                    lifetime_data[col] = round(float(df.ix[len(df.index) - 2][col]), 3)

    return [lifetime_data, secondary_pos]

# returns a list containing the given pitcher's liftime stats used for their rating calculation
# as well as a list of secondary positions for that player
def get_lifetime_pitcher_data(player_link, position):
    dfs = df_gen(player_link)
    lifetime_data = {}
    secondary_pos = []

    # selecting dataframes used for rating calculations
    for df in dfs:
        # Latest Transactions chart for current player (gets time injured and number of injuries)
        if 'Transaction' in df.columns:
            lifetime_data['Days injured'] = 0
            lifetime_data['Number of injuries'] = 0
            for row in range(len(df.index)):
                if type(df.iloc[row][2]) == str and '-day' in df.iloc[row][2] and 'placed' in df.iloc[row][2]:
                    lifetime_data['Days injured'] += int(df.iloc[row][2][df.iloc[row][2][:df.iloc[row][2].rfind('-day')].rfind(' ') + 1:df.iloc[row][2].rfind('-day')])
                    lifetime_data['Number of injuries'] += 1
                elif type(df.iloc[row][2]) == str and 'transferred' in df.iloc[row][2] and '-day' in df.iloc[row][2]:
                    lifetime_data['Days injured'] -= int(df.iloc[row][2][df.iloc[row][2][:df.iloc[row][2].find('-day')].rfind(' ') + 1:df.iloc[row][2].find('-day')])
                    lifetime_data['Days injured'] += int(df.iloc[row][2][df.iloc[row][2][:df.iloc[row][2].rfind('-day')].rfind(' ') + 1:df.iloc[row][2].rfind('-day')])

        # Standard MLB Batting Statistics chart
        if 'LG' in df.columns and 'L.1' not in df.columns and 'SO' in df.columns and 'BB' in df.columns and 'ERA' in df.columns:
            df.columns = df.columns.str.strip().str.replace('\n', '')
            df = df.drop(['Unnamed: 0', 'Tm', 'LG'], axis=1)
            for col in list(df):
                if col == 'Season':
                    lifetime_data['Seasons'] = int(df.ix[len(df.index)-1][col][:df.ix[len(df.index)-1][col].find(' ')])
                elif float(df.ix[len(df.index) - 1][col]) > 1 and float(df.ix[len(df.index) - 1][col]) / int(float(df.ix[len(df.index) - 1][col])) == 1:
                    lifetime_data[col] = int(df.ix[len(df.index) - 1][col])
                else:
                    lifetime_data[col] = round(float(df.ix[len(df.index) - 1][col]), 3)

        # Statcast Pitching chart
        elif 'Batted Balls' in df.columns:
            df.columns = df.columns.str.strip().str.replace('\n', '')
            df = df.drop('Season', axis=1)
            if 'Batted Balls' not in lifetime_data.keys():
                for col in list(df):
                    if float(df.ix[len(df.index) - 2][col]) > 1 and float(df.ix[len(df.index) - 2][col]) / int(float(df.ix[len(df.index) - 2][col])) == 1:
                        lifetime_data[col] = int(df.ix[len(df.index) - 2][col])
                    else:
                        lifetime_data[col] = round(float(df.ix[len(df.index) - 2][col]), 3)

        # Standard MLB Fielding Statistics chart
        elif 'LG' in df.columns and 'L' not in df.columns and 'FPCT%' in df.columns:
            df.columns = df.columns.str.strip().str.replace('\n', '')
            cutoff = len(df.index) - 1
            for i in range(len(df.index) - 1):
                if type(df.ix[i]['Season']) != float and 'Season' in df.ix[i]['Season']:
                    cutoff = i
            if cutoff == len(df.index) - 1:
                lifetime_data['FPCT %'] = float(df.ix[len(df.index)-1]['FPCT%'])
            else:
                df = df.iloc[cutoff:,]
                for r in range(len(df.index)):
                    if position in df.ix[r + cutoff].any():
                        lifetime_data['FPCT %'] = float(df.ix[r + cutoff]['FPCT%'])
                    if str(df.ix[r + cutoff]['LG']) == 'nan':
                        secondary_pos.append(df.ix[r + cutoff]['POS'])

        # Statcast Running Statistics chart
        elif 'Sprint Speed (ft/s)' in df.columns:
            df.columns = df.columns.str.strip().str.replace('\n', '')
            if str(df.ix[len(df.index)-1]['% Rank']) != 'nan':
                lifetime_data['% Rank'] = float(df.ix[len(df.index)-1]['% Rank'])
            else:
                lifetime_data['% Rank'] = float(df.ix[len(df.index)-2]['% Rank'])

        # Statcast Plate Discipline chart
        elif 'Chase %' in df.columns:
            df.columns = df.columns.str.strip().str.replace('\n', '')
            df = df.drop(['Season', 'Pitches'], axis=1)
            for col in list(df):
                if float(df.ix[len(df.index) - 2][col]) > 1 and float(df.ix[len(df.index) - 2][col]) / int(float(df.ix[len(df.index) - 2][col])) == 1:
                    lifetime_data[col] = int(df.ix[len(df.index) - 2][col])
                else:
                    lifetime_data[col] = round(float(df.ix[len(df.index) - 2][col]), 3)

        # Standard MLB Batting Statistics Chart
        elif 'LG' in df.columns and 'L' not in df.columns and '3B' in df.columns and 'W' not in df.columns:
            df.columns = df.columns.str.strip().str.replace('\n', '')
            lifetime_data['Hitting AB'] = int(df.ix[len(df.index)-1]['AB'])
            lifetime_data['Hitting HR'] = int(df.ix[len(df.index)-1]['HR'])
            lifetime_data['Hitting BB'] = int(df.ix[len(df.index)-1]['BB'])
            lifetime_data['Hitting SO'] = int(df.ix[len(df.index)-1]['SO'])
            if lifetime_data['Hitting AB'] == 0:
                lifetime_data['AVG'] = 0
            else:
                lifetime_data['AVG'] = round(float(df.ix[len(df.index)-1]['AVG']), 3)

    return [lifetime_data, secondary_pos]

# sorts a player into their appropriate age group and returns that age group as a string
#  - will be used as a factor in rating generation
def sort_by_exp(stats_dict):

    if stats_dict['Seasons'] <= 1:
        return 'Rookie'
    elif stats_dict['Seasons'] >= 2 and stats_dict['Seasons'] < 7:
        return 'Young guy'
    elif stats_dict['Seasons'] >= 7 and stats_dict['Seasons'] < 13:
        return 'Vet'
    else:
        return 'Old timer'

# sorts a team's roster into 2 categories: hitters and pitchers
def sort_team_roster(team_id):
    players = {'Hitters': {}, 'Pitchers': {}}
    team = get_player_pages(team_id)
    for player in team:
        vitals = get_vitals(player)
        name = vitals[0]
        print(name)
        age = int(vitals[4][vitals[4].rfind(' '):])
        if vitals[1] == 'P':
            pitch_stats = get_lifetime_pitcher_data(player, vitals[1])
            vitals.append(pitch_stats[1])
            group = sort_by_exp(pitch_stats[0])
            vitals.append(group)
            players['Pitchers'][name] = [vitals, pitch_stats[0]]
        else:
            stats = get_lifetime_hitter_data(player, vitals[1])
            vitals.append(stats[1])
            group = sort_by_exp(stats[0])
            vitals.append(group)
            players['Hitters'][name] = [vitals, stats[0]]
    return players

# parses data for entire league, going team by team
def get_league_data():
    league_stats = {}
    for team, id in TEAM_IDS.items():
        league_stats[team] = sort_team_roster(id)
    return league_stats

def print_data(dict):
    for team, stats in dict.items():
        print('{}: '.format(team))
        for type, players in stats.items():
            print('    {}: '.format(type))
            for player, info in players.items():
                print('      {}: '.format(player))
                print('         {}: '.format(info[0]))
                for stat, val in info[1].items():
                    print('        {}: {}'.format(stat, val))

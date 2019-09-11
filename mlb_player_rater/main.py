import parser
import league_data

AL_TEAM_IDS = {'Baltimore Orioles':'110', 'Boston Red Sox':'111', 'Chicago White Sox':'145', 'Cleveland Indians':'114', 'Detroit Tigers':'116',
               'Houston Astros':'117', 'Kansas City Royals':'118', 'Los Angeles Angels':'108', 'Minnesota Twins':'142', 'New York Yankees':'147',
               'Oakland Athletics':'133', 'Seattle Mariners':'136', 'Tampa Bay Rays':'139', 'Texas Rangers':'140', 'Toronto Blue Jays':'141'}

NL_TEAM_IDS = {'Arizona Diamondbacks':'109', 'Atlanta Braves':'144', 'Chicago Cubs':'112', 'Cincinnati Reds':'113', 'Colorado Rockies':'115',
               'Los Angeles Dodgers':'119', 'Miami Marlins':'146', 'Milwaukee Brewers':'158', 'New York Mets':'121','Philadelphia Phillies':'143',
               'Pittsburg Pirates':'134', 'San Diego Padres':'135', 'San Francisco Giants':'137', 'St. Louis Cardinals':'138', 'Washington Nationals':'120'}

parser.get_league_data(AL_TEAM_IDS, 'league_data/AL/')
parser.get_league_data(NL_TEAM_IDS, 'league_data/NL/')

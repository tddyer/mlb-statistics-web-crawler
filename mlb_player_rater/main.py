import parser
import league_data

stats = parser.get_league_data()
parser.print_data(stats)
parser.save_dict_to_json('league_data/league_data.json', stats)
#stats = parser.read_json('league_data/league_data.json')

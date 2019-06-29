import parser

stats = parser.get_league_data()
parser.print_data(stats)
parser.save_dict_to_json('league_data/league_data.json', stats)
#stats = read_json('league_data.json')
#pow_info = rating_scripts.get_pow_info(stats)
#rating_scripts.get_pow_stats_avgs(pow_info, 'HR/PA')
#print_data(stats)

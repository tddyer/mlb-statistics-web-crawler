import parser
import league_data

#stats = parser.get_league_data()
#parser.print_data(stats)
#parser.save_dict_to_json('league_data/league_data.json', stats)
stats = parser.read_json('league_data/league_data.json')
# need to make rating_scripts again as well as info algorithms
pow_info = rating_scripts.get_pow_info(stats)
rating_scripts.get_pow_stats_avgs(pow_info, 'HR/PA')

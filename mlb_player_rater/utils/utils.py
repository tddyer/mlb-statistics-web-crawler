import parser

# cleanses json file of any nan values
def clean_json(file):

    league_data = parser.read_json(file)
    temp = league_data.copy()

    for team, stats in league_data.items():
        for player_type, players in stats.items():
            for player, info in players.items():
                for stat, val in info[1].items():
                    # checking if val is nan
                    if val != val:
                        temp[team][player_type][player][1][stat] = 0

    parser.save_dict_to_json(file, temp)

# retrieves relevant statistic categories for power rating generation
#    -> HR/PA, Exit velo, SLG %, HH %
def get_pow_info(league_data):
    #print(stats_json)
    pow_info = league_data.copy()
    for team, stats in league_data.items():
        for player_type, players in stats.items():
            if player_type == 'Hitters':
                # info -> [vitals, stats]
                for player, info in players.items():
                    pow_info[team][player_type][player] = {}
                    for stat, val in info[1].items():
                        if stat == 'HR/PA' or stat == 'Exit Velocity' or stat == 'SLG' or stat == 'Hard Hit %':
                            pow_info[team][player_type][player][stat] = val
            else:
                for player, info in players.items():
                    pow_info[team][player_type][player] = {}
    print(pow_info)
    #return pow_info

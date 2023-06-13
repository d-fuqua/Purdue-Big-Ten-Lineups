def basic_stats_dict():
    basic_stats = {
        'Stat' : ['plus_minus', 'PUR PTS', 'PUR POSS', 'PUR FG%', 'PUR 3P%', 'PUR FT%', 'PUR OREB',
                  'PUR DREB', 'PUR REB', 'PUR AST', 'PUR STL', 'PUR TO', 'OPP PTS', 'OPP POSS'],
        'Explanation' : ['Purdue Plus/Minus', 'Purdue Points Scored', 'Purdue Possessions',
                         'Purdue Field Goal Percentage' , 'Purdue Three Point Percentage',
                         'Purdue Free Throw Percentage', 'Purdue Offensive Rebounds',
                         'Purdue Offensive Rebounds', 'Purdue Total Rebounds', 'Purdue Assists',
                         'Purdue Steals', 'Purdue Turnovers', 'Opponent Points Scored',
                         'Opponent Possesions']
    }
    return basic_stats

def advanced_stats_dict():
    adv_stats = {
        'Stat' : ['OFF RTG', 'DEF RTG', 'NET RTG', 'AST%', 'AST:TO', 'AST Ratio', 'OREB%', 'DREB%',
                  'REB%', 'eFG%', 'TS%', 'PPP', 'Tempo'],
        'Explanation' : ['Offensive Rating - Points scored per possession multiplied by 100',
                         'Defensive Rating - Points allowed per possession multiplied by 100',
                         'Net Rating - Offensive Rating minus Defensive Rating',
                         'Assist Percentage - Percentage of field goals scored off of assists',
                         'Assist to Turnover Ratio - Assists divided by turnovers',
                         'Assist Ratio - Ratio of assists per offensive possession',
                         'Offensive Rebound Percentage - Percentage of offensive rebounds Purdue comes down with',
                         'Defensive Rebound Percentage - Percentage of defensive rebounds Purdue comes down with',
                         'Rebound Percentage - Percentage of rebounds Purdue gets over an opponent',
                         'Effectie Field Goal Percentage - Field goal percentage that gives extra weight to three pointers',
                         'True Shooting Percentage - Shooting efficiency that includes all field goals and free throws',
                         'Points Per Possession - Total points divided by total possessions',
                         'Tempo - Average number of possessions per 40 minutes']
    }
    return adv_stats
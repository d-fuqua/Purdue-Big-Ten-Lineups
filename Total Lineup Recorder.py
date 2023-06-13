import numpy as np
import pandas as pd

def merge_lineups():
    
    # Create an empty DataFrame to store the aggregated lineup data
    lineup_data = pd.DataFrame(columns=['Lineups', 'Seconds Played', 'Games Played', 'plus_minus', 'PUR PTS', 'PUR POSS',
                                        'OPP POSS', 'OPP PTS', 'PUR FG', 'PUR FGA', 'PUR 3P', 'PUR 3PA', 'PUR FT', 'PUR FTA',
                                        'PUR OREB', 'PUR DREB', 'PUR REB', 'PUR AST', 'PUR STL', 'PUR BLK', 'PUR TO', 'OPP FGA',
                                        'OPP OREB', 'OPP DREB', 'OPP REB', 'OPP TO', 'OPP FTA'])

    for i in range(20):
        curr_lineups = pd.read_csv('.\GameData\game{}_lineups.csv'.format(i + 1))
        
        # Iterate over each row in the current CSV file
        for _, row in curr_lineups.iterrows():
            lineup = row['Lineups']

            # Check if the lineup already exists in lineup_data
            if lineup in lineup_data['Lineups'].values:

                # Determine the existing row in lineup_data that matches the Lineup value
                existing_row = lineup_data[lineup_data['Lineups'] == lineup].iloc[0]

                # Add together the two Series, replace the corresponding Lineups value with the correct value
                new_series = existing_row.add(row)
                new_series.update({'Lineups': lineup})

                # Transpose the new_series Series to a Data Frame
                new_series_transpose = new_series.to_frame().transpose()

                # Find the index of the row in lineup_data that matches the Lineup value in transpose_series
                index_to_replace = lineup_data[lineup_data['Lineups'] == new_series_transpose['Lineups'].iloc[0]].index

                # Replace the row in lineup_data with the row from transpose_series
                lineup_data.loc[index_to_replace] = new_series_transpose.values

            else:
                # Add a new row to lineup_data for the new lineup
                lineup_data = pd.concat([lineup_data, row.to_frame().transpose()], ignore_index=True)
    
    return lineup_data

def calc_basic_stats(lineup_data):

    # Insert new columns with initial value 0
    lineup_data.insert(2, 'Minutes Played', 0)
    lineup_data.insert(11, 'PUR FG%', 0)
    lineup_data.insert(14, 'PUR 3P%', 0)
    lineup_data.insert(17, 'PUR FT%', 0)

    # Calculate 'Minutes Played' by converting 'Seconds Played' to minutes
    for i, row in lineup_data.iterrows():
        lineup_data.at[i, 'Minutes Played'] = round((row['Seconds Played'] / 60), 0)

        # Calculate 'PUR FG%'. Set FG% to 0 if FGA is 0.
        if row['PUR FGA'] == 0:
            lineup_data.at[i, 'PUR FG%'] = 0
        else:
            lineup_data.at[i, 'PUR FG%'] = round((row['PUR FG'] / row['PUR FGA']) * 100, 2)

        # Calculate 'PUR 3P%'. Set 3P% to 0 if 3PA is 0.
        if row['PUR 3PA'] == 0:
            lineup_data.at[i, 'PUR 3P%'] = 0
        else:
            lineup_data.at[i, 'PUR 3P%'] = round((row['PUR 3P'] / row['PUR 3PA']) * 100, 2)

        # Calculate 'PUR FT%' Set FT% to 0 if FTA is 0.
        if row['PUR FTA'] == 0:
            lineup_data.at[i, 'PUR FT%'] = 0
        else:
            lineup_data.at[i, 'PUR FT%'] = round((row['PUR FT'] / row['PUR FTA']) * 100, 2)
    
    lineup_basic_data = lineup_data[['Lineups', 'Games Played', 'Minutes Played', 'plus_minus', 'PUR PTS', 'PUR POSS',
                                 'PUR FG%','PUR 3P%', 'PUR FT%', 'PUR OREB', 'PUR DREB', 'PUR REB', 'PUR AST', 'PUR STL',
                                 'PUR BLK', 'PUR TO', 'OPP PTS', 'OPP POSS']]
    return lineup_basic_data

def calc_adv_stats(lineup_data):

    # Create a new DataFrame lineup_adv_data with 'Lineups' column from lineup_data
    lineup_adv_data = pd.DataFrame(lineup_data['Lineups'], columns=['Lineups'])

    # Add additional columns to lineup_adv_data with initial value of 0
    lineup_adv_data[['Games Played', 'Minutes', 'OFF RTG', 'DEF RTG', 'NET RTG', 'AST%', 'AST:TO', 'AST Ratio', 'OREB%',
                    'DREB%', 'REB%', 'eFG%', 'TS%', 'PPP', 'Tempo']] = 0

    # Iterate over each row in lineup_data
    for i, row in lineup_data.iterrows():
        
        # Assign 'Games Played' and 'Minutes Played' values to corresponding columns in lineup_adv_data
        lineup_adv_data.at[i, 'Games Played'] = row['Games Played']
        lineup_adv_data.at[i, 'Minutes'] = round((row['Seconds Played'] / 60), 0)
        
        # Calculate offensive rating if 'PUR POSS' is not 0
        if row['PUR POSS'] != 0:
            lineup_adv_data.at[i, 'OFF RTG'] = round((row['PUR PTS'] / row['PUR POSS']) * 100, 2)  
        
        # Calculate defensive rating if 'OPP POSS' is not 0
        if row['OPP POSS'] != 0:
            lineup_adv_data.at[i, 'DEF RTG'] = round((row['OPP PTS'] / row['OPP POSS']) * 100, 2)
        
        # Calculate net rating by subtracting defensive rating from offensive rating
        lineup_adv_data.at[i, 'NET RTG'] = lineup_adv_data.at[i, 'OFF RTG'] - lineup_adv_data.at[i, 'DEF RTG']
        
        # Calculate assist percentage if 'PUR FG' is not 0
        if row['PUR FG'] != 0:
            lineup_adv_data.at[i, 'AST%'] = round((row['PUR AST'] / row['PUR FG']) * 100, 2)
            
        # Calculate assist-to-turnover ratio
        if row['PUR TO'] != 0:
            lineup_adv_data.at[i, 'AST:TO'] = round((row['PUR AST'] / row['PUR TO']), 2)
        else:
            lineup_adv_data.at[i, 'AST:TO'] = row['PUR AST']
        
        # Calculate assist ratio if denominator is not 0
        ast_ratio_denom = row['PUR AST'] + row['PUR FGA'] + (0.44 * row['PUR FTA']) + row['PUR TO']
        if ast_ratio_denom != 0:
            lineup_adv_data.at[i, 'AST Ratio'] = round(((100 * row['PUR AST']) / ast_ratio_denom), 2)
        
        # Calculate offensive rebound percentage if denominator is not 0
        oreb_denom = row['PUR OREB'] + row['OPP DREB']
        if oreb_denom != 0:
            lineup_adv_data.at[i, 'OREB%'] = round((row['PUR OREB'] / oreb_denom) * 100, 2)
        
        # Calculate defensive rebound percentage if denominator is not 0
        dreb_denom = row['PUR DREB'] + row['OPP OREB']
        if dreb_denom != 0:
            lineup_adv_data.at[i, 'DREB%'] = round((row['PUR DREB'] / dreb_denom) * 100, 2)

        # Calculate rebound percentage if denominator is not 0
        reb_denom = row['PUR REB'] + row['OPP REB']
        if reb_denom != 0:
            lineup_adv_data.at[i, 'REB%'] = round((row['PUR REB'] / reb_denom) * 100, 2)

        # Calculate effective field goal percentage if 'PUR FGA' is not 0
        if row['PUR FGA'] != 0:
            lineup_adv_data.at[i, 'eFG%'] = round(((row['PUR FG'] + (0.5 * row['PUR 3P'])) / row['PUR FGA']) * 100, 2)

        # Calculate true shooting percentage if denominator is not 0
        ts_denom = 2 * (row['PUR FGA'] + (0.44 * row['PUR FTA']))
        if ts_denom != 0:
            lineup_adv_data.at[i, 'TS%'] = round((row['PUR PTS'] / ts_denom) * 100, 2)

        # Calculate points per possession if 'PUR POSS' is not 0
        if row['PUR POSS'] != 0:
            lineup_adv_data.at[i, 'PPP'] = round((row['PUR PTS'] / row['PUR POSS']), 2)

        # Calculate tempo if 'Minutes Played' is not 0
        if row['Minutes Played'] != 0:
            lineup_adv_data.at[i, 'Tempo'] = round((row['PUR POSS'] / row['Minutes Played']) * 40, 2)
        else:
            lineup_adv_data.at[i, 'Tempo'] = row['PUR POSS'] * 40
    
    return lineup_adv_data

merged_lineups = merge_lineups()

lineup_basic_data = calc_basic_stats(merged_lineups)
lineup_basic_data.to_csv('./GameData/lineup_basic_stats.csv', index=False)

lineup_adv_data = calc_adv_stats(merged_lineups)
lineup_adv_data.to_csv('./GameData/lineup_advanced_stats.csv', index=False)
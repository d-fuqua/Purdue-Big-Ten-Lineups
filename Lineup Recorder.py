import numpy as np
import pandas as pd
from datetime import datetime
import math

def calculate_poss(final_lineups):
    
    # Calculate the possessions for Purdue and Opponents for each lineup
    for lineup in final_lineups['Lineups']:
        temp_df = final_lineups[final_lineups['Lineups'] == lineup]
        pur_poss = math.ceil((temp_df['PUR FGA'] - temp_df['PUR OREB']) + temp_df['PUR TO'] + (0.44 * temp_df['PUR FTA']))
        final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR POSS'] = pur_poss
        opp_poss = math.ceil((temp_df['OPP FGA'] - temp_df['OPP OREB']) + temp_df['OPP TO'] + (0.44 * temp_df['OPP FTA']))
        final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP POSS'] = opp_poss
        
        # Set games played to 1 for each lineup
        final_lineups.loc[final_lineups['Lineups'] == lineup, 'Games Played'] = 1
    
    return final_lineups

def get_play_by_play_stats(game_data, final_lineups):
    
    # List of Purdue players
    purdue_roster = ['Braden Smith', 'Fletcher Loyer', 'Brandon Newman', 'Mason Gillis', 'Zach Edey',
                     'Caleb Furst', 'Trey Kaufman-Renn', 'Ethan Morton', 'David Jenkins', 'Brian Waddell',
                    'Sam King', 'Chase Martin', 'Carson Barrett']

    # List of non players to filter out of the Play row
    non_players = ['Foul on', 'Official TV', 'Beginning of', 'End of']
    
    # Iterate through each row of the data frame
    for index, row in game_data.iterrows():

        # Split the play description into individual words
        full_play = row['PLAY'].split()
        player = ' '.join([full_play[0], full_play[1]])
        
        # Grab the current lineup for each row
        lineup = row['Lineups']
        
        # Check if the player is in the Purdue roster
        if player in purdue_roster:
            
            # Determine what happened in each play using a key word, and then update the respective values in the
            # final_lineup Data Frame.
            if 'Offensive' in full_play:
                final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR OREB'] += 1
                final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR REB'] += 1
            elif 'Defensive' in full_play:
                final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR DREB'] += 1
                final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR REB'] += 1
            elif 'Steal.' in full_play:
                final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR STL'] += 1
            elif 'Block.' in full_play:
                final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR BLK'] += 1
            elif 'Turnover.' in full_play:
                final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR TO'] += 1
            elif 'made' in full_play:
                if 'Assisted' in full_play:
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR AST'] += 1
                if 'Free' in full_play:
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR FT'] += 1
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR FTA'] += 1
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR PTS'] += 1
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'plus_minus'] += 1
                elif 'Three' in full_play:
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR FG'] += 1
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR FGA'] += 1
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR 3P'] += 1
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR 3PA'] += 1
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR PTS'] += 3
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'plus_minus'] += 3
                else:
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR FG'] += 1
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR FGA'] += 1
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR PTS'] += 2
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'plus_minus'] += 2
            else:
                if 'Free' in full_play:
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR FTA'] += 1
                elif 'Three' in full_play:
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR FGA'] += 1
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR 3PA'] += 1
                else:
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'PUR FGA'] += 1
                    
        # Count the needed play values for players not on Purdue's roster
        else:

            # Make sure we are only grabbing plays made by players and not timeouts or start/end of halves
            if player not in non_players:

                # Determine what happened in the play as with Purdue's players, and update the final_lineup Data Frame
                if 'Offensive' in full_play:
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP OREB'] += 1
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP REB'] += 1
                elif 'Defensive' in full_play:
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP DREB'] += 1
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP REB'] += 1
                elif 'Turnover.' in full_play:
                    final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP TO'] += 1
                elif 'made' in full_play:
                    if 'Free' in full_play:
                        final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP FTA'] += 1
                        final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP PTS'] += 1
                        final_lineups.loc[final_lineups['Lineups'] == lineup, 'plus_minus'] -= 1
                    elif 'Three' in full_play:
                        final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP FGA'] += 1
                        final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP PTS'] += 3
                        final_lineups.loc[final_lineups['Lineups'] == lineup, 'plus_minus'] -= 3
                    else:
                        final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP FGA'] += 1
                        final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP PTS'] += 2
                        final_lineups.loc[final_lineups['Lineups'] == lineup, 'plus_minus'] -= 2
                    
                elif 'missed' in full_play:
                    if 'Free' in full_play:
                        final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP FTA'] += 1
                    else:
                        final_lineups.loc[final_lineups['Lineups'] == lineup, 'OPP FGA'] += 1
                    
    return final_lineups

def get_seconds(game_data, final_lineups):
    
    # Add the hour column to the TIME column and then convert to timedelta format
    game_data['TIME'] = pd.to_timedelta('00:' + game_data['TIME'])

    # Create a new column called "Delta Time" that represents the time difference between rows
    game_data['Delta Time'] = game_data['TIME'].diff().fillna(pd.Timedelta(seconds=0))

    # Convert the "Delta Time" and "TIME" columns into total seconds
    game_data['Delta Time'] = game_data['Delta Time'].apply(lambda x: x.total_seconds() * (-1))
    game_data['TIME'] = game_data['TIME'].apply(lambda y: y.total_seconds())

    # Loop through each lineup in the final_lineup DataFrame and count the total seconds played for each lineup
    for lineup in final_lineups['Lineups']:
        temp_df = game_data[game_data['Lineups'] == lineup]
        time_played = temp_df['Delta Time'].sum()
        final_lineups.loc[final_lineups['Lineups'] == lineup, 'Seconds Played'] = time_played

    return final_lineups

def create_lineup_table(num):
    # Load the Excel workbook into a Pandas DataFrame
    game_data = pd.read_excel('.\GameData\game{}_table.xlsx'.format(num), sheet_name='Sheet1')
    
    # Print the first few rows of the data frame to verify it was loaded correctly
    #print(game_data.head())

    # Create a new Data Frame to store lineup specific statistics 
    final_lineups = pd.DataFrame(game_data['Lineups'].unique(), columns=['Lineups'])
    
    # Create a dataframe that contains all of the statistics we want to record
    final_lineups[['Seconds Played', 'Games Played', 'plus_minus', 'PUR PTS', 'PUR POSS', 'OPP POSS', 'OPP PTS', 'PUR FG',
                   'PUR FGA', 'PUR 3P', 'PUR 3PA', 'PUR FT', 'PUR FTA', 'PUR OREB', 'PUR DREB', 'PUR REB', 'PUR AST',
                   'PUR STL', 'PUR BLK', 'PUR TO', 'OPP FGA', 'OPP OREB', 'OPP DREB', 'OPP REB', 'OPP TO', 'OPP FTA']] = 0
    
    # Get the seconds played by each lineup
    final_lineups = get_seconds(game_data, final_lineups)
    
    # Get the play by play stats for each lineup
    final_lineups = get_play_by_play_stats(game_data, final_lineups)
    
    # Calculate the possessions for each lineup
    final_lineups = calculate_poss(final_lineups)
    
    return final_lineups

#Loop through games 1 through 20
for i in range(20):
    
    game_number = i + 1
    final_lineups = create_lineup_table(game_number)
    
    # Exclude rows where Lineups is None
    final_lineups = final_lineups[final_lineups['Lineups'] != 'None']
    
    # Export final_lineups to a csv file
    final_lineups.to_csv('./GameData/game{}_lineups.csv'.format(game_number), index=False)
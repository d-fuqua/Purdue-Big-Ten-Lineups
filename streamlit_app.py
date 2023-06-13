import pandas as pd
import streamlit as st
import plotly.express as px
import glossaries as glos

def highlight_lineup(df, player_list):

    # Extract the last names from the player_list
    lastnames = []
    for name in player_list:
        lastnames.append(name.split()[1])

    # Create a lineup condition based on the last names
    lineup_condition = [', '.join(lastnames)]
    
    # Highlight rows in the DataFrame that match the lineup condition
    highlighted_rows = df['Lineups'].isin(lineup_condition).map({
        True: 'background-color: royalblue',
        False: ''
    })
    return lineup_condition, highlighted_rows

def display_dataframes(basic_df, advanced_df, lineup_exists, highlighted_rows):
   
    # Display the basic and advanced DataFrames in separate tabs
    tab1, tab2 = st.tabs(['Basic Stats', 'Advanced Stats'])
    
    if lineup_exists:

        # Display the DataFrames with highlighted rows if lineup exists
        with tab1:
            st.dataframe(basic_df.style.apply(lambda _: highlighted_rows).format(precision=2))
        with tab2:
            st.dataframe(advanced_df.style.apply(lambda _: highlighted_rows).format(precision=2))
    else:

        # Display the DataFrames without highlighting
        with tab1:
            st.dataframe(basic_df)
        with tab2:
            st.dataframe(advanced_df)
    return

def highlight_bin(df, selected_lineup):

    # Add 'button' and 'color' columns to the DataFrame
    df['button'] = 'Other'
    df['color'] = 'coral'
    
    # Set 'button' and 'color' values for the selected lineup
    df.loc[df['Lineups'] == selected_lineup, 'button'] = 'Selected'
    df.loc[df['Lineups'] == selected_lineup, 'color'] = 'royalblue'
    return

def build_histogram(df, y_axis, hist_title, y_title):
    
    # Build a histogram using Plotly Express
    fig_min = px.histogram(df, x='Lineups', y=y_axis, color='button',
                           color_discrete_sequence=df.color.unique(), title=hist_title)
    
    # Update the x-axis and y-axis labels
    fig_min.update_xaxes(showticklabels=False, visible=False)
    fig_min.update_yaxes(title_text=y_title)
    
    # Update the legend title
    fig_min.update_layout(legend_title_text='Lineup')
    
    # Display the histogram using Streamlit's plotly_chart
    st.plotly_chart(fig_min, use_container_width=True)
    return

def main():

    # Read advanced and basic DataFrames from CSV files
    advanced_df = pd.read_csv(r'C:\Users\David\Desktop\GameData\lineup_advanced_stats.csv')
    basic_df = pd.read_csv(r'C:\Users\David\Desktop\GameData\lineup_basic_stats.csv')

    # Set the page layout and display title and subheader
    st.set_page_config(layout='wide')
    st.title('Purdue 2022-2023 Lineup Analysis 🏀')
    st.subheader('Data from 2022-2023 Big Ten regular season games')
    st.text('')
    st.text('')

    col1, col2, col3, col4, col5 = st.columns(5)
    playerlist = []

    with col1:

        # Select player for PG position
        player1 = st.selectbox('PG', ('Braden Smith', 'David Jenkins Jr.', 'Ethan Morton'))
        playerlist.append(player1)

    with col2:

        # Select player for SG position
        player2 = st.selectbox('SG', ('Fletcher Loyer', 'David Jenkins Jr.', 'Brandon Newman',
                                    'Ethan Morton', 'Carson Barrett'))
        playerlist.append(player2)
    with col3:

        # Select player for SF position
        player3 = st.selectbox('SF', ('Ethan Morton', 'Brandon Newman', 'Fletcher Loyer', 'Brian Waddell',
                                    'Carson Barrett'))
        playerlist.append(player3)
    with col4:

        # Select player for PF position
        player4 = st.selectbox('PF', ('Caleb Furst', 'Mason Gillis', 'Trey Kaufman-Renn', 'Ethan Morton',
                                    'Brian Waddell', 'Sam King'))
        playerlist.append(player4)
    with col5:

        # Select player for C position
        player5 = st.selectbox('C', ('Zach Edey', 'Trey Kaufman-Renn', 'Caleb Furst', 'Mason Gillis'))
        playerlist.append(player5)

    # Highlight the selected lineup and handle button press
    lineup_condition, highlighted_rows = highlight_lineup(advanced_df, playerlist)
    button_press = st.button('Apply')
    st.text('')

    if button_press:
        if lineup_condition[0] in basic_df['Lineups'].values:

            # Display DataFrames with highlighted lineup if it exists
            display_dataframes(basic_df, advanced_df, True, highlighted_rows)
        else:

            # Display an error message if the lineup does not exist
            st.error('Error: This lineup does not exist.', icon='❗')
            display_dataframes(basic_df, advanced_df, False, highlighted_rows)
    else:

        # Display DataFrames without highlighting
        display_dataframes(basic_df, advanced_df, False, highlighted_rows)

    tab3, tab4 = st.tabs(['Basic Stats Glossary', 'Advanced Stats Glossary'])
    with tab3:
        with st.expander('Glossary'):

            # Display basic stats glossary
            st.header('Basic Stats Terminology')
            basic_stats = glos.basic_stats_dict()
            st.table(pd.DataFrame(basic_stats))
    with tab4:
        with st.expander('Glossary'):

            # Display advanced stats glossary
            st.header('Advanced Stats Terminology')
            adv_stats = glos.advanced_stats_dict()
            st.table(pd.DataFrame(adv_stats))

    # Highlight the selected lineup in the histograms
    highlight_bin(basic_df, lineup_condition[0])
    highlight_bin(advanced_df, lineup_condition[0])

    col6, col7 = st.columns(2)

    with col6:

        # Build and display histograms for minutes played and plus/minus
        build_histogram(basic_df, 'Minutes Played', 'Minutes Played per Lineup', 'Minutes Played')
        build_histogram(basic_df, 'plus_minus', 'Plus/Minus per Lineup', 'Plus-Minus')

    with col7:

        # Build and display histograms for True Shooting Percentage (TS%) and Net Rating
        build_histogram(advanced_df, 'TS%', 'True Shooting Percentage (TS%) per Lineup', 'True Shooting %')
        build_histogram(advanced_df, 'NET RTG', 'Net Rating per Lineup', 'Net Rating')

if __name__ == '__main__':
    main()

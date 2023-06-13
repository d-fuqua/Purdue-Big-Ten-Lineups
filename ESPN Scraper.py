from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

def check_exists(url, css_element):
    driver = webdriver.Firefox('C:/Users/David/Downloads/geckodriver')
    driver.get(url)

    try:
        driver.find_element(By.CSS_SELECTOR, css_element)
    except NoSuchElementException:
        driver.quit()
        return False
    driver.quit()
    return True

# Create function to scrape the play by play table from the given html source
def scrape_table(html_source):
    
    # Initialize Beautiful Soup object. The play by play table is the second table scraped from the html source
    soup = BeautifulSoup(html_source, 'html.parser')
    all_tables = soup.find_all('table')
    plays_table = all_tables[1]
    
    # Loop through all of the table header tags and store the text in a headers list
    headers = []
    for i in plays_table.find_all('th'):
        header = i.text
        headers.append(header)
    
    # Initialize a Data Frame to store our table information with the headers list as the column titles
    play_by_play = pd.DataFrame(columns = headers)
    
    # Loop through the body of the table and store the information in the rows of the table in the Data Frame. Use the
    # any() function to remove empty strings from our row data
    table_body = plays_table.find('tbody')
    for j in table_body.find_all('tr'):
        row_data = j.find_all('td')
        row = [k.text for k in row_data if any(k.text)]
        length = len(play_by_play)
        play_by_play.loc[length] = row
    
    return play_by_play

# Create funciton that handles building the play by play dataframe from a given url
def create_dataframe(url):
    
    # Initialize the web driver with our url. Grab the html from the webpage and use the scrape_table() function to get a
    # data frame of the table
    play_by_play_list = []
    driver = webdriver.Firefox('C:/Users/David/Downloads/geckodriver')
    driver.get(url)
    page_source = driver.page_source
    play_by_play_list.append(scrape_table(page_source))
    
    # Locate the list tag that stores the button for the 2nd half. Use the click function to click that button, then sleep 
    # for 2 seconds
    button_list = driver.find_element(By.CSS_SELECTOR, '[title*="2nd"]')
    button_list.find_element(By.TAG_NAME, 'button').click()
    sleep(2)
    
    # Get the html from the page after clicking the 2nd half button. Then use the scrape_table() function on that html to get
    # the table for the 2nd half of the game
    page_source = driver.page_source
    play_by_play_list.append(scrape_table(page_source))
    
    # Check if there is an OT button. If there is, scrape the OT table like the other tables
    if(check_exists(url, '[title*="OT"]')):
        button_list = driver.find_element(By.CSS_SELECTOR, '[title*="OT"]')
        button_list.find_element(By.TAG_NAME, 'button').click()
        sleep(2)
        page_source = driver.page_source
        play_by_play_list.append(scrape_table(page_source))

    # Create a Data Frame for the full game by concatenating both half's Data Frames
    driver.quit()
    full_play_by_play = pd.concat(play_by_play_list)
    return full_play_by_play

# Create a list the contains the urls to all of the games that we'll scrape
links = [
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484836',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484843',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484849',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484875',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484880',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484890',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484897',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484904',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484909',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484917',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484924',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484928',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484932',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484944',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484951',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484958',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484965',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484972',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484985',
    'https://www.espn.com/mens-college-basketball/playbyplay/_/gameId/401484992'
]

# Iterate through the list and create a dataframe of every play for each game. Then, export that dataframe to an Excel file
for url in links:
    full_play_by_play = create_dataframe(url)
    game_number = links.index(url) + 1
    print(game_number)
    full_play_by_play.to_excel('./GameData/game{}_table.xlsx'.format(game_number), index=False)
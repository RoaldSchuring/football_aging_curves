import pandas as pd
from bs4 import BeautifulSoup
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# driver = webdriver.Chrome(executable_path='C:/webdrivers/chromedriver.exe')
# driver.get('https://sofifa.com/players')
#
# a = driver.find_element_by_class_name('choose-version')
# driver.execute_script("arguments[0].click();", a)
#
# b = driver.find_element_by_tag_name('a')
# print(b)
#
#


# now, for all the extracted links get the relevant player information

dated_ratings = requests.get('https://sofifa.com/players?v=15&e=158082&set=true')
soup = BeautifulSoup(dated_ratings.text, 'html.parser')

player_names_and_ratings = []

rating_version_and_date = soup.select('.choose-version')[0].text
game_version = ' '.join(rating_version_and_date.split(' ')[:2])
rating_date = ' '.join(rating_version_and_date.split(' ')[2:])

player_ratings = soup.select('.label.p')
all_player_names = soup.find_all('a')
i = 0
for a in all_player_names:
    try:
        if '/player/' in str(a['href']):
            player_names_and_ratings.append([a['href'], a['title'], game_version, rating_date, player_ratings[i].text, player_ratings[i+1].text])
            i += 2
    except:
        continue

all_player_info = pd.DataFrame(player_names_and_ratings, columns=['player_url', 'name', 'game_version', 'rating_date', 'overall', 'potential'])
print(all_player_info.head())
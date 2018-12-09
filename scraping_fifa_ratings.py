import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from operator import itemgetter


# this function retrieves links to all the historical versions of rating we can mine
def get_links_to_historical_views():
    driver = webdriver.Chrome(executable_path='C:/webdrivers/chromedriver.exe')
    driver.get('https://sofifa.com/players')

    a = driver.find_element_by_class_name('choose-version')
    driver.execute_script("arguments[0].click();", a)

    historical_version_elements = driver.find_elements_by_tag_name('a')
    all_historical_links = []
    for h in historical_version_elements:
        element_attribute_value = h.get_attribute('href')
        if 'https://sofifa.com/players?v=' in element_attribute_value:
            all_historical_links.append(element_attribute_value)

    return all_historical_links


# now, for all the extracted links get the relevant player information
def get_player_names_and_ratings(player_rating_page):
    soup = BeautifulSoup(player_rating_page.text, 'html.parser')

    player_names_and_ratings = []

    rating_version_and_date = soup.select('.choose-version')[0].text
    game_version = ' '.join(rating_version_and_date.split(' ')[:2])
    rating_date = ' '.join(rating_version_and_date.split(' ')[2:])

    player_ages = soup.select('.col-digit.col-ae')
    player_ages = [a.text for a in player_ages if 'class="col-digit col-ae"' in str(a)]

    player_nationalities = soup.find_all('a')
    player_nationalities = [n['title'] for n in player_nationalities if '/players?na=' in str(n)]

    player_team_info = soup.find_all('a')
    player_team_info = [t for t in player_team_info if '/team/' in str(t)]
    player_team = [t.text for t in player_team_info]
    player_team_id = [t['href'] for t in player_team_info]

    # players that are free agents have a nationality listed as their team - this confuses the assignment of both
    # teams and nationalities. The following section mitigates this effect.

    player_status = soup.select('.subtitle.text-ellipsis')
    revised_player_team = []
    revised_player_team_id = []
    nationalities_to_keep = []
    i = 0
    j = 0
    for s in player_status:
        if s.text == 'Free':
            revised_player_team.append('')
            revised_player_team_id.append('')
        else:
            revised_player_team.append(player_team[i])
            revised_player_team_id.append(player_team_id[i])
            nationalities_to_keep.append(j)
            i += 1
        j += 1

    player_nationalities = itemgetter(*nationalities_to_keep)(player_nationalities)

    player_ratings = soup.select('.label.p')
    all_player_names = soup.find_all('a')

    position_tags = soup.find_all("div", {"class": "text-ellipsis rtl"})
    position_tags = [p.text for p in position_tags]

    # now, let us iterate through the full set of 'clean' attributes and append all relevant information for each player to a list

    i = 0
    for a in all_player_names:
        try:
            if '/player/' in str(a['href']):
                player_names_and_ratings.append([a['href'], a['title'], game_version, rating_date,
                                                 player_ratings[i].text, player_ratings[i + 1].text,
                                                 player_ages[int(i / 2)], revised_player_team[int(i / 2)],
                                                 revised_player_team_id[int(i / 2)], player_nationalities[int(i / 2)],
                                                 position_tags[int(i / 2)], ])
                i += 2
        except:
            continue

    return player_names_and_ratings


# this function allows us to scrape all the relevant player information for each historical version
def scrape_all_info_for_dated_version(link):
    all_ratings_for_one_date = []
    i = 0
    duplicates = False
    while duplicates is False:
        link_suffix = '&offset=' + str(i)
        dated_ratings = requests.get(link + link_suffix)
        player_data = get_player_names_and_ratings(dated_ratings)

        all_new_player_urls = [l[0] for l in player_data]
        existing_player_urls = [l[0] for l in all_ratings_for_one_date]

        if not set(all_new_player_urls).issubset(set(existing_player_urls)):
            all_ratings_for_one_date.extend(player_data)
            i += 60
            continue
        else:
            duplicates = True

    return all_ratings_for_one_date

# initiate an empty dataframe that we will append scraped information to
df = pd.DataFrame(columns=['player_url', 'name', 'game_version', 'rating_date', 'overall',
                           'potential', 'age', 'team', 'team_id', 'nationality', 'position'])
df.to_csv('fuller_player_rating_dataset.csv')

# retrieve the links to the historical versions to be mined
all_historical_links = get_links_to_historical_views()
print(len(all_historical_links), ' dated versions to mine')

# iterate through each historical version and append any new ratings to the existing csv
i = 1
for l in all_historical_links:
    print('Now mining data from link', i, 'of', len(all_historical_links))
    all_ratings = scrape_all_info_for_dated_version(l)
    all_player_info = pd.DataFrame(all_ratings,
                                   columns=['player_url', 'name', 'game_version', 'rating_date', 'overall',
                                            'potential', 'age', 'team', 'team_id', 'nationality', 'position'])
    all_player_info.to_csv('fuller_player_rating_dataset.csv', mode='a', header=False)
    i += 1

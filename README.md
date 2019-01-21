Click the button below for a direct link to the interactive aging curve visualization tool:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/RoaldSchuring/Modeling-Football-Aging-Curves/f35dfea57337d0b62196bb69d0b863d36a87ef96?filepath=aging_curves_interactive_visualization.ipynb)


# Building Football Player Aging Curves using FIFA Player Ratings

### Introduction

In this repository, we study aging curves using player ratings from series of FIFA video games. The repository contains the following notebooks and scripts:

- scraping_fifa_ratings.py: this file scrapes FIFA player rating data from (www.sofifa.com)
- compressing_fifa_rating_file.py: this file takes the raw data from the web scraper and compresseses the dataset to a more manageable size
- aging_curves_analysis.ipynb: this notebook explores how to construct aging curves using the FIFA player rating dataset, and presents aging curves for sets of individuals, player positions and teams
- aging_curves_interactive_visualization.ipynb: this notebook presents an interactive visualization of aging curves, filterable by player name, nationality, team, and nationality of league

In addition, it also includes the following datasets:

- compressed_player_rating_dataset.csv: the dataset used to produce the aging curves
- team_mappings.csv: dataset used to join team nationalities onto the compressed_player_rating_dataset dataset

Finally, the soccer_pitch_border.png file provides a background image for one of the visualizations in the aging_curves_analysis notebook


### Technologies

- Python
- Jupyter Notebook
- The necessary Python package versions needed to run the various files in this repository have been listed out in the accompanying requirements.txt file
- In addition, you will need to install Chromedriver and save it in your C drive, or alternatively modify the executable path referenced in the scraping_fifa_ratings.py file


### Project Description

In this project, a dataset of player ratings has been scraped from the website www.sofifa.com. For every historical version of the game, the overall and potential rating for each player has been mined, along with accompanying features for each player at a given point in time: nationality, team and age.
This raw dataset is about 1 GB in size, but for the purposes of our aging curve investigation contains unnecessary duplicate values. We are interested in how player ratings evolve year over year, and do not need ten successive biweekly datapoints telling us that a player has remained at the same overall rating and potential level. As such, the file 'compressing_fifa_rating.py' removes any unnecessary rows, and preserves only those columns required to run our aging curve analysis.
Using the compressed dataset, the aging_curves_analysis.ipynb notebook explores how aging curves can be computed, and demonstrates a few examples for top players in our dataset. Subsequently, aging curves are computed by position and team to demonstrate any differences that exist along those dimensions.
To allow any interested users to explore the aging curves more fully, an interactive visualization tool has been built using Plotly. The visualization tool also uses the difflib package, which has been saved in the repo also. Credits to (https://github.com/enthought/Python-2.7.3/blob/master/Lib/difflib.py).
The [visualization tool](https://mybinder.org/v2/gh/RoaldSchuring/Modeling-Football-Aging-Curves/f35dfea57337d0b62196bb69d0b863d36a87ef96?filepath=aging_curves_interactive_visualization.ipynb) can be reached using the button at the top of this README file, or using the adjacent hyperlink.


### Getting Started

1. Clone this repo

2. If you want to obtain the full raw dataset, run scraping_fifa_ratings.py and subsequently compressing_fifa_rating_file.py. Alternatively, if you just want to run the aging curve analysis, download the contents of the /data folder in this repository.

3. Run the notebook files as you please!


### Authors

Roald Schuring

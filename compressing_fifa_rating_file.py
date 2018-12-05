import pandas as pd

# first, open the full dataset
full_rating_dataset = pd.read_csv('full_player_rating_dataset.csv', encoding='latin-1', names=['rating_id', 'player_url', 'name', 'game_version', 'rating_date', 'overall',
                                                         'potential', 'age', 'team', 'team_id', 'nationality'])
full_rating_dataset.set_index('rating_id', inplace=True)

full_rating_dataset = full_rating_dataset.loc[full_rating_dataset['rating_date'] != '']

# we will only preserve the earliest date at which a new player rating is assigned - to do this, we must convert the
# rating date column to a datetime format
full_rating_dataset['rating_date'] = pd.to_datetime(full_rating_dataset['rating_date'], format='%b %d, %Y')

# now, group by all relevant features and take the minimum date
full_rating_dataset_grouped = full_rating_dataset.groupby(['player_url', 'age', 'overall', 'potential', 'team',
                                               'team_id', 'nationality'], as_index=False)['rating_date'].min()
full_rating_dataset_grouped.sort_values(by=['player_url', 'rating_date'], inplace=True)

# although we did not include the name and game version in the groupby clause, we do want to preserve this information
select_player_info = full_rating_dataset[['player_url', 'game_version', 'name']]
compressed_fifa_ratings = pd.merge(full_rating_dataset_grouped, select_player_info, left_on='player_url',
                                   right_on='player_url', how='left')
compressed_fifa_ratings.drop_duplicates()

# determine the order of the columns we want and save to csv
compressed_fifa_ratings = compressed_fifa_ratings[['player_url', 'name', 'game_version', 'age', 'overall', 'potential',
                                                   'team', 'team_id', 'nationality', 'rating_date']]
compressed_fifa_ratings.to_csv('compressed_player_rating_dataset.csv')
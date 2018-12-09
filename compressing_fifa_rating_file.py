import pandas as pd

# first, open the full dataset
full_rating_dataset = pd.read_csv('fuller_player_rating_dataset.csv', encoding='latin-1',
                                  names=['rating_id', 'player_url', 'name', 'game_version', 'rating_date', 'overall',
                                         'potential', 'age', 'team', 'team_id', 'nationality', 'position'])
full_rating_dataset.set_index('rating_id', inplace=True)

# we will only preserve the earliest date at which a new player rating is assigned - to do this, we must convert the
# rating date column to a datetime format
full_rating_dataset = full_rating_dataset.loc[full_rating_dataset['rating_date'] != 'rating_date']
full_rating_dataset['rating_date'] = pd.to_datetime(full_rating_dataset['rating_date'], format='%b %d, %Y')

# now, group by all relevant features and take the minimum date
compressed_fifa_ratings = full_rating_dataset.groupby(['player_url', 'age', 'overall', 'potential', 'team',
                                                       'team_id', 'nationality', 'position'], as_index=False)['rating_date'].min()
compressed_fifa_ratings.sort_values(by=['player_url', 'rating_date'], inplace=True)
compressed_fifa_ratings.to_csv('compressed_player_rating_dataset.csv')

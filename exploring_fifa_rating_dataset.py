import pandas as pd
import matplotlib.pyplot as plt

#
compressed_fifa_ratings = pd.read_csv('compressed_player_rating_dataset.csv', encoding='latin-1')
compressed_fifa_ratings.set_index('player_url')
parsed_positions = compressed_fifa_ratings['position'].str.split(' ', expand=True)
parsed_positions.columns = ['main_position', 'position_2', 'position_3', 'position_4']
compressed_fifa_ratings = pd.concat([compressed_fifa_ratings, parsed_positions], axis=1)

just_overall_ratings = compressed_fifa_ratings[['player_url', 'age', 'main_position', 'overall']].drop_duplicates()
just_overall_ratings['age_next_year'] = just_overall_ratings['age'].apply(lambda x: x+1)
year_over_year_ratings = pd.merge(just_overall_ratings, just_overall_ratings, left_on=['player_url', 'age_next_year'],
                                  right_on=['player_url', 'age'], how='left').drop_duplicates()
year_over_year_ratings = year_over_year_ratings[['player_url', 'main_position_x', 'age_x', 'age_next_year_x', 'overall_x', 'overall_y']]
year_over_year_ratings.columns = ['player_url', 'main_position', 'age', 'age_next_year', 'overall', 'next_year_overall']
year_over_year_ratings.dropna(inplace=True)

year_over_year_ratings['diff'] = year_over_year_ratings['next_year_overall'] - year_over_year_ratings['overall']

# print(year_over_year_ratings.head())

avg_rating_changes = year_over_year_ratings.groupby(['age', 'age_next_year'], as_index=False)['diff'].mean()
avg_rating_changes.columns = ['age', 'age_next_year', 'diff']
# print(avg_rating_changes)
# avg_rating_changes.sort_values(['age', 'age_next_year'], inplace=True)

avg_rating_changes = avg_rating_changes.loc[(avg_rating_changes['age'] >= 18) & (avg_rating_changes['age'] <= 36)]
avg_rating_changes['cum_sum'] = avg_rating_changes['diff'].cumsum()
plt.plot(avg_rating_changes['age'], avg_rating_changes['cum_sum'])
plt.show()
print(avg_rating_changes)

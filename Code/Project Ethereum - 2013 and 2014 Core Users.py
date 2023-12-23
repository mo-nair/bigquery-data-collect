import pandas as pd
import numpy as np

def rolling_sum_by_days(df, repoName, actorId, column, days):
    result = []
    for index, row in df.iterrows():
        start_date = row['date1'] - pd.Timedelta(days = days)
        end_date = row['date1']
        mask = (df['date1'] >= start_date) & (df['date1'] <= end_date) & (df['GhRepo'] == row[repoName])
    if (actorId != None):
        mask = (df['date1'] >= start_date) & (df['date1'] <= end_date) & (df['GhRepo'] == row[repoName]) & (df['actor_login'] == row[actorId])
        result.append(df.loc[mask, column].sum())
    return result

columns_to_display = ['GhRepo', 'date1', 'actor_login', 'num_activities', 'user_rolling_sum_30_d', 'repo_rolling_sum_30_d', 'percent_activities_use', 'is_core_developer', 'is_user_bot']

df = pd.read_csv('Data20132014.csv', low_memory = False)
pd.set_option('display.max_columns', 30)
df['date1'] = pd.to_datetime(df['date1'], format = '%m/%d/%y')
df.sort_values(by = ['GhRepo', 'date1', 'actor_login'])

sub_df = df.copy()

repo_grp_date = sub_df.groupby(['GhRepo', 'date1'], group_keys = True)
num_activites_by_day = repo_grp_date[['num_activities']].apply(lambda x: x.sum())

repo_activities_df = pd.concat([num_activites_by_day], sort = False)
repo_activities_df.rename(columns = {'num_activities': 'num_activites_by_day'}, inplace = True)

repo_activities_df['repo_rolling_sum_30_d'] = rolling_sum_by_days(repo_activities_df.reset_index(), 'GhRepo', None, 'num_activites_by_day', 30)

user_activities_df = sub_df.groupby(['GhRepo', 'date1', 'actor_login'])
sub_df['user_rolling_sum_30_d'] = rolling_sum_by_days(sub_df.reset_index(), 'GhRepo', 'actor_login', 'num_activities', 30)

merged_df = sub_df.merge(repo_activities_df, on = ['GhRepo', 'date1'], how = 'inner')
merged_df['percent_activities_use'] = np.ceil(100 * merged_df['user_rolling_sum_30_d'] / merged_df['repo_rolling_sum_30_d']).astype(int)
merged_df['is_core_developer'] = np.where(merged_df['percent_activities_use'] > 12, 1, 0)
merged_df['is_user_bot'] = merged_df['actor_login'].apply(lambda x: 1 if 'bot' in x.lower() else 0)
merged_df[columns_to_display].to_csv('Data20132014CoreUser.csv', index = False)
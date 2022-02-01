import pandas as pd
import datetime
import math

def second_to_time(second):
    return datetime.time(0, int(second//60), int(second%60), round(math.modf(second)[0]*1000000))

df = pd.read_csv('./../csv/inter_college_result_second.csv', sep=',')
df.drop(['500m', '1000m', '1500m', 'tournament_name', 'race_number', 'lane', 'Unnamed: 0', 'qualify'], axis=1, inplace=True)
indexNames = df[
    (df['2000m'] == 0.0) |
    (df['boat_type'] != 'm4+') 
].index
df.drop(indexNames , inplace=True)

yosen_df = df[df['section_code'].str.contains('予選')]
median_df = yosen_df.groupby(['year'])['2000m'].median()
print(median_df)

dropIndex = df[
    (df['year'] == 2014) |
    (df['year'] == 2015)
].index
df.drop(dropIndex , inplace=True)

# print(yosen_df.groupby(['year'])['2000m'].describe())
df2 = df[df['section_code'].str.contains('予選')]
print(df2['2000m'].describe())
df2.plot(kind='hist', y='2000m' , bins=10, figsize=(16,8))
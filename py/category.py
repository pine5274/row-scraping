import pandas as pd
import datetime
import math
import matplotlib as mpl
import matplotlib.pyplot as plt

def second_to_time(second):
    return datetime.time(0, int(second//60), int(second%60), round(math.modf(second)[0]*1000000))

df = pd.read_csv('./../csv/inter_college_result_second.csv', sep=',')

df.drop(['500m', '1000m', '1500m','team', 'order', 'tournament_name', 'race_number', 'lane', 'Unnamed: 0', 'qualify'], axis=1, inplace=True)
indexNames = df[
    (df['2000m'] == 0.0)
].index
df.drop(indexNames , inplace=True)
yosen_df = df[df['section_code'].str.contains('予選')].drop(['section_code'], axis=1)
print(yosen_df)

dropIndex = yosen_df[
    (yosen_df['year'] == 2017) |
    (yosen_df['year'] == 2019)
].index
Msingle = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'm1x']['2000m']

dropIndex = yosen_df[
    (yosen_df['year'] == 2017) |
    (yosen_df['year'] == 2019)
].index
Mdouble = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'm2x']['2000m']

dropIndex = yosen_df[
    (yosen_df['year'] == 2013) |
    (yosen_df['year'] == 2018)
].index
Mpair = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'm2-']['2000m']

dropIndex = yosen_df[
    (yosen_df['year'] == 2014) |
    (yosen_df['year'] == 2019)
].index
Mquad = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'm4x']['2000m']

dropIndex = yosen_df[
    (yosen_df['year'] == 2014) |
    (yosen_df['year'] == 2015)
].index
MfourPlus = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'm4+']['2000m']

dropIndex = yosen_df[
    (yosen_df['year'] == 2017) |
    (yosen_df['year'] == 2014)
].index
Mfour = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'm4-']['2000m']

dropIndex = yosen_df[
    (yosen_df['year'] == 2013) |
    (yosen_df['year'] == 2015)
].index
Meight = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'm8+']['2000m']

dropIndex = yosen_df[
    (yosen_df['year'] == 2013) |
    (yosen_df['year'] == 2018)
].index
Wsingle = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'w1x']['2000m']

dropIndex = yosen_df[
    (yosen_df['year'] == 2013) |
    (yosen_df['year'] == 2019)
].index
Wdouble = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'w2x']['2000m']

dropIndex = yosen_df[
    (yosen_df['year'] == 2013) |
    (yosen_df['year'] == 2019)
].index
Wpair = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'w2-']['2000m']

dropIndex = yosen_df[
    (yosen_df['year'] == 2013) |
    (yosen_df['year'] == 2019)
].index
WquadPlus = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'w4x+']['2000m']

Wquad = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'w4x']['2000m']
WfourPlus = yosen_df.drop(dropIndex)[yosen_df['boat_type'] == 'w4+']['2000m']

category = pd.DataFrame({'M1x': Msingle, 'M2x': Mdouble, 'M2-': Mpair, 'M4x': Mquad, 'M4-': Mfour, 'M4+': MfourPlus, 'M8+': Meight, 'W1x': Wsingle, 'W2x': Wdouble, 'W2-': Wpair, 'W4x+': WquadPlus, 'W4x': Wquad, 'W4+': WfourPlus})
categoryM = pd.DataFrame({'M1x': Msingle, 'M2x': Mdouble, 'M2-': Mpair, 'M4x': Mquad, 'M4-': Mfour, 'M4+': MfourPlus, 'M8+': Meight})
categoryW = pd.DataFrame({'W1x': Wsingle, 'W2x': Wdouble, 'W2-': Wpair, 'W4x+': WquadPlus, 'W4x': Wquad, 'W4+': WfourPlus})

plt.figure()
category.plot.box(figsize=(12, 12))
plt.savefig('../dst/box_2.jpg')
plt.close('all')

plt.figure()
categoryM.plot.box(figsize=(12, 12))
plt.savefig('../dst/boxM_2.jpg')
plt.close('all')

plt.figure()
categoryW.plot.box(figsize=(12, 12))
plt.savefig('../dst/boxW_2.jpg')
plt.close('all')
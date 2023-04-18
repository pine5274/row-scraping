import pandas as pd
import numpy as np

def f_time_to_seconds(x):
    if (type(x) is float):
        return x
    minutes = int(x[1])
    seconds = float(x[-5:])
    return round(minutes * 60 + seconds, 2)


df = pd.read_csv('../dst/all_japan.csv', index_col=0)
df = df.dropna(subset=['2000m'])

df['500m'] = df['500m'].map(f_time_to_seconds)
df['1000m'] = df['1000m'].map(f_time_to_seconds)
df['1500m'] = df['1500m'].map(f_time_to_seconds)
df['2000m'] = df['2000m'].map(f_time_to_seconds)
df.to_csv('../dst/all_japan_seconds.csv')
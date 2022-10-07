import pandas as pd

df = pd.read_csv("data\\atlcrime.csv")

# filter = example[example['count'] >= 1000]

# filter = filter.sort_values(by=['count'])

# filter.to_csv('highest_crime_areas_EXAMPLE.csv')

df['count'] = 1
new_df = df.groupby(df['neighborhood']).count()['count'].sort_values(ascending=False)
new_df.to_csv('bar_chart_EXAMPLE.csv')

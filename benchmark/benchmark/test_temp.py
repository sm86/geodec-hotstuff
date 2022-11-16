# from geo_logs import GeoLogParser
import pandas as pd

data = pd.read_csv('/home/ubuntu/results/geo-dec-metrics.csv')
run_id_array = [23,24,25]

data = data.loc[data['run_id'].isin(run_id_array)]
by_name = data.groupby(['name'])

# for name, liveliness in by_name:
#     print(f"entries for {name!r}")
#     print("------------------------")
#     print(liveliness.head(3), end="\n\n")

liveliness_mean = by_name['liveliness'].mean(numeric_only= True).reset_index()
liveliness_mean.rename(columns = {'liveliness':'liveliness_avg'}, inplace = True)
print(liveliness_mean)

data_first = data.loc[data['run_id'] == run_id_array[0]]
result = pd.merge(data_first, liveliness_mean, on='name')
result['runs'] = ([len(run_id_array)] * len(result))
print(result)
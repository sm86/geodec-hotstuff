import pandas as pd
from scipy.stats import pearsonr, spearmanr

data = pd.read_csv("/home/ubuntu/results/mean-geo-dec-metrics.csv")
print(data)


print(pearsonr(data['liveliness_avg'], data['rms_one_third_dist']))
print(pearsonr(data['liveliness_avg'], data['rms_two_third_dist']))
print(pearsonr(data['liveliness_avg'], data['rms_total_dist']))
print(pearsonr(data['liveliness_avg'], data['one_third_dist']))
print(pearsonr(data['liveliness_avg'], data['two_third_dist']))
print(pearsonr(data['liveliness_avg'], data['total_dist']))


id = [8,59,139]

data = data[~data['id'].isin(id)]
print(data)
# print(data.index[data['name'].isin)
# df\.drop(df.index[df['Col1'] == 0], inplace=True)

# print(data['liveliness_avg'].corr(data['total_dist']))

print(pearsonr(data['liveliness_avg'], data['rms_one_third_dist']))
print(pearsonr(data['liveliness_avg'], data['rms_two_third_dist']))
print(pearsonr(data['liveliness_avg'], data['rms_total_dist']))
print(pearsonr(data['liveliness_avg'], data['one_third_dist']))
print(pearsonr(data['liveliness_avg'], data['two_third_dist']))
print(pearsonr(data['liveliness_avg'], data['total_dist']))


# print(spearmanr(data['liveliness_avg'], data['rms_one_third_dist']))
# print(spearmanr(data['liveliness_avg'], data['rms_two_third_dist']))
# print(spearmanr(data['liveliness_avg'], data['rms_total_dist']))
# print(spearmanr(data['liveliness_avg'], data['one_third_dist']))
# print(spearmanr(data['liveliness_avg'], data['two_third_dist']))
# print(spearmanr(data['liveliness_avg'], data['total_dist']))
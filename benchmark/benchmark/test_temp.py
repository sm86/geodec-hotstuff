import pandas as pd
from geodec import GeoDec
from scipy.stats import pearsonr, spearmanr

data1 = pd.read_csv("/home/ubuntu/results/mean-geo-dec-metrics.csv")
data_minority = pd.read_csv("/home/ubuntu/results/minority-mean-geo-dec-metrics.csv")

# # # print(data)
# # # print(data_minority)

# data = pd.read_csv("/home/ubuntu/results/updatedGDI-mean-geo-dec-metrics.csv")
# print(data)
# print(data_minority)

# data = data_minority.append(data1)
data = data_minority
# data = data1

print(data)

# print(pearsonr(data['liveliness_avg'], data['rms_one_third_dist']))
# print(pearsonr(data['liveliness_avg'], data['rms_two_third_dist']))
# print(pearsonr(data['liveliness_avg'], data['rms_total_dist']))
print(pearsonr(data['liveliness_avg'], data['one_third_dist']))
print(pearsonr(data['liveliness_avg'], data['two_third_dist']))
print(pearsonr(data['liveliness_avg'], data['total_dist']))
# print(pearsonr(data['liveliness_avg'], data['quorum_counter']))
    
# id = [8,59,139]

# data = data[~data['id'].isin(id)]
# print(data)
# # print(data.index[data['name'].isin)
# # df\.drop(df.index[df['Col1'] == 0], inplace=True)

# # print(data['liveliness_avg'].corr(data['total_dist']))

# print(pearsonr(data['liveliness_avg'], data['rms_one_third_dist']))
# print(pearsonr(data['liveliness_avg'], data['rms_two_third_dist']))
# print(pearsonr(data['liveliness_avg'], data['rms_total_dist']))
# print(pearsonr(data['liveliness_avg'], data['one_third_dist']))
# print(pearsonr(data['liveliness_avg'], data['two_third_dist']))
# print(pearsonr(data['liveliness_avg'], data['total_dist']))


# print(spearmanr(data['liveliness_avg'], data['rms_one_third_dist']))
# print(spearmanr(data['liveliness_avg'], data['rms_two_third_dist']))
# print(spearmanr(data['liveliness_avg'], data['rms_total_dist']))
# print(spearmanr(data['liveliness_avg'], data['one_third_dist']))
# print(spearmanr(data['liveliness_avg'], data['two_third_dist']))
# print(spearmanr(data['liveliness_avg'], data['total_dist']))
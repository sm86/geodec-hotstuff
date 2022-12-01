import pandas as pd

data = pd.read_csv("/home/ubuntu/results/64node-mean-geo-dec-metrics.csv")
print(len(data)/64)
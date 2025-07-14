import pandas as pd
import numpy as np
import statistics as stat
import matplotlib.pyplot as plt
import math
#question: How does your weight impact your GPA?

def extractNum(string):
    result = ""
    
    if type(string) != str:
        return float(string)

    for char in string:
        if char.isdigit():
            result += char
    
    if len(result) == 0:
        return -1.0
    else:
        return float(result)
    
def map_to_bins(weights, num_bins):
    max_weight, min_weight = max(weights['weight']), min(weights['weight'])
    step = (max_weight - min_weight)/num_bins

    def map_func(row):
        if row.weight != max_weight:
            row.weight = math.floor((row.weight - min_weight)/step)
        else:
            row.weight = num_bins - 1

        return row

    return weights.apply(map_func, axis = 'columns')

df = pd.read_csv('food_coded.csv')

#print(list(df))

df['GPA'] = pd.to_numeric(df['GPA'], errors='coerce')
weights_df = df[df['weight'] != "nan"].map(extractNum)
weights_df = weights_df[weights_df['weight'] > 0]
weight_mean = weights_df.groupby('GPA')['weight'].agg('mean') #average weight of students


#based on this figure, there is not much correspondence between weight and 
weight_mean.plot()
weights_df.plot(kind='scatter', x='weight', y='GPA')
plt.show()

print(stat.stdev(weights_df.weight)) #high standard deviation

num_bins = 20
binned_weights = map_to_bins(weights_df, num_bins).groupby('weight')['GPA'].agg(['mean', 'size'])
print(binned_weights)

plt.bar(x=range(1, len(binned_weights['mean']) + 1), height=binned_weights['mean'])
plt.ylim([3.2, 4.0])
plt.xlim([0, num_bins])
plt.show()






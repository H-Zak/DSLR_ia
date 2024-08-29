import numpy as np
import math

from typing import Union, List

num = Union[int, float, np.float64]

class Course:
    def __init__(self, name : str, raw_data: List[num], data_sorted : List[num], normalize: bool = False):
        self.name = name
        self.raw_data = raw_data
        self.data_sorted = data_sorted
        self.count = len(self.data_sorted)
        self.mean = self.mean_calcul(data_sorted)
        self.std = self.varirance(data_sorted, self.mean)
        self.min = self.init_min_value(self.data_sorted) 
        self.percentile_25 = self.init_percentile(0.25, self.data_sorted)
        self.percentile_50 = self.init_percentile(0.5, self.data_sorted)
        self.percentile_75 = self.init_percentile(0.75, self.data_sorted)
        self.max = self.init_max_value(self.data_sorted)
        if normalize :
            self.data_zscore = self.normalize_data(data_sorted)
            self.mean_zscore = self.mean_calcul(self.data_zscore)
            self.std_zscore = self.varirance(self.data_zscore, self.mean_zscore)
            self.percentile_25_zscore = self.init_percentile(0.25, self.data_zscore)
            self.percentile_50_zscore = self.init_percentile(0.5, self.data_zscore)
            self.percentile_75_zscore = self.init_percentile(0.75, self.data_zscore)
            self.max_zscore = self.init_max_value(self.data_zscore)
            self.min_zscore= self.init_min_value(self.data_zscore) 


    
    
    def __str__(self) -> str:
        return (f'Course: {self.name}\n'
                f'  Count:     {self.count}\n'
                f'  Mean:     {self.mean}\n'
                f'  Std:     {self.std}\n'
                f'  Min Score: {self.min}\n'
                f'  25%      : {self.percentile_25}\n'
                f'  50%      : {self.percentile_50}\n'
                f'  75%      : {self.percentile_75}\n'
                f'  Max Score: {self.max}\n'
                f'  Mean_zcore:     {self.mean_zscore}\n'
                f'  Std_zcore:     {self.std_zscore}\n'
                f'  Min Score: {self.min_zscore}\n'
                f'  25% zcore      : {self.percentile_25_zscore}\n'
                f'  50%  zcore    : {self.percentile_50_zscore}\n'
                f'  75%   zcore   : {self.percentile_75_zscore}\n'
                f'  Max Score: {self.max_zscore}\n'
                )

    def init_min_value(self, data):
        return round(data[0], 4)
    
    def normalize_data(self, data_sorted):
        return [(x - self.mean)/ self.std  for x in data_sorted ]
    
    def init_max_value(self, data):
        return round(data[len(data) - 1], 4)

    def init_percentile(self, divisor, data):
        count = self.count - 1
        index = count * divisor
        percentile = 0
        percentage = index - int(index)
        if index % 2 != 0:
            index = int(index)
            percentile = (data[index] + percentage * (data[index + 1] - data[index]))
        else:
            index = int(index)
            percentile = data[index]
        return round(percentile, 4)

    def get_percentile(self, divisor):
        # print('---------------------------')
        # print(self.count)
        index = math.ceil(divisor * (self.count))
        index_2 = index - 1
        # print(index)
        # print(index_2)
        return self.data_sorted[index]

    def sum(self, data):
        sum = 0
        for value in data:
            sum += value 
        return sum
    
    def mean_calcul(self, data):
        my_sum = self.sum(data)
        if self.count != 0:
            return round(my_sum / self.count, 4)
        else:
             return None
    
    def varirance(self, data, mean):
        variance = 0
        for value in data:
            variance += (value - mean) ** 2
        if self.count == 0:
            return None
        variance = np.sqrt(variance/self.count)
        return round(variance,4)

    # def init_percentile_25(self):
    #     return self.data_sorted[0]
    
    # def init_percentile_50(self):
    #     return self.data_sorted[0]
    
    # def init_(self):
    #     return self.data_sorted[0]
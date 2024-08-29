import numpy as np
import math

from typing import Union, List

num = Union[int, float, np.float64]

class Course:
    def __init__(self, name : str, raw_data: List[num], data_sorted : List[num]):
        self.name = name
        self.raw_data = raw_data
        self.data_sorted = data_sorted
        self.count = len(self.data_sorted)
        self.mean = self.mean_calcul()
        self.std = self.varirance()
        self.min = self.init_min_value() 
        self.percentile_25 = self.init_percentile(0.25)
        self.percentile_50 = self.init_percentile(0.5)
        self.percentile_75 = self.init_percentile(0.75)
        self.max = self.init_max_value()
    
    def __str__(self) -> str:
        return (f'Course: {self.name}\n'
                f'  Count:     {self.count}\n'
                f'  Mean:      {self.mean}\n'
                f'  Std:       {self.std}\n'
                f'  Min Score: {self.min}\n'
                f'  25%      : {self.percentile_25}\n'
                f'  50%      : {self.percentile_50}\n'
                f'  75%      : {self.percentile_75}\n'
                f'  Max Score: {self.max}\n')

    def init_min_value(self):
        return round(self.data_sorted[0], 4)
    
    def init_max_value(self):
        return round(self.data_sorted[len(self.data_sorted) - 1], 4)

    def init_percentile(self, divisor):
        count = self.count - 1
        index = count * divisor
        percentile = 0
        percentage = index - int(index)
        if index % 2 != 0:
            index = int(index)
            percentile = (self.data_sorted[index] + percentage * (self.data_sorted[index + 1] - self.data_sorted[index]))
        else:
            index = int(index)
            percentile = self.data_sorted[index]
        return round(percentile, 4)

    def sum(self):
        sum = 0
        for value in self.data_sorted:
            sum += value 
        return sum
    
    def mean_calcul(self):
        my_sum = self.sum()
        if self.count != 0:
            return round(my_sum / self.count, 4)
        else:
             return None
    
    def varirance(self):
        variance = 0
        for value in self.data_sorted:
            variance += (value - self.mean) ** 2
        if self.count == 0:
            return None
        variance = np.sqrt(variance/self.count)
        return round(variance, 4)
    
    def get_name(self):
        return self.name
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
        self.mean = 0
        self.std = 0
        self.min = self.init_min_value() 
        self.percentile_25 = self.get_percentile(0.25)
        self.percentile_50 = self.get_percentile(0.5)
        self.percentile_75 = self.get_percentile(0.75)
        self.max = self.init_max_value()
    
    def __str__(self) -> str:
        return (f'Course: {self.name}\n'
                f'  Count:     {self.count}\n'
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
        count = self.count + 1
        index = count * divisor
        percentile = 0
        print(index)
        if index % 2 != 0:
            index = int(index)
            percentile = (self.data_sorted[index] + self.data_sorted[index + 1]) / 2
        else:
            index = int(index)
            percentile = self.data_sorted[index]

        return round(percentile, 4)

    def get_percentile(self, divisor):
        print('---------------------------')
        print(self.count)
        index = math.ceil(divisor * (self.count))
        index_2 = index - 1
        print(index)
        print(index_2)
        return self.data_sorted[index]


    # def init_percentile_25(self):
    #     return self.data_sorted[0]
    
    # def init_percentile_50(self):
    #     return self.data_sorted[0]
    
    # def init_(self):
    #     return self.data_sorted[0]
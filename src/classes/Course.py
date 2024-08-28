import numpy as np
from typing import Union, List

num = Union[int, float, np.float64]

class Course:
    def __init__(self, name : str, raw_data: List[num], data_sorted : List[num]):
        self.name = name
        self.raw_data = raw_data
        self.data_sorted = data_sorted
        self.count = 0
        self.mean = 0
        self.std = 0
        self.min = self.init_min_value()
        self.percentile_25 = 0
        self.percentile_50 = 0
        self.percentile_75 = 0
        self.max = self.init_max_value()
    
    def __str__(self) -> str:
        return (f'Course: {self.name}\n'
                f'  Min Score: {self.min}\n'
                f'  Max Score: {self.max}')

    def init_min_value(self):
        return round(self.data_sorted[0], 4)
    
    def init_max_value(self):
        return round(self.data_sorted[len(self.data_sorted) - 1], 4)
    
    # def init_min_value(self):
    #     return self.data_sorted[0]
    
    # def init_min_value(self):
    #     return self.data_sorted[0]
    
    # def init_min_value(self):
    #     return self.data_sorted[0]
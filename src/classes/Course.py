import numpy as np
import math

from typing import Union, List

num = Union[int, float, np.float64]

class Course:
    def __init__(self, name : str, raw_data: List[num], normalize: bool = False):
        self.name : str = name
        self.raw_data : List[num] = raw_data
        # Compute count
        self.count : int = len(self.raw_data)
        # Compute mean with data avalaible
        self.mean : num = self.mean_calcul(raw_data)
        # Sorting the raw data
        self.data_sorted : List[num] = self.sort_data()
        # Compute new count
        self.count : int = len(self.data_sorted)
        

        self.std : num = self.varirance(self.data_sorted, self.mean)
        self.min : num = self.init_min_value(self.data_sorted) 
        self.percentile_25 : num = self.init_percentile(0.25, self.data_sorted)
        self.percentile_50 : num = self.init_percentile(0.5, self.data_sorted)
        self.percentile_75 : num = self.init_percentile(0.75, self.data_sorted)
        self.max : num = self.init_max_value(self.data_sorted)

        
        if normalize :
            self.data_zscore = self.normalize_data(self.data_sorted)
            self.mean_zscore = self.mean_calcul(self.data_zscore)
            self.std_zscore = self.varirance(self.data_zscore, self.mean_zscore)
            self.percentile_25_zscore = self.init_percentile(0.25, self.data_zscore)
            self.percentile_50_zscore = self.init_percentile(0.5, self.data_zscore)
            self.percentile_75_zscore = self.init_percentile(0.75, self.data_zscore)
            self.max_zscore = self.init_max_value(self.data_zscore)
            self.min_zscore= self.init_min_value(self.data_zscore) 
    def __str__(self) -> str:
        return (f'Course: {self.name}\n'
                f'  Count:      {self.count}\n'
                f'  Mean:       {self.mean}\n'
                f'  Std:        {self.std}\n'
                f'  Min Score:  {self.min}\n'
                f'  25%      :  {self.percentile_25}\n'
                f'  50%      :  {self.percentile_50}\n'
                f'  75%      :  {self.percentile_75}\n'
                f'  Max Score:  {self.max}\n'
                f'  Mean Zcore: {self.mean_zscore}\n'
                f'  Std Zcore:  {self.std_zscore}\n'
                f'  Min Zcore:  {self.min_zscore}\n'
                f'  25% Zcore:  {self.percentile_25_zscore}\n'
                f'  50% Zcore:  {self.percentile_50_zscore}\n'
                f'  75% Zcore:  {self.percentile_75_zscore}\n'
                f'  Max Zcore:  {self.max_zscore}\n'
                )


    def quick_sort(self, array : np.ndarray) -> np.ndarray:
        if len(array) <= 1:
            return array
        else:
            pivot = array[len(array) // 2]            
            left = [x for x in array if x < pivot]
            middle = [x for x in array if x == pivot]
            right = [x for x in array if x > pivot]
            return self.quick_sort(left) + middle + self.quick_sort(right)
    
    def sort_data(self) -> np.ndarray:
        # Getting the mean_value
        mean_value = self.get_mean()
        # Remplacing Nan data
        column_with_no_nan = np.array([num if not math.isnan(num) else mean_value for num in self.raw_data])
        # Sorting values
        column_data_sorted = self.quick_sort(column_with_no_nan)
        # Returning data column sorted
        return column_data_sorted

    # Init methods
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

    def sum(self, data):
        sum = 0
        for value in data:
            if not math.isnan(value):
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
    
    # Getters
    def get_describe_feature(self, describe_feature: str, normalized_flag: bool = False) -> float:
        match describe_feature:
            case 'name':
                return self.get_name()
            case 'raw_data':
                return self.get_raw_data()
            case 'data_sorted':
                return self.get_data_sorted(normalized_flag)
            case 'grades':
                return self.get_data_sorted(normalized_flag)
            case 'count':
                return self.get_count()
            case 'mean':
                return self.get_mean(normalized_flag)
            case 'std':
                return self.get_std(normalized_flag)
            case 'min':
                return self.get_min(normalized_flag)
            case 'percentile_25':
                return self.get_percentile_25(normalized_flag)
            case 'percentile_50':
                return self.get_percentile_50(normalized_flag)
            case 'percentile_75':
                return self.get_percentile_75(normalized_flag)
            case 'max':
                return self.get_max(normalized_flag)
            case _:
                raise ValueError(f"Unknown describe feature: {describe_feature}")
            
    # Getters with normalization flag
    def get_name(self) -> str:
        return self.name

    def get_raw_data(self) -> List[float]:
        return self.raw_data

    def get_data_sorted(self, normalized_flag: bool = False) -> List[float]:
        return self.data_zscore if normalized_flag else self.data_sorted

    def get_count(self) -> int:
        return self.count

    def get_mean(self, normalized_flag: bool = False) -> float:
        return self.mean_zscore if normalized_flag else self.mean

    def get_std(self, normalized_flag: bool = False) -> float:
        return self.std_zscore if normalized_flag else self.std

    def get_min(self, normalized_flag: bool = False) -> float:
        return self.min_zscore if normalized_flag else self.min

    def get_percentile_25(self, normalized_flag: bool = False) -> float:
        return self.percentile_25_zscore if normalized_flag else self.percentile_25

    def get_percentile_50(self, normalized_flag: bool = False) -> float:
        return self.percentile_50_zscore if normalized_flag else self.percentile_50

    def get_percentile_75(self, normalized_flag: bool = False) -> float:
        return self.percentile_75_zscore if normalized_flag else self.percentile_75

    def get_max(self, normalized_flag: bool = False) -> float:
        return self.max_zscore if normalized_flag else self.max
    
    def get_data_zscore(self) -> List[float]:
        return self.data_zscore
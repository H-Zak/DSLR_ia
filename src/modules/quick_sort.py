import numpy as np
import math

def quick_sort(array : np.ndarray) -> np.ndarray:
    if len(array) <= 1:
        return array
    else:
        pivot = array[len(array) // 2]            
        left = [x for x in array if x < pivot]
        middle = [x for x in array if x == pivot]
        right = [x for x in array if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)
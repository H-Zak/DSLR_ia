import numpy as np

class ClassBinarizer:
    def __init__(self, classes):
        self.classes = classes
    
    def binarize(self, y, target_class):
        list_labeled = [1.0 if label == target_class else 0.0 for label in y]
        return np.array(list_labeled)
    
    def binarize_all(self, y):
        return {cls: self.binarize(y, cls) for cls in self.classes}

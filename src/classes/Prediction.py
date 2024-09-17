import numpy as np

class Prediction:
    def __init__(self):
        self.raw_houses_likelihood = {
            'Gryffindor': 0.0, 
            'Hufflepuff': 0.0,
            'Ravenclaw': 0.0,  
            'Slytherin': 0.0
        }
    def __str__(self):
        return (f"Gryffindor: {self.raw_houses_likelihood['Gryffindor']}\n"
                f"Hufflepuff: {self.raw_houses_likelihood['Hufflepuff']}\n"
                f"Ravenclaw: {self.raw_houses_likelihood['Ravenclaw']}\n"
                f"Slytherin: {self.raw_houses_likelihood['Slytherin']}\n")


    def add_likelihood(self, house, likelihood):
        self.raw_houses_likelihood[house] = likelihood


    def softmax(self):
        predictions_array = [x for x in self.raw_houses_likelihood.values()]
        e_x = np.exp(predictions_array - np.max(predictions_array))
        return e_x / e_x.sum()

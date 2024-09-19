import json
import numpy as np

class Logger:
    def __init__(self, path_file, houses):
        self.path_file = path_file
        self.houses = houses

        self.log_info = {
            "features" : [],
            "score" : 0,
            "weights" : {}
        }

        for house in houses:
            self.log_info["weights"][house] = {
                "weigths" : [],
                "iterations" : 0
            }

        try:
            with open(self.path_file, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = []
        except ValueError:
            print('Decoding JSON has failed')
            exit()

    def set_features(self, features_list : list):
        self.log_info["features"] = features_list

    def set_weigths_for_house(self, house : str, weigths : np.ndarray):
        self.log_info["weights"][house]["weigths"] = weigths.tolist()
    
    def set_iterations_for_house(self, house : str, iterations : int):
        self.log_info["weights"][house]["iterations"] = iterations

    def set_score(self, score: int):
        self.log_info["score"] = score
    
    def create_log(self):
        self.data.append(self.log_info)
        with open(self.path_file, 'w') as file:
            json.dump(self.data, file ,indent=4)

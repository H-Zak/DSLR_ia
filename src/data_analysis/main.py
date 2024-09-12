import pandas as pd
import numpy as np
from typing import List

# Import utils
from modules.utils import get_tab_courses

def describe_data(path_to_data_file : str):
    # Reading data
    df = pd.read_csv(path_to_data_file)
    # Getting tab of courses
    courses_data = get_tab_courses(df)
    # Printing courses
    for course in courses_data:
        print(course)

def main():
    try:
        describe_data('../datasets/dataset_train.csv')
    except FileNotFoundError:
        print('Failed to read the dataset')


if __name__ == "__main__":
    main()

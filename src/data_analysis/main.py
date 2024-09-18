import pandas as pd
import numpy as np
from typing import List

# Import utils
from modules.utils import get_tab_courses, select_numeric_columns

def describe_data(df : pd.DataFrame, list_courses_str : list):
    # Getting tab of courses
    courses_data = get_tab_courses(df, list_courses_str)
    # Printing courses
    for course in courses_data:
        print(course)

def main():
    try:
        # Reading data
        df = pd.read_csv('../datasets/dataset_train.csv')
        # Getting all the columns with numeric values
        numeric_df = select_numeric_columns(df)
        # Getting names of the numeric columns
        list_courses = [column for column in numeric_df.columns if column != "Index" and column != "Hogwarts House"]
        
        describe_data(df, list_courses)
    except FileNotFoundError:
        print('Failed to read the dataset')


if __name__ == "__main__":
    main()

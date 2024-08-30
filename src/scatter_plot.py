import pandas as pd
import numpy as np
import math

from typing import Union, List

# Import course
from classes.Course import Course
# Import algo for sort
from modules.quick_sort import quick_sort

def sort_column(df : pd.DataFrame, name_column : str) -> np.ndarray:
    # Get values from the column
    column_data = df[name_column].values
    # Select all not Nan values
    column_with_no_nan = [num for num in column_data if not math.isnan(num)]
    # Sorting values
    column_data_sorted = quick_sort(column_with_no_nan)
    # Returning data column sorted
    return column_data_sorted

def get_tab_courses(df : pd.DataFrame) -> List[Course]:
    courses : List[Course] = []
    # Getting all the columns with numeric values
    numeric_df = df.select_dtypes(include=np.number)
    
    # Getting name of the numeric columns
    list_courses = [column for column in numeric_df.columns if column != "Index"]
    # Sorting data
    for course in list_courses:
        sort_data_course = sort_column(numeric_df, course)
        new_course = Course(course, numeric_df[course], sort_data_course)
        courses.append(new_course)

    return courses

def print_data_house_courses(house_courses : dict):
    
    for house in house_courses:
        print("******************************")
        print(house)
        print("******************************")
        for course in house_courses[house]:
            print(course)

def get_course_info_from_house(house_courses : dict, house_searched : str, course_searched : str):
    
    if house_searched in house_courses:
        for course  in house_courses[house_searched]:
            if course.get_name() == course_searched:
                print('//////////////////////')
                print(course)
                print('//////////////////////')

def describe_data_house(path_to_data_file : str):
    # Reading data
    df = pd.read_csv(path_to_data_file)
    # Getting Hogwarts's House
    houses = df['Hogwarts House'].unique()
    # Dict {'House' : List[Course]}
    house_courses = {}
    for house in houses:
        house_df = df[df['Hogwarts House'] == house]
        house_courses[house] = get_tab_courses(house_df)

def main():
    try:
        describe_data_house('../datasets/dataset_train.csv')
    except FileNotFoundError:
        print('Failed to read the dataset')


if __name__ == "__main__":
    main()
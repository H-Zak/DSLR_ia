import pandas as pd
import numpy as np

from typing import Union, List

# Import course
from classes.Course import Course
# Import algo for sort
from modules.quick_sort import quick_sort

df = pd.read_csv('../datasets/dataset_train.csv')

def sort_column(df : pd.DataFrame, name_column : str) -> np.ndarray:
    column_data = df[name_column].values

    column_data_sorted = quick_sort(column_data)

    return column_data_sorted

# def sort_all_course_columns(df : pd.DataFrame) -> dict:
#     # Getting all the columns with numeric values
#     numeric_df = df.select_dtypes(include=np.number)
#     # Getting name of the numeric columns
#     list_name_columns = [column for column in numeric_df.columns if column != "Index"]
    
#     return course_data_sorted

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

def describe_data(path_to_data_file : str):
    # Reading data
    df = pd.read_csv(path_to_data_file)

    courses_data = get_tab_courses(df)

    for course in courses_data:
        print(course)
    # # Sorting data
    # data_sorted = sort_all_course_columns(df)
    # # Printing data
    # # print(data_sorted)
    # print(data_sorted['Arithmancy'][0])

def main():
    try:
        describe_data('../datasets/dataset_train.csv')
    except FileNotFoundError:
        print('Failed to read the dataset')


if __name__ == "__main__":
    main()

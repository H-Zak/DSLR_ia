import pandas as pd
import numpy as np
from typing import List

# Import course
from classes.Course import Course


def select_numeric_columns(df : pd.DataFrame) -> pd.DataFrame:
    return df.select_dtypes(include=np.number)

def get_tab_courses(df : pd.DataFrame, list_str_courses) -> List[Course]:
    courses : List[Course] = []
    # Sorting data
    for course in list_str_courses:
        # sort_data_course = sort_column(numeric_df, course)
        new_course = Course(course, df[course], True)
        courses.append(new_course)

    return courses

def create_houses_list_of_course(df : pd.DataFrame, hogwarts_houses: dict, list_str_courses : list) -> dict:
    # unique_houses = hogwarts_data['Hogwarts House'].unique()
    courses_by_house = {}
    # Dict {'House' : List[Course]}
    for house in hogwarts_houses:
        house_data = df[df['Hogwarts House'] == house]
        courses_by_house[house] = get_tab_courses(house_data, list_str_courses)

    return courses_by_house

def get_name_for_plot(first_class, second_class, feature, normalized_flag):
    normalized : str = ''
    if normalized_flag:
        normalized = '_normalized'
    return f'./plots/{feature}{normalized}:{get_name_class_for_plot(first_class)}-VS-{get_name_class_for_plot(second_class)}'

def get_name_class_for_plot(class_name : str):
    return '-'.join(class_name.split(' ')).lower()
import pandas as pd
import numpy as np
import math

from scipy.stats import ks_2samp
import matplotlib.pyplot as plt


from typing import Union, List

# Import course
from classes.Course import Course
# Import algo for sort
from modules.quick_sort import quick_sort

# df = pd.read_csv('../datasets/dataset_train.csv')

def sort_column(df : pd.DataFrame, name_column : str) -> np.ndarray:
    column_data = df[name_column].values

    column_with_no_nan = [num for num in column_data if not math.isnan(num)]

    column_data_sorted = quick_sort(column_with_no_nan)

    # print(column_data_sorted)

    return column_data_sorted


def get_tab_courses(df : pd.DataFrame, flag) -> List[Course]:
    courses : List[Course] = []
    # Getting all the columns with numeric values
    numeric_df = df.select_dtypes(include=np.number)
    

    # Getting name of the numeric columns
    list_courses = [column for column in numeric_df.columns if column != "Index"]
    # print(list_courses)
    # Sorting data
    for course in list_courses:
        # print(course)
        sort_data_course = sort_column(numeric_df, course)
        new_course = Course(course, numeric_df[course], sort_data_course, flag)
        courses.append(new_course)

    return courses

def describe_data_house(path_to_data_file : str):
    # Reading data
    df = pd.read_csv(path_to_data_file)


    houses = df['Hogwarts House'].unique()
    house_courses = {}
    for house in houses:
        house_df = df[df['Hogwarts House'] == house]
        house_courses[house] = get_tab_courses(house_df, True)
        # print(house_courses[house][2])

    stat, p_value = ks_2samp(house_courses['Gryffindor'][2].data_zscore, house_courses['Slytherin'][2].data_zscore)
    # print(house_courses['Slytherin'][2], house_courses['Gryffindor'][2].data_sorted)
    print(f"Statistique K-S: {stat}, p-value: {p_value}")

    for course_index in range(len(house_courses['Gryffindor'])):
        print(len(house_courses['Gryffindor']))
        course_name = house_courses['Gryffindor'][course_index].name
        plt.figure(figsize=(10, 6))

        # Créer un histogramme pour chaque maison
        for house in houses:
            course_data = house_courses[house][course_index].data_zscore
            plt.hist(course_data, bins=10, alpha=0.5, label=house)

        plt.title(f'Histogrammes des scores par maison pour le cours {course_name}')
        plt.xlabel('Score')
        plt.ylabel('Nombre d\'étudiants')
        plt.legend()
        plt.show()



def describe_data(path_to_data_file : str):
    # Reading data
    df = pd.read_csv(path_to_data_file)

    courses_data = get_tab_courses(df, False)

    # for course in courses_data:
    #     print(course)



def main():
    try:
        # describe_data('../datasets/dataset_train.csv')#exo 1
        describe_data_house('../datasets/dataset_train.csv')
    except FileNotFoundError:
        print('Failed to read the dataset')


if __name__ == "__main__":
    main()

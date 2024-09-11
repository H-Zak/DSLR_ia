import pandas as pd
import numpy as np
import math
import sys
import os
import time
import itertools
import curses
import seaborn as sns
import matplotlib.pyplot as plt

from typing import Union, List, Tuple

# Import course
from classes.Course import Course
# Import exceptions
from exceptions.CourseNotFound import CourseNotFound
# Import algo for sort
from modules.quick_sort import quick_sort
# Import prompt
from modules.prompt import prompt
# Import plotters
from modules.plotting import scatter_plot
# Import utils
from modules.utils import get_name_for_plot
# Import logistic regression
from modules.logistic_regression import logistic_regression

def select_numeric_columns(df : pd.DataFrame) -> pd.DataFrame:
    return df.select_dtypes(include=np.number)

def get_tab_courses(df : pd.DataFrame) -> List[Course]:
    courses : List[Course] = []
    # Getting all the columns with numeric values
    numeric_df = select_numeric_columns(df)
    # Getting name of the numeric columns
    list_courses = [column for column in numeric_df.columns if column != "Index"]
    # Sorting data
    for course in list_courses:
        # sort_data_course = sort_column(numeric_df, course)
        new_course = Course(course, numeric_df[course], True)
        courses.append(new_course)

    return courses

def get_class_data_from_houses(house_courses : dict, course_searched : str) -> dict:

    grades_of_house : dict = {}
    course_found : bool = False
        
    for house in house_courses:
        for course in house_courses[house]:
            if course.get_name() == course_searched:
                course_found = True
                grades_of_house[house] = course

    if not course_found:
        raise CourseNotFound(course_searched)

    return grades_of_house

def create_houses_list_of_course(df : pd.DataFrame ,hogwarts_houses: dict) -> dict:
    # unique_houses = hogwarts_data['Hogwarts House'].unique()
    courses_by_house = {}
    # Dict {'House' : List[Course]}
    for house in hogwarts_houses:
        house_data = df[df['Hogwarts House'] == house]
        courses_by_house[house] = get_tab_courses(house_data)
        # print(courses_by_house)

    return courses_by_house

def extract_classes_grades_data(house_classes_data : dict, class_name : str) -> dict:
    
    # Class data
    class_data = get_class_data_from_houses(house_classes_data, class_name)    

    data_to_be_plotted : dict = {
        class_name : {},
    }

    for house in house_classes_data:
        data_to_be_plotted[class_data[house].get_name()][house] = class_data[house].get_describe_feature('grades', False)

    return data_to_be_plotted

def extract_house_feature_data(house_classes_data,
                               first_class : str, second_class : str,
                               feature : str, normalized_flag : bool) -> dict:
    

    first_class_data = get_class_data_from_houses(house_classes_data, first_class)    
    second_class_data = get_class_data_from_houses(house_classes_data, second_class)

    data_to_be_plotted : dict = {
        first_class : {},
        second_class : {}
    }

    for house in house_classes_data:
        data_to_be_plotted[first_class_data[house].get_name()][house] = first_class_data[house].get_describe_feature(feature, normalized_flag)
        data_to_be_plotted[second_class_data[house].get_name()][house] = second_class_data[house].get_describe_feature(feature, normalized_flag)

    return data_to_be_plotted


def execute_plotter_feature(house_classes_data : dict, classes : tuple, feature : str, normalized_flag : bool):
    # Extracting class from tuple
    first_class = classes[0]
    second_class = classes[1]
    # Getting data to be plotted
    data_to_be_plotted = extract_house_feature_data(house_classes_data, first_class, second_class, feature, normalized_flag)
    # Getting plot name
    plot_name = get_name_for_plot(first_class, second_class, feature, normalized_flag)
    # Plotting
    scatter_plot((first_class, second_class), data_to_be_plotted, plot_name)
    plt.show()

def search_classes_by_name(house_data : dict, class_searched : str):
    for class_name in house_data:
        if class_name.get_name() == class_searched:
            return class_name.get_describe_feature('grades')
        
def single_scatter_plot(ax, house_classes_data : dict, x_class : str, y_class : str):
    for house in house_classes_data:
        notes_house_x_class = search_classes_by_name(house_classes_data[house], x_class)
        notes_house_y_class = search_classes_by_name(house_classes_data[house], y_class)
        ax.scatter(notes_house_x_class, notes_house_y_class, label=house, alpha=0.7)

def pair_plot(house_classes_data : dict, list_classes : list):

    num_classes = len(list_classes)
    fig, axes = plt.subplots(nrows=num_classes, ncols=num_classes, figsize=(50, 50))
    
    for i, x_class in enumerate(list_classes):
        for j, y_class in enumerate(list_classes):
            ax = axes[i, j]
            if i != j:
                single_scatter_plot(ax, house_classes_data, x_class, y_class)
            else:
                for house in house_classes_data:
                    course_data = search_classes_by_name(house_classes_data[house], x_class)
                    ax.hist(course_data, bins=10, alpha=0.5, label=house)
            # Labels
            if j == 0:
                ax.set_ylabel(x_class, fontsize=8)
            if i == (num_classes - 1):
                ax.set_xlabel(y_class, fontsize=8)

    plt.tight_layout()
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, hspace=0.2, wspace=0.2)
    fig.savefig('pair_plot_large.png', dpi=300, bbox_inches='tight')

def map_hogwarts_house_to_class(hogwarts_house : str):
    match hogwarts_house:
        case 'Ravenclaw':
            return 1
        case 'Slytherin':
            return 2
        case 'Gryffindor':
            return 3
        case 'Hufflepuff':
            return 4
        case _:
            raise ValueError(f"Unknown Hogwarts House")
        
def get_x_matrix(numeric_df, list_classes):
    matrix_values = []
    for course in list_classes:
        new_course = Course(course, numeric_df[course], True)
        series_values = new_course.get_data_zscore()
        matrix_values.append(series_values)

    tmp_matrix = np.stack(matrix_values, axis=1)
    ones_column = np.ones((tmp_matrix.shape[0], 1))

    data_x = np.hstack((ones_column, tmp_matrix))
    return data_x


def main():
    try:
        # describe_data('../datasets/dataset_train_2.csv')#exo 1
        print("Logistic regression")
        # Reading data
        df = pd.read_csv('../datasets/dataset_train_2.csv')
        # Getting all the columns with numeric values
        numeric_df = select_numeric_columns(df)
        # Getting names of the numeric columns
        list_classes = [column for column in numeric_df.columns if column != "Index"]
        # Getting matrix of classes notes
        test_data_x = get_x_matrix(numeric_df, list_classes)
        # Getting y
        test_data_y = df['Hogwarts House'].apply(map_hogwarts_house_to_class).to_numpy()

        # print(test_data_x)

        print(type(test_data_x))
        print(type(test_data_y))

        # print(test_data_y)
        # # Get name of Hogwarts classes
        # unique_houses = df['Hogwarts House'].unique()
        
        # # Getting main data structure
        # house_classes_data = create_houses_list_of_course(df, unique_houses)




    except ValueError as e:
        print(e)
    except CourseNotFound as e:
        print(e)
    except FileNotFoundError:
        print('Failed to read the dataset')

if __name__ == "__main__":
    main()
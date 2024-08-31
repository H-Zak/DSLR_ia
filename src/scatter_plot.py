import pandas as pd
import numpy as np
import math
import sys
import os
import time
import itertools
import curses

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
from modules.utils import get_name_class_for_plot

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

def execute_plotter_grades(house_classes_data : dict, plot_choices : list):

    first_class : str = ''
    second_class : str = ''
    
    while True:
        first_class = curses.wrapper(lambda stdscr: prompt(stdscr, plot_choices, "Choose first class:\n", False))
        if first_class == 'EXIT':
            return
        second_class = curses.wrapper(lambda stdscr: prompt(stdscr, plot_choices, "Choose second class:\n", False))
        if second_class == 'EXIT':
            return
        if first_class != second_class:
            break
        else:
            print("The classes choised must be different")
            time.sleep(2)

    grades_of_first_class = get_class_data_from_houses(house_classes_data, first_class)
    grades_of_second_class = get_class_data_from_houses(house_classes_data, second_class)

    # Getting name of the numeric columns
    scatter_plot((first_class, second_class),
                 grades_of_first_class,
                 grades_of_second_class,
                 f'./plots/{get_name_class_for_plot(first_class)}-VS-{get_name_class_for_plot(second_class)}')


def main():
    try:
        # describe_data('../datasets/dataset_train_2.csv')#exo 1

        # 1. Plot all the grades of 2 classes for the four houses.
            # 4 casas
            # 2 classes
        # 2. Plot date with respect to a description characteristic (mean, std, etc).
            # All time
            # list of description characteristic



        # Reading data
        df = pd.read_csv('../datasets/dataset_train.csv')

        # Getting all the columns with numeric values
        numeric_df = select_numeric_columns(df)
        # Getting names of the numeric columns
        list_courses = [column for column in numeric_df.columns if column != "Index"]
        print(list_courses)
        
        # Get name of Hogwarts classes
        unique_houses = df['Hogwarts House'].unique()

        # Getting main data structure
        house_classes_data = create_houses_list_of_course(df, unique_houses)

    
        prompt_options = {
            '1. Plot two courses for all houses' : {
                'choice' : 1,
                'list_choices' : list_courses,
                'func' : execute_plotter_grades
            },

            '2. Plot date with respect to a description characteristic (mean, std, etc).' : {
                'choice' : 2,
                'list_choices' : ['mean', 'std', 'min', '25%', '50%', '75%', 'Max'],
                'func' : 'tete'
            },
        }

        # Lauch prompt
        while True:
            # os.system('clear')
            plot_choice = curses.wrapper(lambda stdscr: prompt(stdscr, list(prompt_options.keys()), "Choose the plot option:\n", False))
            if plot_choice == 'EXIT':
                break
            plot_data = prompt_options[plot_choice]
            plot_data['func'](house_classes_data, plot_data['list_choices'])

            # if first_class != second_choice:
            #     print('epa')
            # else:
            #     print("The classes choised must be different")
            #     time.sleep(2)
            #     continue

            time.sleep(2)
     

        # create_scatter_plot(choices[1], choices[2])

        # grades_of_first_class = get_class_data_from_houses(house_classes_data, first_class)
        # grades_of_second_class = get_class_data_from_houses(house_classes_data, second_class)

        # # # Getting name of the numeric columns
        # # list_courses = [column for column in numeric_df.columns if column != "Index"]

        # scatter_plot((first_class, second_class), grades_of_first_class, grades_of_second_class)

    except ValueError as e:
        print(e)
    except CourseNotFound as e:
        print(e)
    except FileNotFoundError:
        print('Failed to read the dataset')

if __name__ == "__main__":
    main()
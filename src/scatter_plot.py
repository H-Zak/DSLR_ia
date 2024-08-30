import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

def scatter_plot(classes: Tuple[str, str], 
                first_notes : dict, 
                second_notes : dict,
                plot_path : str='./plots/scatter_plots/plot_2.png'):

    data_to_be_plotted : dict = {
        classes[0] : {},
        classes[1] : {}
    }

    for house in first_notes:
        print(house)
        # first_notes[house].get_name()
        data_to_be_plotted[first_notes[house].get_name()][house] = first_notes[house].get_data_sorted()
        data_to_be_plotted[second_notes[house].get_name()][house] = second_notes[house].get_data_sorted()
        # data_to_be_plotted[first_notes[house].get_name()].append(first_notes[house].get_data_zscore())
        # data_to_be_plotted[second_notes[house].get_name()].append(second_notes[house].get_data_zscore())

     # Clear the current figure to prevent overlaying of plots
    plt.clf()

    plt.figure(figsize=(10, 6))

    houses = data_to_be_plotted[classes[0]].keys()

    for house in houses:
        arithmancy_scores = data_to_be_plotted[classes[0]][house]
        astronomy_scores = data_to_be_plotted[classes[1]][house]
        
        plt.scatter(arithmancy_scores, astronomy_scores, label=house, alpha=0.6)

    plt.xlabel(classes[0])
    plt.ylabel(classes[1])
    # Save the plot
    plt.savefig(plot_path)
    print(f'The plot has been saved in {plot_path}!')

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

# def describe_data(path_to_data_file : str):
#     # Reading data
#     df = pd.read_csv(path_to_data_file)

#     courses_data = get_tab_courses(df)

#     for course in courses_data:
#         print(course)


# def display_menu():
#     while True:
#         os.system('clear')
#         print("\n--- Main Menu ---")
#         print("1. Plot raw data")

#         choice = input("Choose an option: ")

def save_scatter_plot_from_choices():
    pass

def prompt(stdscr, collection_list, prompt_message, back):
    # Clear and refresh the screen
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    # Copy the collection list of options
    collection_lst = collection_list[:] 

    if back == True:
        collection_lst.append('GO BACK')
    collection_lst.append('EXIT')

    # Initialize the current selected option to 0
    current_option = 0
    
    # Loop indefinitely until a selection is made
    while True:
        # Clear the screen
        stdscr.clear()
        
        # Display the prompt message at the top of the screen
        stdscr.addstr(prompt_message)
        
        # Iterate over each item in the collection_lst
        for idx, item in enumerate(collection_lst):
            try:
                # Highlight the currently selected option
                if idx == current_option:
                    stdscr.addstr(f"> {item}\n", curses.A_BOLD)
                else:
                    stdscr.addstr(f"  {item}\n")
            except curses.error:
                print('The terminal window might be so small')
                exit()
        # Refresh the screen to display changes
        stdscr.refresh()
        
        # Get the user's input (key press)
        key = stdscr.getch()

        # Handle navigation keys (up and down arrow keys)
        if key == curses.KEY_UP:
            current_option = (current_option - 1) % len(collection_lst)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(collection_lst)
        # Handle selection (Enter key)
        elif key == 10:  # 'Enter' key
            # Return the selected option
            return collection_lst[current_option]

def main():
    try:
        # describe_data('../datasets/dataset_train_2.csv')#exo 1
        # if len(sys.argv) <= 2:
        #     raise ValueError("Not enough arguments provided")

        first_class : str = ''
        second_class : str = ''

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

        while True:
            # endpoint_choice = curses.wrapper(lambda stdscr: prompt(stdscr, list(list_courses)), "Choose the main endpoint:\n", False)
            first_class = curses.wrapper(lambda stdscr: prompt(stdscr, list_courses, "Choose the main endpoint:\n", False))
            if first_class == 'EXIT':
                break
            second_class = curses.wrapper(lambda stdscr: prompt(stdscr, list_courses, "Choose the main eeendpoint:\n", False))
            if second_class == 'EXIT':
                break

          

            if first_class != second_class:
                print('epa')
            else:
                print("The classes choised must be different")
                time.sleep(2)
                continue

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
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
from modules.plotting import scatter_plot, plot_scatter_in_ax
# Import utils
from modules.utils import get_name_for_plot

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

    # data_to_be_plotted = []

    for house in house_classes_data:
        data_to_be_plotted[class_data[house].get_name()][house] = class_data[house].get_describe_feature('grades', False)

    print(data_to_be_plotted)

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

def pair_plot_all_axes(house_classes_data: dict, list_classes: list):
    # Convertimos los datos a un DataFrame para facilitar la manipulación con Seaborn
    df = pd.DataFrame()
    for house, points in house_classes_data.items():
        temp_df = pd.DataFrame(points)
        temp_df['House'] = house
        df = pd.concat([df, temp_df], ignore_index=True)
    
    # Usamos seaborn para generar el pairplot
    sns.pairplot(df, hue="House", markers=["o", "s", "D"], 
                 plot_kws={'alpha': 0.5, 's': 15})  # Ajustamos la transparencia y el tamaño de los puntos
    
    plt.show()

def pair_plot(house_classes_data : dict, list_classes : list):

    num_classes = len(list_classes)
    fig, axes = plt.subplots(nrows=num_classes, ncols=num_classes, figsize=(15, 15))
    
    for i, x_class in enumerate(list_classes):
        for j, y_class in enumerate(list_classes):
            ax = axes[i, j]
            if i != j:
                for house, points in data.items():
                    ax.scatter(points[x_class], points[y_class], label=house, alpha=0.7)
                if i == num_classes - 1:
                    ax.set_xlabel(x_class, fontsize=8)
                if j == 0:
                    ax.set_ylabel(y_class, fontsize=8)
                if j == 0 and i == 0:
                    ax.legend(fontsize=6)
            else:
                ax.hist(data[list(data.keys())[0]][x_class], bins=10, alpha=0.7, color='gray')

    plt.tight_layout()
    plt.show()
    
    # list_classes_test = ['Arithmancy', 'Astronomy']
    # num_classes = len(list_classes)
    
    # f, axes = plt.subplots(nrows=num_classes, ncols=num_classes, figsize=(num_classes * 2, num_classes * 2))
    # # f, axes = plt.subplots(nrows = len(list_classes_test), ncols = len(list_classes_test), sharex=False, sharey = False)

    # for i, first_class in enumerate(list_classes):
    #     for j, second_class in enumerate(list_classes):
    #         print(f'{i}-{j}')
    #         ax = axes[i][j]
    #         if i != j:
    #             data_to_be_plotted = extract_house_feature_data(house_classes_data, first_class, second_class, 'grades', False)
    #             plot_scatter_in_ax(data_to_be_plotted, ax, (first_class, second_class))
    #         else:
    #             ax.set_visible(False)
    #             sns.histplot(house_classes_data, x=first_class, ax=ax, kde=True)

    # plt.tight_layout()
    # plt.savefig('./plots/pair_plot.png')
    # print(f'The plot has been saved in ./plots/pair_plot.png!')


    # axes[0][0].scatter(getRand(100),getRand(100), c = getRand(100), marker = "x")
    # axes[0][0].set_xlabel('Crosses', labelpad = 5)

    # axes[0][1].scatter(getRand(100),getRand(100), c = getRand(100), marker = 'o')
    # axes[0][1].set_xlabel('Circles', labelpad = 5)

    # axes[1][0].scatter(getRand(100),getRand(100), c = getRand(100), marker = '*')
    # axes[1][0].set_xlabel('Stars')

    # axes[1][1].scatter(getRand(100),getRand(100), c = getRand(100), marker = 's' )
    # axes[1][1].set_xlabel('Squares')

    # for house in house_classes_data:
    #     for first_class in list_classes_test:
    #         for second_class in list_classes_test:
    #             if first_class == second_class:
    #                 print(f"Histogram  of {first_class}")
    #         else:
    #             data_to_be_plotted = extract_house_feature_data(house_classes_data, first_class, second_class, 'grades', False)
    #             axes[0][0].scatter(getRand(100),getRand(100), c = getRand(100), marker = "x")
    #             first_class_scores = data_to_be_plotted[first_class][house]
    #             second_class_scores = data_to_be_plotted[second_class][house]
        
    #             plt.scatter(first_class_scores, second_class_scores,
    #                         label=house,
    #                         color=house_colors[house],
    #                         alpha=0.6)
    #             # print(f"Scatter plot of {first_class}-{second_class}")
    #             # print(extract_house_feature_data(house_classes_data, first_class, second_class, 'grades', False))

def main():
    try:
        # describe_data('../datasets/dataset_train_2.csv')#exo 1
        print("Pair plot")
        # Reading data
        df = pd.read_csv('../datasets/dataset_train.csv')

        # Getting all the columns with numeric values
        numeric_df = select_numeric_columns(df)
        # Getting names of the numeric columns
        list_classes = [column for column in numeric_df.columns if column != "Index"]

        # Get name of Hogwarts classes
        unique_houses = df['Hogwarts House'].unique()
        
        # Getting main data structure
        house_classes_data = create_houses_list_of_course(df, unique_houses)

        pair_plot(house_classes_data, list_classes)

    except ValueError as e:
        print(e)
    except CourseNotFound as e:
        print(e)
    except FileNotFoundError:
        print('Failed to read the dataset')

if __name__ == "__main__":
    main()
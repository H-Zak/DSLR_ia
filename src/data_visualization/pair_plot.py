import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import exceptions
from exceptions.CourseNotFound import CourseNotFound
# Import utils
from modules.utils import create_houses_list_of_course, select_numeric_columns, get_name_for_plot

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
    fig.savefig('./plots/pair_plot_large.png', dpi=300, bbox_inches='tight')

def main():
    try:
        # Reading data
        df = pd.read_csv('../datasets/dataset_train.csv')

        # Getting all the columns with numeric values
        numeric_df = select_numeric_columns(df)
        # Getting names of the numeric columns
        list_courses = [column for column in numeric_df.columns if column != "Index"]

        # Get name of Hogwarts classes
        unique_houses = df['Hogwarts House'].unique()
        
        # Getting main data structure
        house_classes_data = create_houses_list_of_course(df, unique_houses, list_courses)

        pair_plot(house_classes_data, list_courses)

    except ValueError as e:
        print(e)
    except CourseNotFound as e:
        print(e)
    except FileNotFoundError:
        print('Failed to read the dataset')

if __name__ == "__main__":
    main()
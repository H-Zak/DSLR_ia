import pandas as pd
import numpy as np
import curses
import time

# Import logistic regression and prediction
from logistic_regression.main import logistic_regression, predict
# Import evaluating function

from evaluation.evaluate import evaluate, save_feature_list
# Import classes
from classes.ClassBinarizer import ClassBinarizer

from classes.Course import Course
# Import exceptions
from exceptions.CourseNotFound import CourseNotFound
# Import utils
from modules.utils import select_numeric_columns
# Import prompt
from modules.prompt import prompt

def prepare_data_X(course_chosen, data):
    courses = []
    for course in course_chosen:
        if '/' in course:
            parts = course.split('/')
            combined_data = []
            for part in parts:
                course_data = data[part].tolist()
                combined_data.append(course_data)
            combined_mean_data = np.mean(combined_data, axis=0).tolist()
            courses.append(Course(course, combined_mean_data, True))
        else:
            course_data = data[course].tolist()
            courses.append(Course(course, course_data, True))
    
    # Creating DataFrame
    df_courses = pd.DataFrame()
    # Adding sorted data into DataFrame
    for course in courses:
        df_courses[course.name] = pd.Series(course.data_zscore)

    num_rows = len(df_courses)
    num_cols = len(courses) + 1 #car il a Hogwarts House qui n'est pas un cours, donc pas besoin de faire +1

    input_matrix = np.ones((num_rows, num_cols))
    # Creating input matrix from DataFrame
    for i, course in enumerate(courses):
        input_matrix[:, i + 1] = df_courses[course.name].values

    return input_matrix

def select_features(list_courses : list):
    chosen_courses: list = []
    feature : str = ''
    first_class : str = ''
    second_class : str = ''

    list_features = list_courses
    list_courses = [x for x  in list_courses if x != 'Hogwarts House']
    list_features.extend(['Combinaison', 'Finish'])
    
    while True:
        feature = curses.wrapper(lambda stdscr: prompt(stdscr, list_features, "Choose feature class:\n", False))
        if feature == 'EXIT':
            return
        elif feature == 'Finish':
            break
        elif feature == 'Combinaison':
            first_class = curses.wrapper(lambda stdscr: prompt(stdscr, list_courses, "Choose first class for combination:\n", False))
            if first_class == 'EXIT':
                break
            second_class = curses.wrapper(lambda stdscr: prompt(stdscr, list_courses, "Choose second class for combination:\n", False))
            if second_class == 'EXIT':
                break
            if first_class != second_class:
                chosen_courses.append(f"{first_class}/{second_class}")
            else:
                print("The classes chosen must be different")
                time.sleep(2)
                continue
        else:
            chosen_courses.append(feature)

    return chosen_courses


def main():
    try:
        # Reading data
        df = pd.read_csv('../datasets/dataset_train.csv')
        # Get name of Hogwarts classes
        unique_houses = df['Hogwarts House'].unique()
        # Getting all the columns with numeric values
        numeric_df = select_numeric_columns(df)
        # Getting names of the numeric columns
        list_courses = [column for column in numeric_df.columns if column != "Index" and column != "Hogwarts House"]

        features =  select_features(list_courses)

        data_X = prepare_data_X(features, numeric_df)

        raw_data_y = df['Hogwarts House'].to_numpy()


        # Initialize class binarizer
        binarizer = ClassBinarizer(unique_houses)

        predictions_list = []
        for house in unique_houses:
            data_y_by_house = binarizer.binarize(raw_data_y, house)
            print(data_y_by_house)
            w = logistic_regression(data_X, data_y_by_house, house)
            print(w)
            predictions = predict(data_X, w)
            predictions_list.append(predictions)


        predictions_matrix = np.column_stack(predictions_list)
        # print(predictions_matrix)
        predictions_house_indices = np.argmax(predictions_matrix, axis=1)
        # print(predictions_house_indices)
        save_feature_list(evaluate(df, predictions_house_indices), features)
        
    except ValueError as e:
        (e)
    except CourseNotFound as e:
        (e)
    except FileNotFoundError:
        ('Failed to read the dataset')

if __name__ == "__main__":
    main()
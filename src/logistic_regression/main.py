import pandas as pd
import numpy as np

from classes.ClassBinarizer import ClassBinarizer
from classes.Prediction import Prediction
# Import course
from classes.Course import Course
# Import exceptions
from exceptions.CourseNotFound import CourseNotFound
# Import utils
from modules.utils import select_numeric_columns
# Import plots
from modules.plotting import plot_cost_function_scatter

def derivative_of_w(predictions : np.ndarray, data_x : np.ndarray, data_y : np.ndarray) -> float:
    # Training examples
    m: int = data_x.shape[0]

    data_x_transpose = data_x.transpose()

    deviation = np.matmul(data_x_transpose, (predictions - data_y))

    # derivative_of_w : float = (1 / m) * np.sum(deviation, axis=0)

    return (1/m) * deviation

def sigmoid_function(z : np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-z))

def compute_cost_ft(data_x : np.ndarray, data_y : np.ndarray, weigths : np.ndarray):
    # Training examples
    m = len(data_y)
    # Predictions
    predictions = sigmoid_function(np.dot(data_x, weigths))
    # Cost functions
    cost = - (1 / m) * np.sum(data_y * np.log(predictions) + (1 - data_y) * np.log(1 - predictions))
    return cost

def logistic_regression(data_x: np.ndarray, data_y: np.ndarray, house : str, max_iterations : int = 10000, tolerance: float = 1e-6) -> np.ndarray:
    # Init weigths
    w = np.zeros(data_x.shape[1])
    # Learning rate
    learning_rate = 0.01
    # For plot function
    costs = []
    iterations = []

    # i = 0
    for i in range(max_iterations):
        # Performing predictions
        predictions = sigmoid_function(np.dot(data_x, w))
        # Perfoming derivatives for gradient descent decision
        dj_dw = derivative_of_w(predictions, data_x, data_y)

        # New array of weigths
        new_w = w - learning_rate * dj_dw
        # Computing costs for plot
        if i % 100 == 0:
            cost = compute_cost_ft(data_x, data_y, new_w)
            # print(f"Cost : {cost:.4f}")
            costs.append(cost)
            iterations.append(i)

        if np.linalg.norm(new_w - w) < tolerance:
            print(f"Converged after {i} iterations.")
            break

        w = new_w
        # i += 1

    plot_cost_function_scatter(iterations, costs, f'./plots/cost_function_scatter_{house}.png')
    return w

def predict(data_x: np.ndarray, w: np.ndarray) -> np.ndarray:

    z = np.dot(data_x, w)

    probabilities = sigmoid_function(z)
    # print(probabilities[0])

    # predictions = (probabilities >= 0.5).astype(int)
    
    return probabilities
        
def get_x_matrix(numeric_df, list_classes):
    matrix_values = []
    for course in list_classes:
        new_course = Course(course, numeric_df[course], True)
        series_values = new_course.get_data_zscore()
        matrix_values.append(series_values)

    tmp_matrix = np.stack(matrix_values, axis=1)
    ones_column = np.ones((tmp_matrix.shape[0], 1))
    matrix = np.hstack((ones_column, tmp_matrix))
    return matrix

def get_single_sample_from_dataset_test(index : int, list_classes : str):
    df = pd.read_csv('../datasets/dataset_train.csv')
    
    if index not in df.index:
        raise ValueError(f"Not index found in DataFrame.")
    
    example = df.loc[index]

    (example['Last Name'])
    
    means = df[list_classes].mean()
    stds = df[list_classes].std()
    
    examples_notes = [1.0]
    
    for subject in list_classes:
        if subject in example.index:
            normalized_note = (example[subject] - means[subject]) / stds[subject]
            examples_notes.append(normalized_note)
    
    return np.array(examples_notes)

def create_dict_predictions(house_list : list) -> dict:
    predictions = {}

    for house in house_list:
        predictions[house] = 0.0

    return predictions

def make_predictions():
    pass

def lab():
    test_df = pd.read_csv('../datasets/dataset_train.csv')
    y_true = get_data_Y(test_df)


def main():
    try:
        # Reading data
        df = pd.read_csv('../datasets/dataset_train.csv')
        # Get name of Hogwarts classes
        unique_houses = df['Hogwarts House'].unique()
        # Getting all the columns with numeric values
        numeric_df = select_numeric_columns(df)
        # Getting names of the numeric columns
        # list_classes = ['Charms', 'Potions', 'Flying', 'Herbology', 'Ancient Runes']
        list_classes = [column for column in numeric_df.columns if column != "Index" or column != "Hogwarts House"]
        # Getting matrix of classes notes
        data_x = get_x_matrix(numeric_df, list_classes)
        # Getting y
        raw_data_y = df['Hogwarts House'].to_numpy()


        # Initalize dict for save predictions
        predictions_results = create_dict_predictions(unique_houses)


        # Initialize class binarizer
        binarizer = ClassBinarizer(unique_houses)

        test_prediction = Prediction()

        for i, house in enumerate(unique_houses):
            data_y_by_house = binarizer.binarize(raw_data_y, house)
            w = logistic_regression(data_x, data_y_by_house, house)
            predictions = predict(data_x, w)
            test_prediction.add_likelihood(house, predictions[0])
            # print(predictions)
            # print(predictions[])

        print(test_prediction)
        print(test_prediction.softmax())
        print(np.sum(test_prediction.softmax()))
        
    except ValueError as e:
        (e)
    except CourseNotFound as e:
        (e)
    except FileNotFoundError:
        ('Failed to read the dataset')

if __name__ == "__main__":
    main()
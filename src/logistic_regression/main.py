import pandas as pd
import numpy as np

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

    derivative_of_w : float = (1 / m) * np.sum(deviation, axis=0)
    return derivative_of_w

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

def logistic_regression(data_x: np.ndarray, data_y: np.ndarray, max_iterations : int, tolerance: float = 1e-6) -> None:
    # Init weigths
    w = np.zeros(data_x.shape[1])
    # Learning rate
    learning_rate = 0.0001
    # For plot function
    costs = []
    iterations = []

    i = 0
    while True:
        # Performing predictions
        # print(w)
        predictions = sigmoid_function(np.dot(data_x, w))
        # Perfoming derivatives for gradient descent decision
        dj_dw = derivative_of_w(predictions, data_x, data_y)
        # New array of weigths
        new_w = w - learning_rate * dj_dw

        # Computing costs for plot
        if i % 100 == 0:
            cost = compute_cost_ft(data_x, data_y, new_w)
            print(f"Cost : {cost:.4f}")
            costs.append(cost)
            iterations.append(i)

        if np.linalg.norm(new_w - w) < tolerance:
            print(f"Converged after {i} iterations.")
            break

        w = new_w
        i += 1

    print(w)
    plot_cost_function_scatter(iterations, costs)
    return w

def predict(data_x: np.ndarray, w: np.ndarray) -> np.ndarray:
    z = np.dot(data_x, w)

    probabilities = sigmoid_function(z)

    predictions = (probabilities >= 0.5).astype(int)
    
    return predictions


def map_hogwarts_house_to_class(hogwarts_house : str):
    match hogwarts_house:
        case 'Ravenclaw':
            return 1
        case 'Slytherin' | 'Gryffindor' | 'Hufflepuff':
            return 0
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
    matrix = np.hstack((ones_column, tmp_matrix))
    return matrix

def get_single_sample_from_dataset_test(index : int, list_classes : str):
    df = pd.read_csv('../datasets/dataset_train_3.csv')
    
    if index not in df.index:
        raise ValueError(f"Not index found in DataFrame.")
    
    example = df.loc[index]

    print(example['Last Name'])
    
    means = df[list_classes].mean()
    stds = df[list_classes].std()
    
    examples_notes = [1.0]
    
    for subject in list_classes:
        if subject in example.index:
            normalized_note = (example[subject] - means[subject]) / stds[subject]
            examples_notes.append(normalized_note)
    
    return np.array(examples_notes)

def main():
    try:
        # describe_data('../datasets/dataset_train_2.csv')#exo 1
        print("Logistic regression")
        # Reading data
        df = pd.read_csv('../datasets/dataset_train.csv')
        # Getting all the columns with numeric values
        numeric_df = select_numeric_columns(df)
        # Getting names of the numeric columns
        list_classes = ['Charms', 'Potions', 'Flying']
        # Getting matrix of classes notes
        test_data_x = get_x_matrix(numeric_df, list_classes)
        print(test_data_x)
        # Getting y
        test_data_y = df['Hogwarts House'].apply(map_hogwarts_house_to_class).to_numpy()

        w = logistic_regression(test_data_x, test_data_y, 5)

        # Lab
        for i in range(50):
            data_test = get_single_sample_from_dataset_test(i, list_classes)

            predictions = predict(data_test, w)

            if predictions == 1:
                print(f'Index {i} is Ravenclaw')

    except ValueError as e:
        print(e)
    except CourseNotFound as e:
        print(e)
    except FileNotFoundError:
        print('Failed to read the dataset')

if __name__ == "__main__":
    main()
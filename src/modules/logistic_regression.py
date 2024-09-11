import numpy as np
import math
from typing import Union, Tuple

# Cost function
# from .cost_function import compute_cost_ft
# Import plot of cost function
# from .plotting import plot_cost_function_scatter

def partial_derivative_cost_function_of_w(data_x: np.ndarray, data_y: np.ndarray, w: float, b: float) -> float:
    """
    Computes the partial derivative of the cost function with respect to the slope (w).

    Args:
        data_x (np.ndarray): Feature data
        data_y (np.ndarray): Target values
        w (float): Current value of the slope (w).
        b (float): Current value of the y-intercept (b).

    Returns:
        float: The partial derivative of the cost function with respect to w.
    """
    # Number of training examples
    m: int = data_x.shape[0]
    
    # Compute the linear function hypothesis: f_wb = w * data_x + b
    f_wb: np.ndarray = w * data_x + b
    
    # Compute the deviation from the real value scaled by x
    deviation: np.ndarray = (f_wb - data_y) * data_x
    
    # Compute the derivative of w
    derivative_of_w: float = (1 / m) * np.sum(deviation)

    return derivative_of_w


def partial_derivative_cost_function_of_b(data_x: np.ndarray, data_y: np.ndarray, w: float, b: float) -> float:
    """
    Computes the partial derivative of the cost function with respect to the intercept (b).

    Args:
        data_x (np.ndarray): Feature data.
        data_y (np.ndarray): Target values.
        w (float): Current value of the slope (w).
        b (float): Current value of the y-intercept (b).

    Returns:
        float: The partial derivative of the cost function with respect to b.
    """
    # Number of training examples
    m: int = data_x.shape[0]
    
    # Compute the linear function hypothesis: f_wb = w * data_x + b
    f_wb: np.ndarray = w * data_x + b
    
    # Compute the deviation from the real value
    deviation: np.ndarray = f_wb - data_y
    
    # Compute the derivative of b
    derivative_of_b: float = (1 / m) * np.sum(deviation)
    
    return derivative_of_b

def gradient_descent(data_x: np.ndarray, \
                    data_y: np.ndarray,  \
                    initial_w: float, initial_b: float, learning_rate: float, tolerance: float = 1e-8, max_iterations: int = 5000):
    """
    Performs gradient descent to optimize w and b for a linear regression model.
    
    Args:
        data_x (np.ndarray): Feature data.
        data_y (np.ndarray): Target values.
        initial_w (float): Initial value for the slope (w).
        initial_b (float): Initial value for the intercept (b).
        learning_rate (float): Learning rate for gradient descent.
        tolerance (float): Convergence tolerance.
        max_iterations (int): Maximum number of iterations to run.

    Returns:
        Tuple[float, float]: The optimized values for w and b.
    """
    w = initial_w
    b = initial_b

    # For plot function
    costs = []
    iterations = []
    
    for i in range(max_iterations):
        # Compute gradients
        dj_dw = partial_derivative_cost_function_of_w(data_x, data_y, w, b)
        dj_db = partial_derivative_cost_function_of_b(data_x, data_y, w, b)


        # Update parameters
        new_w = w - learning_rate * dj_dw
        new_b = b - learning_rate * dj_db

        # Compute and print the cost
        if i % 100 == 0:
            cost = compute_cost_ft(data_x, data_y, new_w, new_b)
            costs.append(cost)
            iterations.append(i)

        # Check for convergence (if the change is smaller than the tolerance)
        if abs(new_w - w) < tolerance and abs(new_b - b) < tolerance:
            print(f"Converged after {i} iterations.")
            break

        # Update w and b for the next iteration
        w = new_w
        b = new_b

    plot_cost_function_scatter(iterations, costs)

    return w, b

# def lauch_gradient_descent(original_data_x: np.ndarray, original_data_y: np.ndarray, initial_w: float = 0, initial_b: float = 0) -> None:
#     """
#     Launches the gradient descent process for linear regression, including standardization 
#     and denormalization steps to determine the optimal coefficients.

#     Save the coefficients into a file.

#     Args:
#         original_data_x (np.ndarray): The original feature data
#         original_data_y (np.ndarray): The target values
#         initial_w (float, optional): The initial value for the slope (w).
#         initial_b (float, optional): The initial value for the intercept (b).

#     Returns:
#         None 
#     """
#     # Learning rate controls the step size in gradient descent:
#     # - Too small: Gradient descent may be slow.
#     # - Too large: Gradient descent may overshoot and fail to reach the minimum.
#     learning_rate: float = 0.01
    
#     # Standardize the feature data (Z-score standardization)
#     standardized_x: np.ndarray = standardization(original_data_x)
    
#     # Perform gradient descent to optimize w and b on standardized data
#     w, b = gradient_descent(standardized_x, original_data_y, initial_w, initial_b, learning_rate)
    
#     # Denormalize coefficients to return them to the original scale
#     w_final, b_final = denormalize_coefficients(original_data_x, w, b)

#     print(f"(w,b) found by gradient descent: ({w_final:8.4f},{b_final:8.4f})")

#     print(f"(w,b) found by gradient descent: ({w_final},{b_final})")

#     plot_with_regression_line(original_data_x, original_data_y, w_final, b_final)

#     save_coefficients_to_file(w_final, b_final, '../prediction/coefficients.txt')

def sigmoid_function(z : np.ndarray) -> np.ndarray:
    return np.divide(1, 1 + np.exp(-z))

def compute_cost(X, y, w, b):
    # Training examples
    m = len(y)
    # Predictions
    predictions = sigmoid_function(np.dot(X, w) + b)
    # Cost functions
    cost = - (1 / m) * np.sum(y * np.log(predictions) + (1 - y) * np.log(1 - predictions))
    return cost

def logistic_regression(data_x: np.ndarray, data_y: np.ndarray, max_iterations : int) -> None:
    # Init weigths
    w = np.zeros(data_x.shape[1])
    # Learning rate
    learning_rate = 0.01
    # For plot function
    costs = []
    iterations = []

    for i in range(max_iterations):
        predictions = sigmoid_function(np.dot(data_x, w))
        error = predictions - data_y

        print(error)


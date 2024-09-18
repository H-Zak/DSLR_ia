import matplotlib.pyplot as plt
from typing import Tuple

def scatter_plot(
                classes: Tuple[str, str], 
                data_to_be_plotted : dict,
                plot_path : str):
    
    # house_colors = {
    #     'Gryffindor': 'red',
    #     'Hufflepuff': 'yellow',
    #     'Ravenclaw': 'blue',
    #     'Slytherin': 'green'
    # }

    house_colors = {
        'Gryffindor': '#9c1203', 
        'Hufflepuff': '#e3a000',
        'Ravenclaw': '#00165e',  
        'Slytherin': '#033807'
    }

    # Clear the current figure to prevent overlaying of plots
    plt.clf()

    plt.figure(figsize=(10, 6))

    houses = data_to_be_plotted[classes[0]].keys()

    for house in houses:
        first_class_scores = data_to_be_plotted[classes[0]][house]
        second_class_scores = data_to_be_plotted[classes[1]][house]
        
        plt.scatter(first_class_scores, second_class_scores,
                    label=house,
                    color=house_colors[house],
                    alpha=0.6)

    # Adding the legends
    plt.legend()

    plt.xlabel(classes[0])
    plt.ylabel(classes[1])

    # Save the plot
    plt.savefig(plot_path)
    print(f'The plot has been saved in {plot_path}!')


def plot_cost_function_scatter(iterations: list, costs: list, plot_path: str = './plots/cost_function_scatter.png') -> None:
    """
    Creates a scatter plot of the cost function versus iterations.

    Args:
        iterations (list): List of iteration numbers.
        costs (list): List of corresponding cost values.
        plot_path (str, optional): Path where the plot will be saved.

    Returns:
        None
    """
    # Clear the current figure to prevent overlaying of plots
    plt.clf()
    
    # Create scatter plot
    # plt.scatter(iterations, costs, color='blue', marker='o')
    plt.plot(iterations, costs)

    # Setting labels and title
    plt.xlabel('Iteration')
    plt.ylabel('Cost')
    plt.title('Cost Function Scatter Plot')
    
    # Save the plot
    plt.savefig(plot_path)
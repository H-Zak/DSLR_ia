import matplotlib.pyplot as plt
from typing import Tuple

def scatter_plot(classes: Tuple[str, str], 
                first_notes : dict, 
                second_notes : dict,
                plot_path : str):

    data_to_be_plotted : dict = {
        classes[0] : {},
        classes[1] : {}
    }

    for house in first_notes:
        # data_to_be_plotted[first_notes[house].get_name()][house] = first_notes[house].get_data_sorted()
        # data_to_be_plotted[second_notes[house].get_name()][house] = second_notes[house].get_data_sorted()
        data_to_be_plotted[first_notes[house].get_name()][house] = first_notes[house].get_data_zscore()
        data_to_be_plotted[second_notes[house].get_name()][house] = second_notes[house].get_data_zscore()

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

    # plt.xlim(-2, 2)
    # plt.ylim(-2, 2)

    # Save the plot
    plt.savefig(plot_path)
    print(f'The plot has been saved in {plot_path}!')
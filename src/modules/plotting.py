import matplotlib.pyplot as plt
from typing import Tuple

def scatter_plot(
                classes: Tuple[str, str], 
                data_to_be_plotted : dict,
                plot_path : str):
    
    house_colors = {
        'Gryffindor': 'red',
        'Hufflepuff': 'yellow',
        'Ravenclaw': 'blue',
        'Slytherin': 'green'
    }

    # house_colors = {
    #     'Gryffindor': '#9c1203', 
    #     'Hufflepuff': '#e3a000',
    #     'Ravenclaw': '#00165e',  
    #     'Slytherin': '#033807'
    # }

    # Clear the current figure to prevent overlaying of plots
    plt.clf()

    plt.figure(figsize=(10, 6))

    houses = data_to_be_plotted[classes[0]].keys()

    for house in houses:
        print(house)
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

    # plt.xlim(-2, 2)
    # plt.ylim(-2, 2)

    # Save the plot
    plt.savefig(plot_path)
    print(f'The plot has been saved in {plot_path}!')

def plot_scatter_in_ax(data_to_be_plotted, ax, classes: Tuple[str, str]):

    house_colors = {
        'Gryffindor': 'red',
        'Hufflepuff': 'yellow',
        'Ravenclaw': 'blue',
        'Slytherin': 'green'
    }

    # print(data_to_be_plotted)

    houses = data_to_be_plotted[classes[0]].keys()

    for house in houses:
        first_class_scores = data_to_be_plotted[classes[0]][house]
        second_class_scores = data_to_be_plotted[classes[1]][house]
        
        ax.scatter(first_class_scores, second_class_scores,
                    label=house,
                    color=house_colors[house],
                    alpha=0.6)

    ax.set_xlabel(classes[0])
    ax.set_ylabel(classes[1])
    ax.tick_params(axis='both', which='major', labelsize=6)
    if ax.is_first_col() or ax.is_first_row():
        ax.legend(fontsize=6)



# def pair_plot(house_classes_data : dict, list_classes : list):

#     list_classes_test = ['Arithmancy', 'Astronomy']

#     for first_course in list_classes_test:
#         for second_course in list_classes_test:
#             if first_course == second_course:
#                 print(f"Histogram  of {first_course}")
#                 # print(numeric_df[first_course])
#                 # print('-----------------------')
#                 # print(numeric_df[second_course])
#                 # return
#             else:
#                 print(f"Scatter plot of {first_course}-{second_course}")
                    

    # f = plt.figure()
    # f, axes = plt.subplots(nrows = len(list_classes_test), ncols = len(list_classes_test), sharex=False, sharey = False)

    # axes[0][0].scatter(getRand(100),getRand(100), c = getRand(100), marker = "x")
    # axes[0][0].set_xlabel('Crosses', labelpad = 5)

    # axes[0][1].scatter(getRand(100),getRand(100), c = getRand(100), marker = 'o')
    # axes[0][1].set_xlabel('Circles', labelpad = 5)

    # axes[1][0].scatter(getRand(100),getRand(100), c = getRand(100), marker = '*')
    # axes[1][0].set_xlabel('Stars')

    # axes[1][1].scatter(getRand(100),getRand(100), c = getRand(100), marker = 's' )
    # axes[1][1].set_xlabel('Squares')

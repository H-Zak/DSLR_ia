import matplotlib.pyplot as plt

def plot_pair_grid(data, list_classes):
    num_classes = len(list_classes)
    fig, axes = plt.subplots(nrows=num_classes, ncols=num_classes, figsize=(15, 15))
    
    for i, x_class in enumerate(list_classes):
        for j, y_class in enumerate(list_classes):
            ax = axes[i, j]
            if i != j:
                for house, points in data.items():
                    ax.scatter(points[x_class], points[y_class], label=house, alpha=0.7)
                # if i == num_classes - 1:
                #     ax.set_xlabel(x_class, fontsize=8)
                # if j == 0:
                #     ax.set_ylabel(y_class, fontsize=8)
                # if j == 0 and i == 0:
                #     ax.legend(fontsize=6)
            else:
                ax.hist(data[list(data.keys())[0]][x_class], bins=10, alpha=0.7, color='gray')

            ax.set_xlabel(x_class, fontsize=8)

    plt.tight_layout()
    plt.show()

# Ejemplo de uso:
house_classes_data = {
    'Gryffindor': {'Arithmancy': [1, 2, 3, 4], 'Astronomy': [4, 5, 6, 7], 'Herbology': [2, 3, 4, 5]},
    'Slytherin': {'Arithmancy': [7, 8, 9, 10], 'Astronomy': [10, 11, 12, 13], 'Herbology': [3, 4, 5, 6]},
    'Ravenclaw': {'Arithmancy': [11, 12, 13, 14], 'Astronomy': [14, 15, 16, 17], 'Herbology': [5, 6, 7, 8]}
}

list_classes = ['Arithmancy', 'Astronomy', 'Herbology']

plot_pair_grid(house_classes_data, list_classes)

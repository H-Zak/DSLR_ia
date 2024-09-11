import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class HistogramApp(tk.Tk):
    def __init__(self, house_courses, houses):
        super().__init__()
        self.title("Histogram Viewer")
        self.course_index = 0
        self.course_index_x = 0
        self.course_index_y = 0
        self.house_courses = house_courses
        self.houses = houses
        self.mode = "effectif"
        
        self.figure = plt.Figure(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack()

        self.prev_button = tk.Button(self, text="Previous", command=self.prev_histogram)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self, text="Next", command=self.next_histogram)
        self.next_button.pack(side=tk.RIGHT)

         # Frame pour les boutons de mode et Y
        self.mode_frame = tk.Frame(self)
        self.mode_frame.pack(side=tk.BOTTOM, pady=10)

        self.prev_y_button = tk.Button(self.mode_frame, text="Prev Y", command=self.prev_y)
        self.prev_y_button.grid(row=0, column=0, padx=5)
        self.prev_y_button.grid_forget()

        self.toggle_button = tk.Button(self.mode_frame, text="Toggle Mode", command=self.toggle_mode)
        self.toggle_button.grid(row=0, column=1, padx=5)

        self.next_y_button = tk.Button(self.mode_frame, text="Next Y", command=self.next_y)
        self.next_y_button.grid(row=0, column = 2, padx=5)
        self.next_y_button.grid_forget()

        self.plot_histogram()

    def plot_effectif_histogram(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        course_name = self.house_courses['Gryffindor'][self.course_index].name
        
        for house in self.houses:
            course_data = self.house_courses[house][self.course_index].data_sorted
            ax.hist(course_data, bins=10, alpha=0.5, label=house)

        ax.set_title(f'Histogrammes des scores par maison pour le cours {course_name}')
        ax.set_xlabel('Score')
        ax.set_ylabel('Nombre d\'étudiants')
        ax.legend()
        self.canvas.draw()
    
    def toggle_mode(self):
        if self.mode == 'effectif':
            self.mode = 'comparison'
        else:
            self.mode = 'effectif'
        self.plot_histogram()

    def plot_comparison_histogram(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        course_name_x = self.house_courses['Gryffindor'][self.course_index_x].name
        course_name_y = self.house_courses['Gryffindor'][self.course_index_y].name
        
        for house in self.houses:
            course_data_x = self.house_courses[house][self.course_index_x].data_sorted
            course_data_y = self.house_courses[house][self.course_index_y].data_sorted
            min_size = min(len(course_data_x), len(course_data_y))
            # Tronquer les données
            course_data_x = course_data_x[:min_size]
            course_data_y = course_data_y[:min_size]
            ax.scatter(course_data_x, course_data_y, alpha=0.5, label=house)

        ax.set_title(f'Comparaison des scores pour les cours {course_name_x} et {course_name_y}')
        ax.set_xlabel(f'Scores {course_name_x}')
        ax.set_ylabel(f'Scores {course_name_y}')
        ax.legend()
        self.canvas.draw()


    def plot_histogram(self):
        if self.mode == 'effectif':
            self.plot_effectif_histogram()
            self.next_y_button.grid_forget()
            self.prev_y_button.grid_forget()
        else:
            self.plot_comparison_histogram()
            self.prev_y_button.grid(row=0, column=0, padx=5)  # Afficher le bouton en mode comparaison
            self.next_y_button.grid(row=0, column = 2, padx=5)  # Afficher le bouton en mode comparaison


    def prev_histogram(self):
        if self.mode == 'effectif':
            if self.course_index > 0:
                self.course_index -= 1
        else:
            if self.course_index_x > 0:
                self.course_index_x -= 1
            # if self.course_index_y > 0:
            #     self.course_index_y -= 1
        self.plot_histogram()

    def next_histogram(self):
        if self.mode == 'effectif':
            if self.course_index < len(self.house_courses['Gryffindor']) - 1:
                self.course_index += 1
        else:
            if self.course_index_x < len(self.house_courses['Gryffindor']) - 1:
                self.course_index_x += 1
            # if self.course_index_y < len(self.house_courses['Gryffindor']) - 1:
            #     self.course_index_y += 1
        self.plot_histogram()
    def next_y(self):
        if self.mode != 'effectif':
            if self.course_index_y < len(self.house_courses['Gryffindor']) - 1:
                self.course_index_y += 1
            self.plot_histogram()
    def prev_y(self):
        if self.mode != 'effectif':
            if self.course_index_y > 0:
                self.course_index_y -= 1
            self.plot_histogram()


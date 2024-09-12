import pandas as pd
from scipy.stats import ks_2samp

# Import HistogramApp
from classes.HistogramApp import HistogramApp
# Import algo for sort
from modules.utils import create_houses_list_of_course, select_numeric_columns

def main():
    try:
        # Reading data
        df = pd.read_csv('../datasets/dataset_train.csv')
        # Numeric columns
        numeric_df = select_numeric_columns(df)
        # Getting names of the numeric columns
        list_courses = [column for column in numeric_df.columns if column != "Index"]   
        # Get name of Hogwarts classes
        houses = df['Hogwarts House'].unique()

        # Getting main data structure
        house_courses = create_houses_list_of_course(df, houses, list_courses)
        
        stat, p_value = ks_2samp(house_courses['Gryffindor'][2].data_sorted, house_courses['Slytherin'][2].data_sorted)

        print(f"Statistique K-S: {stat}, p-value: {p_value}")
        app = HistogramApp(house_courses, houses)
        app.mainloop()
    except FileNotFoundError:
        print('Failed to read the dataset')


if __name__ == "__main__":
    main()

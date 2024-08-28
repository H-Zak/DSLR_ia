import pandas as pd
import numpy as np

df = pd.read_csv('../datasets/dataset_train.csv')

numeric_df = df.select_dtypes(include=np.number)

print(numeric_df.describe())
import pandas as pd
import numpy as np

def select_numeric_columns(df : pd.DataFrame) -> pd.DataFrame:
    return df.select_dtypes(include=np.number, exclude=int)

# Reading data
df = pd.read_csv('../datasets/dataset_train.csv')

# Getting all the columns with numeric values
numeric_df = select_numeric_columns(df)

print(numeric_df.corr(numeric_only = True))

list_classes = [column for column in numeric_df.columns if column != "Index"]
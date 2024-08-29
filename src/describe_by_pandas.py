import pandas as pd

# Charger votre DataFrame
df = pd.read_csv('../datasets/dataset_train.csv')

# Ajuster les options d'affichage
pd.set_option('display.max_columns', None)  # Afficher toutes les colonnes
pd.set_option('display.max_rows', None)     # Afficher toutes les lignes
pd.set_option('display.width', None)        # Ajuster la largeur de l'affichage

# Afficher le résultat complet de describe
print(df.describe())
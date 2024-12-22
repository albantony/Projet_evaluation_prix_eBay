import seaborn as sns
import pandas as pd
import seaborn as sns
from utils import load_data
import numpy as np
import matplotlib.pyplot as plt

df = load_data('data_semicleaned.csv')

#boite à moustache, permet de voir la répartition des valeurs d'une colonne et d'identifier les valeurs aberrantes
def generate_boxplot(df, column_name):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[column_name])
    plt.title(f'Boxplot of {column_name}')
    plt.xlabel(column_name)
    plt.show()

#generate_boxplot(df, 'Prix')
#generate_boxplot(df, 'PPI')
#generate_boxplot(df, 'RAM')
#generate_boxplot(df, 'Stockage')
#generate_boxplot(df, 'Taille écran')

# Générer un boxplot pour voir la répartition de la colonne PPI
#generate_boxplot(df, 'PPI')

#valeurs > 300 et < 80 sont des valeurs aberrantes => on les supprime
df.loc[(df['PPI'] > 300) | (df['PPI'] < 80), 'PPI'] = np.nan

df = df[(df['Prix'] >= 50) & (df['Prix'] <= 5000)]  # Supprimer les lignes avec des prix en dehors de la plage (on remplace par NaN car c'est la variable que l'on veut estimer)

# énormément de gens se trompent en mettant la même valeur pour la RAM et le stockage
df.loc[(df['RAM'] < 2) | (df['RAM'] > 64), 'RAM'] = np.nan  # On limite la RAM entre 2 et 64 Go
df.loc[(df['Stockage'] < 32) | (df['Stockage'] > 4000), 'Stockage'] = np.nan  # On limite le stockage entre 32 et 4000 Go
df.loc[df['Taille écran'] > 20, 'Taille écran'] = np.nan  # On limite la taille de l'écran à 20 pouces, seulement 3 valeurs au delà

# Sauvegarder le dataframe nettoyé dans un nouveau fichier CSV
df.to_csv('data_cleaned.csv', index=False)

#Infos générales sur le dataframe
df.info()


import seaborn as sns
import pandas as pd
import seaborn as sns
from utils import load_data
import matplotlib.pyplot as plt

df = load_data('data_cleaned.csv')

#On commence par des infos globales sur notre df
df.describe()
df.info()

def generer_graphe_prix_taille_ecran(df, marque):
    # Filtrer le DataFrame pour la marque spécifiée
    df_marque = df[df['Marque'] == marque]
    # Créer le graphe
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_marque, x='Taille écran', y='Prix')
    
    # Ajouter des labels et un titre
    plt.xlabel('Taille de l\'écran (pouces)')
    plt.ylabel('Prix (€)')
    plt.title(f'Relation entre le prix et la taille de l\'écran pour la marque {marque}')
    
    # Afficher le graphe
    plt.show()

#boite à moustache, permet de voir la répartition des valeurs d'une colonne et d'identifier les valeurs aberrantes
def generate_boxplot(df, column_name):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[column_name])
    plt.title(f'Boxplot of {column_name}')
    plt.xlabel(column_name)
    plt.show()

#generer_graphe_prix_taille_ecran(df, 'Apple')
#generate_boxplot(df, 'Prix')

# Générer un boxplot pour voir la répartition de la colonne PPI
#generate_boxplot(df, 'PPI')
#valeurs > 300 et < 80 sont des valeurs aberrantes => on les supprime
df = df[(df['PPI'] <= 300) & (df['PPI'] >= 80)]

generate_boxplot(df, 'Prix')

"""
df = df[(df['Price'] >= 50) & (df['Price'] <= 5000)]  # Limiter les prix
df = df[(df['RAM'] >= 2) & (df['RAM'] <= 64)]  # Limiter la RAM
df = df[(df['Stockage'] >= 32) & (df['Stockage'] <= 4000)]
"""
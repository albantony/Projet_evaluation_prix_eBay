import seaborn as sns
import pandas as pd
import seaborn as sns
from utils import load_data
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

df = load_data('data_cleaned.csv')

#simple graphe entre le prix et la taille de l'écran
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



def simple_regression_prix_colonne_marque(df, colonne, marque):
    """
    Régression linéaire simple entre le prix et une colonne spécifiée pour une marque donnée.
    Si on ne spécifie pas la marque, l'effet sera trop fortement biaisé par les différences de prix entre les marques.
    """
    # Filtrer le DataFrame pour la marque spécifiée
    df_marque = df[df['Marque'] == marque]
    
    # Supprimer les lignes avec des valeurs NaN dans les colonnes spécifiées
    df_marque = df_marque.dropna(subset=[colonne, 'Prix'])
    
    # Extraire les variables indépendantes (X) et dépendantes (y)
    X = df_marque[[colonne]].values
    y = df_marque['Prix'].values
    
    # Créer et entraîner le modèle de régression linéaire
    model = LinearRegression()
    model.fit(X, y)
    
    # Afficher les coefficients
    print(f'Coefficients de régression pour la colonne {colonne} et la marque {marque}:')
    print(f'Intercept: {model.intercept_}')
    print(f'Coefficient: {model.coef_[0]}')
    
    # Prédire les valeurs
    y_pred = model.predict(X)
    
    # Afficher le graphe avec la ligne de régression
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df_marque[colonne], y=df_marque['Prix'])
    plt.plot(df_marque[colonne], y_pred, color='red', linewidth=2)
    
    # Ajouter des labels et un titre
    plt.xlabel(colonne)
    plt.ylabel('Prix (€)')
    plt.title(f'Regression linéaire entre le prix et {colonne} pour la marque {marque}')
    
    # Afficher le graphe
    plt.show()
    
#generer_graphe_prix_taille_ecran(df, 'Apple')
simple_regression_prix_colonne_marque(df, 'PPI', 'Asus')
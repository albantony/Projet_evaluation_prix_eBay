import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# 1) Histogramme de la distribution des prix - graphe simple
def plot_log_distribution(df, column):
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column].apply(lambda x: np.log(x + 1)), bins=30, color='skyblue', kde=False, alpha=0.7)
    plt.title(f"Distribution logarithmique de {column}", fontsize=16)
    plt.xlabel(f"Logarithme de {column}", fontsize=14)
    plt.ylabel("Nombre", fontsize=14)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

# 2) Prix en fonction de PPI
def plot_price(df):
    # Supprimer les lignes avec des valeurs NaN dans 'Prix' ou 'Densité pixels'
    #df_clean = df.dropna(subset=['Prix', 'PPI'])

    # Création du graphique
    plt.figure(figsize=(10, 6))
    plt.scatter(df['PPI'], df['Prix'], c='blue', alpha=0.5)
    
    # Ajout des labels et du titre
    plt.title("Prix en fonction de la densité de pixels")
    plt.xlabel("Densité de pixels (PPI)")
    plt.ylabel("Prix (€)")
    
    # Affichage du graphique
    plt.grid(True)
    plt.show()

def ppi_price(df):
    plt.figure(figsize=(10, 6))
    plt.scatter(df['PPI'], df['Prix'], c='blue', alpha=0.5)
    plt.title("Prix en fonction de la densité de pixels")
    plt.xlabel("Densité de pixels (PPI)")
    plt.ylabel("Prix (€)")
    plt.grid(True)
    plt.show()
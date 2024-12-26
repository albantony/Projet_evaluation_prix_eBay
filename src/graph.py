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
    df_clean = df.dropna(subset=['Prix', 'PPI'])

    # Création du graphique
    plt.figure(figsize=(10, 6))
    plt.scatter(df_clean['PPI'], df_clean['Prix'], c='blue', alpha=0.5)
    
    # Ajout des labels et du titre
    plt.title("Prix en fonction de la densité de pixels")
    plt.xlabel("Densité de pixels (PPI)")
    plt.ylabel("Prix (€)")
    
    # Affichage du graphique
    plt.grid(True)
    plt.show()

# Histogramme selon l'état 

def etat(df):
    conditions_counts = df['Condition'].value_counts()
    plt.figure(figsize=(10, 6))
    plt.bar(conditions_counts.index, conditions_counts.values, color='skyblue')

    plt.title("Répartition des ordinateurs portables par état (condition)", fontsize=16)
    plt.xlabel("État", fontsize=14)
    plt.ylabel("Nombre d'ordinateurs", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)  # Inclinaison des labels pour éviter le chevauchement
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()
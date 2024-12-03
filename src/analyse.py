import matplotlib.pyplot as plt
import pandas as pd

def plot_price_vs_ppi(df):
    # S'assurer que les colonnes sont bien numériques
    df['Prix'] = pd.to_numeric(df['Prix'], errors='coerce')
    df['Densité pixels'] = pd.to_numeric(df['Densité pixels'], errors='coerce')

    # Supprimer les lignes avec des valeurs NaN dans 'Prix' ou 'Densité pixels'
    df_clean = df.dropna(subset=['Prix', 'Densité pixels'])

    # Création du graphique
    plt.figure(figsize=(10, 6))
    plt.scatter(df_clean['Densité pixels'], df_clean['Prix'], c='blue', alpha=0.5)
    
    # Ajout des labels et du titre
    plt.title("Prix en fonction de la densité de pixels")
    plt.xlabel("Densité de pixels (PPI)")
    plt.ylabel("Prix (€)")
    
    # Affichage du graphique
    plt.grid(True)
    plt.show()

# Exemple d'utilisation avec ton DataFrame df
# plot_price_vs_ppi(df)

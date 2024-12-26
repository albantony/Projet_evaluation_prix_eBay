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
    # Supprimer les lignes avec des valeurs NaN dans 'Prix' ou 'PPI'
    df_clean = df.dropna(subset=['Prix', 'PPI'])
    
    # Extraire les colonnes nécessaires
    x = df_clean['PPI']
    y = df_clean['Prix']
    
    # Calculer les coefficients de la régression linéaire
    coefficients = np.polyfit(x, y, 1)  # Ajuste une droite (polynôme de degré 1)
    trendline = np.poly1d(coefficients)
    
    # Création du graphique
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, c='blue', alpha=0.5, label="Données")
    
    # Ajouter la droite de tendance
    plt.plot(x, trendline(x), color='black', linewidth=2, label="Droite de tendance")
    
    # Ajouter des labels et un titre
    plt.title("Prix en fonction de la densité de pixels")
    plt.xlabel("Densité de pixels (PPI)")
    plt.ylabel("Prix (€)")
    plt.legend()
    plt.grid(True)
    
    # Afficher le graphique
    plt.show()

# Prix moyen selon la condition 

def avgprice_condition(df, marque=None):
    if marque:
        df = df[df['Marque'] == marque]
    
    avg_price_by_condition = df.groupby('Condition')['Prix'].mean().sort_values()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_price_by_condition.index, y=avg_price_by_condition.values)

    plt.title(f"Prix moyen des ordinateurs portables par condition{' pour ' + marque if marque else ''}", fontsize=16)
    plt.xlabel("État", fontsize=14)
    plt.ylabel("Prix moyen (€)", fontsize=14)
    plt.xticks(rotation=0, fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

# Prix moyen selon la marque 

def avgprice_brand(df):
    """
    Calcule et affiche le prix moyen des ordinateurs portables par marque.
    Cette fonction filtre les marques qui représentent moins de 5% du total des marques
    et les regroupe sous l'étiquette 'Autres'
    """
    brand_counts = df['Marque'].value_counts()
    threshold = 0.05 * brand_counts.sum()  # Seuil de 5% pour les marques
    filtered_brands = brand_counts[brand_counts >= threshold].index
    df['Marque'] = df['Marque'].apply(lambda x: x if x in filtered_brands else 'Autres')

    avg_price_by_brand = df.groupby('Marque')['Prix'].mean().sort_values()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_price_by_brand.index, y=avg_price_by_brand.values)

    plt.title("Prix moyen des ordinateurs portables par marque", fontsize=16)
    plt.xlabel("Marque", fontsize=14)
    plt.ylabel("Prix moyen (€)", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

# Prix moyen selon la marque et certaines spécificités 

def avgprice_brand2(df):

    # Filtrer les ordinateurs avec RAM de 8 Go et stockage de 256 Go
    filter = df[(df['RAM'] == 8) & (df['Stockage'] == 256)]

    # Calcul des marques représentant au moins 5% des occurrences
    brand_counts = filter['Marque'].value_counts()
    print(brand_counts)
    threshold = 0.05 * brand_counts.sum()  # Seuil de 5% pour les marques
    filtered_brands = brand_counts[brand_counts >= threshold].index
    filter.loc[:, 'Marque'] = filter['Marque'].apply(lambda x: x if x in filtered_brands else 'Autres')

    # Calcul du prix moyen par marque
    avg_price_by_brand = filter.groupby('Marque')['Prix'].mean().sort_values()

    # Création du graphique
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_price_by_brand.index, y=avg_price_by_brand.values)

    plt.title("Prix moyen des ordinateurs portables par marque (RAM: 8 Go, Stockage: 256 Go)", fontsize=16)
    plt.xlabel("Marque", fontsize=14)
    plt.ylabel("Prix moyen (€)", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

# Prix selon popularité 
def avg_price_popularity(df):
    popularity = df.groupby('Popularité')['Prix'].mean()

    plt.figure(figsize=(10, 6))
    sns.lineplot(x=popularity.index, y=popularity.values, marker='o')

    plt.title("Impact de la popularité des marques sur les prix moyens", fontsize=16)
    plt.xlabel("Popularité (Classement)", fontsize=14)
    plt.ylabel("Prix moyen (€)", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

# Prix moyen et médian par mois
def avg_price_per_month(df):
    # Extraire le mois
    df['Mois'] = df['Date de publication'].dt.month
    
    # Moyenne et médiane des prix par mois
    avg_price_per_month = df.groupby('Mois')['Prix'].mean()
    median_price_per_month = df.groupby('Mois')['Prix'].median()

    # Compter le nombre d'ordinateurs vendus par mois
    count_per_month = df['Mois'].value_counts().sort_index()
    print("Nombre d'ordinateurs vendus par mois :\n", count_per_month)

    # Visualisation
    plt.figure(figsize=(12, 6))
    plt.plot(avg_price_per_month.index, avg_price_per_month.values, marker='o', label='Prix moyen', color='skyblue')
    plt.plot(median_price_per_month.index, median_price_per_month.values, marker='o', label='Prix médian', color='orange')
    plt.title("Prix moyen et médian des ordinateurs portables par mois", fontsize=16)
    plt.xlabel("Mois", fontsize=14)
    plt.ylabel("Prix (€)", fontsize=14)
    plt.xticks(range(1, 13), ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'], fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()



# Matrice de variance-covariance

def covariance_matrix(df, col1, col2):
    covariance = df[[col1, col2]].cov()
    plt.figure(figsize=(6, 4))
    sns.heatmap(covariance, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title(f"Matrice de covariance entre {col1} et {col2}", fontsize=16)
    plt.show()
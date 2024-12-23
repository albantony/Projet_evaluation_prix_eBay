import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from utils import load_data
from aberrant import boxplot

df = load_data('data_cleaned.csv')

# 1) Histogramme de la distribution des prix - graphe simple
def plot_log_distribution(df, column):
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column].apply(lambda x: np.log(x + 1)), bins=30, color='skyblue', kde=False, alpha=0.7)
    plt.title(f"Distribution logarithmique de {column}", fontsize=16)
    plt.xlabel(f"Logarithme de {column}", fontsize=14)
    plt.ylabel("Nombre", fontsize=14)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

#plot_log_distribution(df, 'Prix')
#La log transformation permet d'observer une distribution normale des prix

#plot_log_distribution(df, 'PPI')
#plot_distribution(df, 'RAM')
#plot_distribution(df, 'Stockage')
#plot_distribution(df, 'Taille écran')

#boxplot
#boxplot(df, 'PPI')
#on peut générer des boxplots pour chaque colonne pour voir la répartition => trouver les colonnes pertinentes


#2) plot price
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

#plot_price(df)

#3) Histogramme condition

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

#etat(df)
#La plupart des ordinateurs sont d'occasion

#4) Pie chart marques 

def brand(df):
    brand_counts = df['Marque'].value_counts()
    threshold = 0.05 * brand_counts.sum() # Seuil de 5% pour les marques
    filtered_brands = brand_counts[brand_counts >= threshold]
    other_brands_count = brand_counts[brand_counts < threshold].sum()
    
    filtered_brands['Autres'] = other_brands_count
    
    plt.figure(figsize=(10, 10))
    plt.pie(filtered_brands, labels=filtered_brands.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title("Répartition des ordinateurs portables par marque", fontsize=16)
    plt.show()

#brand(df)

#5) Prix moyen par condition 

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

#avgprice_condition(df, 'Asus')


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
    sns.barplot(x=avg_price_by_brand.index, y=avg_price_by_brand.values, palette='pastel')

    plt.title("Prix moyen des ordinateurs portables par marque", fontsize=16)
    plt.xlabel("Marque", fontsize=14)
    plt.ylabel("Prix moyen (€)", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

#avgprice_brand(df)
#On voit que les prix des ordinateurs portables Apple sont les plus élevés, ce qui est cohérent avec la réputation de la marque
#Exclure les macbooks pourraient nous aider à identifier certains effets d'autres facteurs que la marque sur les prix


def covariance_matrix(df, col1, col2):
    covariance = df[[col1, col2]].cov()
    plt.figure(figsize=(6, 4))
    sns.heatmap(covariance, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title(f"Matrice de covariance entre {col1} et {col2}", fontsize=16)
    plt.show()

#covariance_matrix(df, 'Taille écran', 'PPI')
#j'avoue que j'ai du mal à l'interpréter, je ne sais pas si c'est pertinent
df['Date de publication'] = pd.to_datetime(df['Date de publication'], errors='coerce')


#6) Prix moyen par mois
def avg_price_per_month(df):
    df['Mois'] = df['Date de publication'].dt.month
    avg_price_per_month = df.groupby('Mois')['Prix'].mean()

    plt.figure(figsize=(10, 6))
    sns.lineplot(x=avg_price_per_month.index, y=avg_price_per_month.values, marker='o', color='skyblue')
    plt.title("Prix moyen des ordinateurs portables par mois", fontsize=16)
    plt.xlabel("Mois", fontsize=14)
    plt.ylabel("Prix moyen (€)", fontsize=14)
    plt.xticks(range(1, 13), ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'], fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

#avg_price_per_month(df)
#On observe une augmentation du prix moyen en décembre, c'est à dire sur les dernières offres
#on pourrait expliquer cela par le fait que ce ne sont que les mauvaises offres qui restent et les vendeurs baissent leurs prix au fur et à mesure


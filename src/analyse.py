import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from utils import load_data

df = load_data('data_cleaned.csv')

#plot price

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

#Histogramme condition

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
#La plupart des ordinateurs sont d'occasion, cette colonne nous apporte peu d'informations mais peut rester interessante

#Pie chart marques 

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

#Prix moyen par condition 

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

avgprice_brand(df)
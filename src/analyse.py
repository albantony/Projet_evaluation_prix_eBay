import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = load_data('data2.csv')
#plot price

def plot_price(df):
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

plot_price(df)

#Histogramme condition

def etat(df):
    conditions_counts = df['Condition'].value_counts()
    plt.bar(conditions_counts.index, conditions_counts.values, color='skyblue')

    plt.title("Répartition des ordinateurs portables par état (condition)", fontsize=16)
    plt.xlabel("État", fontsize=14)
    plt.ylabel("Nombre d'ordinateurs", fontsize=14)
    plt.xticks(rotation=0, fontsize=12)  # Inclinaison des labels si nécessaire
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

"""etat(df)"""

#Pie chart marques 

def brand(df):
    brand_counts = df['Marque'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(brand_counts, labels=brand_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title("Répartition des ordinateurs portables par marque", fontsize=16)
    plt.show()

"""brand(df)"""

#Prix moyen par condition 

def avgprice(df):
    avg_price_by_condition = df.groupby('Condition')['Prix'].mean().sort_values()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_price_by_condition.index, y=avg_price_by_condition.values)

    plt.title("Prix moyen des ordinateurs portables par état", fontsize=16)
    plt.xlabel("État", fontsize=14)
    plt.ylabel("Prix moyen (€)", fontsize=14)
    plt.xticks(rotation=0, fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

"""avgprice(df)"""



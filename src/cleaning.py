import pandas as pd
import numpy as np
from utils import extract_float_from_string  

df = pd.read_csv('data.csv')

# Transformation de la RAM en int (suppression de 'Go' et conversion en numérique)
df['RAM'] = df['RAM'].str.replace('Go', '', regex=False)  # Supprimer 'Go' de chaque valeur
df['RAM'] = pd.to_numeric(df['RAM'], errors='coerce')  # Convertir en numérique, avec gestion des erreurs

# Transformation de la taille de l'écran en float (suppression des guillemets et conversion)
df['Taille écran'] = df['Taille écran'].str.replace(r'\"', '', regex=True)  # Supprimer les guillemets
df['Taille écran'] = df['Taille écran'].apply(extract_float_from_string)  # Convertir en float avec la fonction personnalisée

# Extraction des résolutions correctes avec regex
df[['Largeur', 'Hauteur']] = df['Résolution'].str.extract(r'(\d+)[\s]*[xX][\s]*(\d+)', expand=True)

# Conversion en numérique pour les valeurs de largeur et hauteur
df['Largeur'] = pd.to_numeric(df['Largeur'], errors='coerce')
df['Hauteur'] = pd.to_numeric(df['Hauteur'], errors='coerce')

# Suppression des lignes avec des résolutions invalides (NaN)
df.dropna(subset=['Largeur', 'Hauteur'], inplace=True)

# Calcul de la densité de pixels (PPI)
df['Densité pixels'] = df.apply(
    lambda row: np.sqrt(row['Largeur']**2 + row['Hauteur']**2) / row['Taille écran'] if pd.notna(row['Largeur']) and pd.notna(row['Hauteur']) else np.nan,
    axis=1
)

# Affichage des résultats
print(df[['Taille écran', 'Largeur', 'Hauteur', 'Densité pixels']])

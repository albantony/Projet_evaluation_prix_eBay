import pandas as pd
import numpy as np
from utils import extract_float_from_object, load_data, extract_storage
import seaborn as sns
import matplotlib.pyplot as plt


def clean_giga_columns(df):
    df['RAM'] = df['RAM'].apply(extract_storage)
    df['Stockage'] = df['Stockage'].apply(extract_storage)
    return df

def normalize_color(color):
    if isinstance(color, str):
        color = color.lower()
        if 'gris' in color or 'silver' in color or 'argent' in color or 'argenté' in color or 'grey' in color and 'graphite' in color:
            return 'gris'
        elif 'noir' in color or 'black' in color:
            return 'noir'
        elif 'blanc' in color or 'white' in color:
            return 'blanc'
        elif 'bleu' in color or 'midnight' in color or 'blue' in color:
            return 'bleu'
        elif 'rouge' in color or 'red' in color:
            return 'rouge'
        elif 'vert' in color or 'green' in color:
            return 'vert'
        elif 'jaune' in color or 'yellow' in color:
            return 'jaune'
        elif 'rose' in color or 'pink' in color:
            return 'rose'
        elif 'marron' in color or 'brown' in color:
            return 'marron'
        elif 'violet' in color or 'purple' in color:
            return 'violet'
    return "autre"

def code_couleur(color):
    if color == "noir":
        return int(0)
    if color == "blanc":
        return int(1)
    if color == "gris":
        return int(2)
    if color == "bleu":
        return int(3)
    if color == "rouge":    
        return int(4)
    if color == "vert":
        return int(5)
    if color == "jaune":
        return int(6)
    if color == "rose":   
        return int(7)
    if color == "marron":
        return int(8)  
    if color == "violet":   
        return int(9)   
    if color == "autre":
        return int(10)

def clean_color_column(df):
    df['Couleur'] = df['Couleur'].apply(normalize_color)
    df['Code Couleur'] = df['Couleur'].apply(code_couleur)
    return df

def extract_resolution(df):
    df[['Largeur', 'Hauteur']] = df['Résolution'].str.extract(r'(\d+)[\s]*[xX][\s]*(\d+)', expand=True)
    df[['Largeur', 'Hauteur']] = df[['Largeur', 'Hauteur']].apply(pd.to_numeric, errors='coerce')
    return df

def extract_taille_ecran(df):
    df['Taille écran'] = df['Taille écran'].apply(extract_float_from_object)
    return df

def format_date(df):
    df['Date de publication'] = pd.to_datetime(df['Date de publication'], errors='coerce')
    return df

def calculate_ppi(df):
    # Assurez-vous que les colonnes 'Largeur', 'Hauteur' et 'Taille écran' sont numériques
    df['Taille écran'] = df['Taille écran'].apply(extract_float_from_object)
    # Remplir les valeurs manquantes avec NaN
    df[['Largeur', 'Hauteur', 'Taille écran']] = df[['Largeur', 'Hauteur', 'Taille écran']].replace(0, np.nan)
    # Calculez le PPI uniquement pour les lignes où toutes les valeurs nécessaires sont présentes
    mask = df[['Largeur', 'Hauteur', 'Taille écran']].notnull().all(axis=1)
    df.loc[mask, 'PPI'] = np.round(np.sqrt(df.loc[mask, 'Largeur']**2 + df.loc[mask, 'Hauteur']**2) / df.loc[mask, 'Taille écran'])
    return df

def convertir_condition(condition):
    """ 
    Crée une classification des conditions des produits du meilleur au pire
    """
    if "Neuf" in condition:
        return "Neuf"
    elif "Ouvert (jamais utilisé)" in condition:
        return "Ouvert"
    elif 'Parfait état - Reconditionné' in condition: 
        return "Parfait état"
    elif 'Très bon état - Reconditionné' in condition:
        return "Très bon état"
    elif 'État correct - Reconditionné' in condition:
        return "État correct"
    elif 'Occasion' in condition: 
        return "Occasion"

def clean_condition(df):
    df['Condition'] = df['Condition'].apply(convertir_condition)
    return df

def drop_columns(df, columns):
    return df.drop(columns=columns)

import pandas as pd
import numpy as np

def format_marque(marque):
    if isinstance(marque, str):
        marque = marque.lower()
        if any(substring in marque for substring in ['carte graphique', 'nvidia']):
            return np.nan
        elif 'apple' in marque or 'macbook' in marque:
            return 'Apple'
        elif 'dell' in marque or 'del' in marque:
            return 'Dell'
        elif 'hp' in marque:
            return 'HP'
        elif 'lenovo' in marque:
            return 'Lenovo'
        elif 'asus' in marque:
            return 'Asus'
        elif 'acer' in marque:
            return 'Acer'
        elif 'samsung' in marque:
            return 'Samsung'
        elif 'sony' in marque:
            return 'Sony'
        elif 'toshiba' in marque:
            return 'Toshiba'
        elif 'huawei' in marque:
            return 'Huawei'
        elif 'msi' in marque:
            return 'MSI'
        elif 'panasonic' in marque:
            return 'Panasonic'
        elif 'microsoft' in marque:
            return 'Microsoft'
        elif 'lg' in marque:
            return 'LG'
        elif 'google' in marque:
            return 'Google'
        elif 'alienware' in marque:
            return 'Alienware'
        elif 'razer' in marque:
            return 'Razer'
        elif 'gigabyte' in marque:
            return 'Gigabyte'
        elif 'clevo' in marque:
            return 'Clevo'
        elif 'fujitsu' in marque:
            return 'Fujitsu'
        elif 'medion' in marque:
            return 'Medion'
        elif 'xmg' in marque:
            return 'XMG'
        elif 'chuwi' in marque:
            return 'Chuwi'
        elif 'jumper' in marque:
            return 'Jumper'
        elif 'teclast' in marque:
            return 'Teclast'
        elif 'voyo' in marque:
            return 'Voyo'
        elif 'bmax' in marque:
            return 'BMAX'
        elif 'one-netbook' in marque:
            return 'One-Netbook'
        elif 'gpd' in marque:
            return 'GPD'
        elif 'tuxedo' in marque:
            return 'Tuxedo'
        elif 'system76' in marque:
            return 'System76'
        elif 'purism' in marque:
            return 'Purism'
        elif 'pine64' in marque:
            return 'Pine64'
        elif 'minisforum' in marque:
            return 'Minisforum'
        elif 'azulle' in marque:
            return 'Azulle'
        elif 'beelink' in marque:
            return 'Beelink'
        elif 'meego' in marque:
            return 'Meego'
        elif 'vorke' in marque:
            return 'Vorke'
        elif 'trigkey' in marque:
            return 'Trigkey'
        elif 'acepc' in marque:
            return 'ACEPC'
        elif 'awow' in marque:
            return 'AWOW'
        elif 'niuniutab' in marque:
            return 'Niuniutab'
        else:
            return np.nan
    return np.nan

def clean_brand_column(df):
    df['Marque'] = df['Marque'].apply(format_marque)
    df = df.dropna(subset=['Marque'])
    return df


def main():
    df = load_data('data3.csv')
    df = clean_giga_columns(df)
    df = clean_color_column(df)
    df = extract_resolution(df)
    df = extract_taille_ecran(df)
    df = clean_condition(df)
    df = calculate_ppi(df)
    df = format_date(df)
    df = clean_brand_column(df)
    df = drop_columns(df, ['Largeur', 'Hauteur', 'Résolution','Code Couleur'])
    df['Date de publication'] = pd.to_datetime(df['Date de publication'], errors='coerce')
    #la colonne résolution est remplacée par la colonne PPI qui compile taille de l'écran et résolution
    print(df['Rang'].unique())
    #génération d'un nouveau csv pour les données nettoyées
    df.to_csv('data_semicleaned.csv', index=False)

if __name__ == "__main__":
    main()
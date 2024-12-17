import pandas as pd
import numpy as np
from utils import extract_float_from_object, load_data

def clean_giga_columns(df):
    df['RAM'] = df['RAM'].apply(extract_float_from_object)
    df['Stockage'] = df['Stockage'].apply(extract_float_from_object)
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
    # Calculez le PPI uniquement pour les lignes où toutes les valeurs nécessaires sont présentes
    mask = df[['Largeur', 'Hauteur', 'Taille écran']].notnull().all(axis=1)
    df.loc[mask, 'PPI'] = np.sqrt(df.loc[mask, 'Largeur']**2 + df.loc[mask, 'Hauteur']**2) / df.loc[mask, 'Taille écran']
    return df

def convertir_condition(condition):
    """ 
    Crée une classification des conditions des produits du meilleur au pire
    """
    if "Neuf" in condition:
        return int(0)
    elif "Ouvert (jamais utilisé)" in condition:
        return int(1)
    elif 'Parfait état - Reconditionné' in condition: 
        return int(2)
    elif 'Très bon état - Reconditionné' in condition:
        return int(3)
    elif 'État correct - Reconditionné' in condition:
        return int(4)
    elif 'Occasion' in condition: 
        return int(5)

def clean_condition(df):
    df['Code Condition'] = df['Condition'].apply(convertir_condition)
    return df

def drop_columns(df, columns):
    return df.drop(columns=columns)

def main():
    df = load_data('data2.csv')
    df = clean_giga_columns(df)
    df = clean_color_column(df)
    df = extract_resolution(df)
    df = extract_taille_ecran(df)
    df = clean_condition(df)
    df = calculate_ppi(df)
    df = format_date(df)
    df = drop_columns(df, ['ID'])
    #print(df["Date de publication"].head(10))
    column_counts = df["Condition"].value_counts()
    print(column_counts)
    #génération d'un nouveau csv pour les données nettoyées
    df.to_csv('data_cleaned.csv', index=False)

if __name__ == "__main__":
    main()
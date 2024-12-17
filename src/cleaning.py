import pandas as pd
import numpy as np
from utils import extract_float_from_object

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

def convert_giga_to_numeric(ram_value):
    if isinstance(ram_value, str):
        numeric_value = extract_float_from_object(ram_value)
        if 'Go' in ram_value:
            return numeric_value
        elif 'To' in ram_value:
            return numeric_value * 1024
    return np.nan

def clean_giga_columns(df):
    df['RAM'] = df['RAM'].apply(extract_float_from_object)
    df['Stockage'] = df['Stockage'].apply(extract_float_from_object)
    return df

def normalize_color(color):
    if isinstance(color, str):
        color = color.lower()
        if 'gris' in color or 'silver' in color or 'argenté' in color:
            return 'gris'
        elif 'noir' in color or 'black' in color:
            return 'noir'
        elif 'blanc' in color or 'white' in color:
            return 'blanc'
        elif 'bleu' in color or 'blue' in color:
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

def clean_color_column(df):
    df['Couleur'] = df['Couleur'].apply(normalize_color)
    return df

def extract_resolution(df):
    df[['Largeur', 'Hauteur']] = df['Résolution'].str.extract(r'(\d+)[\s]*[xX][\s]*(\d+)', expand=True)
    df[['Largeur', 'Hauteur']] = df[['Largeur', 'Hauteur']].apply(pd.to_numeric, errors='coerce')
    return df

def extract_taille_ecran(df):
    df['Taille écran'] = df['Taille écran'].apply(extract_float_from_object)
    return df

def main():
    df = load_data('data.csv')
    df = clean_giga_columns(df)
    df = clean_color_column(df)
    df = extract_resolution(df)
    df = extract_taille_ecran(df)
    print(df["Stockage"].head(10))

if __name__ == "__main__":
    main()
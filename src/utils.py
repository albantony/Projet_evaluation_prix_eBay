import re
import numpy as np
import pandas as pd

def extract_float_from_object(obj):
    """
    Extrait un nombre flottant à partir d'un objet de type 'object'.
    """
    if isinstance(obj, str):  # On s'assure que l'entrée est bien une chaîne
        # Utiliser une expression régulière pour extraire les chiffres et la virgule éventuelle
        number = re.findall(r'[\d,]+', obj)
        
        if number:  # Si on a trouvé une correspondance
            clean_number = number[0].replace(',', '.').replace('"', '').strip()  # Remplacer la virgule par un point et supprimer les guillemets
            try:
                return float(clean_number)  # Convertir en float
            except ValueError:
                return np.nan
    elif isinstance(obj, (int, float)):  # Si l'objet est déjà un nombre
        return float(obj)
    return np.nan  # Si l'objet est invalide ou vide, retourner np.nan

#test rapide de la fonction extract_float_from_object
extract_float_from_object('on a mangé 4 pommes') # 256.0


def extract_storage(obj):
    """
    return the storage size in GB, or NaN if the input is invalid.
    """
    storage = str(obj)
    if 'TO' in storage.upper():
        return extract_float_from_object(obj) * 1024
    else:
        return extract_float_from_object(obj)

#test rapide de la fonction extract_storage
extract_storage('256Go')  # 256.0
extract_storage('1to')  # 1024.0

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")
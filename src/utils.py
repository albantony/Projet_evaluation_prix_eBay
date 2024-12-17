import re
import numpy as np

def extract_float_from_string(s):
    """
    Extrait un nombre flottant à partir d'une chaîne 
    """
    if isinstance(s, str):  # On s'assure que l'entrée est bien une chaîne
        # Utiliser une expression régulière pour extraire les chiffres et la virgule éventuelle
        number = re.findall(r'[\d,]+', s)
        
        if number:  # Si on a trouvé une correspondance
            clean_number = number[0].replace(',', '.').replace('"', '').strip()  # Remplacer la virgule par un point et supprimer les guillemets
            try:
                return float(clean_number)  # Convertir en float
            except ValueError:
                return np.nan
    return np.nan  # Si la chaîne est invalide ou vide, retourner np.nan

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

def convert_screen_size(screen_size):
    """
    Convertit une chaîne de caractères représentant la taille de l'écran en float.
    """
    if isinstance(screen_size, object):
        # Remplacer la virgule par un point et supprimer les guillemets
        clean_number = screen_size.replace(',', '.')
        clean_number = screen_size.replace('"', '').replace(' ', '')
    return clean_number

def extract_numeric_value(value):
    # Utilise une expression régulière pour extraire le premier nombre trouvé dans la chaîne
    import re
    match = re.search(r'(\d+(\.\d+)?)', value)
    if match:
        return float(match.group(1))
    return np.nan

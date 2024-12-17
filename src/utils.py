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

def convert_screen_size(screen_size):
    """
    Convertit une chaîne de caractères représentant la taille de l'écran en float.
    """
    if isinstance(screen_size, str):
        # Remplacer la virgule par un point et supprimer les guillemets
        clean_number = screen_size.replace(',', '.').replace('"', '').strip()
        try:
            return float(clean_number)
        except ValueError:
            return np.nan
    return np.nan

def extract_numeric_value(value):
    # Utilise une expression régulière pour extraire le premier nombre trouvé dans la chaîne
    import re
    match = re.search(r'(\d+(\.\d+)?)', value)
    if match:
        return float(match.group(1))
    return np.nan

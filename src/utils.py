import re

def extract_float_from_string(s):
    """
    Extrait un nombre flottant à partir d'une chaîne 
    """
    
    if isinstance(s, str):  # On s'assure que l'entrée est bien une chaîne
        # Utiliser une expression régulière pour extraire les chiffres et la virgule éventuelle
        number = re.findall(r'[\d,]+', s)
        
        if number:  # Si on a trouvé une correspondance
            clean_number = number[0].replace(',', '.')  # Remplacer la virgule par un point
            return float(clean_number)  # Convertir en float
    return None  # Si la chaîne est invalide ou vide, retourner None

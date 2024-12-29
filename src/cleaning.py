"""
Repertoire contenant certaines fonctions de nettoyage des données: 
Des fonctions longues mais simples non integrées au notebook par souci de lisibilité
"""

import numpy as np

def normalize_color(color):
    """
    Normalise les noms de couleurs en minuscules et les simplifie.
    """
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


def format_marque(marque):
    """
    Normalise les noms de marques en minuscules et les simplifie.
    """
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
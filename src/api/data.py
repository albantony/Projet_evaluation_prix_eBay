
import requests
from collect import access_token
import pandas as pd

# On initialise une liste vide pour les données plus tard
data = []

EBAY_TOKEN = access_token

# On fixe les paramètres de recherche

NUM_ITEMS = 25  # On limite à un certain nombre

# Lien API EBAY
EBAY_API_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

# Paramètres requête
params = {
    "category_ids": "175672", # Recherche pour ordinateurs portables/netbooks
    "limit": NUM_ITEMS,  
    "filter": "listingType: FIXED_PRICE" #On veut seulement les achats immédiats
}


HEADERS = {
    "Authorization": f"Bearer {EBAY_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-EBAY-C-MARKETPLACE-ID": "EBAY_FR" # On limite au marché français
}

# Recherche
response = requests.get(EBAY_API_URL, headers=HEADERS, params=params)

# Verif réponse
if response.status_code == 200:
    # Extraire les données JSON
    items_data = response.json().get('itemSummaries', [])
    
    # Tri des données
    for item in items_data:
        item_id = item['itemId']
        item_title = item['title']
        
        # URL API pour avoir les détails d'un item
        item_detail_url = f"https://api.ebay.com/buy/browse/v1/item/{item_id}"
        
        item_response = requests.get(item_detail_url, headers=HEADERS)
        
        if item_response.status_code == 200:
            item_details = item_response.json()
            
            # Initialisation des variables
            ram = None
            capacité = None
            marque = None
            couleur = None
            price = None
            condition = None
            monnaie = None
            taille = None
            
            # On extrait les informations de prix, condition et currency
            price_info = item_details.get('price', {})
            if price_info:
                price = price_info.get('value', None)
                monnaie = price_info.get('currency', None)
            
            condition = item.get('condition')
            
            # Extraire les infos précises du produit
            localized_aspects = item_details.get("localizedAspects", [])
            
            for aspect in localized_aspects:
                name = aspect.get("name", "").lower()
                value = aspect.get("value", "")
                
                # Info sur la RAM
                if "ram" in name:
                    ram = value
                # Info sur capacité de stockage
                elif "capacité" in name:
                    capacité = value
                # Marque
                elif "marque" in name:
                    brand = value
                # Couleur
                elif "couleur" in name:
                    couleur = value
                # Taille écran 
                elif "écran" in name:
                    taille = value

            if all([item_id, item_title, price, monnaie, condition, ram, capacité, brand, couleur, taille]) : 
                # On ne garde que les ordinateurs qui ont toutes les infos 
                data.append({
                "ID": item_id,
                "Title": item_title,
                "Prix": price,
                "Monnaie": monnaie,
                "Condition": condition,
                "RAM": ram,
                "Capacité de stockage": capacité,
                "Marque": brand,
                "Couleur": couleur,
                "Taille de l'écran": taille
            })
        
else:
    print(f"Erreur lors de la requête de recherche : {response.status_code}")
    print(response.json())

# Conversion en DataFrame
df = pd.DataFrame(data)

print(df.head(3))

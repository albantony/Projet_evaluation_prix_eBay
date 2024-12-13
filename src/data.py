import requests
from collect import access_token
import pandas as pd

# On initialise une liste vide pour les données plus tard
data = []

### Paramètre de la recherche ###

NUM_ITEMS = 25  # On limite à un certain nombre
ITEMS_VALIDES = 0 # On va comptabiliser les items ayant toutes les informations valides
OFFSET = 0 # On initialise un compteur offset pour relancer la requête si nous n'avons pas le bon nombre d'items 
EBAY_API_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

while ITEMS_VALIDES < NUM_ITEMS:
    params = {
    "category_ids": "175672", # Recherche pour ordinateurs portables/netbooks
    "offset" : OFFSET,
    "limit": 100,  
    "filter": "listingType: FIXED_PRICE" #On veut seulement les achats immédiats (pas d'enchères)
}

    HEADERS = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-EBAY-C-MARKETPLACE-ID": "EBAY_FR" # On limite le champ de recherche au marché français
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
                taille = None
                resolution = None
            
            # On extrait les informations de prix, condition
                price_info = item_details.get('price', {})
                if price_info:
                    price = price_info.get('value', None)            
                condition = item.get('condition')

                if condition and "pièces" in condition.lower():
                    continue  # Passer au prochain item
            
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
                        marque = value
                # Couleur
                    elif "couleur" in name:
                        couleur = value
                # Taille écran 
                    elif "écran" in name:
                        taille = value
                    elif "résolution" in name: 
                        resolution = value


                if all([price, condition, ram, capacité, marque, couleur, taille, resolution]) :
                    data.append({
                "ID": item_id,
                "Prix": price,
                "Condition": condition,
                "RAM": ram,
                "Stockage": capacité,
                "Marque": marque,
                "Couleur": couleur,
                "Taille écran": taille,
                "Résolution": resolution
                })
                    ITEMS_VALIDES += 1
                    if ITEMS_VALIDES >= NUM_ITEMS:
                        break
                
        
    else:
        print(f"Erreur lors de la requête de recherche : {response.status_code}")
        print(response.json())

    OFFSET += 100

# Conversion en DataFrame
df = pd.DataFrame(data)

#utile pour visualisation rapide en csv
df.to_csv("data.csv")
df = pd.read_csv("data.csv")



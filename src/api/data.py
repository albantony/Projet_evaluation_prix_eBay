
import requests
from collect import access_token
import pandas as pd

# On initialise une liste vide pour les données plus tard
data = []

EBAY_TOKEN = access_token

# On fixe les paramètres de recherche

SEARCH_QUERY = "laptop"
NUM_ITEMS = 5  # On limite à 5

# Lien API EBAY
EBAY_API_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

# Paramètres requête
params = {
    "q": SEARCH_QUERY,  # Recherche pour "laptop"
    "limit": NUM_ITEMS,  
    "filter": "listingType: FIXED_PRICE" #On veut seulement les achats immédiats
}


HEADERS = {
    "Authorization": f"Bearer {EBAY_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
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
            ram = "N/A"
            storage = "N/A"
            brand = "N/A"
            color = "N/A"
            price = "N/A"
            condition = "N/A"
            currency = "N/A"
            
            # On extrait les informations de prix, condition et currency
            price_info = item_details.get('price', {})
            if price_info:
                price = price_info.get('value', "N/A")
                currency = price_info.get('currency', "N/A")
            
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
                elif "capacity" in name:
                    storage = value
                # Marque
                elif "brand" in name:
                    brand = value
                # Couleur
                elif "color" in name:
                    color = value

            data.append({
                "Title": item_title,
                "Price": price,
                "Currency": currency,
                "Condition": condition,
                "RAM": ram,
                "Storage": storage,
                "Brand": brand,
                "Color": color
            })
        
else:
    print(f"Erreur lors de la requête de recherche : {response.status_code}")
    print(response.json())

# Conversion en DataFrame
df = pd.DataFrame(data)

print(df.head())

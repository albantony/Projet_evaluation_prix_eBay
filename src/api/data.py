
import requests
from collect import access_token

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
            
            print(item_id)
            print(f"Title: {item_title}")
            print(f"Price: {price} {currency}")
            print(f"Condition: {condition}")
            print(f"RAM: {ram}")
            print(f"Storage/Capacity: {storage}")
            print(f"Brand: {brand}")
            print(f"Color: {color}")
            print("-" * 40)
        
        else:
            print(f"Erreur pour l'article {item_title} (ID: {item_id}): {item_response.status_code}")
else:
    print(f"Erreur lors de la requête de recherche : {response.status_code}")
    print(response.json())

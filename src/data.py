import requests
from collect import access_token
import pandas as pd
import time

# Charger les données existantes
try:
    df_exist = pd.read_csv("data3.csv")
    existing_ids = set(df_exist["ID"])  # Extraire les IDs existants
    print(f"{len(existing_ids)} articles déjà présents dans le fichier CSV.")

except FileNotFoundError:
    print("Aucun fichier précédent trouvé, démarrage depuis le début.")
    existing_ids = set()

# On initialise une liste vide pour les données plus tard
data = []

### Paramètre de la recherche ###

NUM_ITEMS = 10000  # On limite à un certain nombre

# On va comptabiliser les items ayant toutes les informations valides
ITEMS_VALIDES = len(existing_ids)  

OFFSET = 0 # On initialise un compteur offset pour relancer la requête si nous n'avons pas le bon nombre d'items 

NBCALL = 0

MAXCALL = 4500

EBAY_API_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

while ITEMS_VALIDES < NUM_ITEMS and NBCALL < MAXCALL :
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
    NBCALL += 1

# Verif réponse
    if response.status_code == 200:
    # Extraire les données JSON
        items_data = response.json().get('itemSummaries', [])
    
    # Tri des données
        for item in items_data:
            if NBCALL >= MAXCALL or ITEMS_VALIDES >= NUM_ITEMS:
                break 


            item_id = item['itemId']

            if item_id in existing_ids:
                continue 
            
            # On ajoute l'ID à la liste des ID connus 
            existing_ids.add(item_id)
                
        # URL API pour avoir les détails d'un item
            item_detail_url = f"https://api.ebay.com/buy/browse/v1/item/{item_id}"
        
            item_response = requests.get(item_detail_url, headers=HEADERS)
            NBCALL +=1
        
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
                date = None
            
            # On extrait les informations de prix, condition
                price_info = item_details.get('price', {})
                if price_info:
                    price = price_info.get('value', None)            
                condition = item.get('condition')

            #On enlève les ordinateurs en pièces détachées 

                if condition and "pièces" in condition.lower():
                    continue  # Passer au prochain item
            
            # Extraire les infos précises du produit
                localized_aspects = item_details.get("localizedAspects", [])
                date = item_details.get("itemCreationDate")
            
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

                # On garde les lignes contenant obligatoirement ces 4 variables 

                if all([price, ram, capacité, marque]) :
                    data.append({
                "ID": item_id,
                "Prix": price,
                "Condition": condition,
                "RAM": ram,
                "Stockage": capacité,
                "Marque": marque,
                "Couleur": couleur,
                "Taille écran": taille,
                "Résolution": resolution,
                "Date de publication": date
                })
                    ITEMS_VALIDES += 1
                    
            time.sleep(0.2)
        
    else:
        print(f"Erreur lors de la requête de recherche : {response.status_code}")
        print(response.json())

    OFFSET += 100

# Conversion data frame 

df_new = pd.DataFrame(data)

if not df_new.empty:
    try:
        df_combined = pd.concat([df_exist, df_new]).drop_duplicates(subset="ID", keep="first")
    except NameError:
        df_combined = df_new

    df_combined.to_csv("data3.csv", index=False)
    print(f"Fichier mis à jour avec {len(df_combined)} articles uniques.")
else:
    print("Aucun nouvel article à ajouter.")

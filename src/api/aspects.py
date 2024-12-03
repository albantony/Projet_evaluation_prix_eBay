import requests
from collect import access_token

EBAY_TOKEN = access_token

# On spécifie l'ID
ITEM_ID = "326323962677"
ITEM_ID_FORMATED = f"v1|{ITEM_ID}|0"

# Lien de l'API
EBAY_API_URL = f"https://api.ebay.com/buy/browse/v1/item/{ITEM_ID_FORMATED}"


HEADERS = {
    "Authorization": f"Bearer {EBAY_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# On récupère les détails du produit
response = requests.get(EBAY_API_URL, headers=HEADERS)

# On vérifie si la requête fonctionne
if response.status_code == 200:
    # Extraire les données JSON
    item_data = response.json()
    
    # Accéder aux `localizedAspects`
    localized_aspects = item_data.get("localizedAspects", [])
    
    # Afficher les aspects localisés
    print("Localized Aspects:")

    for aspect in localized_aspects:
        # Joindre correctement les valeurs si elles sont dans une liste
        name = aspect.get("name", "N/A")
        value = "".join(aspect.get("value", []))  # Corrige les listes de caractères
        
        print(f"{name}: {value}")
else:
    # En cas d'erreur
    print(f"Erreur lors de la requête : {response.status_code}")
    print(response.json())

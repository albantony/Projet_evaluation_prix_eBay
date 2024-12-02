#collecte des données via l'API d'eBay
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# Vos identifiants API
APP_ID = os.getenv("APP_ID")
CERT_ID = os.getenv("CERT_ID")

if not APP_ID or not CERT_ID: 
    raise ValueError("Les identifiants API sont manquants ! Vérifiez votre fichier .env")

# Point de terminaison pour OAuth
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# Encodage Base64 des identifiants
auth = base64.b64encode(f"{APP_ID}:{CERT_ID}".encode()).decode()

# Headers pour la requête
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Données pour obtenir un token
data = {
    "grant_type": "client_credentials",
    "scope": "https://api.ebay.com/oauth/api_scope"
}

# Requête pour obtenir le token
response = requests.post(TOKEN_URL, headers=headers, data=data)

if response.status_code == 200:
    access_token = response.json().get("access_token")
    print(f"Access Token : {access_token}")
else:
    print("Erreur :", response.json())


# Remplacez ces variables avec vos propres valeurs
ebay_token = access_token  # Token d'accès OAuth
item_id = "123456789012"  # Remplacez par l'ID de l'objet que vous souhaitez rechercher

# URL de l'API eBay Shopping
url = "https://api.ebay.com/ws/api.dll"

# Les en-têtes nécessaires pour authentifier la requête
headers = {
    "X-EBAY-API-CALL-NAME": "GetSingleItem",
    "X-EBAY-API-SITEID": "0",  # ID de site eBay (0 pour eBay US)
    "X-EBAY-API-APP-ID": "VOTRE_APP_ID",  # Remplacez par votre propre App ID
    "X-EBAY-API-DEV-ID": "VOTRE_DEV_ID",  # Remplacez par votre propre Dev ID
    "X-EBAY-API-CERT-ID": "VOTRE_CERT_ID",  # Remplacez par votre propre Cert ID
    "Content-Type": "text/xml"
}

# Corps de la requête pour l'API GetSingleItem (demander des informations sur un seul objet)
body = f"""
<?xml version="1.0" encoding="utf-8"?>
<GetSingleItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <ItemID>{item_id}</ItemID>
    <DetailLevel>ItemSpecifics</DetailLevel>
    <IncludeSelector>Details,ItemSpecifics</IncludeSelector>
</GetSingleItemRequest>
"""

# Faire la requête à l'API eBay
response = requests.post(url, headers=headers, data=body)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Analysez la réponse XML
    response_xml = response.text
    print(response_xml)
    
    # Pour rechercher les spécifications de l'article (comme la RAM), vous pouvez analyser la réponse XML
    # Exemple d'extraction d'informations (vous pouvez utiliser une bibliothèque comme xml.etree.ElementTree)
else:
    print(f"Erreur de requête: {response.status_code}")

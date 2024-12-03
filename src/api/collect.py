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
    print("Token obtenu avec succès")
else:
    print("Erreur :", response.json())



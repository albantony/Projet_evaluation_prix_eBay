import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

df = pd.read_csv('data.csv')

#Mesure de l'intérêt des consommateurs
def extract_item_info(IDitem):
    url = f"https://www.ebay.com/itm/{IDitem}"
    request_text = requests.get(url).content
    page = BeautifulSoup(request_text, "html.parser")
    html_content = str(page.findAll("span", class_="ux-textspans"))

    # Expression régulière pour extraire les informations pertinentes
    watched_pattern = r"(\d+)\s*watched\s*in\s*the\s*last\s*24\s*hours"
    watchlist_pattern = r"(\d+)\s*have\s*added\s*this\s*to\s*their\s*watchlist"
    sold_pattern = r"(\d+)\s*has\s*already\s*sold"
    
    # Recherche des informations avec les expressions régulières
    watched_match = re.search(watched_pattern, html_content)
    watchlist_match = re.search(watchlist_pattern, html_content)
    sold_match = re.search(sold_pattern, html_content)
    
    # Extraire les résultats trouvés
    watched_count = int(watched_match.group(1)) if watched_match else 0
    watchlist_count = int(watchlist_match.group(1)) if watchlist_match else 0
    sold_count = int(sold_match.group(1)) if sold_match else 0
    
    # Retourner un dictionnaire avec les résultats
    print( {
        "watched": watched_count,
        "watchlist": watchlist_count,
        "sold": sold_count
    })

#Création du dictionnaire qui contient le classement pondéré de tout les sites
Classements = {}
marques_uniques = df['Marque'].dropna().unique()
marques_liste = marques_uniques.tolist()
for element in marques_liste:
    Classements[element] = 0  

# Création du dictionnaire qui contient les URL des diféérents sites comparatifs
url_sites = {
    "GeekWise": "https://www.geekwise.fr/fiabilite-des-marques-de-pc-classement-des-meilleures-options/",
    "LaptopSpirit": "https://www.laptopspirit.fr/meilleure-marque-ordinateur-portable",
    "ElectroGuide": "https://www.electroguide.com/top-12-marque-ordinateur-pc-portable-tablette",
    "LeParisien": "https://www.leparisien.fr/guide-shopping/high-tech/les-meilleures-marques-dordinateurs-portables-sur-le-marche-en-2024-27-09-2024-SNER775JEVDDHLDST4QPHLGCLY.php",
    "ApprendreInformatique": "https://www.apprendreinformatique.fr/top-10-des-meilleures-marques-dordinateurs-portables/",
    "SelfDirection": "https://www.selfdirection.org/quelle-marque-ordinateur-portable/",
    "FormationMax": "https://www.formationmax.com/actu/165/top-10-des-meilleures-marques-d-ordinateur-portable",
}

balise_sites = {     
    "GeekWise": "",
    "LaptopSpirit": "https://www.laptopspirit.fr/meilleure-marque-ordinateur-portable",
    "ElectroGuide": "https://www.electroguide.com/top-12-marque-ordinateur-pc-portable-tablette",
    "LeParisien": "https://www.leparisien.fr/guide-shopping/high-tech/les-meilleures-marques-dordinateurs-portables-sur-le-marche-en-2024-27-09-2024-SNER775JEVDDHLDST4QPHLGCLY.php",
    "ApprendreInformatique": "https://www.apprendreinformatique.fr/top-10-des-meilleures-marques-dordinateurs-portables/",
    "SelfDirection": "https://www.selfdirection.org/quelle-marque-ordinateur-portable/",
    "FormationMax": "https://www.formationmax.com/actu/165/top-10-des-meilleures-marques-d-ordinateur-portable",
}

def Classements_Scrape(url,Balise,SectionClass):
    request_text = requests.get(url).content
    page = BeautifulSoup(request_text, "html.parser")
    html_content = str(page.find(Balise, class_=SectionClass))
    soup = BeautifulSoup(html_content, "html.parser")
    links = soup.find_all("a")
    classement_ordis = {}
    rank = 1
    for link in links:
        text = link.get_text(strip=True)
        for marque in Classements:
            if marque in text and marque not in classement_ordis:
                classement_ordis[marque] = rank
                rank += 1
    for marque in Classements:
        if marque in classement_ordis:
            Classements[marque] = classement_ordis[marque]
    print(Classements)


















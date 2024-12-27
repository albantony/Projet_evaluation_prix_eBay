import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

df = pd.read_csv('data_cleaned.csv')
df3 = pd.read_csv('data3.csv')

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
    return {
        "watched": watched_count,
        "watchlist": watchlist_count,
        "sold": sold_count
    }

#Modification de la table pour ajouter le coefficient  
L_coeff=[]

for index, row in df.head(50).iterrows():
    IDitem = row["ID"].split('|')[1] 
    watched=extract_item_info(IDitem)["watched"]
    watchlist=extract_item_info(IDitem)["watchlist"]
    sold=extract_item_info(IDitem)["sold"]
    coeff=round((watched+2*watchlist+3*sold)/6,2)
    L_coeff.append(coeff)

df[:49,"Coefficent"]=L_coeff
df.to_csv('data_cleaned.csv', index=False)

#Dictionnaire qui contient le classement pondéré de tout les sites
Classements = {}
marques_uniques = df['Marque'].dropna().unique()
marques_liste = marques_uniques.tolist()
for element in marques_liste:
    Classements[element] = 0  

# Dictionnaire qui contient les URL des diféérents sites comparatifs
url_sites = {
    "GeekWise": "https://www.geekwise.fr/fiabilite-des-marques-de-pc-classement-des-meilleures-options/",
    "LaptopSpirit": "https://www.laptopspirit.fr/meilleure-marque-ordinateur-portable",
    "LeParisien": "https://www.leparisien.fr/guide-shopping/high-tech/les-meilleures-marques-dordinateurs-portables-sur-le-marche-en-2024-27-09-2024-SNER775JEVDDHLDST4QPHLGCLY.php",
    "ApprendreInformatique": "https://www.apprendreinformatique.fr/top-10-des-meilleures-marques-dordinateurs-portables/",
    "FormationMax": "https://www.formationmax.com/actu/165/top-10-des-meilleures-marques-d-ordinateur-portable",
    "Test-Achats" : "https://www.test-achats.be/hightech/ordinateurs-portables/news/meilleures-marques-ordinateurs-portables"
}

# Fonction qui retourne le classement pour le site Geekwise
def Classements_GeekWise(url):
    request_text=requests.get(url).content 
    page = BeautifulSoup(request_text,"html.parser")
    html_content=str(page.find("table"))
    soup = BeautifulSoup(html_content, "html.parser")
    marques = [td.get_text(strip=True) for td in soup.find_all("td", {"align": None})[::2]]  # On saute une cellule à chaque fois pour ne prendre que les marques
    classement_ordis = {marque: idx + 1 for idx, marque in enumerate(marques)}
    for marque in Classements:
        # Si la marque existe dans le deuxième dictionnaire, on remplace None par la valeur correspondante
        if marque in classement_ordis:
            Classements[marque] = classement_ordis[marque]
    return Classements

# Fonction qui retourne le classement pour le site LaptopSpirit
def Classements_LaptopSpirit(url):
    request_text = requests.get(url).content
    page = BeautifulSoup(request_text, "html.parser")
    html_content = str(page.find("nav", class_="lps-content-nav lps-main-nav"))
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
    return Classements
            
# Fonction qui retourne le classement pour le site LeParisien
def Classements_LeParisien(url):
    request_text = requests.get(url).content
    page = BeautifulSoup(request_text, "html.parser")
    html_content = str(page.findAll("h2", class_="inline_title margin_bottom_md margin_top_xxl"))
    soup = BeautifulSoup(html_content, "html.parser")
    links = soup.find_all("h2")
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
    return Classements

# Fonction qui retourne le classement pour le site ApprendreInformatique 
def Classements_ApprendreInformatique(url):
    request_text = requests.get(url).content
    page = BeautifulSoup(request_text, "html.parser")
    html_content = str(page.findAll("div", class_="the-post"))
    soup = BeautifulSoup(html_content, "html.parser")
    links = soup.find_all("h2")
    classement_ordis = {}
    rank = 1
    for link in links:
        text = link.get_text(strip=True)
        for marque in Classements:
            if marque.upper() in text and (marque) not in classement_ordis:
                classement_ordis[marque] = rank
                rank += 1
    seen = {}
    for key, value in classement_ordis.items():
        lower_key = key.lower()  # Convertir la clé en minuscules pour comparaison
        if lower_key not in seen:
            seen[lower_key] = (key, value)  # Conserver la version originale de la clé
    # Reconstruire un dictionnaire avec les clés originales
    classement_ordis = {original_key: value for original_key, value in seen.values()}
    for marque in Classements:
        if marque in classement_ordis:
            Classements[marque] = classement_ordis[marque]
    return Classements

# Fonction qui retourne le classement pour le site FormationMax 
def Classements_FormationMax(url):
    request_text = requests.get(url).content
    page = BeautifulSoup(request_text, "html.parser")
    html_content = str(page.findAll("h2"))
    soup = BeautifulSoup(html_content, "html.parser")
    links = soup.find_all("h2")
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
    return Classements

# Fonction qui retourne le classement pour le site Test-Achats 
def Classements_TestAchats(url):
    request_text = requests.get(url).content
    page = BeautifulSoup(request_text, "html.parser")
    html_content = str(page.findAll("li"))
    soup = BeautifulSoup(html_content, "html.parser")
    links = soup.find_all("li")
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
    return Classements

#Obtention du classement final 
dict= [

    Classements_GeekWise(url_sites["GeekWise"]),
    Classements_LaptopSpirit(url_sites["LaptopSpirit"]),
    Classements_LeParisien(url_sites["LeParisien"]),
    Classements_ApprendreInformatique(url_sites["ApprendreInformatique"]),
    Classements_FormationMax(url_sites["FormationMax"]),
    Classements_TestAchats(url_sites["Test-Achats"])
]

def rang()
    total_sum = {}
    count = {}

    # Parcourir chaque dictionnaire dans la liste
    for d in dict:
        for key, value in d.items():
            # Ajouter la valeur au total de la clé et incrémenter le compteur
            total_sum[key] = total_sum.get(key, 0) + value
            count[key] = count.get(key, 0) + 1

    # Calculer les moyennes pondérées et les convertir en entiers
    weighted_avg = {key: (total_sum[key] // count[key]) for key in total_sum}













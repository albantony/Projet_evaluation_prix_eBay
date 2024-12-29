import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests

df_test = pd.read_csv('data3.csv')
df = pd.read_csv('data3.csv')

#fonction asynchrone pour extraire les informations
async def fetch_item_info(session, IDitem):
    url = f"https://www.ebay.com/itm/{IDitem}"
    async with session.get(url) as response:
        request_text = await response.text()
        page = BeautifulSoup(request_text, "html.parser")
        html_content = str(page.findAll("span", class_="ux-textspans"))

        #expression régulière pour extraire les informations pertinentes
        watched_pattern = r"(\d+)\s*viewed\s*in\s*the\s*last\s*24\s*hours"
        watchlist_pattern = r"(\d+)\s*have\s*added\s*this\s*to\s*their\s*watchlist"
        sold_pattern = r"(\d+)\s*has\s*already\s*sold"
        want_pattern = r"(\d+)\s*(?:person|people)\s*(?:is|are)\s*watching\s*this"  

        #recherche des informations avec les expressions régulières
        watched_match = re.search(watched_pattern, html_content)
        watchlist_match = re.search(watchlist_pattern, html_content)
        sold_match = re.search(sold_pattern, html_content)
        want_match = re.search(want_pattern, html_content)

        #extraire les résultats trouvés
        watched_count = int(watched_match.group(1)) if watched_match else 0
        watchlist_count = int(watchlist_match.group(1)) if watchlist_match else 0
        sold_count = int(sold_match.group(1)) if sold_match else 0
        want_count= int(want_match.group(1)) if want_match else 0

        return {
            "watched": watched_count,
            "watchlist": watchlist_count,
            "sold": sold_count,
            "want": want_count
        }

#fonction pour traiter un lot de lignes
async def process_batch(df_batch):
    L_coeff = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _, row in df_batch.iterrows():
            IDitem = row["ID"].split('|')[1]
            tasks.append(fetch_item_info(session, IDitem))
        results = await asyncio.gather(*tasks)

        # Calcul des coefficients
        for result in results:
            watched = result["watched"]
            watchlist = result["watchlist"]
            sold = result["sold"]
            want = result["want"]
            coeff = round((watched + 2 * watchlist + 3 * sold + 2 * want) / 8, 2)
            L_coeff.append(coeff)
    return L_coeff

# fonction principale pour traiter tout le df
def get_coefficient(df, batch_size=100, output_file="output.csv"):
    #On ajoute une colonne coefficient si le df n'en a pas
    if "Coefficient" not in df.columns:
        df["Coefficient"] = None  #on initialise à None pour reconnaitre les lignes ou le coef est manquant

    #on ne traite que les lignes ou le coef est manquant pour assurer la reproductibilité du projet
    new_items_df = df[df["Coefficient"].isna()]
    for i in range(0, len(new_items_df), batch_size):
        print(f"Processing batch {i // batch_size + 1}...")
        df_batch = new_items_df.iloc[i:i+batch_size]
        L_coeff = asyncio.run(process_batch(df_batch))
        df.loc[df_batch.index, "Coefficient"] = L_coeff

    #On initilialise à 0.0 les coef pour ceux qui n'en ont pas
    df["Coefficient"] = df["Coefficient"].fillna(0.0)

    #On renvoie un csv pour mieux manipuler dans le notebook
    df.to_csv(output_file, index=False)
    print(f"Fichier CSV généré : {output_file}")

get_coefficient(df,100,'final_data.csv') #On sépare en paquet de 100 pour aller plus vite



#Dictionnaire qui contient le classement pondéré de tout les sites
Classements = {}
marques_uniques = df_test['Marque'].dropna().unique()
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
classement_sites= [

    Classements_GeekWise(url_sites["GeekWise"]),
    Classements_LaptopSpirit(url_sites["LaptopSpirit"]),
    Classements_LeParisien(url_sites["LeParisien"]),
    Classements_ApprendreInformatique(url_sites["ApprendreInformatique"]),
    Classements_FormationMax(url_sites["FormationMax"]),
    Classements_TestAchats(url_sites["Test-Achats"])
]

def get_rang(df):
    total_sum = {}
    count = {}

    # Parcourir chaque dictionnaire dans la liste
    for d in classement_sites:
        for key, value in d.items():
            total_sum[key] = total_sum.get(key, 0) + value
            count[key] = count.get(key, 0) + 1

    # Calculer les moyennes pondérées et les convertir en entiers
    weighted_avg = {key: (total_sum[key] // count[key]) for key in total_sum}

    # Ajouter les résultats au DataFrame
    df['Rang'] = df['Marque'].map(weighted_avg)
    return df
 













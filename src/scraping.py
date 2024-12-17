import requests
import bs4
import pandas as pd

df = pd.read_csv('data.csv')

#Création du dictionnaire qui contient le classement pondéré de tout les sites
Classements = {}
marques_uniques = df['Marque'].dropna().unique()
marques_liste = marques_uniques.tolist()
for element in marques_liste:
    Classements[element] = 0  

# Création du dictionnaire qui contient les URL des diféérents sites comparatifs
url_sites=  {
    "GeekWise": "https://www.geekwise.fr/fiabilite-des-marques-de-pc-classement-des-meilleures-options/",
    "LaptopSpirit": "https://www.laptopspirit.fr/meilleure-marque-ordinateur-portable",
    "ElectroGuide": "https://www.electroguide.com/top-12-marque-ordinateur-pc-portable-tablette",
    "LeParisien": "https://www.leparisien.fr/guide-shopping/high-tech/les-meilleures-marques-dordinateurs-portables-sur-le-marche-en-2024-27-09-2024-SNER775JEVDDHLDST4QPHLGCLY.php",
    "ApprendreInformatique": "https://www.apprendreinformatique.fr/top-10-des-meilleures-marques-dordinateurs-portables/",
    "SelfDirection": "https://www.selfdirection.org/quelle-marque-ordinateur-portable/",
    "FormationMax": "https://www.formationmax.com/actu/165/top-10-des-meilleures-marques-d-ordinateur-portable",
}

# Création de la fonction qui retourne le classement pour le site GeekWise
def Classements_GeekWise(url):
    request_text=requests.get(url).content 
    page = bs4.BeautifulSoup(request_text,"html")
    html_content=str(page.find("table"))
    soup = bs4.BeautifulSoup(html_content, "html.parser")
    marques = [td.get_text(strip=True) for td in soup.find_all("td", {"align": None})[::2]]  # On saute une cellule à chaque fois pour ne prendre que les marques
    classement_ordis = {marque: idx + 1 for idx, marque in enumerate(marques)}
    for marque in Classements:
        # Si la marque existe dans le deuxième dictionnaire, on remplace None par la valeur correspondante
        if marque in classement_ordis:
            Classements[marque] = classement_ordis[marque]
    return Classements

Classements_GeekWise(url_sites["GeekWise"])

















import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests

df1 = pd.read_csv('data3.csv')

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

        #calcul des coefficients
        for result in results:
            watched = result["watched"]
            watchlist = result["watchlist"]
            sold = result["sold"]
            want = result["want"]
            coeff = round((watched + 2 * watchlist + 3 * sold + 2 * want) / 8, 2)
            L_coeff.append(coeff)
    return L_coeff

# fonction principale pour traiter tout le df
def get_coefficient(df1, batch_size=100, output_file="output.csv"):
    #On ajoute une colonne coefficient si le df n'en a pas
    if "Coefficient" not in df1.columns:
        df1["Coefficient"] = None  #on initialise à None pour reconnaitre les lignes ou le coef est manquant

    #on ne traite que les lignes ou le coef est manquant
    new_items_df = df1[df1["Coefficient"].isna()]
    for i in range(0, len(new_items_df), batch_size):
        print(f"Processing batch {i // batch_size + 1}...")
        df_batch = new_items_df.iloc[i:i+batch_size]
        L_coeff = asyncio.run(process_batch(df_batch))
        df1.loc[df_batch.index, "Coefficient"] = L_coeff

    #on initilialise à 0.0 les coef pour ceux qui n'en ont pas
    df1["Coefficient"] = df1["Coefficient"].fillna(0.0)

    #On renvoie un csv pour mieux manipuler dans le notebook et assurer la reproductibilité
    df1.to_csv(output_file, index=False)
    print(f"Fichier CSV généré : {output_file}")

get_coefficient(df1,100,'final_data.csv') #On sépare en paquet de 100 pour aller plus vite



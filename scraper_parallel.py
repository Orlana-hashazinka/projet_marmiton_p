from scraper_functions import scraper_recette
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import time



# -------------------------------
# Lire les URLs
# -------------------------------
def lire_urls(fichier="urls_recettes.txt"):
    with open(fichier, "r", encoding="utf-8") as f:
        return [u.strip() for u in f.readlines() if u.strip()]


# -------------------------------
# Travail d'un thread
# -------------------------------
def worker(url):
    time.sleep(0.02)   
    return scraper_recette(url)


# -------------------------------
# Scraping parallèle (version rapide)
# -------------------------------
def scraper_parallel(nb_workers=20):
    urls = lire_urls()
    urls = urls[:10000]   # limiter à 10 000 recettes
    recettes = []
    futures = []
    erreurs = []

    print(f"Nombre total d'URLs à scraper : {len(urls)}")

    # Lancement de tous les workers
    with ThreadPoolExecutor(max_workers=nb_workers) as executor:

        # soumettre toutes les tâches
        futures = [executor.submit(worker, url) for url in urls]

       
        for f in tqdm(as_completed(futures), total=len(futures), desc="Scraping"):
            try:
                r = f.result()
                if r:
                    recettes.append(r)
            except Exception as e:
                erreurs.append(str(e))

            # Checkpoint toutes les 500 recettes
            #if len(recettes) % 500 == 0 and len(recettes) > 0:
            #    df_tmp = pd.DataFrame(recettes)
            #    df_tmp.to_csv("recettes_checkpoint.csv", index=False)
            #    print(f"Checkpoint sauvegardé ({len(recettes)} recettes)")


    # Sauvegarde finale 
    df = pd.DataFrame(recettes)
    df.to_csv("data/recettes_marmiton.csv", index=False)

    print("\n Scraping terminé !")
    print("Recettes valides :", len(df))
    print("Erreurs :", len(erreurs))

    return df


# -------------------------------
# Lancer le scraping
# -------------------------------
if __name__ == "__main__":
    df = scraper_parallel()




















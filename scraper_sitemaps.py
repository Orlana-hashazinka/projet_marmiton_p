##Importation des packages

import requests
from bs4 import BeautifulSoup
import time



## Techargement du sitemap principal

HEADERS = {"User-Agent": "M2-MAS-projet"}

# -----------------------------------------
# 1) Fonction générique : télécharger un contenu
# -----------------------------------------
def telecharger(url):
    """Télécharge une page XML/HTML et renvoie le texte."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            return r.text
        else:
            print("Erreur HTTP", r.status_code, "pour", url)
            return None
    except Exception as e:
        print("Exception pour", url, ":", e)
        return None


# -----------------------------------------
# 2) Fonction : extraire les balises <loc> d'un XML (voir si il faut enlever l'affichage)
# -----------------------------------------
def extraire_loc(xml_text):
    """Extrait la liste des balises <loc> d'un sitemap XML."""
    soup = BeautifulSoup(xml_text, "xml")
    loc_tags = soup.find_all("loc")
    return [loc.text.strip() for loc in loc_tags]


# -----------------------------------------
# 3) Fonction : écrire une liste dans un fichier
# -----------------------------------------
def ecrire_liste(fichier, liste):
    with open(fichier, "w", encoding="utf-8") as f:
        for item in liste:
            f.write(item + "\n")


# -----------------------------------------
# 4) Fonction : lire un fichier contenant une liste
# -----------------------------------------
def lire_liste(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        return [ligne.strip() for ligne in f.readlines() if ligne.strip()]


# -----------------------------------------
# 5) Fonction : extraire toutes les URLs de recettes
# -----------------------------------------
def extraire_urls_recettes_depuis_sitemaps(liste_sitemaps):
    """Parcourt chaque sitemap secondaire, télécharge son contenu,
       et extrait les URLs des recettes."""
    
    toutes_les_urls = []

    for i, sitemap_url in enumerate(liste_sitemaps, 1):
        print(f"\n Sitemap {i}/{len(liste_sitemaps)} : {sitemap_url}")

        xml = telecharger(sitemap_url)
        if xml:
            urls = extraire_loc(xml)   # les <loc> contiennent les recettes
            print(f"{len(urls)} URLs extraites")
            toutes_les_urls.extend(urls)

        time.sleep(0.5)  # politesse serveur

    return toutes_les_urls


# -----------------------------------------
# 6) Programme principal
# -----------------------------------------
def main():
    # Étape 1 : télécharger sitemap index
    print("Téléchargement du sitemap index…")
    xml_index = telecharger("https://www.marmiton.org/wsitemap_recipes_index.xml")

    # Étape 2 : extraire les sitemaps secondaires
    liste_sitemaps = extraire_loc(xml_index)
    print(f"{len(liste_sitemaps)} sitemaps secondaires trouvés.")

    ecrire_liste("liste_sitemaps_recettes.txt", liste_sitemaps)

    # Étape 3 : extraire toutes les URLs de recettes
    urls_recettes = extraire_urls_recettes_depuis_sitemaps(liste_sitemaps)

    print("\n Total des URLs recettes trouvées :", len(urls_recettes))

    # Étape 4 : sauvegarde finale
    ecrire_liste("urls_recettes.txt", urls_recettes)
    print("Fichier 'urls_recettes.txt' généré.")


if __name__ == "__main__":
    main()










import requests
from bs4 import BeautifulSoup



# -------------------------------
# Téléchargement page HTML
# -------------------------------

HEADERS = {"User-Agent": "M2-MAS-projet"}
session = requests.Session()



def telecharger_html(url):
    try:
        r = session.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            return r.text
        print("HTTP error:", r.status_code)
        return None
    except Exception as e:
        print("Exception:", e)
        return None

# -------------------------------
# Extraction ingrédients complets
# -------------------------------
def extraire_ingredients(soup):
    ingredients = []

    for bloc in soup.select(".card-ingredient"):
        # Quantité
        qte_tag = bloc.select_one(".card-ingredient-quantity")
        quantite = qte_tag.get_text(strip=True) if qte_tag else ""

        # Nom
        nom_tag = bloc.select_one(".ingredient-name")
        nom = nom_tag.get_text(strip=True) if nom_tag else ""

        # Complément
        comp_tag = bloc.select_one(".ingredient-complement")
        complement = comp_tag.get_text(strip=True) if comp_tag else ""

        # Construction finale propre
        ingr = " ".join(x for x in [quantite, nom, complement] if x)
        ingredients.append(ingr)

    return ingredients


# -----------------------------------------
# Convertir un texte "25 min" 
# -----------------------------------------

def convertir_minutes(txt):
    """Convertit les formats Marmiton: '3 h', '3h30', '3 min'."""
    if not txt or txt in ["-", ""]:
        return None

    txt = txt.lower().strip()

    # --------- FORMAT : "3 min" ------------
    if "min" in txt:
        return int(txt.replace("min", "").strip())

    # --------- FORMAT : "3 h" ------------
    # exemple: "3 h", "3h"
    if "h" in txt and "min" not in txt and (" " in txt or txt.endswith("h")):
        h = int(txt.replace("h", "").strip())
        return h * 60

    # --------- FORMAT : "3h30" ------------
    if "h" in txt and not " " in txt:
        # format collé ex: "3h30"
        h, m = txt.split("h")
        return int(h) * 60 + int(m)

    return None

# -----------------------------------------
# Nettoyer la sortie finale
# -----------------------------------------

def nettoyer_recette(recette):
    return {
        "titre": recette["titre"],
        "ingredients": recette["ingredients_raw"].split(" | ") if recette["ingredients_raw"] else [],
        "etapes": recette["etapes"].split(" || ") if recette["etapes"] else [],
        "difficulte": recette["difficulte"],
        "cout": recette["cout"],
        "personnes": recette["personnes"],
        "temps_preparation": convertir_minutes(recette["temps_preparation"]),
        "temps_cuisson": convertir_minutes(recette["temps_cuisson"]),
        "temps_repos": convertir_minutes(recette["temps_repos"]),
        "temps_total": convertir_minutes(recette["temps_total"]),
        "image": recette["image"],
        "url": recette["url"]
    }

# -------------------------------
# Scraper une seule recette
# -------------------------------

def scraper_recette(url):
    html = telecharger_html(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "lxml")

    # ---- TITRE ----
    titre = soup.find("h1").get_text(strip=True) if soup.find("h1") else None

    # ---- INGRÉDIENTS ----
    ingredients = extraire_ingredients(soup)


    # ---- NOMBRE DE PERSONNES ----
    nb_personnes = None
    compteur = soup.select_one(".mrtn-recette_ingredients-counter")

    if compteur and compteur.has_attr("data-servingsnb"):
        try:
            nb_personnes = int(compteur["data-servingsnb"])
        except ValueError:
            nb_personnes = None

    # ---- ÉTAPES ----
    etapes = [
        p.get_text(strip=True)
        for p in soup.select(".recipe-step-list__container p")
    ]

    # ---- TEMPS TOTAL ----
    temps_total_tag = soup.select_one(".time__total div")
    temps_total = temps_total_tag.get_text(strip=True) if temps_total_tag else None
    
    # ---- DÉTAILS TEMPS (préparation, repos, cuisson) ----
    temps_prep = temps_repos = temps_cuisson = None
    
    details_block = soup.select_one(".time__details")
    if details_block:
        for span in details_block.find_all("span"):
            label = span.get_text(strip=True).rstrip(" :").lower()
            value_div = span.find_next("div")  # le <div> qui suit le <span>
            if not value_div:
                continue
            valeur = value_div.get_text(strip=True)
    
            if "préparation" in label:
                temps_prep = valeur
            elif "repos" in label:
                temps_repos = valeur
            elif "cuisson" in label:
                temps_cuisson = valeur

    # ---- DIFFICULTÉ ----
    diff_tag = soup.select_one(".icon-difficulty + span")
    difficulte = diff_tag.get_text(strip=True) if diff_tag else None

    # ---- COÛT (niveau financier) ----
    cout_tag = soup.select_one(".icon-price + span")
    cout = cout_tag.get_text(strip=True) if cout_tag else None

       # ---- IMAGE (corrigée) ----
    image_url = None

    # On cible l'image dans le bon conteneur
    media_img = soup.select_one(".recipe-media-viewer-media-container-picture-only img")

    if media_img:
        # 1) priorité : data-src (là où se trouve la vraie image dans le HTML brut)
        if media_img.has_attr("data-src"):
            image_url = media_img["data-src"]
        # 2) sinon : data-srcset (on prend le premier lien)
        elif media_img.has_attr("data-srcset"):
            image_url = media_img["data-srcset"].split()[0]
        # 3) sinon : srcset
        elif media_img.has_attr("srcset"):
            image_url = media_img["srcset"].split()[0]
        # 4) dernier recours : src (souvent = lazyload.png)
        elif media_img.has_attr("src"):
            image_url = media_img["src"]

    # normaliser si l'URL commence par //
    if image_url and image_url.startswith("//"):
        image_url = "https:" + image_url


    # RECETTE BRUTE ---
    recette_brute = {
        "url": url,
        "titre": titre,
        "ingredients_raw": " | ".join(ingredients),
        "etapes": " || ".join(etapes),
        "temps_total": temps_total,
        "temps_preparation": temps_prep,
        "temps_repos": temps_repos,
        "temps_cuisson": temps_cuisson,
        "difficulte": difficulte,
        "cout": cout,
        "image": image_url,
        "personnes": nb_personnes
    }

    # retour propre
    return nettoyer_recette(recette_brute)
    














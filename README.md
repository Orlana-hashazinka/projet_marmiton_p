# 🍳 ViteUneRecette

> **L'intelligence au service de votre cuisine.**  
> Un moteur de recommandation culinaire fondé sur le NLP, entraîné sur des milliers de recettes Marmiton.

---

## 🚀 Demo live

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://projetmarmitonp-xjv5meyvs4uuk56bwwx5aj.streamlit.app/)

🚀 **Demo live** : [projetmarmitonp.streamlit.app](https://projetmarmitonp-xjv5meyvs4uuk56bwwx5aj.streamlit.app/)

---

## 📖 Présentation

**ViteUneRecette** est une application de recommandation culinaire basée sur le **traitement automatique du langage naturel (NLP)**. À partir d'une simple liste d'ingrédients, elle identifie les recettes les plus pertinentes grâce à la similarité TF-IDF et au clustering K-Means.

L'application propose deux modes d'interaction :
- **Mode Express** — Top 5 instantané à partir d'une liste d'ingrédients
- **Assistant Gourmi** — Chatbot interactif pour explorer librement les recettes

---

## ✨ Fonctionnalités

- 🔍 **Recommandation TF-IDF** — Similarité cosinus entre vos ingrédients et le corpus
- 🤖 **Chatbot Gourmi** — Discussion libre avec relance automatique
- 🗂️ **8 univers culinaires** — Identifiés par clustering K-Means non supervisé
- 📊 **Exploration des données** — Visualisations NLP (nuage de mots, histogrammes, projections SVD)

---

## 🧠 Pipeline NLP

```
Données brutes (Marmiton — web scraping)
    ↓
Nettoyage Regex
    → Suppression quantités, unités, adjectifs non informatifs
    ↓
Prétraitement spaCy (fr_core_news_md)
    → Tokenisation → POS-tagging → Lemmatisation
    ↓
Extraction des ingrédients (noms + ingrédients forcés)
    ↓
Vectorisation TF-IDF (ingrédients + titres)
    ↓
Clustering K-Means (8 univers culinaires)
    → Évaluation : méthode du coude + coefficient de silhouette
    ↓
Moteur de recommandation
    → Similarité cosinus + pondération cluster
    → Évaluation : Recall@K et MRR
    ↓
Sauvegarde Pickle + Application Streamlit
```

---

## 🗂️ Univers culinaires identifiés

| Cluster | Thématique |
|---|---|
| 0 | 🧁 Desserts fruités et lactés |
| 1 | 🥗 Plats salés du quotidien |
| 2 | 🍗 Cuisine asiatique |
| 3 | 🐟 Plats italiens |
| 4 | 🍝 Plats à base de pommes de terre |
| 5 | 🥘 Cuisine méditerranéenne |
| 6 | 🍫 Desserts chocolatés |
| 7 | 🥧 Pâtisserie et gâteaux de base |

---

## 📁 Structure du projet

```
ViteUneRecette/
├── data/
│   └── recettes_propres.csv       # Corpus nettoyé
├── models/
│   ├── df_nlp.pkl                 # DataFrame NLP final
│   ├── df_chatbot.pkl             # DataFrame chatbot
│   ├── tfidf_both.pkl             # Matrice TF-IDF
│   ├── vec_both.pkl               # Vectoriseur TF-IDF
│   └── vocab_ingredients.pkl      # Vocabulaire des ingrédients
├── logo/
│   ├── ViteUneRecette.png
│   ├── Gourmi.png
│   ├── Histogram_bigram.png
│   ├── Nuage_mots.png
│   ├── visualisation_2d_clusters.png
│   └── distribution_clusters.png
├── main.ipynb                     # Notebook principal
├── app.py                         # Application Streamlit
├── nlp_fonctions.py               # Fonctions NLP
├── requirements.txt
└── README.md
```

---

## 🚀 Lancer l'application en local

### 1. Cloner le dépôt
```bash
git clone https://github.com/Orlana-hashazinka/ViteUneRecette.git
cd ViteUneRecette
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Télécharger le modèle spaCy français
```bash
python -m spacy download fr_core_news_md
```

### 4. Générer les modèles
Exécuter le notebook complet :
```bash
jupyter notebook main.ipynb
```

### 5. Lancer l'app
```bash
streamlit run app.py
```

---

## 🛠️ Stack technique

| Outil | Usage |
|---|---|
| Python 3.10 | Langage principal |
| spaCy (`fr_core_news_md`) | Tokenisation, POS-tagging, lemmatisation |
| Scikit-Learn | TF-IDF, K-Means, SVD/LSA |
| Pandas | Manipulation des données |
| Matplotlib / Seaborn | Visualisations |
| Streamlit | Interface web interactive |
| Pickle | Sérialisation des modèles |
| Regex | Nettoyage des données brutes |

---

## 📊 Données

- **Source** : Marmiton — web scraping
- **Nettoyage** : Regex + spaCy (`fr_core_news_md`)
- **Représentation** : TF-IDF sur ingrédients + titres normalisés

---

## 👥 Équipe

**Master 2 Mathématiques Appliquées, Statistiques (MAS)**  
Parcours Science des Données & IA — Université Rennes 2

- **Mitossede Séphora**
- **Orlana Hashazinka**

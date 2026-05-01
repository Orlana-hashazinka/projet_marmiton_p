import streamlit as st
import streamlit as st
from nlp_fonctions import load_models, culinary_chatbot_step1, culinary_chatbot_step2

#Avant d'executer ce fichier, svp Exécutez d'abord le notebook main.ipynb pour générer les modèles (fichiers Pickle) dans le dossier models/."
# Charger tous les objets
df, df_chatbot, VOCAB_INGREDIENTS, tfidf_both, vec_both = load_models()


# =========================
# CONFIG (TOUJOURS EN PREMIER)
# =========================
st.set_page_config(
    page_title="ViteUneRecette",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS GLOBAL (PROPRE & UX SAFE)
# =========================

st.markdown(
"""
<style>

/* ======================================================
   TYPOGRAPHIE — LIBRE BASKERVILLE
   ====================================================== */
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&display=swap');

body {
    font-family: 'Libre Baskerville', serif;
    font-weight: 400;
}

/* ======================================================
   FOND GLOBAL
   ====================================================== */
.stApp {
        background: none;
    }
    
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-image: url("https://images.unsplash.com/photo-1498837167922-ddd27525d352");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        filter: blur(8px);
        brightness: 0.8;
        z-index: -1;
    }

/* ======================================================
   CONTENU PRINCIPAL
   ====================================================== */
.block-container {
    background-color: rgba(0, 0, 0, 0.65);
    backdrop-filter: blur(5px);
    padding: 3rem 2.5rem !important;
    max-width: 1100px;
    margin: 3rem auto;
    border-radius: 14px;
}

/* ======================================================
   TITRES
   ====================================================== */
.block-container h1 {
    color: #FFFFFF;
    font-size: 3.2rem;
    font-weight: 700;
    letter-spacing: 0.015em;
    line-height: 1.15;
}

.block-container h2 {
    color: #FFFFFF;
    font-size: 2rem;
    font-weight: 400;
    letter-spacing: 0.015em;
}

.block-container h3 {
    color: #FFFFFF;
    font-size: 1.5rem;
    font-weight: 400;
}

/* ======================================================
   TEXTE COURANT
   ====================================================== */
.block-container p,
.block-container li,
.block-container label,
.block-container span {
    color: #F3F4F6;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* ======================================================
   TABS
   ====================================================== */
div[data-baseweb="tab-list"] {
    justify-content: center !important;
    gap: 0.4rem;
}

button[data-baseweb="tab"] {
    all: unset;
    background: rgba(0,0,0,0.7);
    color: #FFFFFF;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    cursor: pointer;
    border: 1px solid rgba(255,255,255,0.25);
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #24415E;
    color: #e5f0ff;
    border-color: rgba(31,41,51,0.3);
}


/* ======================================================
   EN-TÊTE — ALIGNEMENT LOGO & BIENVENUE
   ====================================================== */
.header-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 25px; /* Espace équilibré entre le logo et le texte */
    margin-bottom: 1.5rem;
}

.logo-header {
    width: 120px; /* Taille optimale pour votre logo ViteUneRecette */
    height: auto;
    filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3)); /* Petit relief sur le logo */
}

/* ======================================================
   BULLLES DE CHAT
   ====================================================== */

button[kind="primary"] {
    background-color: #24415E !important;
    color: white !important;
    border-radius: 999px !important;
    padding: 0.55rem 1.4rem !important;
    font-weight: 600 !important;
    border: none !important;
}

button[kind="primary"]:hover {
    background-color: #1a3046 !important; /* Un peu plus sombre au survol */
}

.chat-bubble {
    padding: 12px 16px;
    border-radius: 18px;
    margin-bottom: 10px;
    max-width: 70%;
    font-size: 0.9rem;
    line-height: 1.5;
}

.bot-bubble {
    background: rgba(255, 255, 255, 0.95);
    color: #1A1A1A !important;
    border: 1px solid #d1d5db;
    margin-right: auto;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

.user-bubble {
    background: #24415E; /* Votre bleu foncé des tabs */
    color: #ffffff !important;
    margin-left: auto;
}

/* ======================================================
   UNIVERS CULINAIRES (GRILLE D'IMAGES) - AJOUTÉ ICI
   ====================================================== */
.cluster-card {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 25px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: background 0.3s ease;
}

.cluster-img-container {
    width: 100%;
    height: 180px; /* Hauteur fixe pour l'alignement */
    overflow: hidden;
    border-radius: 10px;
    margin-bottom: 12px;
}

.cluster-img-container img {
    width: 100%;
    height: 100%;
    object-fit: cover; /* Recadrage intelligent sans déformer */
    transition: transform 0.4s ease;
}

.cluster-card:hover .cluster-img-container img {
    transform: scale(1.1); /* Effet zoom au survol de la carte */
}

.cluster-title {
    color: white;
    font-weight: bold;
    font-size: 0.95rem;
    margin-top: 5px;
}


/* ======================================================
   SECTION FINALE — CALL TO ACTION
   ====================================================== */
.bottom-bg-wrapper {
    margin-top: 4rem;
    width: 100%;
}

.bottom-bg {
    background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                      url("https://images.unsplash.com/photo-1556910103-1c02745aae4d?q=80&w=2070"); /* Image de cuisine conviviale */
    background-size: cover;
    background-position: center;
    border-radius: 20px;
    padding: 60px 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
}

.bottom-bg-text h2 {
    font-size: 2.2rem !important;
    margin-bottom: 10px !important;
    color: #FFFFFF !important;
    font-family: 'Libre Baskerville', serif;
}

.bottom-bg-text p {
    font-size: 1.2rem !important;
    color: #F3F4F6 !important;
}

/* ======================================================
   description des données
   ====================================================== */

[data-testid="stMetricValue"] {
        color: white !important;
    }
    [data-testid="stMetricLabel"] {
        color: white !important;
    }

</style>
""",
unsafe_allow_html=True
)




# =========================
# TABS 
# =========================
tabs = st.tabs([
    "🏠 Accueil",
    "🍳 Cuisiner",
    "📖 Mode d'emploi",
    "📊 Coulisses des données",
    "ℹ️ À propos"
])

# ======================================================
# TAB 0 — ACCUEIL 
# ======================================================
with tabs[0]:
    # En-tête : Alignement horizontal du Logo et du Titre
    col_logo, col_titre = st.columns([1, 4], vertical_alignment="center")
    
    with col_logo:
        # Votre logo principal
        st.image("logo/ViteUneRecette.png", width=150) 

    with col_titre:
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; justify-content: center;">
                <h1 style="font-size:3.5rem; margin:0; color:white; text-align:left; line-height:1.1;">
                    Bienvenue sur ViteUneRecette
                </h1>
                <h3 style="font-size:1.4rem; font-weight:300; color:white; opacity:0.85; margin-top:0.5rem; text-align:left;">
                    L'intelligence au service de votre cuisine.
                </h3>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # Espacement avant la suite
    st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)

    # Section Concept (fusionnée)
    st.markdown("---")
    st.markdown("### 🍳 Comment ça marche ?")
    st.markdown(
        """
        - **Proposez** vos ingrédients principaux (ex: poulet, riz, crème).
        - **ViteUneRecette** analyse des milliers de recettes pour vous.
        - **Cuisinez** des plats parfaitement adaptés à vos ingrédients principaux !
        """
    )

    st.markdown("---")

    # --- SECTION : UNIVERS CULINAIRES  ---
    st.header("✨ Explorez nos univers")
    st.markdown("Nos algorithmes NLP ont regroupé les recettes par thématiques pour vous inspirer :")

    
    row1 = st.columns(2)
    row2 = st.columns(2)
    row3 = st.columns(2)
    row4 = st.columns(2)

    clusters = [
        ("🧁 Desserts fruités et lactés", "https://plus.unsplash.com/premium_photo-1713551474697-15fe83485bc7?q=80&w=1469&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
        ("🥗 Plats salés du quotidien", "https://plus.unsplash.com/premium_photo-1673108852141-e8c3c22a4a22?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
        ("🍗 Cuisine asiatique", "https://images.unsplash.com/photo-1718777791239-c473e9ce7376?q=80&w=765&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
        ("🐟 Plats italiens", "https://images.unsplash.com/photo-1635264685671-739e75e73e0f?q=80&w=1964&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
        ("🍝 Plats à base de pommes de terre", "https://plus.unsplash.com/premium_photo-1669261882830-1e504a9abf1d?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
        ("🥘 Cuisine méditerranéenne", "https://images.unsplash.com/photo-1574788032365-69e929e3ec68?q=80&w=1964&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
        ("🍫 Desserts chocolatés", "https://images.unsplash.com/photo-1577805947697-89e18249d767?q=80&w=698&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
        ("🥧 Pâtisserie et gâteaux de base", "https://plus.unsplash.com/premium_photo-1716584036745-5f5049e3e822?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
    ]

    for col, (title, img) in zip(row1 + row2 + row3 + row4, clusters):
        with col:
            st.markdown(
                f"""
                <div class="cluster-card">
                    <div class="cluster-img-container">
                        <img src="{img}">
                    </div>
                    <div class="cluster-title">{title}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # --- SECTION : L'ASSISTANTE GOURMI ---
    # On passe d'un ratio [1, 3] à un ratio [0.5, 3] pour réduire la largeur de la colonne logo
    col_assistante, col_text = st.columns([0.5, 3], vertical_alignment="center")

    with col_assistante:
        # On affiche le logo sans marge inutile
        st.image("logo/Gourmi.png", width=100) 

    with col_text:
        st.markdown(
            """
            <div style="padding-left: 0px; margin-left: -10px;">
                <h3 style="margin-top:0; margin-bottom:5px;">🤖 Gourmi, votre IA Culinaire</h3>
                <p style="font-size: 1.1rem; line-height: 1.3; margin:0;">
                    Finies les recherches interminables ! Gourmi utilise le <b>NLP</b> pour 
                    extraire le meilleur de vos ingrédients et vous proposer un <b>Top 5 ultra-pertinent</b>.
                    <br>
                    <b>Efficace. Rapide. Sans gaspillage.</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.info("💡 Astuce : Plus vous donnez de détails sur vos ingrédients, plus Gourmi sera précise !")






# =========================
# TAB 2 — RECOMMANDATIONS
# =========================
with tabs[1]:

    # =========================
    # TITRE DE LA PAGE
    # =========================
    st.title("🍳 Cuisiner avec ViteUneRecette")
    
    st.markdown(
        """
        ### L'intelligence culinaire à votre service.
        Que vous ayez une liste précise ou juste une vague idée, notre moteur 
        **ViteUneRecette** utilise le **NLP** pour analyser vos ingrédients et extraire, 
        en quelques secondes, le **Top 5 des créations** les plus adaptées à vos stocks.
        """
    )

    st.markdown("---")

    # =========================
    # CHOIX DU MODE
    # =========================
    mode = st.radio(
        "Choisissez votre expérience :",
        [
            "📝 Mode Express (Moteur de recommandation)",
            "🤖 Discussion libre (Chatbot Gourmi)"
        ],
        horizontal=True
    )

    st.markdown("---")

    # =========================
    # MODE 1 — LISTE D'INGRÉDIENTS
    # =========================

    if mode == "📝 Mode Express (Moteur de recommandation)":
        st.subheader("📝 Vos ingrédients")

        ingredients_input = st.text_area(
            "Entrez vos ingrédients (séparés par des virgules)",
            placeholder="ex : poulet, champignons, crème, ail",
            height=100
        )

        if st.button("🔍 Recommander des recettes", type="primary"):
            if ingredients_input.strip():
                recs, message = culinary_chatbot_step1(
                    user_text=ingredients_input,
                    df_nlp=df,
                    df_chatbot=df_chatbot,
                    tfidf_matrix=tfidf_both,
                    vectorizer=vec_both,
                    vocab_ingredients=VOCAB_INGREDIENTS,
                    top_k=5
                )

                st.markdown("### 📋 Recettes recommandées")
                # On remplace les \n par des <br> pour que le texte s'affiche bien sur plusieurs lignes
                st.info(message.replace("\n", "  \n")) 

                # CORRECTION ICI : on utilise .empty pour vérifier si on a des résultats
                if recs is not None and not recs.empty:
                    st.markdown("---")
                    st.subheader("👨‍🍳 Détail de la meilleure suggestion")
                    # On affiche le détail de la 1ère recette trouvée
                    st.markdown(culinary_chatbot_step2(recs, "1"))


    

    #=========================
    # MODE 2 — CHATBOT GOURMI
    # =========================
    else:
        st.subheader("🤖 Discussion libre (Chatbot Gourmi)")

        # Initialisation des variables d'état
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "last_recs" not in st.session_state:
            st.session_state.last_recs = None

        user_message = st.text_input(
            "Votre message ou numéro de recette",
            placeholder="ex: Riz, poulet... ou tapez '1' pour les détails"
        )

        # On place les boutons sur la même ligne pour garder le design propre
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            send_btn = st.button("💬 Envoyer", type="primary")
        with col_btn2:
            clear_btn = st.button("🗑️ Effacer la discussion", type="primary")

        # Logique pour effacer
        if clear_btn:
            st.session_state.chat_history = []
            st.session_state.last_recs = None
            st.rerun()

        if send_btn and user_message.strip():
            msg_lower = user_message.lower().strip()

            # CAS A : L'utilisateur choisit un numéro (1, 2 ou 3)
            if msg_lower.isdigit() and st.session_state.last_recs is not None:
                detail_response = culinary_chatbot_step2(st.session_state.last_recs, user_message.strip())
                
                # Ajout de la relance automatique
                relance = "\n\n---\n✨ *J'espère que cela vous aide ! Souhaitez-vous un dessert pour accompagner ce plat ou une autre idée ?*"
                
                st.session_state.chat_history.append(("user", user_message))
                st.session_state.chat_history.append(("bot", detail_response + relance))
            
            # CAS B : L'utilisateur demande "autre chose" ou "encore"
            elif any(word in msg_lower for word in ["autre", "encore", "suivant", "plus"]):
                st.session_state.chat_history.append(("user", user_message))
                st.session_state.chat_history.append(("bot", "Pas de soucis ! Dites-moi quels autres ingrédients vous avez ou quel style de cuisine vous tente ? 🍳"))

            # CAS C : Nouvelle recherche classique
            else:
                recs, message = culinary_chatbot_step1(
                    user_text=user_message,
                    df_nlp=df,
                    df_chatbot=df_chatbot,
                    tfidf_matrix=tfidf_both,
                    vectorizer=vec_both,
                    vocab_ingredients=VOCAB_INGREDIENTS,
                    top_k=5
                )
                st.session_state.last_recs = recs
                st.session_state.chat_history.append(("user", user_message))
                st.session_state.chat_history.append(("bot", message))

        # Affichage de la conversation
        st.markdown("### 💬 Conversation")
        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f'<div class="chat-bubble user-bubble">{msg}</div>', unsafe_allow_html=True)
            else:
                # 1. On sépare l'URL de l'image s'il y en a une
                display_msg = msg
                image_url = None
                
                if "🖼️ Image :" in msg:
                    # On extrait l'URL qui se trouve après "Image :"
                    parts = msg.split("🖼️ Image :")
                    display_msg = parts[0] # Le texte avant l'image
                    rest = parts[1].split("\n")
                    image_url = rest[0].strip() # L'URL elle-même
                    # On rajoute le reste du texte (ex: lien original) s'il existe
                    if len(rest) > 1:
                        display_msg += "\n" + "\n".join(rest[1:])

                # 2. Affichage du texte dans la bulle
                html_msg = display_msg.replace("\n", "<br>")
                st.markdown(f'<div class="chat-bubble bot-bubble">🤖 <strong>Gourmi</strong><br>{html_msg}</div>', unsafe_allow_html=True)
                
                # 3. Affichage de l'image REELLEMENT (hors de la bulle pour le style)
                if image_url and image_url.startswith("http"):
                    st.image(image_url, caption="Votre recette en image 📸", width=350)



    # =========================
    # SECTION VISUELLE DE FIN
    # =========================
    st.markdown(
        """
        <div class="bottom-bg-wrapper">
            <div class="bottom-bg">
                <div class="bottom-bg-text">
                    <h2>À vos fourneaux ! 👨‍🍳</h2>
                    <p>
                        ViteUneRecette a sélectionné le meilleur pour vous. 
                        Il ne vous reste plus qu'à cuisiner et vous régaler.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ======================================================
# TAB 2 — MODE D'EMPLOI 
# ======================================================
with tabs[2]:
    st.title("📖 Comment utiliser ViteUneRecette ?")
    st.write("Découvrez comment exploiter toute la puissance de notre moteur d'intelligence culinaire.")

    st.markdown("---")

    # SECTION 1 : LES DEUX MÉTHODES DE RECHERCHE
    col_express, col_gourmi = st.columns(2)

    with col_express:
        st.markdown("### 📝 1. Le Mode Express")
        st.markdown("""
        **Pour aller au plus vite :**
        - **Saisissez** simplement vos ingrédients (ex: *poulet, tomates*).
        - Le moteur calcule instantanément le **Top 5**.
        - **Automatique :** Les détails de la 1ère recette s'affichent immédiatement pour vous faire gagner du temps.
        """)

    with col_gourmi:
        st.markdown("### 🤖 2. L'Assistant Gourmi")
        st.markdown("""
        **Pour une recherche interactive sur mesure :**
        - **Discutez librement** (phrases, listes d'ingrédients ou styles).
        - Gourmi vous présente son **Top 5** sous forme de liste.
        - **Interactif :** C'est vous qui décidez ! Tapez le **numéro (1 à 5)** pour voir les détails de la recette qui vous tente.
        """)

    st.markdown("---")

    # SECTION 2 : LA FLEXIBILITÉ DE GOURMI (Tableau de compréhension)
    st.markdown("### 🧠 Ce que Gourmi comprend")
    st.write("Dans le mode interactif, Gourmi utilise le NLP pour interpréter vos envies :")
    
    st.table({
        "Type de demande": ["Ingrédients seuls", "Phrase complète", "Style Culinaire"],
        "Exemple": ["Poulet, Riz, Curry", "J'ai du riz, sel et poivre dans mon placard", "Cuisine italienne"]
    })

    # SECTION 3 : LES STYLES CULINAIRES (VOS CLUSTERS)
    st.markdown("### 🌍 Explorez nos Univers Culinaires")
    st.write("Vous pouvez demander directement un style à Gourmi. Elle maîtrise parfaitement ces 8 catégories :")

    # Affichage stylisé des clusters
    st.info("""
    ✨ **Essayez de taper l'un de ces styles :**
    * 🍜 **Cuisine asiatique** | 🍝 **Plats italiens** | 🏖️ **Cuisine méditerranéenne**
    * 🏠 **Plats salés du quotidien** | 🥔 **Plats à base de pommes de terre**
    * 🍫 **Desserts chocolatés** | 🍓 **Desserts fruités et lactés**
    * 🍰 **Pâtisserie et gâteaux de base**
    """)

    st.success("""
        **Le petit plus :** Même après avoir choisi une recette, vous pouvez changer d'avis ! 
        Demandez le numéro d'une autre recette du Top 5, proposez un nouvel ingrédient 
        ou changez totalement d'univers. Gourmi s'adapte à chaque étape.
    """)

# =========================
# TAB 4 — MÉTHODOLOGIE
# =========================

with tabs[3]:
    st.title("📊 Coulisses de données")
    st.write("De la donnée brute à l'intelligence culinaire : exploration du corpus Marmiton.")

    # --- SECTION 1 : VUE D'ENSEMBLE (KPIs) ---
    st.markdown("### 1. Vue d'ensemble du Corpus")
    
    # Calcul des indicateurs (KPIs) sur la colonne finale nettoyée
    total_recettes = len(df)
    
    # Extraction des ingrédients à partir de la colonne ingredients_clean_final
    # On gère le cas où c'est une liste ou une chaîne séparée par des virgules
    all_ingredients_list = ",".join(df['ingredients_clean_final'].astype(str)).split(",")
    unique_ingredients = len(set([i.strip() for i in all_ingredients_list if i.strip()]))

    col1, col2 = st.columns(2)
    col1.metric("Recettes scrapées", f"{total_recettes}")
    col2.metric("Ingrédients uniques", f"{unique_ingredients}")
    

    st.write("**Aperçu des données finales (échantillon) :**")
    st.dataframe(df.head(6))

    st.markdown("---")

    # --- SECTION 2 : VECTORISATION & ANALYSE ---
    st.markdown("### 2. Du Texte aux Chiffres (NLP)")
    st.write("Analyse fréquentielle des unités linguistiques")
    
    # Création des colonnes pour l'affichage côte à côte
    st.write("**Top 20 des ingrédients**")
       
    st.image("logo/Histogram_bigram.png", 
                 caption="Distribution des ingrédients fréquents", 
                 width=800)
    
    
    st.write("**Nuage de mots sémantique**")
       
    st.image("logo/Nuage_mots.png", 
                 caption="Visualisation des poids lexicaux", 
                 width=800)

    st.markdown("---")

    # --- SECTION 3 : STRUCTURE CACHÉE (CLUSTERING) ---
    st.markdown("### 3. La Structure des Clusters")
    
    # Affichage de la projection SVD (Le graphique en éventail)
    st.write("**Projection spatiale des recettes (SVD / LSA)**")
    st.image("logo/visualisation_2d_clusters.png", width=800)
    

    # Affichage de la distribution des clusters
    st.write("**Répartition des univers culinaires**")
    st.image("logo/distribution_clusters.png", width=800)



# =========================
# TAB 5 — À PROPOS
# =========================

with tabs[4]:
    st.title("ℹ️ À Propos de ce Projet")

    # --- SECTION 1 : PRÉSENTATION ---
    st.markdown(
        """
        ### 📖 Présentation du Projet
        **ViteUneRecette** est une application de recommandation culinaire fondée sur le  
        **traitement automatique du langage naturel (NLP)**. Elle utilise des modèles de  
        fouille de texte pour identifier les correspondances sémantiques entre vos stocks 
        d'ingrédients et des milliers de recettes de notre base de données.

        L'objectif est de transformer une simple liste d'ingrédients en une expérience culinaire 
        créative et sans gaspillage, grâce à une approche mathématique de la similarité textuelle.

        ---
        """
    )

    # --- SECTION 2 : ÉQUIPE ---
    st.markdown("### 👥 Équipe du Projet")
    st.write("**Master 2 Mathématiques Appliquées, Statistiques (MAS)**")
    st.caption("Parcours Science des Données & IA — Université Rennes 2 ")
    
    col_team1, col_team2 = st.columns(2)
    with col_team1:
        st.markdown("- **Mitossede Séphora**")
    with col_team2:
        st.markdown("- **Orlana Hashazinka**")

    st.markdown("---")

    # --- SECTION 3 : TECHNOLOGIES ---
    st.markdown("### 🛠️ Technologies Utilisées")
    st.markdown(
        """
        - **Python 3.10** - Langage de programmation principal
        - **Streamlit** - Framework pour la création de l'interface interactive
        - **Pandas** - Manipulation et analyse statistique des données
        - **Scikit-Learn** - Algorithmes de Vectorisation (TF-IDF) et Clustering (K-Means)
        - **spaCy** - Prétraitement linguistique et lemmatisation spécialisée 
        - **Matplotlibet seaborn** - Visualisation des données et des clusters culinaires
        - **Regex** - Expressions régulières pour le nettoyage fin des données brutes 
        """
    )

    st.markdown("---")

    # --- SECTION 4 : FONCTIONNALITÉS ---
    st.markdown("### 🍽️ Fonctionnalités Principales")
    st.markdown(
        """
        - **Mode Express** - Obtenez instantanément le Top 5 des recettes adaptées à vos ingrédients.
        - **Assistant Gourmi** - Discutez avec notre IA pour explorer des styles culinaires spécifiques.
        - **Exploration des Clusters** - Visualisez les thématiques identifiées par la méthode de clustering.
        - **Analyse par Mots-Clés** - Découvrez les ingrédients les plus représentatifs de chaque univers.
        """
    )

    st.markdown("---")

    # --- SECTION 5 : SOURCES DES DONNÉES ---
    st.markdown("### 📊 Sources des Données")
    st.markdown(
        """
        Les données utilisées dans ce projet proviennent de :

        - **Marmiton** - Extraction de milliers de recettes de cuisine grâce au **web scraping**.
        - **Nettoyage & Formatage** - Utilisation rigoureuse des **expressions régulières (Regex)** pour garantir la qualité du corpus.
        - **Prétraitement** - Normalisation des textes pour optimiser la pertinence du moteur de recommandation.
        """
    )


    
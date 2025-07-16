# 🚀 Analyse stratégique des tweets d'Elon Musk

## 💬 Description

Ce projet permet d'**automatiser la collecte, l'analyse et la structuration des tweets** d'un compte Twitter (ici Elon Musk), afin d'identifier et classifier les informations stratégiques ou financières susceptibles d'impacter ses entreprises.

Il combine :
- ✅ **Téléchargement des tweets originaux** via une API
- ✅ **Annotation sémantique** par un modèle OpenAI (GPT)
- ✅ **Structuration JSON et enrichissement**
- ✅ **Visualisation interactive** avec Streamlit

---

## 🗂️ Arborescence du projet
```
.
├── app.py
├── get_tweets.py
├── Extraction_information.py
├── Structuration.py
├── .env
├── requirements.txt
└── README.md
```
---

## 🚀 Comment lancer le projet

### 1️⃣ Installer les dépendances

pip install -r requirements.txt


### 2️⃣ Créer un fichier `.env` à la racine

OPENAI_API_KEY=ta_clé_openai_ici
TWITTER_API_KEY=ta_clé_twitter_ici


### 3️⃣ Lancer l'application Streamlit

streamlit run app.py


### 4️⃣ Cliquer sur **« Rafraîchir et analyser les tweets »** dans l'interface

Le tableau final des tweets analysés s'affiche directement, et tu peux également télécharger le CSV final.


---

## ⚙️ Fonctionnement global (pipeline)

### 1️⃣ Récupération des tweets

- Via `get_tweets.py` → fonction `get_all_tweets()`
- Filtrage pour ne garder que les **tweets originaux** (sans réponses ni retweets)
- Par défaut, **5 ou 10 tweets** seulement pour **limiter les appels API**, réduire les coûts, et éviter les restrictions

📄 **Résultat sauvegardé :** `data/elonmusk_tweets.csv`

---

### 2️⃣ Annotation des tweets

- Via `extraction_information.py`
- Chaque tweet est analysé par OpenAI pour estimer son **impact potentiel** sur :
  - Tesla
  - SpaceX
  - xAI
  - Neuralink
  - Twitter/X

📄 **Résultat sauvegardé :** `data/elonmusk_tweets_annotated.csv`

---

### 3️⃣ Structuration et enrichissement

- Via `Structuration.py`
- Nettoyage du JSON, extraction des jugements, entreprises impactées et explications
- Construction d'un CSV final lisible

📄 **Résultat sauvegardé :** `data/elonmusk_tweets_final.csv`

---

## 🔐 Gestion des clés API (sécurité)

Pour protéger les clés d'API, elles sont **stockées dans un fichier `.env`** non versionné.

### Exemple de fichier `.env`

OPENAI_API_KEY = ta_clé_openai_ici

TWITTER_API_KEY = ta_clé_twitterapi.io

---

## 💾 Pourquoi sauvegarder chaque étape en CSV ?

L'approche par étapes sauvegardées permet de limiter drastiquement les appels à l'IA, qui sont coûteux en tokens et peuvent générer rapidement des frais élevés, car chaque étape produit un fichier CSV que l'on peut reprendre.

Ainsi, si l'on souhaite rejouer la pipeline (ou seulement une partie), il n’est pas nécessaire de refaire inutilement les appels aux API.

Cette logique a aussi été pensée en prévision d'une automatisation future.

---

## 🖥️ Interface Streamlit

- Définie dans **`app.py`**
- Pipeline exécutée **uniquement sur clic utilisateur**, afin d’éviter de déclencher inutilement des appels API coûteux
- Tableau final affiché directement dans l'interface (données finales issues du CSV final) : Mauvaise lisibilité actuel mais amériorable pas la suite si-besoin.

---

## 💡 Choix techniques & modèle

🧠 **Modèle OpenAI utilisé** : `o1-mini` - Le moins couteux en Token

💬 **Prompt strict et "JSON only"**, afin de garantir une réponse parsable facilement, sans texte parasite.  

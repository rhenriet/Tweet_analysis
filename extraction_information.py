import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def extract(username = "elonmusk"):
    data_dir = "./data"
    filename = f"{username}_tweets.csv"
    filepath = os.path.join(data_dir, filename)
    df = pd.read_csv('data/elonmusk_tweets.csv')
    client = OpenAI(api_key=OPENAI_API_KEY)

    def analyze_tweet(tweet_text):
        prompt = (
        f"Voici un tweet publié par Elon Musk : \"{tweet_text}\".\n\n"
        "Analyse ce tweet et détermine s'il contient des informations susceptibles d'impacter financièrement ou stratégiquement les entreprises suivantes :\n"
        "- Tesla ($TSLA)\n"
        "- SpaceX\n"
        "- xAI (par exemple, Grok, son chatbot IA, ou tout autre projet lié)\n"
        "- Neuralink\n"
        "- Twitter/X\n\n"
        "Tu dois OBLIGATOIREMENT répondre en format JSON strict avec la structure suivante :\n\n"
        "{\n"
        "  \"jugement\": \"impact probable\" | \"neutre\" | \"non lié\",\n"
        "  \"entreprises_impactees\": [\"Tesla\", \"SpaceX\", \"xAI\", \"Neuralink\", \"Twitter/X\"],\n"
        "  \"explication\": \"Explication courte (1-2 phrases max) du pourquoi de l'impact ou de l'absence d'impact\"\n"
        "}\n\n"
        "Critères pour le jugement :\n"
        "- \"impact probable\" : Information financière, stratégique, ou annonce importante\n"
        "- \"neutre\" : Information mineure ou générale sans impact significatif\n"
        "- \"non lié\" : Tweet personnel, humoristique, ou sans lien avec les entreprises\n\n"
        "⚠️ IMPORTANT :\n"
        "- Réponds UNIQUEMENT en JSON valide\n"
        "- Si aucune entreprise n'est impactée, laisse \"entreprises_impactees\" vide : []\n"
        "- Sois concis dans l'explication (maximum 2 phrases)\n"
        "- Ne génère aucun texte en dehors du JSON\n\n")
        try:
            response = client.chat.completions.create(
                model="o1-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Erreur lors de l'analyse du tweet : {e}")
            return "Erreur d'analyse"

    df['signal_analysis'] = df['text'].apply(analyze_tweet)
    data_dir = "./data"
    filename = f"{username}_tweets_annotated.csv"
    output_file = os.path.join(data_dir, filename)
    df.to_csv(output_file, index=False)

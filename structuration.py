import pandas as pd
import json
import re
import os

def structuration(username = "elonmusk"):
    data_dir = "./data"
    filename = f"{username}_tweets_annotated.csv"
    input_file = os.path.join(data_dir, filename)
    df = pd.read_csv(input_file)

    jugements = []
    entreprises = []
    explications = []

    def extract_clean_json(text):
        try:
            text_clean = re.sub(r"```json|```", "", text).strip()
            text_clean = text_clean.replace('""', '"')
            return json.loads(text_clean)
        except Exception as e:
            return None
        

    for row_text in df["signal_analysis"]:
        analysis = extract_clean_json(row_text)
        if analysis:
            jugements.append(analysis.get("jugement", "non précisé"))
            entreprises.append(", ".join(analysis.get("entreprises_impactees", [])))
            explications.append(analysis.get("explication", ""))
        else:
            jugements.append("Erreur")
            entreprises.append("")
            explications.append("Erreur de parsing ou analyse indisponible.")

    df["jugement"] = jugements
    df["entreprises_impactees"] = entreprises
    df["explication"] = explications

    final_df = df[["text", "date", "jugement", "entreprises_impactees", "explication"]]
    data_dir = "./data"
    filename = f"{username}_tweets_final.csv"
    output_file = os.path.join(data_dir, filename)
    final_df.to_csv(output_file, index=False, encoding="utf-8")
    print("Fichier final")

import streamlit as st
import pandas as pd
import os

from get_tweets import main
from extraction_information import extract
from structuration import structuration

def pipeline():
    main()
    extract()
    structuration()


st.title(" Analyse stratégique des tweets d'Elon Musk")

if st.button("Rafraîchir et analyser les tweets"):
    with st.spinner("Récupération et analyse en cours..."):
        result_msg = pipeline()
    st.success(result_msg)

if os.path.exists('data/elonmusk_tweets_final.csv'):
    st.subheader("Tweets analysés")
    df_display = pd.read_csv('data/elonmusk_tweets_final.csv')
    st.dataframe(df_display)
else:
    st.info("Aucun fichier final trouvé. Cliquez sur le bouton pour lancer la génération.")
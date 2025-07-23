import streamlit as st
from fruit_manager import *

st.title("Dashborad de la plantation")
inventaire = ouvrir_inventaire()
prix = ouvrir_prix()
tresorerie = ouvrir_tresorerie()

st.header("💰 Trésorerie")
st.metric(label="Montant disponible", value=f"{tresorerie['montant']}$")


st.header("🏬 Inventaire")
st.table(inventaire)



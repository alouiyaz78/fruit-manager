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

st.sidebar.title("🌿 Gestion de la production")

# --- Menu Vente de fruits ---
st.sidebar.subheader("🍌 Vendre des fruits")
fruit_a_vendre = st.sidebar.selectbox("Choisir un fruit à vendre", list(inventaire.keys()))
quantite_vendre = st.sidebar.number_input("Quantité à vendre", min_value=1, max_value=inventaire.get(fruit_a_vendre, 0), step=1, value=1)
if st.sidebar.button("✅ Vendre"):
    inventaire, tresorerie = vendre_fruits(inventaire, fruit_a_vendre, quantite_vendre, tresorerie, prix)
    ecrire_inventaire(inventaire)
    ecrire_tresorerie(tresorerie)
    st.success(f"{quantite_vendre} unités de {fruit_a_vendre} vendues avec succès !")
    st.rerun()

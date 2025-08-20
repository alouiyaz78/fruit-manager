import streamlit as st
from fruit_manager import *
import altair as alt
import pandas as pd 
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
    
# --- Menu Récolte de fruits ---
st.sidebar.subheader("🌳 Récolter des fruits")
fruit_a_recolter = st.sidebar.selectbox("Choisir un fruit à récolter", list(inventaire.keys()), key="recolte")
quantite_recolte = st.sidebar.number_input("Quantité à récolter", min_value=1, step=1, value=1, key="quantite_recolte")
if st.sidebar.button("✅ Récolter"):
    inventaire = recolter_fruits(inventaire, fruit_a_recolter, quantite_recolte)
    ecrire_inventaire(inventaire)
    st.success(f"{quantite_recolte} unités de {fruit_a_recolter} récoltées avec succès !")
    st.rerun()    
# --- Valeur du stock ---
st.header("📦 Valeur du stock")
valeur_totale = valeur_stock(inventaire, prix)

#  le détail par fruit
st.subheader("Détail par fruit")
st.table(valeur_totale)

# total général
total_general = sum(valeur_totale.values())
st.metric(label="Valeur totale du stock", value=f"{total_general}$")
# --- Graphique Inventaire ---
st.subheader("📊 Visualisation de l'inventaire")

# Transformer en DataFrame
df_inventaire = pd.DataFrame(list(inventaire.items()), columns=["Fruit", "Quantité"])

# Trier du plus grand au plus petit
df_inventaire = df_inventaire.sort_values(by="Quantité", ascending=False)

# Créer un graphique Altair
chart = (
    alt.Chart(df_inventaire)
    .mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10)  # coins arrondis
    .encode(
        x=alt.X("Quantité:Q", title="Quantité en stock"),
        y=alt.Y("Fruit:N", sort="-x", title=""),
        color=alt.Color("Fruit:N", legend=None),  # couleurs auto
        tooltip=["Fruit", "Quantité"],  # info au survol
    )
    .properties(width=600, height=400)
)

st.altair_chart(chart, use_container_width=True)

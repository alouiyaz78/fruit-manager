import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from fruit_manager import *

st.title("Dashboard de la plantation")

# --- Charger données ---
inventaire = ouvrir_inventaire()
prix = ouvrir_prix()
tresorerie = ouvrir_tresorerie()
historique = lire_tresorerie_historique()  # historique depuis fichier

# --- Trésorerie ---
st.header("💰 Trésorerie")
st.metric(label="Montant disponible", value=f"{tresorerie['montant']}$")

# --- Inventaire ---
st.header("🏬 Inventaire")
st.table(inventaire)

# --- Sidebar Gestion de la production ---
st.sidebar.title("🌿 Gestion de la production")

# Vente de fruits
st.sidebar.subheader("🍌 Vendre des fruits")
fruit_a_vendre = st.sidebar.selectbox("Choisir un fruit à vendre", list(inventaire.keys()))
quantite_vendre = st.sidebar.number_input(
    "Quantité à vendre",
    min_value=1,
    max_value=inventaire.get(fruit_a_vendre, 0),
    step=1,
    value=1
)
if st.sidebar.button("✅ Vendre"):
    inventaire, tresorerie = vendre_fruits(inventaire, fruit_a_vendre, quantite_vendre, tresorerie, prix)
    ecrire_inventaire(inventaire)
    ecrire_tresorerie(tresorerie)
    
    # Enregistrer transaction
    enregistrer_tresorerie_historique(tresorerie)
    
    st.success(f"{quantite_vendre} unités de {fruit_a_vendre} vendues avec succès !")
    st.experimental_rerun()

# Récolte de fruits
st.sidebar.subheader("🌳 Récolter des fruits")
fruit_a_recolter = st.sidebar.selectbox("Choisir un fruit à récolter", list(inventaire.keys()), key="recolte")
quantite_recolte = st.sidebar.number_input(
    "Quantité à récolter",
    min_value=1,
    step=1,
    value=1,
    key="quantite_recolte"
)
if st.sidebar.button("✅ Récolter"):
    inventaire = recolter_fruits(inventaire, fruit_a_recolter, quantite_recolte)
    ecrire_inventaire(inventaire)
    
    # Enregistrer récolte comme transaction dans le fichier historique
    enregistrer_tresorerie_historique(tresorerie)
    
    st.success(f"{quantite_recolte} unités de {fruit_a_recolter} récoltées avec succès !")
    st.experimental_rerun()

# --- Valeur du stock ---
st.header("📦 Valeur du stock")
valeur = valeur_stock(inventaire, prix)

st.subheader("Détail par fruit")
df_valeur = pd.DataFrame(list(valeur.items()), columns=["Fruit", "Valeur ($ CAD)"])
df_valeur = df_valeur.sort_values(by="Valeur ($ CAD)", ascending=False)
st.table(df_valeur)

total_general = sum(valeur.values())
st.metric(label="Valeur totale du stock", value=f"{total_general}$")

# Graphique barres valeur du stock
chart_valeur = (
    alt.Chart(df_valeur)
    .mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10)
    .encode(
        x=alt.X("Valeur ($ CAD):Q", title="Valeur en $"),
        y=alt.Y("Fruit:N", sort="-x", title=""),
        color=alt.Color("Fruit:N", legend=None),
        tooltip=["Fruit", "Valeur ($ CAD)"]
    )
    .properties(width=600, height=400)
)
st.altair_chart(chart_valeur, use_container_width=True)

# --- Graphique Inventaire ---
st.subheader("📊 Visualisation de l'inventaire")
df_inventaire = pd.DataFrame(list(inventaire.items()), columns=["Fruit", "Quantité"])
df_inventaire = df_inventaire.sort_values(by="Quantité", ascending=False)

chart_inventaire = (
    alt.Chart(df_inventaire)
    .mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10)
    .encode(
        x=alt.X("Quantité:Q", title="Quantité en stock"),
        y=alt.Y("Fruit:N", sort="-x", title=""),
        color=alt.Color("Fruit:N", legend=None),
        tooltip=["Fruit", "Quantité"]
    )
    .properties(width=600, height=400)
)
st.altair_chart(chart_inventaire, use_container_width=True)

# --- Historique des transactions ---
st.header("📝 Historique des transactions")
historique = lire_tresorerie_historique()

if historique:
    # Transformer en DataFrame
    df_historique = pd.DataFrame(historique)
    
    # Extraire juste le montant de la trésorerie
    df_historique['tresorerie'] = df_historique['tresorerie'].apply(lambda x: x.get('montant', 0))
    
    st.table(df_historique)
else:
    st.info("Aucune transaction pour l'instant.")

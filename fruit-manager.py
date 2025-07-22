# %%
inventaire ={"bananes": 130, "pommes": 60, "oranges": 45, "kiwis": 20,"ananas": 60}

# %%
def afficher_inventaire(inventaire):
    for fruit, quantite in inventaire.items():
        print(f"{fruit.capitalize()}: {quantite} unités")

# %%
afficher_inventaire(inventaire)

# %%
def recolter_fruits(inventaire, fruit, quantite):
   inventaire[fruit] = inventaire.get(fruit, 0) + quantite
   print(f"Récolté {quantite} unités de {fruit}. Inventaire mis à jour.")

# %%
def vendre_fruits(inventaire, fruit, quantite):
    if fruit in inventaire and inventaire[fruit] >= quantite:
        inventaire[fruit] -= quantite
        print(f"Vendu {quantite} unités de {fruit}. Inventaire mis à jour.")
    else:
        print(f"Impossible de vendre {quantite} unités de {fruit}. Stock insuffisant.")

# %%
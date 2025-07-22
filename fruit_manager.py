import json
inventaire ={"bananes": 130, "pommes": 60, "oranges": 45, "kiwis": 20,"ananas": 60}

def ouvrir_inventaire(path="inventaire.json"):
    
        with open(path, 'r',encoding='utf-8') as fichier:
            inventaire = json.load(fichier)
        return inventaire
            
def ecrire_inventaire(path="inventaire.json"):
    with open(path, 'w', encoding='utf-8') as fichier:
        json.dump(inventaire, fichier, ensure_ascii= False,indent=4)  
def afficher_inventaire(inventaire):
    for fruit, quantite in inventaire.items():
        print(f"{fruit.capitalize()}: {quantite} unités")


afficher_inventaire(inventaire)

def recolter_fruits(inventaire, fruit, quantite):
   inventaire[fruit] = inventaire.get(fruit, 0) + quantite
   print(f"Récolté {quantite} unités de {fruit}. Inventaire mis à jour.")


def vendre_fruits(inventaire, fruit, quantite):
    if fruit in inventaire and inventaire[fruit] >= quantite:
        inventaire[fruit] -= quantite
        print(f"Vendu {quantite} unités de {fruit}. Inventaire mis à jour.")
    else:
        print(f"Impossible de vendre {quantite} unités de {fruit}. Stock insuffisant.")


               
# Exemple d'utilisation
recolter_fruits(inventaire, "bananes", 20)
vendre_fruits(inventaire, "pommes", 10)
afficher_inventaire(inventaire)     
ecrire_inventaire()  # Enregistre l'inventaire dans le fichier JSON
# Ouvrir l'inventaire depuis le fichier JSON
inventaire = ouvrir_inventaire()
afficher_inventaire(inventaire)  # Affiche l'inventaire chargé depuis

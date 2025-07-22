import json

# Initialisation correcte de l'inventaire
inventaire = {"bananes": 130, "pommes": 60, "oranges": 45, "kiwis": 20, "ananas": 60}

def ouvrir_inventaire(path="Data/inventaire.json"):
    try:
        with open(path, 'r', encoding='utf-8') as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        return inventaire  # Retourne l'inventaire par défaut si le fichier n'existe pas

def ecrire_inventaire(inventaire, path="Data/inventaire.json"):  # Ajout du paramètre inventaire
    with open(path, 'w', encoding='utf-8') as fichier:
        json.dump(inventaire, fichier, ensure_ascii=False, indent=4)

def ouvrir_tresorerie(path="Data/tresorerie.txt"):
    try:
        with open(path, 'r', encoding='utf-8') as fichier:
            content = fichier.read().strip()  # Lit et supprime les espaces/newlines
            if not content:  # Vérifie si le fichier est vide
                return {"montant": 0}
            return json.loads(content)  # Utilise loads pour parser le contenu
    except (FileNotFoundError, json.JSONDecodeError):
        return {"montant": 0}  # Valeur par défaut si le fichier n'existe pas ou est invalide

def ecrire_tresorerie(tresorerie, path="Data/tresorerie.txt"):
    with open(path, 'w', encoding='utf-8') as fichier:
        json.dump(tresorerie, fichier, ensure_ascii=False, indent=4)

def afficher_tresorerie(tresorerie):
    print(f"Trésorerie actuelle: {tresorerie['montant']} $ CAD")

def afficher_inventaire(inventaire):
    for fruit, quantite in inventaire.items():
        print(f"{fruit.capitalize()}: {quantite} unités")

def recolter_fruits(inventaire, fruit, quantite):
    inventaire[fruit] = inventaire.get(fruit, 0) + quantite
    print(f"Récolté {quantite} unités de {fruit}. Inventaire mis à jour.")
    return inventaire  # Retourne l'inventaire modifié

def vendre_fruits(inventaire, fruit, quantite, tresorerie):
    if fruit in inventaire and inventaire[fruit] >= quantite:
        inventaire[fruit] -= quantite
        tresorerie['montant'] += 1 * quantite  # Mise à jour correcte du dictionnaire
        print(f"Vendu {quantite} unités de {fruit}. Inventaire mis à jour.")
        return inventaire, tresorerie
    else:
        print(f"Impossible de vendre {quantite} unités de {fruit}. Stock insuffisant.")
        return inventaire, tresorerie  # Retourne même en cas d'échec

# Exemple d'utilisation
if __name__ == "__main__":
    # Charge ou initialise la trésorerie
    tresorerie = ouvrir_tresorerie()
    afficher_tresorerie(tresorerie)
    
    # Charge ou utilise l'inventaire par défaut
    inventaire = ouvrir_inventaire()
    afficher_inventaire(inventaire)
    
    # Récolte de fruits
    inventaire = recolter_fruits(inventaire, "bananes", 10)
    inventaire = recolter_fruits(inventaire, "pommes", 5)
    
    # Vente de fruits
    inventaire, tresorerie = vendre_fruits(inventaire, "bananes", 5, tresorerie)
    afficher_inventaire(inventaire)
    
    # Mise à jour des fichiers
    ecrire_inventaire(inventaire)
    ecrire_tresorerie(tresorerie)
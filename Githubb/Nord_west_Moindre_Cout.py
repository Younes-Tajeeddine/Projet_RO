import numpy as np
from tabulate import tabulate
from tkinter import simpledialog, messagebox, Toplevel, Text, Scrollbar

def generate_data(nb_usines, nb_magasins, min_cost=1, max_cost=20, min_cap=10, max_cap=50):
    """Génère des données aléatoires pour les coûts, capacités et demandes."""
    couts = np.random.randint(min_cost, max_cost, size=(nb_usines, nb_magasins))
    capacites = np.random.randint(min_cap, max_cap, size=nb_usines)
    demandes = np.random.randint(min_cap, max_cap, size=nb_magasins)

    total_capacite = sum(capacites)
    total_demande = sum(demandes)
    if total_capacite > total_demande:
        demandes[-1] += total_capacite - total_demande
    else:
        capacites[-1] += total_demande - total_capacite

    return couts, capacites, demandes

def calculer_cout_total(couts, allocation):
    """Calcule le coût total pour une allocation donnée."""
    return np.sum(couts * allocation)

def nord_ouest(capacites, demandes):
    """Applique l'algorithme Nord-Ouest pour une allocation initiale."""
    allocation = np.zeros((len(capacites), len(demandes)), dtype=int)
    i, j = 0, 0
    while i < len(capacites) and j < len(demandes):
        alloc = min(capacites[i], demandes[j])
        allocation[i, j] = alloc
        capacites[i] -= alloc
        demandes[j] -= alloc
        if capacites[i] == 0:
            i += 1
        if demandes[j] == 0:
            j += 1
    return allocation

def moindre_cout(couts, capacites, demandes):
    """Applique l'algorithme des moindres coûts pour une allocation initiale."""
    allocation = np.zeros_like(couts, dtype=int)
    couts_temp = couts.astype(float)
    while np.any(capacites) and np.any(demandes):
        i, j = np.unravel_index(np.argmin(couts_temp, axis=None), couts_temp.shape)
        alloc = min(capacites[i], demandes[j])
        allocation[i, j] = alloc
        capacites[i] -= alloc
        demandes[j] -= alloc
        if capacites[i] == 0:
            couts_temp[i, :] = np.inf
        if demandes[j] == 0:
            couts_temp[:, j] = np.inf
    return allocation

def transport_gui(gui, output_label):
    """Fonction principale pour exécuter les algorithmes de transport via l'interface graphique."""
    nb_usines = simpledialog.askinteger("Entrée", "Entrez le nombre d'usines :", parent=gui, minvalue=1)
    if nb_usines is None:  # Si l'utilisateur annule
        output_label.config(text="Action annulée par l'utilisateur.")
        return

    nb_magasins = simpledialog.askinteger("Entrée", "Entrez le nombre de magasins :", parent=gui, minvalue=1)
    if nb_magasins is None:  # Si l'utilisateur annule
        output_label.config(text="Action annulée par l'utilisateur.")
        return

    couts, capacites, demandes = generate_data(nb_usines, nb_magasins)

    # Afficher les coûts, capacités et demandes
    output = "Coûts unitaires :\n"
    output += tabulate(couts, 
                       headers=[f"Magasin {j+1}" for j in range(nb_magasins)], 
                       showindex=[f"Usine {i+1}" for i in range(nb_usines)], 
                       tablefmt="fancy_grid")
    output += "\n\nCapacités des usines : " + str(capacites)
    output += "\nDemandes des magasins : " + str(demandes)

    # Résolution avec Nord-Ouest
    allocation_nord_ouest = nord_ouest(capacites.copy(), demandes.copy())
    cout_nord_ouest = calculer_cout_total(couts, allocation_nord_ouest)
    output += "\n\nAllocation (Nord-Ouest) :\n"
    output += tabulate(allocation_nord_ouest, 
                       headers=[f"Magasin {j+1}" for j in range(nb_magasins)], 
                       showindex=[f"Usine {i+1}" for i in range(nb_usines)], 
                       tablefmt="fancy_grid")
    output += f"\nCoût total (Nord-Ouest) : {cout_nord_ouest}"

    # Résolution avec Moindres Coûts
    allocation_moindre_cout = moindre_cout(couts, capacites.copy(), demandes.copy())
    cout_moindre_cout = calculer_cout_total(couts, allocation_moindre_cout)
    output += "\n\nAllocation (Moindres Coûts) :\n"
    output += tabulate(allocation_moindre_cout, 
                       headers=[f"Magasin {j+1}" for j in range(nb_magasins)], 
                       showindex=[f"Usine {i+1}" for i in range(nb_usines)], 
                       tablefmt="fancy_grid")
    output += f"\nCoût total (Moindres Coûts) : {cout_moindre_cout}"

    # Création d'une nouvelle fenêtre pour afficher les résultats avec une barre de défilement
    result_window = Toplevel(gui)
    result_window.title("Résultats des Calculs de Transport")
    
    # Ajouter une barre de défilement
    scrollbar = Scrollbar(result_window)
    scrollbar.pack(side="right", fill="y")

    # Créer un widget Text pour afficher les résultats
    text_widget = Text(result_window, wrap="word", yscrollcommand=scrollbar.set, width=100, height=30)
    text_widget.pack(side="left", fill="both", expand=True)

    # Insérer les résultats dans le widget Text
    text_widget.insert("1.0", output)
    text_widget.config(state="disabled")  # Empêche l'édition du texte

    # Lier la barre de défilement au widget Text
    scrollbar.config(command=text_widget.yview)

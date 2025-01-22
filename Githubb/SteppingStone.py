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

def stepping_stone(couts, allocation):
    """Applique l'algorithme Stepping Stone pour optimiser l'allocation."""
    rows, cols = allocation.shape
    couts = couts.astype(float)  # S'assurer que les coûts sont en float
    while True:
        # Étape 1 : Identifier les cases non allouées
        empty_cells = [(i, j) for i in range(rows) for j in range(cols) if allocation[i, j] == 0]

        # Étape 2 : Tester chaque case vide pour des cycles d'amélioration
        best_improvement = 0
        best_allocation = allocation.copy()
        
        for cell in empty_cells:
            # Trouver un cycle fermé pour la case vide
            cycle, gain = find_cycle_and_gain(couts, allocation, cell)
            if cycle and gain < best_improvement:
                best_improvement = gain
                best_allocation = adjust_allocation(allocation, cycle)

        # Étape 3 : Appliquer la meilleure amélioration si possible
        if best_improvement >= 0:
            break  # Pas d'amélioration possible, la solution est optimale
        allocation = best_allocation

    return allocation

def find_cycle_and_gain(couts, allocation, start_cell):
    """Trouve un cycle fermé et calcule le gain pour une case vide."""
    rows, cols = allocation.shape
    visited = set()
    cycle = []

    def dfs(cell, path):
        if cell in visited:
            if cell == start_cell and len(path) >= 4:  # Cycle trouvé
                return path
            return None

        visited.add(cell)
        row, col = cell

        # Explorer les cases dans la même ligne et colonne
        for next_cell in [(row, c) for c in range(cols)] + [(r, col) for r in range(rows)]:
            if next_cell != cell and allocation[next_cell] > 0 or next_cell == start_cell:
                new_path = dfs(next_cell, path + [cell])
                if new_path:
                    return new_path

        visited.remove(cell)
        return None

    # Trouver un cycle en démarrant du point
    cycle = dfs(start_cell, [])

    if not cycle:
        return None, 0

    # Calculer le gain net du cycle
    gain = calculate_cycle_gain(couts, allocation, cycle)
    return cycle, gain

def calculate_cycle_gain(couts, allocation, cycle):
    """Calcule le gain net pour un cycle donné."""
    gain = 0
    for k, (i, j) in enumerate(cycle):
        sign = 1 if k % 2 == 0 else -1  # Alterner entre + et -
        gain += sign * couts[i, j]
    return gain

def adjust_allocation(allocation, cycle):
    """Ajuste l'allocation le long d'un cycle."""
    min_alloc = min(allocation[i, j] for k, (i, j) in enumerate(cycle) if k % 2 == 1)  # Trouver la plus petite allocation

    # Ajuster les allocations le long du cycle
    for k, (i, j) in enumerate(cycle):
        sign = 1 if k % 2 == 0 else -1
        allocation[i, j] += sign * min_alloc

    return allocation

def stepping_stone_gui(gui, output_label):
    """Fonction principale pour exécuter l'algorithme de Stepping Stone via l'interface graphique."""
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

    # Optimisation avec Stepping Stone
    allocation_optimisee = stepping_stone(couts, allocation_moindre_cout)
    cout_optimise = calculer_cout_total(couts, allocation_optimisee)
    output += "\n\nAllocation Optimisée (Stepping Stone) :\n"
    output += tabulate(allocation_optimisee, 
                       headers=[f"Magasin {j+1}" for j in range(nb_magasins)], 
                       showindex=[f"Usine {i+1}" for i in range(nb_usines)], 
                       tablefmt="fancy_grid")
    output += f"\nCoût total optimisé : {cout_optimise}"

    # Créer une nouvelle fenêtre pour afficher les résultats
    result_window = Toplevel(gui)
    result_window.title("Résultats de l'Algorithme de Stepping Stone")
    result_window.geometry("1200x800")

    # Ajouter une barre de défilement
    scrollbar = Scrollbar(result_window)
    scrollbar.pack(side="right", fill="y")

    # Créer un widget Text pour afficher les résultats
    text_widget = Text(result_window, wrap="word", yscrollcommand=scrollbar.set, width=120, height=40)
    text_widget.pack(side="left", fill="both", expand=True)

    # Insérer les résultats dans le widget Text
    text_widget.insert("1.0", output)
    text_widget.config(state="disabled")  # Empêche l'édition du texte

    # Lier la barre de défilement au widget Text
    scrollbar.config(command=text_widget.yview)
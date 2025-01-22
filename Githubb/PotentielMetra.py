import random
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import simpledialog, Toplevel, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Importation correcte pour Tkinter

def generate_task_table(num_tasks):
    """Générer un tableau de tâches avec durées et antériorités."""
    tasks = {}
    for i in range(1, num_tasks + 1):
        duration = random.randint(1, 10)  # Durée aléatoire (1-10 jours)
        predecessors = random.sample(range(1, i), random.randint(0, min(2, i - 1)))
        tasks[f"T{i}"] = {"duration": duration, "predecessors": [f"T{p}" for p in predecessors]}
    return tasks

def calculate_potential_metra(tasks):
    """Calculer les dates au plus tôt, au plus tard, la durée totale et le chemin critique."""
    early_start = {}
    late_start = {}

    # Calcul des dates au plus tôt
    for task in tasks:
        predecessors = tasks[task]["predecessors"]
        early_start[task] = max([early_start[p] + tasks[p]["duration"] for p in predecessors] + [0])

    # Durée totale du projet
    total_duration = max(early_start[task] + tasks[task]["duration"] for task in tasks)

    # Calcul des dates au plus tard
    late_start = {task: total_duration - tasks[task]["duration"] for task in tasks}
    for task in sorted(tasks, key=lambda x: -early_start[x]):
        successors = [t for t in tasks if task in tasks[t]["predecessors"]]
        if successors:
            late_start[task] = min([late_start[s] - tasks[task]["duration"] for s in successors])

    # Chemin critique
    critical_path = [task for task in tasks if early_start[task] == late_start[task]]

    return early_start, late_start, total_duration, critical_path

def plot_potential_metra(tasks, early_start, total_duration, critical_path):
    """Afficher un graphe du potentiel Métra avec NetworkX."""
    G = nx.DiGraph()
    for task, details in tasks.items():
        for predecessor in details["predecessors"]:
            G.add_edge(predecessor, task)

    pos = nx.spring_layout(G)
    node_colors = ["red" if node in critical_path else "skyblue" for node in G.nodes]
    edge_colors = [
        "red" if (u in critical_path and v in critical_path and early_start[v] == early_start[u] + tasks[u]["duration"]) else "black"
        for u, v in G.edges
    ]
    labels = {node: f"{node}\n{early_start[node]}" for node in G.nodes}

    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        with_labels=True,
        labels=labels,
        node_color=node_colors,
        edge_color=edge_colors,
        node_size=3000,
        font_size=10,
        font_weight="bold"
    )
    plt.title(f"Diagramme de potentiel Métra (Durée totale: {total_duration})", fontsize=14)
    
    # Renvoie la figure pour intégration dans Tkinter
    return plt

def potentiel_metra(gui, output_label):
    """Fonction principale pour exécuter l'algorithme du Potentiel Métra via l'interface graphique."""
    num_tasks = simpledialog.askinteger("Entrée", "Entrez le nombre de tâches :", parent=gui, minvalue=1)
    if num_tasks is None:  # Si l'utilisateur annule
        output_label.config(text="Action annulée par l'utilisateur.")
        return

    tasks = generate_task_table(num_tasks)

    # Calcul du potentiel Métra
    early_start, late_start, total_duration, critical_path = calculate_potential_metra(tasks)

    # Créer une nouvelle fenêtre pour afficher les résultats
    result_window = Toplevel(gui)
    result_window.geometry("800x600")
    result_window.title("Résultats du Potentiel Métra")

    # Afficher les résultats textuels dans la nouvelle fenêtre
    result_text = f"Dates au plus tôt : {early_start}\n"
    result_text += f"Dates au plus tard : {late_start}\n"
    result_text += f"Durée totale du projet : {total_duration}\n"
    result_text += f"Chemin critique : {critical_path}\n"

    result_label = Label(result_window, text=result_text, font=("Helvetica", 12), justify="left", padx=20, pady=20)
    result_label.pack()

    # Afficher le graphe du potentiel Métra
    fig = plot_potential_metra(tasks, early_start, total_duration, critical_path)

    # Convertir le graphe en image et l'afficher dans Tkinter
    canvas = FigureCanvasTkAgg(fig.gcf(), master=result_window)  # Utiliser gcf() pour obtenir la figure courante
    canvas.draw()  # Dessiner le graphe
    canvas.get_tk_widget().pack(pady=20)  # Ajouter le canvas à la fenêtre Tkinter

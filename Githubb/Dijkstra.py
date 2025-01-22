import networkx as nx
import matplotlib.pyplot as plt
import random
import time
from tkinter import simpledialog, messagebox, Toplevel, Label, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Importation pour afficher le graphe dans Tkinter

def generate_weighted_graph(gui):
    """Génère un graphe pondéré avec des sommets nommés x0 à xN."""
    num_vertices = simpledialog.askinteger("Entrée", "Entrez le nombre de sommets :", parent=gui, minvalue=1)
    if num_vertices is None:  # Si l'utilisateur annule
        return None

    G = nx.Graph()
    vertices = [f"x{i}" for i in range(num_vertices)]
    G.add_nodes_from(vertices)

    # Ajouter des arêtes avec des pondérations aléatoires entre 1 et 100
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            weight = random.randint(1, 100)
            G.add_edge(vertices[i], vertices[j], weight=weight)

    return G

def dijkstra(gui, output_label):
    """Fonction principale pour exécuter l'algorithme de Dijkstra via l'interface graphique."""
    G = generate_weighted_graph(gui)
    if G is None:
        output_label.config(text="Action annulée par l'utilisateur.")
        return

    # Demande des sommets de départ et d'arrivée
    start_vertex = simpledialog.askstring("Entrée", "Entrez le sommet de départ (ex: x0) :", parent=gui)
    end_vertex = simpledialog.askstring("Entrée", "Entrez le sommet d'arrivée (ex: x1) :", parent=gui)

    if start_vertex is None or end_vertex is None:
        output_label.config(text="Action annulée par l'utilisateur.")
        return

    # Vérifie si les sommets existent dans le graphe
    if start_vertex not in G or end_vertex not in G:
        output_label.config(text="L'un des sommets n'existe pas dans le graphe.")
        return

    try:
        # Calcul du plus court chemin avec Dijkstra
        start_time = time.time()
        length, path = nx.single_source_dijkstra(G, start_vertex, end_vertex, weight='weight')
        end_time = time.time()
        execution_time = end_time - start_time

        # Création d'une nouvelle fenêtre pour afficher les résultats
        result_window = Toplevel(gui)
        result_window.geometry("800x600")
        result_window.title(f"Résultats de Dijkstra ({start_vertex} -> {end_vertex})")
        
        # Affichage des résultats dans la nouvelle fenêtre
        result_label = Label(result_window, text=f"Distance minimale : {length}\n"
                                                f"Chemin le plus court : {' -> '.join(path)}\n"
                                                f"Temps d'exécution : {execution_time:.4f} secondes",
                             font=("Helvetica", 12), justify="left", padx=20, pady=20)
        result_label.pack()

        # Création de la figure pour le graphe
        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(G)
        edge_colors = ['red' if (u, v) in zip(path[:-1], path[1:]) or (v, u) in zip(path[:-1], path[1:]) else 'gray' for u, v in G.edges()]
        nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color=edge_colors, node_size=500, font_size=10, ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
        ax.set_title("Graphe avec chemin le plus court (Dijkstra)")

        # Convertir le graphe en image et l'afficher dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=result_window)  # Créer un canvas matplotlib pour Tkinter
        canvas.draw()  # Dessiner le graphe
        canvas.get_tk_widget().pack(pady=20)  # Ajouter le canvas à la fenêtre

    except nx.NetworkXNoPath:
        # Cas où il n'y a pas de chemin entre les sommets
        result_window = Toplevel(gui)
        result_window.geometry("600x400")
        result_window.title(f"Résultats de Dijkstra ({start_vertex} -> {end_vertex})")

        result_label = Label(result_window, text=f"Aucun chemin trouvé entre {start_vertex} et {end_vertex}.",
                             font=("Helvetica", 12), justify="left", padx=20, pady=20)
        result_label.pack()

        messagebox.showerror("Erreur", f"Aucun chemin entre {start_vertex} et {end_vertex}.")

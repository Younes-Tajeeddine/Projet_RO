import networkx as nx
import matplotlib.pyplot as plt
import random
from tkinter import simpledialog, messagebox, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Pour intégrer matplotlib dans Tkinter

def generate_weighted_digraph(gui):
    """Génère un graphe pondéré dirigé avec des sommets nommés x0 à xN."""
    num_vertices = simpledialog.askinteger("Entrée", "Entrez le nombre de sommets :", parent=gui, minvalue=1)
    if num_vertices is None:  # Si l'utilisateur annule
        return None

    graph = nx.DiGraph()
    vertices = [f"x{i}" for i in range(num_vertices)]
    graph.add_nodes_from(vertices)

    # Ajout des arêtes dirigées avec des poids aléatoires entre 1 et 100
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            weight = random.randint(1, 100)
            graph.add_edge(vertices[i], vertices[j], weight=weight)

    return graph

def bellman_ford(gui, output_label):
    """Fonction principale pour exécuter l'algorithme de Bellman-Ford via l'interface graphique."""
    graph = generate_weighted_digraph(gui)
    if graph is None:
        output_label.config(text="Action annulée par l'utilisateur.")
        return

    # Demande des sommets de départ et d'arrivée
    start_vertex = simpledialog.askstring("Entrée", "Entrez le sommet de départ (ex: x0) :", parent=gui)
    end_vertex = simpledialog.askstring("Entrée", "Entrez le sommet d'arrivée (ex: x1) :", parent=gui)

    if start_vertex is None or end_vertex is None:
        output_label.config(text="Action annulée par l'utilisateur.")
        return

    # Vérifie si les sommets existent dans le graphe
    if start_vertex not in graph or end_vertex not in graph:
        output_label.config(text="L'un des sommets n'existe pas dans le graphe.")
        return

    try:
        # Calcul du plus court chemin avec Bellman-Ford
        length = nx.single_source_bellman_ford_path_length(graph, start_vertex)
        path = nx.single_source_bellman_ford_path(graph, start_vertex)

        if end_vertex in path:
            output = f"Distance minimale de {start_vertex} à {end_vertex} : {length[end_vertex]}\n"
            output += f"Chemin le plus court : {path[end_vertex]}"
            output_label.config(text=output)

            # Créer une nouvelle fenêtre pour afficher le graphe
            graph_window = Toplevel(gui)
            graph_window.title("Graphe avec chemin le plus court (Bellman-Ford)")
            graph_window.geometry("800x800")

            # Dessiner le graphe avec les couleurs des nœuds et des arêtes
            pos = nx.spring_layout(graph)
            fig, ax = plt.subplots(figsize=(8, 8))
            nx.draw(graph, pos, with_labels=True, node_color="lightblue", edge_color="gray", ax=ax)
            nx.draw_networkx_nodes(graph, pos, nodelist=path[end_vertex], node_color="red", ax=ax)
            path_edges = [(path[end_vertex][i], path[end_vertex][i + 1]) for i in range(len(path[end_vertex]) - 1)]
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color="blue", width=2, ax=ax)
            nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): d['weight'] for u, v, d in graph.edges(data=True)}, ax=ax)
            plt.title("Graphe avec chemin le plus court (Bellman-Ford)")

            # Intégrer le graphe dans la nouvelle fenêtre avec FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        else:
            output_label.config(text=f"Aucun chemin entre {start_vertex} et {end_vertex}")
    except nx.NetworkXNoPath:
        output_label.config(text=f"Aucun chemin entre {start_vertex} et {end_vertex}")
    except nx.NetworkXUnbounded:
        output_label.config(text="Le graphe contient un cycle de poids négatif.")
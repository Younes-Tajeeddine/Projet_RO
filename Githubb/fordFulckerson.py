import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from tkinter import simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def generate_random_graph(num_vertices, max_capacity=10):
    """Génère un graphe aléatoire avec des capacités aléatoires."""
    G = nx.DiGraph()
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i != j:  # Pas d'arcs auto-bouclants
                capacity = random.randint(1, max_capacity)
                G.add_edge(i, j, capacity=capacity)
    return G

def bfs(capacity, flow, source, sink):
    """Recherche en largeur (BFS) pour trouver un chemin augmentant."""
    parent = [-1] * len(capacity)
    parent[source] = -2
    queue = deque([(source, float('inf'))])
    while queue:
        u, min_cap = queue.popleft()
        for v in range(len(capacity)):
            if parent[v] == -1 and capacity[u][v] - flow[u][v] > 0:
                parent[v] = u
                new_flow = min(min_cap, capacity[u][v] - flow[u][v])
                if v == sink:
                    return new_flow, parent
                queue.append((v, new_flow))
    return 0, parent

def ford_fulkerson(capacity, source, sink):
    """Algorithme de Ford-Fulkerson pour trouver le flot maximal."""
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    max_flow = 0
    while True:
        path_flow, parent = bfs(capacity, flow, source, sink)
        if path_flow == 0:
            break
        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u
    return max_flow, flow

def find_min_cut(capacity, flow, source):
    """Trouve la coupe minimale en utilisant un BFS."""
    visited = [False] * len(capacity)
    queue = deque([source])
    visited[source] = True
    while queue:
        u = queue.popleft()
        for v in range(len(capacity)):
            if capacity[u][v] - flow[u][v] > 0 and not visited[v]:
                visited[v] = True
                queue.append(v)
    return visited

def draw_graph_with_cut(G, capacity, flow, min_cut, source, sink):
    """Affiche le graphe avec la coupe minimale."""
    pos = nx.spring_layout(G)
    fig, ax = plt.subplots(figsize=(8, 8))
    
    node_colors = ['green' if min_cut[u] else 'blue' for u in G.nodes()]
    edge_colors = []
    for u, v in G.edges():
        if min_cut[u] and not min_cut[v]:
            edge_colors.append('red')
        else:
            edge_colors.append('black')
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=500, font_size=16, font_weight='bold', ax=ax)
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels={(u, v): f"{capacity[u][v]}" for u, v in G.edges()},
        font_color='black', ax=ax
    )
    plt.text(pos[source][0], pos[source][1], "Source", color='red', fontsize=12, ha='center', fontweight='bold')
    plt.text(pos[sink][0], pos[sink][1], "Puits", color='purple', fontsize=12, ha='center', fontweight='bold')
    ax.set_title(f"Graphe avec coupe minimale (Source: {source}, Puits: {sink})")
    return fig

def display_min_cut_edges(capacity, flow, min_cut):
    """Affiche les arêtes de la coupe minimale."""
    cut_edges = []
    for u in range(len(capacity)):
        for v in range(len(capacity)):
            if min_cut[u] and not min_cut[v] and capacity[u][v] > 0:
                cut_edges.append((u, v))
    return cut_edges

def ford_fulkerson_gui(gui, output_label):
    """Fonction principale pour exécuter l'algorithme de Ford-Fulkerson via l'interface graphique."""
    num_vertices = simpledialog.askinteger("Entrée", "Entrez le nombre de sommets :", parent=gui, minvalue=2)
    if num_vertices is None:  # Si l'utilisateur annule
        output_label.config(text="Action annulée par l'utilisateur.")
        return

    # Génération du graphe
    G = generate_random_graph(num_vertices)

    # Choix de la source et du puits
    source = 0  # Source par défaut
    sink = num_vertices - 1  # Puits par défaut

    # Création d'une matrice de capacité
    capacity = [[0] * num_vertices for _ in range(num_vertices)]
    for u, v, data in G.edges(data=True):
        capacity[u][v] = data['capacity']

    # Calcul du flot maximal avec Ford-Fulkerson
    max_flow, flow = ford_fulkerson(capacity, source, sink)

    # Affichage du flot maximal
    output = f"Flot maximal : {max_flow}\n"

    # Trouver la coupe minimale
    min_cut = find_min_cut(capacity, flow, source)

    # Affichage des arêtes de la coupe minimale
    cut_edges = display_min_cut_edges(capacity, flow, min_cut)
    output += "Arêtes de la coupe minimale :\n"
    for u, v in cut_edges:
        output += f"({u}, {v}) avec capacité {capacity[u][v]}\n"

    output_label.config(text=output)

    # Affichage du graphe avec la coupe minimale dans une nouvelle fenêtre
    fig = draw_graph_with_cut(G, capacity, flow, min_cut, source, sink)

    # Création d'une fenêtre pour afficher le graphe
    graph_window = tk.Toplevel(gui)
    graph_window.title("Graphique avec coupe minimale")

    # Ajouter le graphique dans la fenêtre
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

import networkx as nx
import matplotlib.pyplot as plt
from random import randint
from randomcolor import RandomColor
import time
from tkinter import simpledialog, Tk, Label, Frame, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Pour intégrer matplotlib dans Tkinter

# Fonction pour démarrer le chronomètre
def tic():
    global start_time
    start_time = time.time()

# Fonction pour arrêter le chronomètre et afficher le temps écoulé
def toc():
    if 'start_time' in globals():
        elapsed_time = time.time() - start_time
        print(f"Temps écoulé : {elapsed_time:.6f} secondes")
    else:
        print("tic() n'a pas été appelé avant toc()")

# Fonction pour obtenir un entier positif via un champ Entry dans l'interface graphique
def get_positive_integer_gui(prompt, gui):
    value = simpledialog.askinteger("Entrée", prompt, parent=gui, minvalue=1)
    return value

# Fonction principale pour l'algorithme Welsh-Powell
def welsh_powell(gui, output_label):
    # Demander à l'utilisateur de saisir le nombre de sommets via Tkinter
    n = get_positive_integer_gui("Entrez le nombre de sommets :", gui)
    if n is None:  # Si l'utilisateur annule l'action
        output_label.config(text="Action annulée par l'utilisateur.")
        return

    # Créer un générateur de couleurs aléatoires
    rand_color = RandomColor()

    # Créer un graphe aléatoire
    G = nx.gnm_random_graph(n, randint(n, n * (n - 1) // 2))

    # Fonction pour appliquer l'algorithme Welsh-Powell
    def welsh_powell_coloring(graph):
        # Vérifier si le graphe contient des sommets
        if graph.number_of_nodes() == 0:
            output_label.config(text="Le graphe est vide.")
            return {}

        # Trier les sommets par degré décroissant
        sorted_nodes = sorted(graph.degree, key=lambda x: x[1], reverse=True)
        # Dictionnaire pour stocker les couleurs de chaque sommet
        color_map = {}
        
        for node, _ in sorted_nodes:
            # Trouver les couleurs des voisins du sommet courant
            neighbor_colors = {color_map.get(neigh) for neigh in graph.neighbors(node)}
            # Déterminer la première couleur disponible
            current_color = 0
            while current_color in neighbor_colors:
                current_color += 1
            color_map[node] = current_color

        # Calculer et afficher le nombre chromatique
        chromatic_number = max(color_map.values()) + 1
        output_label.config(text=f"Le nombre chromatique du graphe est : {chromatic_number}")

        return color_map

    # Démarrer le chronomètre avant la coloration
    tic()
    # Obtenir la coloration des sommets
    color_map = welsh_powell_coloring(G)
    # Arrêter le chronomètre après la coloration
    toc()

    # Vérifier si le graphe a des sommets avant de générer les couleurs
    if G.number_of_nodes() > 0 and color_map:
        # Générer une couleur aléatoire pour chaque index de couleur
        unique_colors = len(set(color_map.values()))
        color_palette = rand_color.generate(count=unique_colors, luminosity="light")

        # Assurez-vous que tous les nœuds ont une couleur dans color_map
        node_colors = [color_palette[color_map.get(node, 0)] for node in G.nodes()]

        # Créer une nouvelle fenêtre pour afficher le graphe
        graph_window = Toplevel(gui)
        graph_window.title("Graphe colorié avec l'algorithme Welsh-Powell")
        graph_window.geometry("800x800")

        # Dessiner le graphe avec les couleurs des nœuds
        fig, ax = plt.subplots(figsize=(6, 6))
        nx.draw(G, with_labels=True, node_color=node_colors, edge_color='gray', node_size=500, font_size=10, ax=ax)
        plt.title(f"Graphe colorié avec {unique_colors} couleurs (Algorithme Welsh-Powell)")

        # Intégrer le graphe dans la nouvelle fenêtre avec FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    else:
        output_label.config(text="Le graphe n'a pas de sommets à afficher.")
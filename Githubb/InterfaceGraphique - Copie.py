from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from WelshPowell import welsh_powell
from Kruskal import kruskal
from PotentielMetra import potentiel_metra
from BellmanFord import bellman_ford
from SteppingStone import stepping_stone_gui
from Dijkstra import dijkstra
from FordFulkerson import ford_fulkerson_gui
from Nord_west_Moindre_Cout import transport_gui

# Couleurs modernes et claires
bg_color = "#F5F5F5"  # Fond clair
button_color = "#4CAF50"  # Boutons verts
button_hover_color = "#45a049"  # Boutons au survol
text_color = "#333333"  # Texte sombre
accent_color = "#2196F3"  # Couleur d'accent (bleu)
progress_color = "#FF9800"  # Couleur de la barre de progression (orange)

# Création de la fenêtre principale
gui = Tk()
gui.geometry("1200x800")  # Taille de la fenêtre
gui.title("Recherches Opérationnelles")
gui.config(bg=bg_color)

# Charger l'image du logo
logo_image = Image.open(r"C:\Users\msi\Desktop\oussama\logo.png")  # Utiliser le chemin complet
logo_image = logo_image.resize((400, 60), Image.Resampling.LANCZOS)  # Redimensionner l'image
logo_photo = ImageTk.PhotoImage(logo_image)

# Ajouter le logo à l'interface
logo_label = Label(gui, image=logo_photo, bg=bg_color)
logo_label.pack(pady=20)

# Label de titre
title_label = Label(gui, text="Interface De DFSK", font=("Helvetica", 24, "bold"), fg=accent_color, bg=bg_color)
title_label.pack(pady=10)

# Cadre principal
main_frame = Frame(gui, bg=bg_color)
main_frame.pack(pady=20)

# Titre secondaire
algo_label = Label(main_frame, text="Merhba Bik F l'application concernant les algorithmes\nRéalisé par : Khedif Oussama\nEncadré par : El Mkhalet Mouna",
                   font=("Helvetica", 12), fg=text_color, bg=bg_color)
algo_label.pack(pady=10)

# Style des boutons
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), background=button_color, foreground=text_color)
style.map("TButton", background=[("active", button_hover_color)])

# Fonction pour ouvrir une nouvelle fenêtre
def algorithme():
    guiA = Toplevel(gui)
    guiA.geometry("1200x800")
    guiA.config(bg=bg_color)

    # Cadre pour les boutons
    button_frame = Frame(guiA, bg=bg_color)
    button_frame.pack(pady=20)

    # Label de sortie pour afficher les résultats
    output_label = Label(guiA, text="", font=("Helvetica", 12), fg=text_color, bg=bg_color, wraplength=1100)
    output_label.pack(pady=20)

    # Barre de progression
    progress = ttk.Progressbar(guiA, orient=HORIZONTAL, length=400, mode='indeterminate')
    progress.pack(pady=10)

    # Fonction pour exécuter les algorithmes
    def run_algorithm(algorithm, name):
        try:
            output_label.config(text=f"Exécution de l'algorithme {name}...")
            progress.start(10)  # Démarrer la barre de progression
            guiA.update_idletasks()  # Mettre à jour l'interface
            algorithm(guiA, output_label)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            progress.stop()  # Arrêter la barre de progression

    # Création des boutons pour les algorithmes
    # Ligne 1
    welsh_powell_button = ttk.Button(button_frame, text="Welsh Powell", command=lambda: run_algorithm(welsh_powell, "Welsh-Powell"))
    welsh_powell_button.grid(row=0, column=0, padx=10, pady=10)
    
    kruskal_button = ttk.Button(button_frame, text="Kruskal", command=lambda: run_algorithm(kruskal, "Kruskal"))
    kruskal_button.grid(row=0, column=1, padx=10, pady=10)

    potentiel_metra_button = ttk.Button(button_frame, text="Potentiel Métra", command=lambda: run_algorithm(potentiel_metra, "Potentiel Métra"))
    potentiel_metra_button.grid(row=0, column=2, padx=10, pady=10)

    bellman_ford_button = ttk.Button(button_frame, text="Bellman-Ford", command=lambda: run_algorithm(bellman_ford, "Bellman-Ford"))
    bellman_ford_button.grid(row=0, column=3, padx=10, pady=10)

    # Ligne 2
    stepping_stone_button = ttk.Button(button_frame, text="Stepping Stone", command=lambda: run_algorithm(stepping_stone_gui, "Stepping Stone"))
    stepping_stone_button.grid(row=1, column=0, padx=10, pady=10)

    dijkstra_button = ttk.Button(button_frame, text="Dijkstra", command=lambda: run_algorithm(dijkstra, "Dijkstra"))
    dijkstra_button.grid(row=1, column=1, padx=10, pady=10)

    ford_fulkerson_button = ttk.Button(button_frame, text="Ford-Fulkerson", command=lambda: run_algorithm(ford_fulkerson_gui, "Ford-Fulkerson"))
    ford_fulkerson_button.grid(row=1, column=2, padx=10, pady=10)

    transport_button = ttk.Button(button_frame, text="Nord-Ouest/Moindre coût", command=lambda: run_algorithm(transport_gui, "Transport"))
    transport_button.grid(row=1, column=3, padx=10, pady=10)

# Boutons de la fenêtre principale
btn1 = ttk.Button(gui, text="Entrer", command=algorithme)
btn1.place(x=500, y=300, width=200, height=50)

btn2 = ttk.Button(gui, text="Quitter", command=gui.destroy)
btn2.place(x=500, y=400, width=200, height=50)

gui.mainloop()
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

# Couleurs pastel
bg_color = "Brown"  # Fond clair
button_color = "#8B4513"  # Marron pour les boutons
button_hover_color = "#A0522D"  # Marron clair au survol
text_color = "White"  # Texte noir/gris foncé
accent_color = "White"  # Saumon pour les accents
frame_color = "Black"  # Fond blanc pour les cadres

# Création de la fenêtre principale
gui = Tk()
gui.geometry("1200x800")
gui.title("Recherches Opérationnelles")
gui.config(bg=bg_color)

# Charger l'image du logo
logo_image = Image.open(r"C:\Users\az\Desktop\YounesRO\Younes\logo.png")  # Chemin complet
logo_image = logo_image.resize((300, 60), Image.Resampling.LANCZOS)  # Redimensionner
logo_photo = ImageTk.PhotoImage(logo_image)

# Ajouter le logo
logo_label = Label(gui, image=logo_photo, bg=bg_color)
logo_label.pack(pady=20)

# Label de titre
title_label = Label(gui, text="Interface Graphic", font=("Segoe UI", 28, "bold"), fg=accent_color, bg=bg_color)
title_label.pack(pady=10)

# Cadre principal
main_frame = Frame(gui, bg=frame_color, bd=0, relief="flat")
main_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

# Titre secondaire
algo_label = Label(main_frame, text="Les algorithmes de YFT \n\nRealised by : Yahya Fettane\nSupervised by : BENNAR ABDELKARIM",
                   font=("Segoe UI", 14), fg=text_color, bg=frame_color)
algo_label.pack(pady=20)

# Style des boutons
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 12, "bold"), background=button_color, foreground="black", padding=10)
style.map("TButton",
          background=[("active", button_hover_color)],
          foreground=[("disabled", "#a0a0a0")])

# Fonction pour ouvrir une nouvelle fenêtre
def algorithme():
    guiA = Toplevel(gui)
    guiA.geometry("1200x800")
    guiA.title("Choisir un algorithme")
    guiA.config(bg=bg_color)

    # Cadre pour les boutons
    button_frame = Frame(guiA, bg=frame_color, bd=0, relief="flat")
    button_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

    # Label de sortie pour afficher les résultats
    output_label = Label(guiA, text="", font=("Segoe UI", 14), fg=text_color, bg=frame_color, wraplength=1000)
    output_label.pack(pady=20)

    # Barre de progression
    progress = ttk.Progressbar(guiA, orient=HORIZONTAL, length=400, mode='indeterminate', style="TProgressbar")
    progress.pack(pady=10)

    # Fonction pour exécuter les algorithmes
    def run_algorithm(algorithm, name):
        try:
            output_label.config(text=f"Exécution de l'algorithme {name}...")
            progress.start(10)
            guiA.update_idletasks()
            algorithm(guiA, output_label)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            progress.stop()

    # Création des boutons
    algorithms = [
        ("Welsh Powell", welsh_powell),
        ("Kruskal", kruskal),
        ("Potentiel Métra", potentiel_metra),
        ("Bellman-Ford", bellman_ford),
        ("Stepping Stone", stepping_stone_gui),
        ("Dijkstra", dijkstra),
        ("Ford-Fulkerson", ford_fulkerson_gui),
        ("MN", transport_gui)
    ]

    for idx, (name, func) in enumerate(algorithms):
        button = ttk.Button(button_frame, text=name, command=lambda f=func, n=name: run_algorithm(f, n))
        button.grid(row=idx // 4, column=idx % 4, padx=30, pady=20)

# Récupérer la largeur et la hauteur de la fenêtre
window_width = 1200
window_height = 800

# Calcul des positions pour centrer les boutons
btn_width = 150
btn_height = 50
x_center = (window_width - btn_width) // 2  # Calculer la position x pour centrer
y_center_btn1 = (window_height // 2) - 50  # Bouton "Entrer" au-dessus
y_center_btn2 = y_center_btn1 + btn_height + 20  # Bouton "Quitter" en dessous avec un espace de 20px

# Boutons de la fenêtre principale
btn1 = ttk.Button(gui, text="Enter", command=algorithme, style="TButton")
btn1.place(x=x_center, y=y_center_btn1, width=btn_width, height=btn_height)

btn2 = ttk.Button(gui, text="Exit", command=gui.destroy, style="TButton")
btn2.place(x=x_center, y=y_center_btn2, width=btn_width, height=btn_height)

gui.mainloop()

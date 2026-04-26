import tkinter as tk  
import subprocess  
import sys  

# Classe principale de l'application
class ApplicationTableauBord:
    def __init__(self, racine):
        # fenêtre principale
        self.racine = racine
        self.racine.title("Dashboard")  
        self.racine.geometry("1100x650") 
        self.racine.configure(bg="#f5f5f5")  

        # données (simulation)
        self.donnees = {
            "Entrée": {"actuel": 4, "objectif": 5},
            "Plat": {"actuel": 2, "objectif": 5},
            "Dessert": {"actuel": 1, "objectif": 5},
            "Boisson": {"actuel": 3, "objectif": 5}
        }

        # création de l'interface
        self.creer_header()
        self.creer_zone_principale()

    # partie en haut de la fenêtre
    def creer_header(self):
        header = tk.Frame(self.racine, bg="#d9d2c7", height=60)
        header.pack(fill="x")  
        header.pack_propagate(False)  

        # titre à gauche
        tk.Label(
            header,
            text="Mon Repas d’Anniversaire",
            bg="#d9d2c7",
            font=("Helvetica", 14)
        ).pack(side="left", padx=20, pady=10)

        # cadre pour les boutons à droite
        cadre_btn = tk.Frame(header, bg="#d9d2c7")
        cadre_btn.pack(side="right", padx=20, pady=10)

        # bouton retour accueil
        tk.Button(
            cadre_btn,
            text="Accueil",
            bg="#f4a300",
            width=12,
            command=self.retourner_accueil  # action au clic
        ).pack(side="left", padx=5)

        # autres boutons ( partie logique qu'on vas s'en charger plus tard )
        tk.Button(cadre_btn, text="Créer", bg="#f4a300", width=12).pack(side="left", padx=5)
        tk.Button(cadre_btn, text="Tableau de bord", bg="black", fg="white", width=15).pack(side="left", padx=5)

        # bordure jaune sous le header
        tk.Frame(self.racine, bg="#f4a300", height=3).pack(fill="x")

    # fonction pour retourner à l'accueil
    def retourner_accueil(self):
        chemin = __file__.replace("dashboard.py", "accueil.py")

        subprocess.Popen([sys.executable, chemin])

        self.racine.destroy()

    # partie principale qui contient tout les informations necessaires pour l'organisateur
    def creer_zone_principale(self):
        zone = tk.Frame(self.racine, bg="#f5f5f5")
        zone.pack(fill="both", expand=True)

        # création des deux parties
        self.creer_sidebar(zone) # partie gauche 
        self.creer_contenu(zone) # partie droite

    # partie gauche 
    def creer_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg="#e6ded3", width=280)
        sidebar.pack(side="left", fill="y")

        tk.Label(
            sidebar,
            text="CONSEILS POUR L’ORGANISATEUR",
            bg="#e6ded3",
            font=("Helvetica", 10, "bold")
        ).pack(pady=20)

        for _ in range(5):
            carte = tk.Frame(sidebar, bg="#e7bfa7", width=240, height=100)
            carte.pack(pady=10, padx=20)

            # titre du conseil
            tk.Label(
                carte,
                text="Chercher pour entrée",
                fg="red",
                bg="#e7bfa7",
                font=("Helvetica", 10, "bold")
            ).pack(anchor="w", padx=10, pady=5)

            # description du conseil
            tk.Label(
                carte,
                text="Il manque encore des portions.\nOriente les prochains inscrits vers cette catégorie.",
                fg="red",
                bg="#e7bfa7",
                justify="left"
            ).pack(anchor="w", padx=10)

    # partie droit le tableau de bord
    def creer_contenu(self, parent):
        contenu = tk.Frame(parent, bg="#f5f5f5")
        contenu.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        # titre principal
        tk.Label(
            contenu,
            text="Tableau de bord",
            font=("Helvetica", 22, "bold"),
            bg="#f5f5f5"
        ).pack()

        # ligne sous le titre
        tk.Frame(contenu, bg="black", height=2, width=250).pack(pady=5)

        # section des barres
        tk.Label(contenu, text="JAUGES DE BESOIN", bg="#f5f5f5").pack(pady=20)

        # création des barres
        self.creer_barre(contenu, "Entrée", "blue")
        self.creer_barre(contenu, "Plat", "green")
        self.creer_barre(contenu, "Dessert", "pink")
        self.creer_barre(contenu, "Boisson", "orange")

        # section graphique
        tk.Label(contenu, text="RÉPARTITION ACTUELLE", bg="#f5f5f5").pack(pady=20)

        # création du graphique
        self.creer_graphique(contenu)

    # fonction pour créer une barre de progression pour chaque catégorie
    def creer_barre(self, parent, categorie, couleur):
        # récupération des données
        data = self.donnees[categorie]

        actuel = data["actuel"]  # valeur actuelle
        objectif = data["objectif"]  # valeur cible
        reste = actuel - objectif  # différence

        # ligne contenant la barre
        frame = tk.Frame(parent, bg="#f5f5f5")
        frame.pack(fill="x", pady=8)

        # petit carré couleur
        tk.Frame(frame, bg=couleur, width=10, height=10).pack(side="left", padx=5)

        # nom de la catégorie
        tk.Label(frame, text=categorie, bg="#f5f5f5").pack(side="left", padx=5)

        # zone de dessin de la barre
        canvas = tk.Canvas(frame, height=6, bg="#eee", highlightthickness=0)
        canvas.pack(side="left", fill="x", expand=True, padx=10)

        # calcul de la largeur de la barre
        largeur = (actuel / objectif) * 300

        # dessin de la barre
        canvas.create_rectangle(0, 0, largeur, 6, fill="#a52a2a")

        # affichage des valeurs
        tk.Label(frame, text=f"{actuel}/{objectif}", bg="#f5f5f5").pack(side="left", padx=10)
        tk.Label(frame, text=f"{reste}", fg="red", bg="#f5f5f5").pack(side="left")

    # fonction pour créer un graphique simple montrant la répartition actuelle des catégories
    def creer_graphique(self, parent):
        # zone de dessin
        canvas = tk.Canvas(parent, width=520, height=240, bg="white")
        canvas.pack(pady=5)

        # titre du graphique
        canvas.create_text(15, 12, text="RÉPARTITION ACTUELLE",
                           anchor="w", font=("Helvetica", 10, "bold"))

        # titre 
        legend_y = 30
        couleurs = ["#4a90e2", "#2ecc71", "#e91e63", "#c97a00"]
        categories = list(self.donnees.keys())

        # affichage des catégories en haut
        for i, cat in enumerate(categories):
            x = 15 + i * 120
            canvas.create_rectangle(x, legend_y, x+8, legend_y+8, fill=couleurs[i])
            canvas.create_text(x+12, legend_y+4,
                               text=f"{cat} ({self.donnees[cat]['actuel']})",
                               anchor="w", font=("Helvetica", 8))

        # simulation de données pour le graphique
        base_x = 60
        base_y = 170
        largeur_max = 480
        hauteur_min = 60

        # axes
        canvas.create_line(base_x, base_y, largeur_max, base_y)  # axe X
        canvas.create_line(base_x, hauteur_min, base_x, base_y)  # axe Y

        # graduations
        step = 12
        for i in range(0, 9):
            y = base_y - i * step
            canvas.create_text(base_x - 12, y, text=str(i), font=("Helvetica", 7))
            canvas.create_line(base_x, y, largeur_max, y, fill="#ddd")

        # points du graphique
        points = []
        for i, cat in enumerate(categories):
            x = base_x + 50 + i * 90
            val = self.donnees[cat]["actuel"]
            y = base_y - val * step

            points.append((x, y))
            canvas.create_text(x, base_y + 10, text=cat + "s", font=("Helvetica", 8))

        # ligne entre les points
        for i in range(len(points)-1):
            canvas.create_line(points[i], points[i+1], fill="gray", dash=(3, 2))

        # points visibles
        for x, y in points:
            canvas.create_oval(x-3, y-3, x+3, y+3, fill="gray")

        # petite barre verte sous "Plat"
        x_plat = base_x + 50 + 1 * 90
        canvas.create_rectangle(
            x_plat - 20, base_y - 6,
            x_plat + 20, base_y,
            fill="#2ecc71"
        )

# fonction principale pour lancer l'application
if __name__ == "__main__":
    racine = tk.Tk()  
    app = ApplicationTableauBord(racine)  
    racine.mainloop()  
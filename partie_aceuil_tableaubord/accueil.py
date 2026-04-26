import tkinter as tk  
from PIL import Image, ImageTk  
import subprocess  # sert a lancer un autre fichier python
import sys  # sert a récupérer le chemin de Python

# Classe principale de l'application Accueil
class ApplicationAccueil:
    def __init__(self, fenetre):
       
        self.fenetre = fenetre
        self.fenetre.title("Accueil")
        self.fenetre.geometry("900x600")
        self.fenetre.resizable(False, False)

        # couleurs utilisées
        self.couleur_header = "#e6ded3"
        self.couleur_bordure = "#f4a300"

        self.creer_entete()
        self.creer_corps()

    # partie entete(titre + bouton)
    def creer_entete(self):
        # création d'une zone en haut
        self.entete = tk.Frame(self.fenetre, bg=self.couleur_header, height=60)
        self.entete.pack(fill="x")

       
        self.bouton_demarrer = tk.Button(
            self.entete,
            text="Démarrez ici",
            font=("Helvetica", 12, "bold"),
            bg="#f4a300",
            command=self.ouvrir_tableau_bord  # action quand on clique
        )
       
        self.bouton_demarrer.pack(side="right", padx=20, pady=10)

        self.bordure = tk.Frame(self.fenetre, bg=self.couleur_bordure, height=3)
        self.bordure.pack(fill="x")

    def creer_corps(self):
        
        self.canvas = tk.Canvas(self.fenetre, width=900, height=540)
        self.canvas.pack()

       
        self.charger_image()

        # Affichage du texte par-dessus l'image
        self.canvas.create_text(
            450, 200,
            text="Organisez des repas de groupe\nparfaitement équilibrés, sans prise de tête.",
            font=("Helvetica", 20, "bold"),
            fill="black",
            justify="center"
        )

    # ajouter une image de fond
    def charger_image(self):
        try:
           
            chemin_image = r"C:\Users\HP\Documents\L2  informatique\S4\ing_sys_int\projet2\Projet_ingSI_2\partie_aceuil_tableaubord\img.jpg"
            image = Image.open(chemin_image)
            image = image.resize((900, 540))
            self.image_fond = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=self.image_fond, anchor="nw")

        except Exception as erreur:
            print("Erreur image :", erreur)

    # aller dans le tableau de bord
    def ouvrir_tableau_bord(self):
        chemin = __file__.replace("accueil.py", "dashboard.py")
        subprocess.Popen([sys.executable, chemin])

        self.fenetre.destroy()


# fonction main pour lancer l'application
if __name__ == "__main__":
    fenetre = tk.Tk()  # créer la fenêtre
    app = ApplicationAccueil(fenetre)  # lancer l'application
    fenetre.mainloop()  # boucle tkinter (obligatoire)
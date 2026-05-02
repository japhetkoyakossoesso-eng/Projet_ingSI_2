import tkinter as tk
from tkinter import messagebox


class CreationRepasPage(tk.Frame):

    VALEUR_MIN = 0
    VALEUR_MAX = 99

    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        self.sv_nom      = tk.StringVar()
        self.iv_entrees  = tk.IntVar(value=5)
        self.iv_plats    = tk.IntVar(value=12)
        self.iv_desserts = tk.IntVar(value=10)
        self.iv_boissons = tk.IntVar(value=12)

        titre = tk.Label(
            self,
            text="Création d'un repas",
            bg="white",
            font=("Helvetica", 20),
        )
        titre.pack(pady=(30, 20))

        corps = tk.Frame(self, bg="white")
        corps.pack(fill="both", expand=True, padx=30)

        tk.Label(
            corps,
            text="Nom de l'évènement",
            bg="white",
            font=("Helvetica", 12),
            anchor="w",
        ).pack(fill="x", pady=(0, 4))

        entry_nom = tk.Entry(
            corps,
            textvariable=self.sv_nom,
            font=("Helvetica", 13),
            bd=1,
            relief="solid",
        )
        entry_nom.pack(fill="x", ipady=6)

        tk.Frame(corps, bg="white", height=16).pack()

        self._creer_compteur(corps, "Nombre d'entrées requis",    self.iv_entrees)
        self._creer_compteur(corps, "Nombre de plats requis",     self.iv_plats)
        self._creer_compteur(corps, "Nombre de désserts requis",  self.iv_desserts)
        self._creer_compteur(corps, "Nombre de boissons requis",  self.iv_boissons)

        btn_creer = tk.Button(
            self,
            text="Créer",
            bg="black",
            fg="black",
            font=("Helvetica", 14),
            bd=0,
            pady=12,
            cursor="hand2",
            command=self._valider,
        )
        btn_creer.pack(fill="x", padx=30, pady=24)

    def _creer_compteur(self, parent, label_texte: str, variable: tk.IntVar):
        cadre = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=12, pady=10)
        cadre.pack(fill="x", pady=6)

        tk.Label(
            cadre,
            text=label_texte,
            bg="white",
            font=("Helvetica", 12),
            anchor="w",
        ).pack(fill="x")

        ligne = tk.Frame(cadre, bg="white")
        ligne.pack(fill="x", pady=(6, 0))

        btn_plus = tk.Button(
            ligne,
            text="+",
            font=("Helvetica", 13),
            bd=1,
            relief="solid",
            padx=10,
            pady=2,
            cursor="hand2",
            command=lambda: self._incrementer(variable, +1),
        )
        btn_plus.pack(side="left")

        lbl_valeur = tk.Label(
            ligne,
            textvariable=variable,
            bg="white",
            font=("Helvetica", 14),
            width=6,
        )
        lbl_valeur.pack(side="left", expand=True)

        btn_moins = tk.Button(
            ligne,
            text="−",
            font=("Helvetica", 13),
            bd=1,
            relief="solid",
            padx=10,
            pady=2,
            cursor="hand2",
            command=lambda: self._incrementer(variable, -1),
        )
        btn_moins.pack(side="right")

    def _incrementer(self, variable: tk.IntVar, delta: int):
        nouvelle_valeur = variable.get() + delta
        nouvelle_valeur = max(self.VALEUR_MIN, min(self.VALEUR_MAX, nouvelle_valeur))
        variable.set(nouvelle_valeur)

    def _valider(self):
        nom = self.sv_nom.get().strip()
        if not nom:
            messagebox.showwarning("Champ manquant", "Veuillez saisir le nom de l'événement.")
            return

        nouveau_repas = {
            "nom":               nom,
            "entrees_requises":  self.iv_entrees.get(),
            "plats_requis":      self.iv_plats.get(),
            "desserts_requis":   self.iv_desserts.get(),
            "boissons_requises": self.iv_boissons.get(),
            "entrees_actuelles":  0,
            "plats_actuels":      0,
            "desserts_actuels":   0,
            "boissons_actuelles": 0,
        }

        self.controller.repas.append(nouveau_repas)

        self.sv_nom.set("")
        self.iv_entrees.set(5)
        self.iv_plats.set(12)
        self.iv_desserts.set(10)
        self.iv_boissons.set(12)

        self.controller.afficher_page("liste")
        self.controller.frames["liste"].afficher_repas()

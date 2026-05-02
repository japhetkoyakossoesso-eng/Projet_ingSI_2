import tkinter as tk
from tkinter import font as tkfont


class ListeRepasPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        titre = tk.Label(
            self,
            text="Liste des repas",
            bg="white",
            font=("Helvetica", 20),
        )
        titre.pack(pady=(30, 20))

        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True, padx=20)

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="white")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        btn_nouveau = tk.Button(
            self,
            text="+ Nouveau repas",
            bg="black",
            fg="black",
            font=("Helvetica", 12),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: controller.afficher_page("creation"),
        )
        btn_nouveau.pack(pady=(10, 20))

        self.afficher_repas()

    def afficher_repas(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        repas_liste = self.controller.repas  

        if not repas_liste:
            vide = tk.Label(
                self.scroll_frame,
                text="Aucun repas créé pour l'instant, cliquez sur + Nouveau repas pour en ajouter un !",
                bg="white",
                fg="gray",
                font=("Helvetica", 13),
            )
            vide.pack(pady=40)
            return

        for repas in repas_liste:
            self._creer_carte(repas)

    def _creer_carte(self, repas: dict):
        carte = tk.Frame(
            self.scroll_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=15,
            pady=12,
        )
        carte.pack(fill="x", pady=6)

        nom = tk.Label(
            carte,
            text=repas["nom"],
            bg="white",
            font=("Helvetica", 14, "bold"),
            anchor="w",
        )
        nom.pack(fill="x")

        plats      = repas["plats_actuels"]
        max_plats  = repas["plats_requis"]
        entrees    = repas["entrees_actuelles"]
        max_ent    = repas["entrees_requises"]
        desserts   = repas["desserts_actuels"]
        max_des    = repas["desserts_requis"]
        boissons   = repas["boissons_actuelles"]
        max_boi    = repas["boissons_requises"]

        resume = (
            f"{plats} / {max_plats} Plats  –  "
            f"{entrees} / {max_ent} Entrées  –  "
            f"{desserts} / {max_des} Désserts  –  "
            f"{boissons} / {max_boi} Boissons"
        )

        resume_label = tk.Label(
            carte,
            text=resume,
            bg="white",
            fg="#e05c3a",
            font=("Helvetica", 11),
            anchor="w",
        )
        resume_label.pack(fill="x")

import tkinter as tk
from liste_repas import ListeRepasPage
from creation_repas import CreationRepasPage


class Application(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Organisation de Repas")
        self.geometry("520x700")
        self.resizable(False, True)
        self.configure(bg="white")

        self.repas = []

        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for NomPage, cle in [(ListeRepasPage, "liste"), (CreationRepasPage, "creation")]:
            frame = NomPage(parent=container, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[cle] = frame

        self.afficher_page("liste")

    def afficher_page(self, cle: str):
        self.frames[cle].tkraise()


if __name__ == "__main__":
    app = Application()
    app.mainloop()

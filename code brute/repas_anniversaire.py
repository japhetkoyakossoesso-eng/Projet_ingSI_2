import tkinter as tk
from tkinter import ttk, messagebox, font
import random

# ─── Palette de couleurs ────────────────────────────────────────────────────
BG_MAIN       = "#FFF8F0"
BG_CARD       = "#FFFFFF"
BG_NAVBAR     = "#FFFFFF"
ACCENT_ORANGE = "#F5A623"
ACCENT_RED    = "#E8413C"
ACCENT_DARK   = "#1A1A1A"
TEXT_MAIN     = "#1A1A1A"
TEXT_MUTED    = "#888888"
BORDER_COLOR  = "#E5E5E5"
ALERT_BG      = "#FDE8DF"
ALERT_FG      = "#D84315"

AVATAR_COLORS = [
    "#F5A623", "#26C6DA", "#AB47BC", "#66BB6A",
    "#EF5350", "#42A5F5", "#FF7043", "#26A69A",
]

CATEGORIES = {
    "Entrée":   {"icon": "🍽", "color": "#5BB5A2", "min": 5,  "key": "entree"},
    "Plat":     {"icon": "🔔", "color": "#D4A850", "min": 8,  "key": "plat"},
    "Dessert":  {"icon": "🧁", "color": "#E07070", "min": 4,  "key": "dessert"},
    "Boisson":  {"icon": "🥤", "color": "#D4A850", "min": 15, "key": "boisson"},
}


# ─── Données globales ────────────────────────────────────────────────────────
participants = []          # liste de dicts
selected_categories = {}   # {nom_cat: bool}
portions = 10
avatar_counter = {}        # pour alterner les couleurs


# ─── Helpers ────────────────────────────────────────────────────────────────
def get_avatar_color(nom, prenom):
    key = f"{nom}{prenom}"
    if key not in avatar_counter:
        avatar_counter[key] = random.choice(AVATAR_COLORS)
    return avatar_counter[key]


def totals_by_category():
    t = {k: 0 for k in CATEGORIES}
    for p in participants:
        for cat, info in CATEGORIES.items():
            t[cat] += p["categories"].get(cat, 0) * p["portions"]
    return t


def missing_categories():
    t = totals_by_category()
    missing = []
    for cat, info in CATEGORIES.items():
        if t[cat] < info["min"]:
            missing.append(cat.lower())
    return missing


# ─── Application principale ─────────────────────────────────────────────────
class RepasApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mon Repas d'Anniversaire")
        self.configure(bg=BG_MAIN)
        self.geometry("1280x800")
        self.minsize(900, 600)
        self.resizable(True, True)

        # Fonts
        self.f_title  = font.Font(family="Helvetica Neue", size=14, weight="bold")
        self.f_nav    = font.Font(family="Helvetica Neue", size=11, weight="bold")
        self.f_label  = font.Font(family="Helvetica Neue", size=10)
        self.f_small  = font.Font(family="Helvetica Neue", size=9)
        self.f_big    = font.Font(family="Helvetica Neue", size=26, weight="bold")
        self.f_section= font.Font(family="Helvetica Neue", size=10, weight="bold")

        self._build_navbar()
        self._build_body()
        self.refresh()

    # ── Navbar ───────────────────────────────────────────────────────────────
    def _build_navbar(self):
        nav = tk.Frame(self, bg=BG_NAVBAR, height=52, bd=0)
        nav.pack(fill="x", side="top")
        nav.pack_propagate(False)

        inner = tk.Frame(nav, bg=BG_NAVBAR)
        inner.pack(fill="both", expand=True, padx=20)

        # Titre à gauche
        tk.Label(inner, text="Mon Repas d'Anniversaire",
                 font=self.f_title, bg=BG_NAVBAR, fg=TEXT_MAIN).pack(side="left", pady=12)

        # Boutons groupés à droite (space-between effect)
        btn_group = tk.Frame(inner, bg=BG_NAVBAR)
        btn_group.pack(side="right")

        def nav_btn(parent, text, bg, fg, cmd=None):
            btn = tk.Button(parent, text=text, font=self.f_nav,
                            bg=bg, fg=fg, relief="flat", padx=16, pady=6,
                            cursor="hand2", bd=0, activebackground=bg,
                            activeforeground=fg, command=cmd or (lambda: None))
            btn.pack(side="left", padx=4, pady=8)
            return btn

        nav_btn(btn_group, "Accueil",            ACCENT_ORANGE, "#FFF", self.go_accueil)
        nav_btn(btn_group, "Créer",              ACCENT_ORANGE, "#FFF", self.go_creer)
        nav_btn(btn_group, "Tableau de bord",    ACCENT_DARK,   "#FFF", self.go_tableau)
        nav_btn(btn_group, "Supprimer le repas", ACCENT_RED,    "#FFF", self.supprimer_repas)

        sep = tk.Frame(self, bg=BORDER_COLOR, height=1)
        sep.pack(fill="x")

    # ── Corps principal ──────────────────────────────────────────────────────
    def _build_body(self):
        self.body = tk.Frame(self, bg=BG_MAIN)
        self.body.pack(fill="both", expand=True, padx=30, pady=24)

        # Colonne gauche
        self.left_col = tk.Frame(self.body, bg=BG_MAIN)
        self.left_col.pack(side="left", fill="both", expand=False)

        # Colonne droite
        self.right_col = tk.Frame(self.body, bg=BG_MAIN)
        self.right_col.pack(side="left", fill="both", expand=True, padx=(20, 0))

        self._build_form()
        self._build_categories_portions()
        self._build_validate_btn()
        self._build_viability()
        self._build_participants_list()

    # ── Formulaire ajout participant ─────────────────────────────────────────
    def _build_form(self):
        card = self._card(self.left_col)
        card.pack(fill="x", pady=(0, 12))

        tk.Label(card, text="Ajouter un participant",
                 font=self.f_section, bg=BG_CARD, fg=TEXT_MAIN).grid(
                 row=0, column=0, columnspan=4, sticky="w", padx=18, pady=(16, 12))

        tk.Label(card, text="Nom", font=self.f_label, bg=BG_CARD, fg=TEXT_MUTED).grid(
            row=1, column=0, sticky="w", padx=18)
        tk.Label(card, text="Prénom", font=self.f_label, bg=BG_CARD, fg=TEXT_MUTED).grid(
            row=1, column=2, sticky="w", padx=(18, 18))

        self.nom_var    = tk.StringVar()
        self.prenom_var = tk.StringVar()

        self._entry(card, self.nom_var).grid(
            row=2, column=0, columnspan=2, padx=(18, 8), pady=(4, 16), sticky="ew")
        self._entry(card, self.prenom_var).grid(
            row=2, column=2, columnspan=2, padx=(8, 18), pady=(4, 16), sticky="ew")

        card.columnconfigure(0, weight=1)
        card.columnconfigure(1, weight=1)
        card.columnconfigure(2, weight=1)
        card.columnconfigure(3, weight=1)

    def _entry(self, parent, var):
        e = tk.Entry(parent, textvariable=var, font=self.f_label,
                     relief="solid", bd=1, bg=BG_CARD, fg=TEXT_MAIN,
                     highlightthickness=1, highlightbackground=BORDER_COLOR,
                     highlightcolor=ACCENT_ORANGE, insertbackground=TEXT_MAIN)
        e.configure(width=18)
        return e

    # ── Catégories + Portions ────────────────────────────────────────────────
    def _build_categories_portions(self):
        row = tk.Frame(self.left_col, bg=BG_MAIN)
        row.pack(fill="x", pady=(0, 0))

        # Catégories
        cat_card = self._card(row)
        cat_card.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(cat_card, text="Catégories", font=self.f_section,
                 bg=BG_CARD, fg=TEXT_MAIN).pack(pady=(14, 8))

        grid = tk.Frame(cat_card, bg=BG_CARD)
        grid.pack(padx=14, pady=(0, 14))

        self.cat_vars = {}
        self.cat_tiles = {}   # {cat: (frame, icon_bg, lbl)}
        self.selected_cat = tk.StringVar(value="")

        for i, (cat, info) in enumerate(CATEGORIES.items()):
            col = i % 2
            rw  = i // 2
            tile = self._cat_tile(grid, cat, info)
            tile.grid(row=rw, column=col, padx=6, pady=6)

        # Portions
        port_card = self._card(row)
        port_card.pack(side="left", fill="both", expand=True)

        tk.Label(port_card, text="Quantité de\nportions", font=self.f_section,
                 bg=BG_CARD, fg=TEXT_MAIN, justify="center").pack(pady=(14, 10))

        self.portions_var = tk.IntVar(value=10)

        display = tk.Frame(port_card, bg=BORDER_COLOR, bd=0)
        display.pack(padx=18, pady=(0, 10), fill="x")

        self.port_label = tk.Label(display, text="10\nPortion(s)",
                                   font=self.f_big, bg=BG_CARD, fg=TEXT_MAIN,
                                   relief="solid", bd=1, width=10)
        self.port_label.pack(fill="x")

        btns = tk.Frame(port_card, bg=BG_CARD)
        btns.pack(padx=18, pady=(0, 14), fill="x")
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        tk.Button(btns, text="+", font=self.f_nav,
                  bg=BG_CARD, fg=TEXT_MAIN, relief="solid", bd=1,
                  cursor="hand2",
                  command=self._increment_portions).grid(row=0, column=0, sticky="ew", padx=(0, 3))
        tk.Button(btns, text="−", font=self.f_nav,
                  bg=BG_CARD, fg=TEXT_MAIN, relief="solid", bd=1,
                  cursor="hand2",
                  command=self._decrement_portions).grid(row=0, column=1, sticky="ew", padx=(3, 0))

    def _cat_tile(self, parent, cat, info):
        frame = tk.Frame(parent, bg=BG_CARD, cursor="hand2")

        icon_bg = tk.Label(frame, text=info["icon"], font=font.Font(size=28),
                           bg=info["color"], fg="white", width=4, height=2)
        icon_bg.pack()

        lbl = tk.Label(frame, text=cat, font=self.f_small, bg=BG_CARD, fg=TEXT_MAIN)
        lbl.pack(pady=(4, 0))

        self.cat_tiles[cat] = (frame, icon_bg, lbl, info)

        def select():
            prev = self.selected_cat.get()
            if prev == cat:
                # Désélectionner
                self.selected_cat.set("")
                self._update_tile_style(cat, False)
            else:
                # Désélectionner l'ancien
                if prev and prev in self.cat_tiles:
                    self._update_tile_style(prev, False)
                self.selected_cat.set(cat)
                self._update_tile_style(cat, True)

        for w in (frame, icon_bg, lbl):
            w.bind("<Button-1>", lambda e, s=select: s())

        return frame

    def _update_tile_style(self, cat, selected):
        frame, icon_bg, lbl, info = self.cat_tiles[cat]
        if selected:
            # Fond de l'icône plus foncé (opacité simulée en assombrissant)
            dark_color = self._darken(info["color"], 0.65)
            icon_bg.config(bg=dark_color)
            frame.config(bg="#F0F0F0")
            lbl.config(bg="#F0F0F0", fg=TEXT_MAIN, font=font.Font(size=9, weight="bold"))
        else:
            icon_bg.config(bg=info["color"])
            frame.config(bg=BG_CARD)
            lbl.config(bg=BG_CARD, fg=TEXT_MAIN, font=font.Font(size=9))

    def _darken(self, hex_color, factor):
        """Assombrit une couleur hex par un facteur (0=noir, 1=inchangé)."""
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    # ── Bouton Valider ───────────────────────────────────────────────────────
    def _build_validate_btn(self):
        btn = tk.Button(self.left_col, text="Valider l'ajout",
                        font=self.f_nav, bg=ACCENT_DARK, fg="white",
                        relief="flat", bd=0, pady=14, cursor="hand2",
                        activebackground="#333", activeforeground="white",
                        command=self._add_participant)
        btn.pack(fill="x", pady=(12, 0))

    # ── Viabilité ────────────────────────────────────────────────────────────
    def _build_viability(self):
        self.viab_frame = tk.Frame(self.right_col, bg=BG_MAIN)
        self.viab_frame.pack(fill="x", pady=(0, 16))

    def _refresh_viability(self):
        for w in self.viab_frame.winfo_children():
            w.destroy()

        tk.Label(self.viab_frame, text="VIABILITÉ DU REPAS",
                 font=self.f_section, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w")

        miss = missing_categories()
        if miss:
            alert = tk.Frame(self.viab_frame, bg=ALERT_BG, bd=0)
            alert.pack(fill="x", pady=(8, 0))
            txt = "Il manque : " + ", ".join(miss)
            tk.Label(alert, text=txt, font=self.f_label,
                     bg=ALERT_BG, fg=ALERT_FG, padx=14, pady=10).pack(anchor="w")
        else:
            ok = tk.Frame(self.viab_frame, bg="#DFF2E1", bd=0)
            ok.pack(fill="x", pady=(8, 0))
            tk.Label(ok, text="✓ Le repas est complet !",
                     font=self.f_label, bg="#DFF2E1", fg="#2E7D32",
                     padx=14, pady=10).pack(anchor="w")

        # Totaux par catégorie
        totals = totals_by_category()
        total_row = tk.Frame(self.viab_frame, bg=BG_MAIN)
        total_row.pack(fill="x", pady=(14, 0))

        tk.Label(total_row, text="TOTAL PAR CATÉGORIE",
                 font=self.f_section, bg=BG_MAIN, fg=TEXT_MUTED).grid(
                 row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

        for i, (cat, info) in enumerate(CATEGORIES.items()):
            col_frame = tk.Frame(total_row, bg=BG_MAIN)
            col_frame.grid(row=1, column=i, padx=(0, 20), sticky="w")

            tk.Label(col_frame, text=cat,
                     font=self.f_small, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w")

            val = totals[cat]
            color = TEXT_MAIN if val >= info["min"] else ACCENT_ORANGE
            tk.Label(col_frame, text=str(val),
                     font=self.f_big, bg=BG_MAIN, fg=color).pack(anchor="w")

            tk.Label(col_frame, text=f"Min. {info['min']} requis",
                     font=self.f_small, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w")

    # ── Liste participants ────────────────────────────────────────────────────
    def _build_participants_list(self):
        self.part_frame = tk.Frame(self.right_col, bg=BG_MAIN)
        self.part_frame.pack(fill="both", expand=True)

    def _refresh_participants(self):
        for w in self.part_frame.winfo_children():
            w.destroy()

        card = self._card(self.part_frame)
        card.pack(fill="both", expand=True)

        # Header
        header = tk.Frame(card, bg=BG_CARD)
        header.pack(fill="x", padx=16, pady=(14, 10))

        tk.Label(header, text=f"{len(participants)} Participant(s)",
                 font=self.f_section, bg=BG_CARD, fg=TEXT_MAIN).pack(side="left")

        tk.Button(header, text="Tout supprimer",
                  font=self.f_small, bg=BG_CARD, fg=ACCENT_RED,
                  relief="flat", bd=0, cursor="hand2",
                  command=self._supprimer_tous).pack(side="right")

        sep = tk.Frame(card, bg=BORDER_COLOR, height=1)
        sep.pack(fill="x", padx=16)

        # Scrollable list
        canvas = tk.Canvas(card, bg=BG_CARD, highlightthickness=0)
        scrollbar = tk.Scrollbar(card, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_CARD)

        scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        win_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Forcer scroll_frame à prendre toute la largeur du canvas
        def _on_canvas_resize(event):
            canvas.itemconfig(win_id, width=event.width)
        canvas.bind("<Configure>", _on_canvas_resize)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        for idx, p in enumerate(participants):
            self._participant_row(scroll_frame, p, idx)

    def _participant_row(self, parent, p, idx):
        row = tk.Frame(parent, bg=BG_CARD)
        row.pack(fill="x", padx=16, pady=6)

        # Avatar
        av_color = get_avatar_color(p["nom"], p["prenom"])
        initials = (p["prenom"][:1] + p["nom"][:1]).upper()
        av = tk.Label(row, text=initials, font=font.Font(size=11, weight="bold"),
                      bg=av_color, fg="white", width=3, height=1,
                      relief="flat", padx=4, pady=6)
        av.pack(side="left", padx=(0, 12))

        # Infos
        info_col = tk.Frame(row, bg=BG_CARD)
        info_col.pack(side="left", fill="x", expand=True)

        tk.Label(info_col, text=f"{p['prenom']} {p['nom']}",
                 font=self.f_section, bg=BG_CARD, fg=TEXT_MAIN).pack(anchor="w")

        parts = []
        for cat in CATEGORIES:
            cnt = p["categories"].get(cat, 0)
            if cnt:
                parts.append(f"{cnt} {cat}{'s' if cnt>1 else ''}")
        detail = f"{p['portions']} portion(s) • " + " - ".join(parts) if parts else f"{p['portions']} portion(s)"
        tk.Label(info_col, text=detail,
                 font=self.f_small, bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")

        # Bouton supprimer
        tk.Button(row, text="✕", font=font.Font(size=14),
                  bg=BG_CARD, fg=TEXT_MUTED, relief="flat", bd=0,
                  cursor="hand2",
                  command=lambda i=idx: self._supprimer_participant(i)).pack(side="right")

        sep = tk.Frame(parent, bg=BORDER_COLOR, height=1)
        sep.pack(fill="x", padx=16)

    # ── Logique ──────────────────────────────────────────────────────────────
    def _increment_portions(self):
        v = self.portions_var.get()
        self.portions_var.set(v + 1)
        self.port_label.config(text=f"{v+1}\nPortion(s)")

    def _decrement_portions(self):
        v = self.portions_var.get()
        if v > 1:
            self.portions_var.set(v - 1)
            self.port_label.config(text=f"{v-1}\nPortion(s)")

    def _add_participant(self):
        nom    = self.nom_var.get().strip()
        prenom = self.prenom_var.get().strip()
        if not nom or not prenom:
            messagebox.showwarning("Champs manquants", "Veuillez entrer un nom et un prénom.")
            return

        cat_sel = self.selected_cat.get()
        cats = {cat_sel: 1} if cat_sel else {}

        p = {
            "nom":        nom,
            "prenom":     prenom,
            "portions":   self.portions_var.get(),
            "categories": cats,
        }
        participants.append(p)

        # Reset
        self.nom_var.set("")
        self.prenom_var.set("")
        prev = self.selected_cat.get()
        if prev:
            self._update_tile_style(prev, False)
        self.selected_cat.set("")
        self.portions_var.set(10)
        self.port_label.config(text="10\nPortion(s)")

        self.refresh()

    def _supprimer_participant(self, idx):
        if 0 <= idx < len(participants):
            participants.pop(idx)
            self.refresh()

    def _supprimer_tous(self):
        if participants and messagebox.askyesno(
                "Tout supprimer", "Supprimer tous les participants ?"):
            participants.clear()
            self.refresh()

    def supprimer_repas(self):
        if messagebox.askyesno("Supprimer le repas",
                                "Êtes-vous sûr de vouloir supprimer tout le repas ?"):
            participants.clear()
            self.refresh()

    def go_accueil(self):
        messagebox.showinfo("Navigation", "Vous êtes déjà sur la page d'accueil.")

    def go_creer(self):
        messagebox.showinfo("Créer", "Fonctionnalité 'Créer un nouveau repas' à implémenter.")

    def go_tableau(self):
        TableauDeBord(self)

    def refresh(self):
        self._refresh_viability()
        self._refresh_participants()

    # ── Helper card ──────────────────────────────────────────────────────────
    def _card(self, parent):
        return tk.Frame(parent, bg=BG_CARD, relief="solid", bd=1,
                        highlightthickness=1, highlightbackground=BORDER_COLOR)


# ─── Fenêtre Tableau de bord ─────────────────────────────────────────────────
class TableauDeBord(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Tableau de bord")
        self.configure(bg=BG_MAIN)
        self.geometry("700x500")
        self.grab_set()

        self.f_title   = font.Font(family="Helvetica Neue", size=14, weight="bold")
        self.f_section = font.Font(family="Helvetica Neue", size=10, weight="bold")
        self.f_label   = font.Font(family="Helvetica Neue", size=10)
        self.f_big     = font.Font(family="Helvetica Neue", size=24, weight="bold")
        self.f_small   = font.Font(family="Helvetica Neue", size=9)

        tk.Label(self, text="Tableau de bord", font=self.f_title,
                 bg=BG_MAIN, fg=TEXT_MAIN).pack(pady=(24, 6), padx=30, anchor="w")

        sep = tk.Frame(self, bg=BORDER_COLOR, height=1)
        sep.pack(fill="x", padx=30)

        self._build_stats()
        self._build_table()

    def _build_stats(self):
        frame = tk.Frame(self, bg=BG_MAIN)
        frame.pack(fill="x", padx=30, pady=20)

        totals = totals_by_category()
        stats = [
            ("Participants", str(len(participants)), TEXT_MAIN),
            ("Total portions", str(sum(p["portions"] for p in participants)), ACCENT_ORANGE),
        ]
        for cat, info in CATEGORIES.items():
            color = TEXT_MAIN if totals[cat] >= info["min"] else ACCENT_ORANGE
            stats.append((cat, str(totals[cat]), color))

        for i, (label, val, color) in enumerate(stats):
            col = tk.Frame(frame, bg=BG_CARD, relief="solid", bd=1,
                           highlightbackground=BORDER_COLOR, highlightthickness=1)
            col.grid(row=0, column=i, padx=6, pady=0, sticky="ew")
            tk.Label(col, text=val, font=self.f_big, bg=BG_CARD, fg=color,
                     padx=16, pady=8).pack()
            tk.Label(col, text=label, font=self.f_small, bg=BG_CARD, fg=TEXT_MUTED,
                     padx=16).pack(pady=(0, 10))
            frame.columnconfigure(i, weight=1)

    def _build_table(self):
        tk.Label(self, text="Détail des participants", font=self.f_section,
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", padx=30, pady=(0, 8))

        columns = ("Prénom", "Nom", "Portions", "Entrées", "Plats", "Desserts", "Boissons")
        tree = ttk.Treeview(self, columns=columns, show="headings", height=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=BG_CARD, fieldbackground=BG_CARD,
                        foreground=TEXT_MAIN, rowheight=28, font=("Helvetica Neue", 9))
        style.configure("Treeview.Heading", background=BORDER_COLOR,
                        foreground=TEXT_MUTED, font=("Helvetica Neue", 9, "bold"))

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=80, anchor="center")

        for p in participants:
            cats = p["categories"]
            tree.insert("", "end", values=(
                p["prenom"], p["nom"], p["portions"],
                cats.get("Entrée", 0), cats.get("Plat", 0),
                cats.get("Dessert", 0), cats.get("Boisson", 0),
            ))

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True, padx=(30, 0), pady=(0, 20))
        scrollbar.pack(side="left", fill="y", pady=(0, 20))


# ─── Lancement ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = RepasApp()
    app.mainloop()
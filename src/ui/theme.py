from tkinter import Tk, ttk


def configure_theme(root: Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")
    root.configure(bg="#f4f1ea")

    style.configure("TNotebook", background="#f4f1ea", borderwidth=0)
    style.configure("TNotebook.Tab", padding=(18, 10), font=("Helvetica", 11, "bold"))
    style.configure("Card.TFrame", background="#fffdf8", relief="flat")
    style.configure("Title.TLabel", background="#f4f1ea", foreground="#1f2937", font=("Helvetica", 24, "bold"))
    style.configure("Subtitle.TLabel", background="#f4f1ea", foreground="#4b5563", font=("Helvetica", 11))
    style.configure("CardTitle.TLabel", background="#fffdf8", foreground="#111827", font=("Helvetica", 12, "bold"))
    style.configure("CardValue.TLabel", background="#fffdf8", foreground="#b45309", font=("Helvetica", 20, "bold"))
    style.configure("Treeview", rowheight=28)

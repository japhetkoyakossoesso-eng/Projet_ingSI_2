from __future__ import annotations

import tkinter as tk
from tkinter import Tk, ttk


BG_MAIN = "#fff8f0"
BG_CARD = "#ffffff"
BG_SOFT = "#f4eee4"
BG_SIDEBAR = "#e6ded3"
ACCENT_ORANGE = "#f5a623"
ACCENT_RED = "#e8413c"
ACCENT_DARK = "#1a1a1a"
TEXT_MAIN = "#1a1a1a"
TEXT_MUTED = "#6b7280"
BORDER = "#e5e5e5"
SUCCESS_BG = "#dff2e1"
SUCCESS_FG = "#2e7d32"
ALERT_BG = "#fde8df"
ALERT_FG = "#d84315"


FONT_TITLE = ("Helvetica", 24, "bold")
FONT_SECTION = ("Helvetica", 12, "bold")
FONT_LABEL = ("Helvetica", 10)
FONT_SMALL = ("Helvetica", 9)
FONT_BIG = ("Helvetica", 28, "bold")


def configure_theme(root: Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")
    root.configure(bg=BG_MAIN)

    style.configure("TNotebook", background=BG_MAIN, borderwidth=0)
    style.configure("TNotebook.Tab", padding=(18, 10), font=("Helvetica", 11, "bold"))
    style.configure("Card.TFrame", background=BG_CARD, relief="flat")
    style.configure("Title.TLabel", background=BG_MAIN, foreground=TEXT_MAIN, font=FONT_TITLE)
    style.configure("Subtitle.TLabel", background=BG_MAIN, foreground=TEXT_MUTED, font=("Helvetica", 11))
    style.configure("CardTitle.TLabel", background=BG_CARD, foreground=TEXT_MAIN, font=FONT_SECTION)
    style.configure("CardValue.TLabel", background=BG_CARD, foreground="#b45309", font=("Helvetica", 20, "bold"))
    style.configure("Treeview", rowheight=28)
    style.configure("Treeview.Heading", font=("Helvetica", 9, "bold"))


def clear_frame(frame: tk.Frame) -> None:
    for widget in frame.winfo_children():
        widget.destroy()


def make_button(
    parent: tk.Widget,
    text: str,
    command,
    *,
    variant: str = "primary",
    width: int | None = None,
) -> tk.Button:
    palette = {
        "primary": (ACCENT_DARK, "#ffffff"),
        "accent": (ACCENT_ORANGE, "#ffffff"),
        "danger": (ACCENT_RED, "#ffffff"),
        "light": (BG_CARD, TEXT_MAIN),
    }
    bg, fg = palette.get(variant, palette["primary"])
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=bg,
        activeforeground=fg,
        relief="flat",
        bd=0,
        padx=16,
        pady=8,
        width=width,
        cursor="hand2",
        font=("Helvetica", 10, "bold"),
    )
    return button


def card(parent: tk.Widget, *, bg: str = BG_CARD, padx: int = 16, pady: int = 14) -> tk.Frame:
    return tk.Frame(
        parent,
        bg=bg,
        padx=padx,
        pady=pady,
        highlightbackground=BORDER,
        highlightthickness=1,
    )

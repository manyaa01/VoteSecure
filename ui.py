from pathlib import Path
import subprocess as sb_p
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk


BG = "#f4efe6"
SURFACE = "#fffaf2"
SURFACE_ALT = "#f0e4d4"
PRIMARY = "#113946"
PRIMARY_SOFT = "#2c5f6f"
ACCENT = "#c38b2f"
TEXT = "#1d2b36"
MUTED = "#6a7680"
SUCCESS = "#2b7a4b"
ERROR = "#b13d3d"

IMG_DIR = Path(__file__).resolve().parent / "img"


def prepare_root(root, title):
    root.title(title)
    root.geometry("980x720")
    root.minsize(900, 640)
    root.configure(bg=BG)
    root.option_add("*Font", "Helvetica 11")
    try:
        style = ttk.Style(root)
        style.theme_use("clam")
    except tk.TclError:
        style = ttk.Style(root)

    style.configure("App.TFrame", background=BG)
    style.configure("Surface.TFrame", background=SURFACE)
    style.configure("Soft.TFrame", background=SURFACE_ALT)
    style.configure(
        "Title.TLabel",
        background=BG,
        foreground=PRIMARY,
        font=("Helvetica", 24, "bold"),
    )
    style.configure(
        "Hero.TLabel",
        background=BG,
        foreground=TEXT,
        font=("Helvetica", 12),
    )
    style.configure(
        "Heading.TLabel",
        background=SURFACE,
        foreground=PRIMARY,
        font=("Helvetica", 20, "bold"),
    )
    style.configure(
        "Subheading.TLabel",
        background=SURFACE,
        foreground=MUTED,
        font=("Helvetica", 11),
    )
    style.configure(
        "Body.TLabel",
        background=SURFACE,
        foreground=TEXT,
        font=("Helvetica", 11),
    )
    style.configure(
        "SoftBody.TLabel",
        background=SURFACE_ALT,
        foreground=TEXT,
        font=("Helvetica", 11),
    )
    style.configure(
        "Nav.TButton",
        padding=(14, 8),
        background=PRIMARY,
        foreground="white",
        borderwidth=0,
        focusthickness=0,
        font=("Helvetica", 10, "bold"),
    )
    style.map("Nav.TButton", background=[("active", PRIMARY_SOFT)])
    style.configure(
        "Primary.TButton",
        padding=(18, 12),
        background=PRIMARY,
        foreground="white",
        borderwidth=0,
        focusthickness=0,
        font=("Helvetica", 11, "bold"),
    )
    style.map("Primary.TButton", background=[("active", PRIMARY_SOFT)])
    style.configure(
        "Accent.TButton",
        padding=(18, 12),
        background=ACCENT,
        foreground="white",
        borderwidth=0,
        focusthickness=0,
        font=("Helvetica", 11, "bold"),
    )
    style.map("Accent.TButton", background=[("active", "#d39f4e")])
    style.configure(
        "Form.TEntry",
        fieldbackground="white",
        foreground=TEXT,
        bordercolor=SURFACE_ALT,
        padding=8,
    )
    style.configure(
        "Form.TCombobox",
        fieldbackground="white",
        foreground=TEXT,
        padding=6,
    )
    style.configure("CardTitle.TLabel", background=SURFACE_ALT, foreground=PRIMARY, font=("Helvetica", 15, "bold"))
    style.configure("CardText.TLabel", background=SURFACE, foreground=MUTED, font=("Helvetica", 10))


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def create_nav(frame, items):
    clear_frame(frame)
    frame.configure(bg=PRIMARY, padx=24, pady=18)
    frame.pack(fill="x", side="top")
    for col, (label, command) in enumerate(items):
        ttk.Button(frame, text=label, command=command, style="Nav.TButton").grid(
            row=0, column=col, padx=(0, 12), sticky="w"
        )
    frame.grid_columnconfigure(len(items), weight=1)


def create_surface(frame):
    clear_frame(frame)
    frame.configure(bg=BG, padx=36, pady=28)
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame, bg=BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    card = ttk.Frame(canvas, style="Surface.TFrame", padding=28)
    window_id = canvas.create_window((0, 0), window=card, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_resize(event):
        canvas.itemconfig(window_id, width=event.width)

    card.bind("<Configure>", on_configure)
    canvas.bind("<Configure>", on_canvas_resize)

    def on_mousewheel(event):
        top, bottom = canvas.yview()
        if event.delta < 0 and bottom >= 1.0:
            canvas.yview_moveto(1.0 - (bottom - top))
            return
        if event.delta > 0 and top <= 0.0:
            canvas.yview_moveto(0.0)
            return
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    return card


def build_hero(parent, title, subtitle):
    hero = ttk.Frame(parent, style="Surface.TFrame")
    hero.pack(fill="x", pady=(0, 22))
    ttk.Label(hero, text=title, style="Heading.TLabel").pack(anchor="w")
    ttk.Label(hero, text=subtitle, style="Subheading.TLabel", wraplength=760, justify="left").pack(anchor="w", pady=(8, 0))
    return hero


def build_button_row(parent, buttons):
    row = ttk.Frame(parent, style="Surface.TFrame")
    row.pack(fill="x", pady=(12, 0))
    for text, style, command in buttons:
        ttk.Button(row, text=text, command=command, style=style).pack(side="left", padx=(0, 12))
    return row


def build_form(parent, fields):
    form = ttk.Frame(parent, style="Surface.TFrame")
    form.pack(fill="x", pady=(8, 0))
    variables = {}
    for row, field in enumerate(fields):
        label = field["label"]
        name = field["name"]
        var = field["var"]
        variables[name] = var
        ttk.Label(form, text=label, style="Body.TLabel").grid(row=row, column=0, sticky="w", padx=(0, 18), pady=10)
        if field.get("kind") == "combobox":
            widget = ttk.Combobox(form, textvariable=var, values=field.get("values", ()), state="readonly", width=28, style="Form.TCombobox")
            default = field.get("default")
            if default is not None:
                widget.set(default)
        else:
            widget = ttk.Entry(form, textvariable=var, width=32, show=field.get("show", ""), style="Form.TEntry")
        widget.grid(row=row, column=1, sticky="ew", pady=10)
    form.grid_columnconfigure(1, weight=1)
    return form, variables


def set_message(parent, text, tone="info"):
    colors = {"info": PRIMARY_SOFT, "success": SUCCESS, "error": ERROR}
    try:
        parent_bg = parent.cget("background")
    except tk.TclError:
        parent_bg = SURFACE
    label = tk.Label(
        parent,
        text=text,
        bg=BG if parent_bg == BG else SURFACE,
        fg=colors.get(tone, PRIMARY_SOFT),
        font=("Helvetica", 11, "bold"),
        justify="left",
        wraplength=760,
    )
    label.pack(anchor="w", pady=(16, 0))
    return label


def build_option_cards(parent, cards):
    wrap = ttk.Frame(parent, style="Surface.TFrame")
    wrap.pack(fill="both", expand=True, pady=(8, 0))
    for index, card_data in enumerate(cards):
        card = ttk.Frame(wrap, style="Soft.TFrame", padding=20)
        r, c = divmod(index, 2)
        card.grid(row=r, column=c, sticky="nsew", padx=8, pady=8)
        ttk.Label(card, text=card_data["title"], style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text=card_data["text"], style="SoftBody.TLabel", wraplength=280, justify="left").pack(anchor="w", pady=(8, 18))
        ttk.Button(card, text=card_data["button"], command=card_data["command"], style=card_data.get("style", "Primary.TButton")).pack(anchor="w")
    wrap.grid_columnconfigure(0, weight=1)
    wrap.grid_columnconfigure(1, weight=1)
    return wrap


def load_logo(filename, size):
    image = Image.open(IMG_DIR / filename).resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)


def launch_script(script_name):
    script_dir = Path(__file__).resolve().parent
    sb_p.Popen(f"start python {script_name}", shell=True, cwd=script_dir)

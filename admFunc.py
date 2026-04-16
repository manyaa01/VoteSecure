import tkinter as tk
import dframe as df
from PIL import ImageTk,Image
from tkinter import ttk
from ui import PRIMARY, SURFACE, TEXT, build_button_row, build_hero, create_surface, prepare_root, set_message

def resetAll(root,frame1):
    from Admin import AdminHome
    import tkinter.messagebox as mb
    frame3 = root.winfo_children()[1]
    prepare_root(root, "Reset Election")
    surface = create_surface(frame1)
    build_button_row(
        surface,
        [("← Back", "TButton", lambda: AdminHome(root, frame1, frame3))],
    )
    build_hero(
        surface,
        "Reset Election",
        "This will reset all vote counts to zero and allow all registered voters to vote again.",
    )

    def confirm_reset():
        result = mb.askyesno(
            "Confirm Reset",
            "Are you sure you want to reset the election?\n\nThis will:\n• Clear all vote counts\n• Allow all voters to vote again\n\nThis action cannot be undone."
        )
        if result:
            df.count_reset()
            set_message(surface, "Election reset successfully. All votes cleared and voters can vote again.", tone="success")

    build_button_row(
        surface,
        [("Reset Election", "Accent.TButton", confirm_reset)],
    )

def showVotes(root,frame1):
    from Admin import AdminHome
    frame3 = root.winfo_children()[1]
    result = df.show_result()
    prepare_root(root, "Vote Count")
    surface = create_surface(frame1)
    build_button_row(
        surface,
        [("← Back", "TButton", lambda: AdminHome(root, frame1, frame3))],
    )
    build_hero(
        surface,
        "Live Vote Count",
        "Current totals are shown below for each party and the NOTA choice.",
    )

    rows = [
        ("BJP", "Narendra Modi", result["bjp"], "img/bjp.png", (42, 42)),
        ("Congress", "Rahul Gandhi", result["cong"], "img/cong.jpg", (34, 46)),
        ("Aam Aadmi Party", "Arvind Kejriwal", result["aap"], "img/aap.png", (52, 36)),
        ("Shiv Sena", "Udhav Thakrey", result["ss"], "img/ss.png", (46, 40)),
        ("NOTA", "No candidate selected", result["nota"], "img/nota.jpg", (42, 30)),
    ]

    table = ttk.Frame(surface, style="Surface.TFrame")
    table.pack(fill="both", expand=True)
    frame1.result_images = []

    for party, candidate, count, path, size in rows:
        row = tk.Frame(table, bg=SURFACE, highlightbackground="#dccfbf", highlightthickness=1, padx=16, pady=12)
        row.pack(fill="x", pady=6)
        image = ImageTk.PhotoImage((Image.open(path)).resize(size, Image.LANCZOS))
        frame1.result_images.append(image)
        tk.Label(row, image=image, bg=SURFACE).pack(side="left", padx=(0, 16))
        info = tk.Frame(row, bg=SURFACE)
        info.pack(side="left", fill="x", expand=True)
        tk.Label(info, text=party, bg=SURFACE, fg=PRIMARY, font=("Helvetica", 13, "bold")).pack(anchor="w")
        tk.Label(info, text=candidate, bg=SURFACE, fg=TEXT, font=("Helvetica", 10)).pack(anchor="w", pady=(4, 0))
        count_card = tk.Frame(row, bg="#113946", padx=16, pady=8)
        count_card.pack(side="right")
        tk.Label(count_card, text=str(count), bg="#113946", fg="white", font=("Helvetica", 14, "bold")).pack()

# if __name__ == "__main__":
#         root = Tk()
#         root.geometry('500x500')
#         frame1 = Frame(root)
#         showVotes(root,frame1)
